# coding: utf-8
""" As this class is a :class:`~base.DockerV` extension need to have the same values in the config
dictionary, but inside a config_container key::

        "container_config": {
            "apt_install": [],
            "pip_install": [],
            "domain": "localhost",
            "command": "sleep 20",
            "env_vars": {
                "odoo_config_file": "/home/odoo/.openerp_serverrc",
                "odoo_home": "/home/odoo",
                "odoo_user": "odoo"
            },
            "image_name": "busybox",
            "mem_limit": "768m",
            "ports": {
                "8069": 8069,
                "8072": None
            },
            "remove_previous": True,
            "working_folder": "/path/to/docker_volumes",
            "volumes":{
                "filestore": "/home/odoo/.local/share/Odoo",
                "logs": "/var/log/supervisor",
                "ssh": "/home/odoo/.ssh",
                "tmp": "/tmp"
            }
        },
        "instance": {
            "action_type": "replace",
            "task_id":"t1234",
            "customer_id": "customer80",
            "config": {
                "admin": "admin_pass",
                "admin_passwd": "123",
                "db_host": "172.17.42.1",
                "db_name": "{{ instance.task_id }}_{{ instance.customer_id }}",
                "db_password": "psql_user",
                "db_user": "psql_pass",
                "dbfilter": "{{ instance.task_id }}_{{ instance.customer_id }}.*",
                "list_db": True
            },
            "ssh_key":"base64_encoded_key",
            "repositories": [
                {
                    "branch": "8.0",
                    "commit": "8f159f276e7c8da4e5475e604e9057dcaadfedf9",
                    "depth": 1,
                    "is_dirty": False,
                    "name": "odoo",
                    "path": "odoo",
                    "repo_url": {
                        "origin": "git@github.com:Vauxoo/odoo.git"
                    },
                    "type": "git"
                },
            ],
            "update_module":"all",
            "install_module": None
        }

.. note:: For more information about *container_config* keys and values check
    :class:`~deployv.base.dockerv.DockerV` documentation

Where:

* *action_type*: Replace/create Odoo container
* *task_id*: associated task/issue/user story in the instance un the format [tiu]id
* *customer_id*: Unique customer id
* *config*: Dict with the values to be changed inside Odoo configuration file
* *ssh_key*: the id_rsa key ot be used to clone private repos, must be in base64 format
* *repositories*: A list of repos to be updated/added.
  Check `backupws <https://github.com/ruiztulio/backupws/blob/master/branches.py>`_
  if you want more detail about the format

"""
import tarfile
import logging
import base64
import github
import os
from os import path
from tempfile import gettempdir
import zipfile
import shutil
import time
import re
from passlib.context import CryptContext
import psycopg2
import simplejson as json
from deployv.base.dockerv import DockerV
from deployv.base.postgresv import PostgresShell, PostgresConnector
from deployv.base import postgresv
from deployv.helpers import utils, container, build_helper
from deployv.base import errors


logger = logging.getLogger('deployv')  # pylint: disable=C0103
INSTANCE_TYPES = ['test', 'develop', 'updates', 'production']
UPDATE = ['develop', 'updates']
DEACTIVATE = ['test', 'develop', 'updates']
INSTALL_RIBBON = ['test', 'develop', 'updates']


