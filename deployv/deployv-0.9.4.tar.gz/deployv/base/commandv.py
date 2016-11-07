# coding: utf-8

""" This class have the algorithms that will be executed bu deployvcmd and deployvd, both are
interfaces between the input (files, cmd interface and rabbitmq) and CommandV.


`extend_me <http://pythonhosted.org/extend_me/>`_ is used in the event manager class and the core
command component because allows an easy app extension without the need of modifying the core
components.

CommandV inherits from `Extensible <http://pythonhosted.org/extend_me/#extensible>`_ base class so
it can be extended in a simple way just inheriting from CommandV
"""

import logging
import os
import re
import time
import yaml
import simplejson as json
import base64
from tempfile import mkdtemp
from extend_me import Extensible
from psycopg2 import OperationalError
from docker import Client
from docker.errors import APIError, NullResource, NotFound
from deployv.base.errors import BuildError, NoSuchContainer
from deployv.base.extensions_core import events, load_extensions
from deployv.base import postgresv, nginxv
from deployv.helpers import backup, utils, container
from deployv.instance import instancev
from deployv.extensions.checkers import InstallTestRepo

logger = logging.getLogger('deployv')  # pylint: disable=C0103

load_extensions()


class CommandV(Extensible):
    def __init__(self, config, instance_class=None):
        """
        :param config: Configuration dict. See :class:`~deployv.base.instancev.InstanceV`
        :return:
        """
        self.__config = config
        self._domains = None
        if self.__config.get('instance', False):
            prefix = container.generate_prefix(self.__config)
            self.__config.get('instance').update({'prefix': prefix})
        if instance_class:
            self.__instance_manager = instance_class(self.__config)
        else:
            self.__instance_manager = instancev.InstanceV(self.__config, timeout=3000)

    @property
    def instance_manager(self):
        return self.__instance_manager

    def _can_add_new(self):
        """ As we have a limited amount of resources in each node we need to check if the running
        instances count is less than the allowed to run a new one

        :return: False or True if the count of running instances is < than the allowed max
        """
        containers = self.instance_manager.cli.containers()
        try:
            max_instances = self.__config.get('node').get('max_instances')
        except AttributeError:
            return True
        count = 0
        for container_info in containers:
            for name in container_info.get('Names'):
                if re.match(r'^/[tiu][0-9]+_[a-z]+[0-9][0-9]_odoo', name):
                    count += 1
                    break
        logger.debug('Instance count %s/%s', count, max_instances)
        return count < max_instances

    @events
    def create(self):
        """ Creates an Odoo dockerized instance with the provided configuration

        :return: a response in json format containing the info dict returned by
            :func:`~deployv.base.dockerv.DockerV.basic_info`
        """
        res = {'command': 'create'}
        if not self._can_add_new():
            logger.info('Max instance count reached (%s allowed)',
                        self.__config.get('node').get('max_instances'))
            res.update({'error': 'Reached max instance count for this node ({} allowed)'
                       .format(self.__config.get('node').get('max_instances'))})
            return res
        if self.__config.get('container_config').get('build_image') or \
                self.__config.get('container_config').get('postgres_container'):
            build_res = self.__instance_manager.build_image()
            logger.debug('Build res %s', build_res)
            if not build_res[0]:
                res.update(build_res[1])
                return res
        try:
            info = self.__instance_manager.start_odoo_container()
        except Exception as error:  # pylint: disable=W0703
            logger.exception('Could not start container')
            res.update({'error': utils.get_error_message(error)})
            return res
        time.sleep(10)
        if info and self.__config.get('instance').get('ssh_key'):
            self.__instance_manager.deploy_key()
            self.__instance_manager.check_keys()
        try:
            res_build = self.__instance_manager.build_instance()
            if not res_build[0]:
                res.update({
                    'error': res_build[1]
                })
                return res
            if not res.get('attachments', False):
                res.update({'attachments': list()})
            post_branch = os.path.join(self.__instance_manager.temp_folder, 'post_process.json')
            res.get('attachments').append(
                {
                    'file_name': os.path.basename(post_branch),
                    'file': utils.generate_attachment(post_branch),
                    'type': 'application/json'
                }
            )
        except TypeError as error:
            res.update({'error': utils.get_error_message(error)})
        install_log = self.__instance_manager.install_deps()
        logger.info(install_log)
        if info:
            info.update({'domain': self.__instance_manager.config.get('domain')})
            if install_log:
                info.update(install_log)
            res.update({'result': info})
            if self.__config.get('node', False):
                logger.debug('Use nginx config: %s',
                             self.__config.get('node').get('use_nginx', False))
                if self.__config.get('node').get('use_nginx', False):
                    logger.debug('Using nginx')
                    self._domains = self.update_nginx()
                    nginx_url = self._get_nginx_url(info.get('name')[:-5])
                    res.get('result').update({
                        'nginx_url': nginx_url,
                        'instance_log': '{url}/logs/odoo_stdout.log'.format(url=nginx_url)
                    })
        res = self.cloc_report(res)
        return res

    def _build_image(self):
        res = (True, dict())
        try:
            build_res = self.__instance_manager.build_instance_image()
        except BuildError as error:
            res = (False, {'error': utils.get_error_message(error)})
        else:
            if not build_res.get('result'):
                res = (False, build_res)
        return res

    def _get_nginx_url(self, name):
        nginx_url = None
        for domain in self._domains:
            if domain.get('domain').startswith(name):
                nginx_url = domain.get('domain')
                break
        logger.debug('Updating url : %s', nginx_url)
        return nginx_url

    def deactivate(self, database):
        env_vars = self.__instance_manager.docker_env
        config = {
            'db_user': env_vars.get('db_user'),
            'db_host': env_vars.get('db_host'),
            'db_password': env_vars.get('db_password'),
            'db_port': env_vars.get('db_port')
        }
        instancev.deactivate_database(config, database)
        new_admin = self.__config.get('instance').get('config').get('admin', False)
        if new_admin:
            self.__instance_manager.\
                change_password(1, new_admin, database)

    def restore_process(self, backup_src, database_name, deactivate=False):
        instance_type = self.__instance_manager.instance_type
        update = False
        if instance_type in instancev.UPDATE:
            update = True
            InstallTestRepo.event = 'after.updatedb.event'
        working_dir = mkdtemp(prefix='deployv_')
        try:
            dest_dir = utils.decompress_files(backup_src, working_dir)
        except EOFError:
            utils.clean_files(working_dir)
            raise
        dump = self.__instance_manager.get_dump(dest_dir)
        res_stop = self._stop_instance()
        if isinstance(res_stop, str):
            utils.clean_files(working_dir)
            res = {'error': res_stop}
            return (False, res)
        self.__instance_manager.restore_backup(dump, database_name, dest_dir)
        if instance_type in instancev.DEACTIVATE or deactivate:
            instancev.deactivate_database(self.__instance_manager.db_config, database_name)
        if update:
            self.updatedb(database_name)
        utils.clean_files(working_dir)
        self.__instance_manager.start_instance()
        return (True, {})

    def cloc_report(self, msg):
        """
        This method generates a report by the cloc command the number
        of lines of code that has an instance and stores it in yaml format
        to be added as an attachments
        :return: a list of the dictionary that has the the output
        of the cloc command in yaml format to be added as an attachments
        """
        res = msg
        if not res.get('attachments', False):
            res.update({'attachments': list()})
            return res
        command_exists = self.__instance_manager.exec_cmd("which cloc")
        if not command_exists:
            res_install = self.__instance_manager.\
                install_packages(apt_packages=["cloc"])
            if not res_install['apt_install'][0]['cloc']['installed']:
                message = "It failed to install the cloc command"
                logger.warning(message)
                res.get('attachments').append(
                    {
                        "file_name": "cloc_error",
                        "file": base64.b64encode(message),
                        "type": 'application/json'
                    }
                )
                return res
        odoo_home = self.__instance_manager.\
            config.get('env_vars').get('odoo_home')
        module = os.path.join(odoo_home, 'instance')
        command_cloc = "cloc --yaml {module}".format(module=module)
        execute_cloc = self.__instance_manager.exec_cmd(command_cloc)
        body_content = execute_cloc.split('\n---')
        res.get('attachments').append(
            {
                "file_name": "cloc_report",
                "file": base64.b64encode(str(yaml.load(body_content[1]))),
                "type": 'application/json'
            }
        )
        return res

    @events
    def restore(self, backup_src=None, database_name=None, deactivate=False):
        """ Restores a backup from a file or folder. If a folder is provided searches the best
        match for the given configuration. Database name is an optional parameter.

        The return value is a dict as follows::

                {
                    'command': 'command executed',
                    'result':
                    {
                        'backup': 'backup file used to restore the database',
                        'database_name': 'the database name created with the corresponding backup'
                    }
                }

        In the case of any error::

                {
                    'command': 'command executed',
                    'error': 'error message'
                }

        :param backup_src: Backup source, can be a folder or a backup file
        :param database_name: Database name to restore, if None is generated automatically
        :param deactivate: Force database deactivation ignoring the instance type
        :return: A json object with the result or error generated. If any result is generated the
            result key will have the backup used and the database name.
        """
        res = {'command': 'restore'}
        bkp_chk = self._check_backup_folder(backup_src)
        if not bkp_chk[0]:
            res.update({'error': bkp_chk[1]})
            return res
        database_file = bkp_chk[1]
        if not database_name:
            if self.__config.get('instance').get('config').get('db_name'):
                db_name = self.__config.get('instance').get('config').get('db_name')
            elif self.__config.get('prefix'):
                prefix = self.__config.get('prefix')
                db_name = utils.generate_dbname(self.__config,
                                                os.path.basename(database_file),
                                                prefix=prefix)
            else:
                db_name = utils.generate_dbname(
                    self.__config, os.path.basename(database_file))
        else:
            db_name = database_name
        try:
            restore_res = self.restore_process(database_file, db_name, deactivate)
            if not restore_res[0]:
                res.update(restore_res[1])
                return res
            if self.__config.get('instance').get('config').get('admin'):
                new_passwd = self.__config.get('instance').get('config').get('admin')
                self.__instance_manager.change_password(1, new_passwd, db_name)
        except OperationalError as error:
            res.update({
                'error': error.message
            })
            return res
        except AttributeError as error:
            if "'NoneType' object has no attribute 'get'" in error.message:
                self.__config.get('instance').update({
                    'config': {
                        "db_host": self.__instance_manager.docker_env.get('DB_HOST'),
                        "db_password": self.__instance_manager.docker_env.get('DB_PASSWORD'),
                        "db_port": self.__instance_manager.docker_env.get('DB_PORT'),
                        "db_user": self.__instance_manager.docker_env.get('DB_USER')
                    }
                })
            else:
                res.update({
                    'error': error.message
                })
                return res
        except EOFError as error:
            res.update({
                'error': utils.get_error_message(error)
            })
            return res

        res.update({
            'result': {
                'backup': os.path.abspath(database_file),
                'database_name': db_name
            }
        })
        if self.__config.get('instance').get('install_module'):
            install_res = self._install_module(db_name)
            res.get('result').update({
                'install_module': install_res
            })
            res = self._attach_file(res, install_res.get('log_file'), 'text/plain')
        return res

    def _attach_file(self, msg, file_name, file_type):
        res = msg
        if not res.get('attachments', False):
            res.update({'attachments': list()})
        res.get('attachments').append(
            {
                'file_name': os.path.basename(file_name),
                'file': utils.generate_attachment(file_name),
                'type': file_type
            }
        )
        return res

    def _check_backup_folder(self, backup_src=None):
        if not backup_src:
            backup_src = os.path.expanduser(
                self.__config.get('container_config').get('database_folder'))
        if not backup_src or not os.path.exists(backup_src):
            logger.warn('Path %s does not exists', backup_src and backup_src or '')
            res = (False, 'No backup path supplied or does not exits')
        elif os.path.isdir(backup_src):
            if 'database_dump.sql' in os.listdir(backup_src) or \
                    'database_dump.b64' in os.listdir(backup_src):
                res = (True, backup_src)
            else:
                customer_id = self.__config.get('instance').get('customer_id') or \
                    self.__instance_manager.docker_env.get('customer')
                database_file = backup.search_backup(backup_src, customer_id)
                if not database_file:
                    res = (False, 'Not found any candidate backup to be restored')
                else:
                    res = (True, database_file)
        else:
            res = (True, backup_src)
        return res

    def _install_module(self, db_name):
        install_res = self.__instance_manager.install_module(
            self.__config.get('instance').get('install_module'),
            db_name
        )
        return install_res

    @events
    def backup(self, backup_dir, database_name, cformat=False, reason=False, tmp_dir=False,
               prefix=False):
        res = {'command': 'backup'}
        bkp = self.__instance_manager.generate_backup(database_name,
                                                      backup_dir,
                                                      cformat=cformat,
                                                      reason=reason,
                                                      tmp_dir=tmp_dir,
                                                      prefix=prefix)
        if bkp:
            res.update({'result': bkp})
        else:
            res.update({'error': 'Could not generate the backup'})
        return res

    def change_passwords(self):
        """ Generates a random password for each one of the users in an instance.
        """
        res = {'command': 'change_passwords'}
        results = {}
        db_name = self.__config.get('instance').get('config').get('db_name')
        users = self.instance_manager.get_odoo_users(db_name)
        for user in users:
            if user.get('login') not in ['public', 'portaltemplate']:
                password = utils.random_string(10)
                self.instance_manager.change_password(user.get('id'), password, db_name)
                results.update({user.get('login'): password})
        res.update({'result': results})
        return res

    @events
    def updatedb(self, database_name=None):
        """ Updates an instance (branches and database) and return the json with the operation
        resume

        :param database_name: Database name to be updated
        :return: The result from :meth:`deployv.instance.instancev.run_and_log`
        """
        db_name = database_name if database_name is not None \
            else self.__config.get('instance').get('config').get('db_name')
        res = {'command': 'updatedb'}
        try:
            self.__instance_manager.stop_instance()
        except APIError as error:
            logger.exception('Could not update database %s: %s', db_name, error.message)
            res.update({'error': error.explanation})
            return res
        retry = 0
        while retry <= 1:
            res_update = self.__instance_manager.update_db('all', db_name)
            if len(res_update.get('errors')) > 0:
                if retry < 1:
                    logger.info(
                        'Some error shown in the update log, updating again')
                    retry = retry + 1
                else:
                    logger.error('The instance was not updated properly, check logfile: %s',
                                 res_update.get('log_file'))
                    res.update({'result': res_update})
                    return res
            else:
                break
        self.__instance_manager.start_instance()
        res.update({'attachments': [
            {
                'file_name': os.path.basename(res_update.get('log_file')),
                'file': utils.generate_attachment(res_update.get('log_file')),
                'type': 'text/plain'
            }
        ]})
        res_update.update({'database_name': db_name})
        res.update({'result': res_update})
        if self.__config.get('instance').get('install_module'):
            install_res = self.__instance_manager.install_module(
                self.__config.get('instance').get('install_module'),
                db_name
            )
            res.get('result').update({
                'install_module': install_res
            })
            if not res.get('attachments', False):
                res.update({'attachments': list()})
            res.get('attachments').append(
                {
                    'file_name': os.path.basename(install_res.get('log_file')),
                    'file': utils.generate_attachment(install_res.get('log_file')),
                    'type': 'text/plain'
                }
            )
        return res

    @events
    def update_branches(self):
        """ Updates repos in the given instance

        :return: Returns the operation result in the json format, additionally will attach the
            actual instance status with the commits, repos and branches see
            :mod:`~deployv.helpers.branches` for more info about the format
        """
        res = {'command': 'update_branches'}
        if self.__config.get('instance').get('ssh_key'):
            self.__instance_manager.deploy_key()
            self.__instance_manager.check_keys()
        try:
            res_build = self.__instance_manager.build_instance()
            if not res_build[0]:
                res.update({
                    'error': 'Could not generate instance with the given branches: {}'
                             .format(res_build[1])
                })
                return res
            self.__instance_manager.stop_instance()
            if not res.get('attachments', False):
                res.update({'attachments': list()})
            post_branch = os.path.join(self.__instance_manager.temp_folder, 'post_process.json')
            res.get('attachments').append(
                {
                    'file_name': os.path.basename(post_branch),
                    'file': utils.generate_attachment(post_branch),
                    'type': 'application/json'
                }
            )
        except TypeError as error:
            res.update({'error': error.message})
        else:
            res.update({'result': 'Branches updated'})
        self.cloc_report(res)
        return res

    def _stop_instance(self):
        try:
            self.__instance_manager.stop_instance()
        except NotFound as error:
            logger.debug('Error message %s', utils.get_error_message(error))
            utils.get_error_message(error)
            return 'Instance already deleted'
        except NullResource as error:
            if "image or container param is undefined" in error.message:
                return 'Instance already deleted or misspelled name'
        return True

    def _drop_dbs(self):
        res_dropdb = list()
        psql_dict = utils.odoo2postgres(self.__instance_manager.db_config)
        error_msgs = ["Connection refused", "password authentication failed"]
        try:
            psql_shell = postgresv.PostgresShell(psql_dict)
            db_list = psql_shell.list_databases()
        except OperationalError as error:
            if not any([msg in error.message for msg in error_msgs]):
                raise
        else:
            prefix = container.generate_prefix(self.__config)
            for db in db_list:
                logger.debug('Db in the list: %s', db.get('name'))
                if db.get('name').startswith(prefix):
                    logger.debug('Dropping %s database', db.get('name'))
                    psql_shell.drop(db.get('name'))
                    res_dropdb.append('Dropped {} database'.format(db.get('name')))
        return res_dropdb

    @events
    def delete_instance(self):
        """ Delete an instance and database from the node, if it does not exists or was already
        deleted will indicate in the message.

        :return: A json object with the result or error generated. If any result is generated the
            result key will have the message indicating such.
        """
        logger.info('Deleting container')
        res = {'command': 'delete_instance'}
        res_stop = self._stop_instance()
        if isinstance(res_stop, str):
            res.update({'result': [res_stop]})
            return res
        res_dropdb = self._drop_dbs()
        try:
            container_info = self.__instance_manager.basic_info
            self.__instance_manager.remove_container()
            res.update({
                'result': ['Instance {} deleted'.format(container_info.get('name')), ] + res_dropdb
            })
            if self.__config.get('node').get('use_nginx'):
                self.update_nginx()
        except Exception as error:  # pylint: disable=W0703
            logger.exception('Could not remove container')
            if "No such container or id: None" in utils.get_error_message(error):
                res.update({'result': 'Instance already deleted or misspelled name'})
            else:
                res.update({'error': utils.get_error_message(error)})
            return res
        return res

    def get_containers(self):
        """ Get the containers list that are actually executing and which names are like:
            t111_cust80_odoo, thats matching the regex: '^/([tiu][0-9]+_[a-z]+[0-9][0-9])_odoo'

        :return: Dict with the domain and mapping ports
        """
        cli = Client()
        containers = cli.containers()
        res = list()
        logger.debug('Geting containes names')
        for container_info in containers:
            for name in container_info.get('Names'):
                logger.debug('Name : %s', name)
                domain = re.search(r'^/([tiu][0-9]+_[a-z]+[0-9][0-9])_odoo', name)
                if domain:
                    inspected = self.__instance_manager.inspect(container_info.get('Id'))
                    ports_info = container.get_ports_dict(inspected)
                    res.append({
                        'domain': '{sub}.{domain}'.format(
                            sub=domain.group(1),
                            domain=self.__config.get('container_config').get('domain')),
                        'port': ports_info.get('8069'),
                        'lp_port': ports_info.get('8072'),
                        'logs': os.path.join(
                                os.path.expanduser(
                                        self.__config.get('container_config').get('working_folder')
                                ),
                                inspected.get('Name')[1:])
                    })
                    break
        return res

    @events
    def update_nginx(self):
        """ Updates nginx config file to match running containers, if one is stopped or removed
        will be removed from nginx config too.

        :return: Containers config see :meth:`deployv.base.commandv.get_containers`
        """
        containers_config = self.get_containers()
        nginx_manager = nginxv.NginxV(self.__config.get('node').get('nginx_folder'))
        nginx_manager.update_sites(containers_config)
        nginx_manager.restart()
        return containers_config

    @events
    def push_image(self):
        res = {'command': 'push_image'}
        res.update({'attachments': list()})
        response = ""
        try:
            container_info = self.__instance_manager.basic_info
        except NoSuchContainer:
            res.update({'error': 'Instance already deleted or misspelled name'})
            return res
        repo_image = self.__config.get('container_config').get('customer_image')
        if not repo_image:
            res.update({'error': "It is not specified the repository to upload the image"})
            return res
        split_repo = repo_image.split("/", 1)
        tag_name = split_repo[1].split(":", 1)
        name = tag_name[0]
        tag = tag_name[1]
        repo_image = "{base}/{name}".\
            format(base=split_repo[0], name=utils.clean_string(name))
        message = 'Commit container {container} to images {image}:{tag}'\
            .format(container=container_info.get('Id'), image=repo_image, tag=tag)
        logger.info(message)
        commit = self.instance_manager.cli.commit(container_info.get('Id'),
                                                  repository=repo_image, tag=tag)
        image = self.instance_manager.cli.inspect_image(commit.get('Id'))
        for line in self.instance_manager.cli.push(image.get('RepoTags')[0], stream=True):
            obj = json.loads(line)
            if obj.get('status'):
                logger.info(obj)
                response = response+'\n'+line
            elif obj.get('error'):
                logger.info(obj.get('error').strip())
                res.update({'error': obj.get('error').strip()})
                return res
        res.get('attachments').append(
            {
                "file_name": "push_image.txt",
                "file": base64.b64encode(response),
                "type": 'application/txt'
            }
        )
        res.update({'result': {'image': image.get('RepoTags')[0]}})
        return res