class InstanceV(DockerV):

    def __init__(self, config, timeout=300, docker_url="unix://var/run/docker.sock"):
        self.__full_config = config
        container_config = config.get('container_config')
        logger.debug('Container config : %s',
                     json.dumps(container_config, sort_keys=True, indent=2))
        if not container_config.get('container_name', False):
            container_config.update({
                'container_name': '{prefix}_odoo'.format(
                    prefix=config.get('instance').get('prefix'))})
            env_vars = config.get('instance').get('config').copy()
            if not env_vars.get('admin'):
                env_vars.update({'admin': utils.random_string(6)})
            if not env_vars.get('admin_passwd'):
                env_vars.update({'admin_passwd': utils.random_string(6)})
            env_vars.update({'instance_type':
                             config.get('instance').get('instance_type', 'production'),
                             'customer': config.get('instance').get('customer_id')})
            self._update_env_vars(env_vars)
        super(InstanceV, self).__init__(container_config,
                                        timeout=timeout, docker_url=docker_url)

    def start_odoo_container(self):
        """ Specifically starts an Odoo container and configure all the parameters,
        see :func:`~dockerv.DockerV.basic_info` for more information about the format and content

        :return: A dict with the basic info of container
        """
        logger.debug('Psql in container: %s', self.config.get('postgres_container', False))
        # if it will be a full stack container all the parameters are changed (no matter what is
        # specified in the config) to target the local env and added the nginx, postgres and ssh
        # ports
        if self.config.get('postgres_container', False):
            self.config.get('ports').update({
                '8080': None,
                '22': None,
                '5432': None
            })
            self.config.get('env_vars').update({
                'db_host': '127.0.0.1',
                'db_port': 5432
            })
        logger.info('pulling %s', self.config.get('image_name'))
        self.cli.pull(self.config.get('image_name'))
        logger.info('Starting Odoo container %s',
                    self.config.get('container_name'))
        self.config.update({'container_hostname': container.generate_hostname(self.__full_config)})
        info = self.deploy_container()
        if self.config.get('postgres_container', False):
            self.add_authorized_keys()
            self.check_postgres()
        logger.info('Odoo container "%s" created. Ports %s',
                    info.get('name'), info.get('ports'))
        return info

    def add_authorized_keys(self):
        git_cli = github.Github()
        with open('authorized_keys', 'w') as authorized_keys:
            for user in self.__full_config.get('instance').get('authorized_users', []):
                try:
                    user_keys = git_cli.get_user(user).get_keys()
                except github.GithubException as error:
                    error_msg = error.data.get('message')
                    if 'Not Found' in error_msg:
                        logger.warning('User not found %s, could not retrieve any key', user)
                    else:
                        logger.warning(error_msg)
                for user_key in user_keys:
                    authorized_keys.write(user_key.key + '\n')
        with tarfile.open('keys.tar', 'w') as tar_keys:
            tar_keys.add('authorized_keys')
        with open('keys.tar', 'r') as tar_data:
            self.cli.put_archive(self.config.get('container_name'),
                                 '/home/odoo/.ssh/', tar_data.read())
            self.exec_cmd('cp /home/odoo/.ssh/authorized_keys /root/.ssh/')
        utils.clean_files(['keys.tar', 'authorized_keys'])

    def check_postgres(self):
        retry = 0
        while retry <= 3:
            logger.info('Testing postgres connection')
            try:
                PostgresShell(utils.odoo2postgres(self.db_config))
                logger.info('Postgres connection test passed')
                return True
            except psycopg2.OperationalError as error:
                if 'the database system is starting up' in error.message:
                    retry += 1
                    logger.warn('Postgres is starting up, retry %s', retry)
                    time.sleep(5)
                    continue
                else:
                    logger.error(
                        'Could not connect to the postgres server: %s',
                        error.message)
                    return False

    @property
    def is_running(self):
        """ If the Odoo instance ins running inside the container (or at least supervisord
        detects it) return True, False otherwise. If an unexpected state is detected raises
        a TypeError exception

        :return: True or False
        """
        retry = 0
        while retry <= 3:
            try:
                res = self.exec_cmd('supervisorctl status odoo')
            except errors.NotRunning:
                retry += 1
                logger.debug('Container not running, retry %s', retry)
                time.sleep(4)
                continue
            logger.debug('is_running: %s', res.strip())
            if 'STARTING' in res or 'STOPPING' in res:
                retry += 1
                logger.debug('The Odoo process in in a intermediate state, retrying %s', retry)
                time.sleep(4)
            elif 'RUNNING' in res:
                return True
            elif 'STOPPED' in res:
                return False
            elif res == '' or 'no such file' in res and retry < 3:
                retry += 1
                logger.debug('Supervisor returned empty or not running yet, retrying %s', retry)
                time.sleep(4)
            else:
                raise TypeError('Unknown state: %s' % res)

    @property
    def instance_type(self):
        """ The instance type

        :return: Instance type: production, test, develop or false if it not set
        """
        return self.__full_config.get('instance').get('instance_type') or\
            self.docker_env.get('instance_type', 'production')

    @property
    def temp_folder(self):
        """ This is a very important property because the tmp folder is used to share files between
            the container and the host, widely used along the code.
            The best way (so far) is iterating all the mounted volumes until we find the /tmp

        :return: Full host path where the tmp volume is mounted
        """
        inspected = self.inspect()
        volumes = inspected.get('Mounts')
        res = None
        for volume in volumes:
            if volume.get("Destination") == '/tmp' and volume:
                res = volume.get("Source")
                break
        return res

    def start_instance(self):
        """ Start an instance inside a docker container using supervisord

        :return: Supervisord response
        """
        res = 'RUNNING'
        if not self.is_running:
            res = self.exec_cmd('supervisorctl start odoo')
            logger.debug('start_instance: %s', res.strip())
        return res

    def stop_instance(self):
        """ Stop an instance inside a docker container using supervisord

        :return: Supervisord response
        """
        res = 'STOPPED'
        if self.is_running:
            res = self.exec_cmd('supervisorctl stop odoo')
            logger.info('stop_instance: %s', res.strip())
        return res

    def deploy_key(self):
        """ Deploy a ssh_key into the container

        """
        ssk_key = base64.b64decode(self.__full_config.get('instance').get('ssh_key'))
        logger.info('Deploying keys')
        ssh_key_filename = path.join(self.temp_folder, 'id_rsa')
        with open(ssh_key_filename, 'w') as key_file:
            key_file.write(ssk_key)
        odoo_home = self.config.get('env_vars').get('odoo_home')
        odoo_user = self.config.get('env_vars').get('odoo_user')
        bash_lines = [
            'mv /tmp/id_rsa {home}/.ssh/id_rsa'.format(home=odoo_home),
            'chown -R {user}:{user} {home}/.ssh/id_rsa'.format(home=odoo_home, user=odoo_user),
            'chmod 0600 {home}/.ssh/id_rsa'.format(home=odoo_home),
            'su {user} -c "ssh-keyscan github.com > {home}/.ssh/known_hosts"'.format(
                home=odoo_home, user=odoo_user),
            'su {user} -c "ssh-keyscan bitbucket.org >> {home}/.ssh/known_hosts"'.format(
                home=odoo_home, user=odoo_user),
            'su {user} -c "ssh-keyscan git.vauxoo.com >> {home}/.ssh/known_hosts"'.format(
                home=odoo_home, user=odoo_user)
        ]
        for line in bash_lines:
            logger.debug('Executing "%s"', line)
            res = self.exec_cmd(line)
            logger.debug('Response "%s"', res.strip())

    def run_and_log(self, command):
        """ Executes an Odoo related command inside the container (i.e.: update, install) and
            returns the resumed log and full path to the generated log. See
            :func:`~dockerv.helpers.utils.resume_log` for detailed information about
            the return format

        :param command: Command line to be executed inside Odoo container
        :return: Resumed log and full path to the generated file
        """
        self.stop_instance()
        logger.debug('run_and_log: %s', command)
        res = self.exec_cmd(command)
        resume = utils.resume_log(res.split('\n'))
        self.start_instance()
        working_path = path.join(
            self.temp_folder,
            'cmd_{timestamp}.log'.format(timestamp=utils.get_strtime())
        )
        with open(working_path, 'w') as log_file:
            log_file.write(res)
        resume.update({'log_file': working_path})
        logger.info('+-- Critical errors %s', len(resume.get('critical')))
        logger.info('+-- Errors %s', len(resume.get('errors')))
        logger.info('+-- Import errors %s', len(resume.get('import_errors')))
        logger.info('+-- Warnings %s', len(resume.get('warnings')))
        logger.info('+-- Translation Warnings %s', len(resume.get('warnings_trans')))
        logger.info('Logger was saved to: "%s"', working_path)
        return resume

    def update_db(self, modules, db_name):
        """ Executes "-u module" or "-u module1,module2" on the selected database and returns
            resumed log and full path to the generated log. See
            :func:`~dockerv.helpers.utils.resume_log` for detailed information about
            the return format

        :param modules: Module (str) o modules (list) to be updated
        :param db_name: Database name to be updated
        :return: Resumed log and full path to the generated file
        """
        if utils.is_iterable(modules):
            modules_str = ','.join(modules)
        else:
            modules_str = modules

        logger.info('Updating database %s, modules %s', db_name, modules_str)
        if self.config.get('env_vars'):
            env_vars = self.config.get('env_vars')
            if env_vars.get('odoo_home') and env_vars.get('odoo_user'):
                odoo_home = env_vars.get('odoo_home')
                odoo_user = env_vars.get('odoo_user')
        else:
            odoo_home = self.docker_env.get('odoo_home')
            odoo_user = self.docker_env.get('odoo_user')

        update_command = ('su {user} -c "{home}/instance/odoo/odoo.py'
                          ' -d {database} -u {modules} --stop-after-init"') \
            .format(home=odoo_home, user=odoo_user, database=db_name, modules=modules_str)
        return self.run_and_log(update_command)

    def install_module(self, modules, db_name, without_demo=True):
        """ Executes "-i module" or "-i module1,module2" on the selected database and returns
            resumed log and full path to the generated log. See
            :func:`~dockerv.helpers.utils.resume_log` for detailed
            information about the return format

        :param modules: Module (str) o modules (list) to be installed
        :param db_name: Database name to be updated
        :param without_demo: Install the mdule/s with or without demo,
            if true will use --without-demo=all, if false omit the option,
            otherwise the module list
        :return: Resumed log and full path to the generated file
        """
        if utils.is_iterable(modules):
            modules_str = ','.join(modules)
        else:
            modules_str = modules

        if isinstance(without_demo, bool):
            wodemo = '--without-demo=all' if without_demo else ''
        elif utils.is_iterable(modules):
            wodemo = '--without-demo={}'.format(','.join(modules))
        elif isinstance(without_demo, str):
            wodemo = '--without-demo={}'.format(modules)
        logger.info('Installing modules %s in database %s',
                    modules_str, db_name)
        if self.config.get('env_vars'):
            env_vars = self.config.get('env_vars')
            if env_vars.get('odoo_home') and env_vars.get('odoo_user'):
                odoo_home = env_vars.get('odoo_home')
                odoo_user = env_vars.get('odoo_user')
        else:
            odoo_home = self.docker_env.get('odoo_home')
            odoo_user = self.docker_env.get('odoo_user')

        update_command = ('su {user} -c "{home}/instance/odoo/odoo.py'
                          ' -d {database} -i {modules} --stop-after-init {wodemo}"') \
            .format(home=odoo_home, user=odoo_user, database=db_name, modules=modules_str,
                    wodemo=wodemo)

        return self.run_and_log(update_command)

    def move_file(self, filename):
        """Moves a file into the container temp shared volume

        :filename: File to be moved
        """
        actual_path = path.dirname(path.realpath(__file__))
        file_lib_src = path.join(
            actual_path, '..', 'helpers', filename)
        file_lib_dst = path.join(self.temp_folder, filename)
        shutil.copyfile(file_lib_src, file_lib_dst)

    def build_instance(self):
        """ Build the instance inside the container using the specified branches and repos

        :return: True if all the branches are cloned successfully otherwise False
        """
        success = (True, 'Build successfully')
        logger.info('Building branches')
        try:
            self.stop_instance()
        except TypeError:
            return (False, "process manager supervisord could not start")
        odoo_home = self.config.get('env_vars').get('odoo_home')
        odoo_user = self.config.get('env_vars').get('odoo_user')
        branches_filename = path.join(self.temp_folder, 'branches.json')
        getaddons_path = path.join(path.dirname(path.abspath(__file__)), '..',
                                   'templates', 'files', 'getaddons.py')
        shutil.copyfile(getaddons_path, path.join(self.temp_folder, 'getaddons.py'))
        self.move_file('helpers-requirements.txt')
        with open(branches_filename, 'w') as fout:
            json.dump(self.__full_config.get('instance').get('repositories'),
                      fout, indent=4, ensure_ascii=False,
                      separators=(',', ':'))
        addons_paths = list()
        for repo in self.__full_config.get('instance').get('repositories'):
            if repo.get('name') != 'odoo':
                addons_paths.append(path.join(odoo_home, 'instance', repo.get('path')))
        addons_path = ','.join(addons_paths)
        bash_lines = [
            'pip install -r /tmp/helpers-requirements.txt -q ',
            'su {user} -c "branchesv load -p {home}/instance -f /tmp/branches.json"'
        ]
        for line in bash_lines:
            res = self.exec_cmd(line.format(home=odoo_home, user=odoo_user))
            logger.debug(res)
            regex = re.compile(r'Cloning repo (.*?) - branch (.*)')
            matches = regex.finditer(res)
            if matches:
                for match in matches:
                    logger.debug('Object %s', str(match))
                    logger.debug('Groups %s', match.groups())
                    repo = match.group(1)
                    branch = match.group(2)
                    logger.debug('Gotten repo: %s', repo)
                    logger.debug('Gotten branch: %s', branch)
            error_regex = re.compile(r'[fatal|ERROR]: (.*)')
            fatal = error_regex.search(res)
            if fatal:
                logger.error(fatal.group(1))
                success = (False, fatal.group(1))
        if success[0] and addons_path:
            self.exec_cmd('python /tmp/getaddons.py {paths}'.format(paths=addons_path))
        logger.debug(success)
        self.start_instance()
        return success

    @property
    def db_config(self):
        """ Parse env vars from a container to get the needed parameters to dump the database

        :return: dict with the needed configuration parameter
        """

        env_vars = self.docker_env
        logger.debug(json.dumps(env_vars, sort_keys=True, indent=2))
        if env_vars is None:
            logger.warn(
                "No such container (or not started yet)")
            instance_cfg = self.__full_config.get("instance").get("config")
            logger.debug("Instance config dict from json: %s",
                         str(instance_cfg))
            res = {
                'db_host': instance_cfg.get('db_host', None),
                'db_port': instance_cfg.get('db_port', 5432),
                'db_user': instance_cfg.get('db_user', 'odoo'),
                'db_password': instance_cfg.get('db_password'),
            }
        else:
            if env_vars.get('db_host') == 'localhost' \
                    or env_vars.get('db_host') == '127.0.0.1':
                db_host = '127.0.0.1'
                db_port = self.basic_info.get('ports').get('5432')
            else:
                db_host = env_vars.get('db_host')
                db_port = env_vars.get('db_port', 5432)
            res = {
                'db_host': db_host,
                'db_port': db_port,
                'db_user': env_vars.get('db_user', 'odoo'),
                'db_password': env_vars.get('db_password'),
            }

            inspected = self.inspect()
            volumes = inspected.get('Mounts')
            for volume in volumes:
                if '.local/share/Odoo' in volume.get('Destination') and volume:
                    res.update({'data_dir': volume.get('Source')})
                    break
            else:
                logger.error(
                    'Datadir not found, wont be able to backup attachments')

            if not res.get('data_dir'):
                logger.error(('The attachments directory was not mounted from the host,'
                              ' wont be able to backup attachments'))
            res.update({'odoo_container': self.docker_id})

        if res.get('db_host').startswith('172.17.'):
            res.update({'db_host': '127.0.0.1'})
        return res

    def get_dump(self, dest_dir):
        dump_name = path.join(dest_dir, 'database_dump.sql')
        if path.exists(path.join(dest_dir, 'database_dump.b64')):
            logger.debug('Is a backup generated with WS')
            destination_file = path.join(dest_dir, 'backup.zip')
            if 'dump.sql' in os.listdir(dest_dir):
                dump_name = path.join(dest_dir, 'dump.sql')
            else:
                if 'backup.zip' not in os.listdir(dest_dir):
                    utils.decode_b64_file(
                        path.join(dest_dir, 'database_dump.b64'), destination_file)
                if 'backup.zip' in os.listdir(dest_dir):
                    zfile = zipfile.ZipFile(destination_file)
                    logger.info('Unzipping backup')
                    try:
                        zfile.extractall(dest_dir)
                    except IOError as error:
                        logger.error(
                            'Could not extract database_dump.b64: %s', error.message)
                        return None
                    dump_name = path.join(dest_dir, 'dump.sql')
        return dump_name

    def restore_backup(self, dump_name, database_name, dest_dir, rebuild=False):
        odoo_cfg = self.db_config
        odoo_cfg.update({'database': database_name})
        filestore_folder = path.join(dest_dir, 'filestore')
        postgres = PostgresShell(utils.odoo2postgres(odoo_cfg))
        postgres.drop(database_name)
        postgres.restore(database_name, dump_name)
        self.restore_filestore(filestore_folder, database_name)
        return True

    def generate_backup(self, database_name, dest_folder,
                        cformat=False, reason=False, tmp_dir=False, prefix=False):
        """ Generate an instance backup that contains:
            - Database dump in sql format
            - A folder with instance attachments called *filestore*
            - Json file with the repos ans hashes from the actual instance

        .. note:: If the method cannot access the filestore folder it won't be included in the
            backup

        :param dest_folder: Folder where the backup will be stored
        :param  reason: Optional parameter that is used in case
                          there is a particular reason for the backup
        :param tmp_dir (str): Optional parameter to store the temporary working dir,
                                default is /tmp
        :return: Full path to the generated backup
        """
        if not cformat:
            cformat = 'bz2'
        if not tmp_dir:
            tmp_dir = gettempdir()
        odoo_cfg = self.db_config
        odoo_home = self.config.get('env_vars').get('odoo_home')
        odoo_user = self.config.get('env_vars').get('odoo_user')
        odoo_cfg.update({'database': database_name})
        postgres = PostgresShell(utils.odoo2postgres(odoo_cfg))
        dump_name = path.join(tmp_dir, 'database_dump.sql')
        dump_name = postgres.dump(database_name, dump_name)
        if not dump_name:
            logger.error('Database could not be dumped')
            return None
        bkp_name = utils.generate_backup_name(odoo_cfg.get('database'), reason, prefix)
        files2backup = [dump_name]
        if odoo_cfg.get('data_dir'):
            attachments_folder = path.join(odoo_cfg.get('data_dir'),
                                           'filestore',
                                           odoo_cfg.get('database'))
            if path.exists(attachments_folder):
                logger.debug('Attachments folder "%s"', attachments_folder)
                files2backup.append((attachments_folder, 'filestore'))
            else:
                logger.warn(('Folder "%s" does not exists,'
                             ' attachments are not being added to the backup'), attachments_folder)
        else:
            logger.info('There is not attachments folder to backup')
        self.exec_cmd(
            ('su {user} -c "ches.py save -p {home}/instance -f /tmp/repositories.json"')
            .format(user=odoo_user, home=odoo_home)
        )
        json_repos = path.join(self.temp_folder, 'repositories.json')
        if path.exists(json_repos):
            files2backup.append((json_repos, 'repositories.json'))
        logger.info('Compressing files')
        logger.debug('Files : %s', str(files2backup))
        full_name = utils.compress_files(
            bkp_name, files2backup, dest_folder=dest_folder, cformat=cformat)
        logger.info('Compressed backup, cleaning')
        utils.clean_files(dump_name)
        return full_name

    def restore_filestore(self, src_folder, database_name):
        """ Restore a filestore folder into a docker container that is already running
            and has the /tmp folder mounted as a volume un the host

        :param src_folder: Full path to the folder that contains the filestore you want to restore
        :param database_name: Database name being restored
        """
        dest_folder = path.join(self.temp_folder, path.basename(src_folder))
        try:
            shutil.move(src_folder, dest_folder)
        except shutil.Error as error:
            if "already exists" in error.message:
                logger.info("%s folder already exists, replacing", dest_folder)
                utils.clean_files(dest_folder)
                shutil.move(src_folder, dest_folder)
            else:
                raise
        except IOError as error:
            if "No such file or directory" in error.strerror:
                logger.warn("No filestore in the backup file")
            else:
                raise
        data_dir = self._get_fstore_from_config()
        fs_name = path.join(data_dir, "filestore", database_name)
        bash_lines = [
            "rm -rf {fsname}",
            "mkdir -p {newfs}",
            "mv /tmp/filestore {fsname}",
            "chown -R {user}:{user} {fsname}",
            "chmod -R o+r {fsname}"
        ]
        for bash_cmd in bash_lines:
            cmd = bash_cmd.format(
                fsname=fs_name,
                user=self.docker_env.get('odoo_user'),
                newfs=path.join(data_dir, "filestore"))
            res = self.exec_cmd(cmd)
            logger.debug('Command "%s", returned "%s"', cmd, res)

    def _get_fstore_from_config(self):
        data_dir = None
        container_name = self.docker_id
        odoo_config_file = self.docker_env.get('odoo_config_file')
        try:
            res = self.cli.copy(container_name, odoo_config_file)
        except errors.FileNotFoundInContainer:
            logger.error(
                "Odoo config file is not in the path '%s'", odoo_config_file)
            return None
        for line in res.data.split('\n'):
            if line.strip().startswith("data_dir"):
                data_dir = line.split("=")[1].strip()
                break
        return data_dir

    def get_odoo_users(self, database):
        """ Retrieves the user ids of all the current users registered in
        the odoo instance.

        :param database: Name of the database where deployv will retrieve
                         the users ids from.
        :return: List of users ids
        """
        psql_dict = self.db_config
        psql_dict.update({'db_name': database})
        with PostgresConnector(utils.odoo2postgres(psql_dict)) as db:
            users = db.execute("SELECT id,login FROM res_users")
        return users

    def change_password(self, user_id, new_pass, db_name):
        """ Changes the specified user_id password

        :param user_id: Users id
        :param new_pass: New password that will be set to the user
        :param db_name: Database name to be updated
        :return: True if the password was changed, None otherwise
        """
        logger.info('Changing password for user_id %s', user_id)
        default_crypt_context = CryptContext(
            ['pbkdf2_sha512', 'md5_crypt'],
            deprecated=['md5_crypt'],
        )
        psql_dict = self.db_config
        psql_dict.update({'db_name': db_name})
        with PostgresConnector(utils.odoo2postgres(psql_dict)) as db:
            res_user = db.execute(("select password, password_crypt"
                                   " from res_users where id = %(id)s"), {'id': user_id})
            res = None
            if res_user:
                if not res_user[0].get('password') and res_user[0].get('password_crypt'):
                    logger.info('Encrypted password')
                    crypted_passwd = default_crypt_context.encrypt(new_pass)
                    db.execute(("update res_users set password='',"
                                " password_crypt=%(passwd)s where id = %(id)s"),
                               {'passwd': crypted_passwd, 'id': user_id})
                    res = True
                elif res_user[0].get('password') and res_user[0].get('password_crypt') == '':
                    logger.info('Non encrypted password')
                    db.execute("update res_users set password=%(passwd)s where id = %(id)s",
                               {'passwd': new_pass, 'id': user_id})
                    res = True
        return res

    def check_keys(self):
        """ Check if the provided keys into the docker container allows the user to connect
            github.com but does not check permissions

        :return: True if it is a valid key, False otherwise
        """
        logger.info('Checking keys in container %s', self.docker_id)
        res = self.exec_cmd('su {user} -c "ssh -T git@github.com"'
                            .format(user=self.config.get('env_vars').get('odoo_user')))
        if 'successfully authenticated, but GitHub does not provide shell access.' in res:
            logger.info('Keys checked properly')
            return True
        logger.error(
            'An error occurred while trying to connect to github.com: %s', res.strip())
        return False

    def install_deps(self):
        """ Install dependencies specified in the config json (if any). To see the return
        format check :func:`~deployv.base.dockerv.DockerV.install_packages`

        :return: A dic with the installation process
        """
        apt_list = self.config.get('apt_install', None)
        pip_list = self.config.get('pip_install', None)
        res = self.install_packages(apt_list, pip_list)
        return res

    def build_image(self):
        """ Calls the build helper in order to build the image that
        will be used to create the container, updates the configuration
        with the name of the new image and removes all the repos in the config
        if the build_image parameter is true so the repos in the image are not
        overriden when the container is created.

        :return: dict with the result of the build
        """
        build_res = build_helper.build_image(self.__full_config)
        if build_res[0] and build_res[1].get('result'):
            new_image = build_res[1].get('result')
            logger.debug('New image %s', new_image)
            self.config.update({'image_name': new_image})
            if self.__full_config.get('container_config').get('build_image'):
                self.__full_config.get('instance').update({'repositories': []})
        return build_res

    def _update_env_vars(self, env):
        """ Export enviroment when create container
            updated the dictionary env_vars
        :param env: dictionary with new variable environment to export
        """
        self.__full_config.get('container_config').get('env_vars').update(env)


def deactivate_database(config, db_name):
    """ Deactivate a database: mail, cron (all but osv_memory.autovacuum, pac

    :param config: Config dict used to create the container and instance
    :param db_name: Database to be deactivated
    """

    logger.info('Deactivating database %s', db_name)
    # Sqls to be executed
    sqls = {
        'partner': "UPDATE res_partner SET opt_out = True;",
        'out_mail': ("UPDATE ir_mail_server"
                     " SET active = False, smtp_user = 'user', smtp_pass = 'pass';"),
        'in_mail': ("UPDATE fetchmail_server"
                    " SET active = False, \"user\" = 'user', password = 'pass';"),
        'pac': "UPDATE params_pac SET active = False;",
        'cron': "UPDATE ir_cron SET active = False WHERE model <> 'osv_memory.autovacuum';",
        'notify': "UPDATE res_partner SET notify_email = 'none'",
        'ir_action': ("UPDATE base_action_rule SET active = False"
                      " WHERE name LIKE '%Create Sale from Purchase%'"),
        'url_freeze': "DELETE FROM ir_config_parameter WHERE key = 'web.base.url.freeze';"
    }

    psql_dict = {
        'dbname': db_name,
        'user': config.get('db_user'),
        'host': config.get('db_host'),
        'password': config.get('db_password'),
        'port': config.get('db_port', 5432)
    }

    try:
        with postgresv.PostgresConnector(psql_dict) as db:
            for name, sql in sqls.items():
                logger.debug('Running %s', name)
                try:
                    db.execute(sql)
                except psycopg2.ProgrammingError as error:
                    if 'relation' in error.message:
                        logger.warn(
                            'This database has not %s, nothing to execute', name)
                    else:
                        raise
    except psycopg2.OperationalError as error:
        logger.exception('Could not deactivate the database: %s', error.message)
        return False
