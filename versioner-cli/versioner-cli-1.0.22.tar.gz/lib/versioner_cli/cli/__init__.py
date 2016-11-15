from future import standard_library

standard_library.install_aliases()
import logging
from subprocess import getoutput, CalledProcessError, PIPE

PYTHON2 = False
try:
    from subprocess import run
except ImportError:
    logging.getLogger(__name__).info('running python2')
    PYTHON2 = True
from os import environ
from docker import Client
from docker.errors import APIError
import requests
import json
from requests.auth import HTTPBasicAuth
from requests.packages.urllib3.exceptions import InsecureRequestWarning, SNIMissingWarning, InsecurePlatformWarning
from future.utils import raise_with_traceback
from os.path import expanduser, join, isfile
from os import environ
from .config import VersionerConfig
from .tasks import verify_task, Tasks
from .exceptions import ConfigValueError
from versioner_cli.api import VersionerApi
from .enums import ContinuousDeliveryEnum
from os.path import expanduser, join

logger = logging.getLogger(__name__)
ch = logging.StreamHandler()
logger.setLevel(logging.DEBUG)
logger.addHandler(ch)


def find_config(*args, **kwargs):
    """

    :param args:
    :param kwargs:
    :return:
    """
    lookup_order = [join(expanduser('~'), '.versioner'), environ.get('VERSIONER_CONFIG', VersionerCli.DEFAULT_CONFIG_PATH)]
    for i, path in enumerate(lookup_order):

        if path is not None:
            try:
                if isfile(path):
                    return lookup_order[i]
            except AttributeError as msg:
                logger.info(msg)


class VersionerCli(object):
    DEFAULT_CONFIG_PATH = '/etc/default/versioner'
    pre_tasks = []
    build_tasks = []
    post_tasks = []

    @staticmethod
    def continuous_deployment_hook(username, password, url):
        """

        :param username:
        :param password:
        :param url:
        :return:
        """
        if requests.post(url, auth=HTTPBasicAuth(username=username, password=password), verify=False).status_code == 200:
            return True
        return False

    def tag_docker(self, image, version, repo):
        """

        :param image:
        :param version:
        :param repo:
        :return:
        """
        print('Tagging docker version\nimage: {}\nversion: {}\nrepo: {}'.format(image, version, repo))
        success = self.docker.tag(image=image, tag=version, repository=repo)
        if success:
            response = [line for line in self.docker.push(repo, tag=version, stream=True, auth_config=self.docker_auth)]
            if 'error' in ''.join(response):
                raise_with_traceback(APIError('Something went wrong pushing to dockerhub'))
            return True

    def npm_version(self, version):
        """

        :param version:
        :return:
        """
        logger.info('changing package.json file')
        data = None
        with open(join(expanduser('~'), self.config.project_name, 'package.json')) as json_file:
            data = json.load(json_file)
            data['version'] = version
        with open(join(expanduser('~'), self.config.project_name, 'package.json'), 'w') as write_file:
            json.dump(data, write_file)

    def npm_publish(self, tag):
        """

        :param tag:
        :return:
        """
        try:
            logger.info('running npm publish'.format(tag))
            if not PYTHON2:
                if self.branch_from == 'master':
                    output = run(["npm", "publish"],
                                 shell=True,
                                 check=True,
                                 universal_newlines=True,
                                 stdout=PIPE)
                else:
                    output = run(["npm", "publish", "--tag={}".format(self.branch_from)],
                                 shell=True,
                                 check=True,
                                 universal_newlines=True,
                                 stdout=PIPE)

            else:
                if self.branch_from == 'master':
                    output = getoutput("npm publish").rstrip('\n')
                else:
                    output = getoutput("npm publish --tag={}".format(self.branch_from)).rstrip('\n')
                logger.info('output: {}'.format(output))
        except CalledProcessError as msg:
            logger.error(msg)

    def git_push_flags(self):
        """

        :param args:
        :param kwargs:
        :return:
        """
        try:
            logger.info('running git publish --follow-flags')
            if not PYTHON2:
                output = run(["git", "push", "--follow-flags"], shell=True, check=True, universal_newlines=True,
                             stdout=PIPE)
            else:
                output = getoutput("git push --follow-flags").rstrip('\n')
                logger.info('output: {}'.format(output))
        except CalledProcessError as msg:
            logger.error(msg)

    def trigger_cd(self, environment):
        jenkins_username = environ.get('JENKINS_USER')
        jenkins_password = environ.get('JENKINS_API_TOKEN')
        if jenkins_username is not None and jenkins_password is not None:
            if environment == ContinuousDeliveryEnum.dev.value:
                response = requests.post(self.config.continuous_deployment_hook_dev, auth=HTTPBasicAuth(username=jenkins_username,
                                                                                password=jenkins_password), verify=False)
            elif environment == ContinuousDeliveryEnum.stage.value:
                response = requests.post(self.config.continuous_deployment_hook_stage, auth=HTTPBasicAuth(username=jenkins_username,
                                                                                password=jenkins_password), verify=False)

            print('Jenkins Response Status: {}'.format(response.status_code))
        else:
            logger.error('BAD ENVIRONMENT VARIABLES FOR JENKINS')
            raise_with_traceback(LookupError('BAD ENVIRONMENT VARIABLES FOR JENKINS'))

    def execute_pre_tasks(self, pre_tasks):
        for task in pre_tasks:
            if task == 'get version':
                logger.info('executing get version')
                build_num = environ.get('CIRCLE_BUILD_NUM', None)
                commit_hash = environ.get('CIRCLE_SHA1', None)
                if build_num is not None:
                    if self.args.build_type is not None:
                        self.version = self.api.bump_version(bump_type=self.branch_from,
                                              project_name=self.config.project_name,
                                              branch_from=self.args.build_type,
                                              build_number=build_num)
                    else:
                        self.version = self.api.bump_version(bump_type=self.args.build_type,
                                              project_name=self.config.project_name,
                                              build_number=build_num,
                                              branch_from=self.args.build_type)
                else:
                    self.version = self.api.bump_version(bump_type=self.args.build_type,
                                                         project_name=self.config.project_name,
                                                         branch_from=self.args.build_type,
                                                         merge_to=self.args.merge_to)

    def parse_pre_tasks(self):
        pre_tasks = []
        if hasattr(self.config, 'pre_tasks'):
            for task in self.config.pre_tasks:
                try:
                    pre_tasks.append(verify_task(Tasks.pre_tasks.value, task))
                except ConfigValueError as msg:
                    logger.error(msg)
            return pre_tasks
        return None

    def parse_tasks(self):
        tasks = []
        if hasattr(self.config, 'tasks'):
            for task in self.config.tasks:
                try:
                    tasks.append(verify_task(Tasks.tasks.value, task))
                except ConfigValueError as msg:
                    logger.error(msg)
            return tasks
        return None

    def execute_main_tasks(self, main_tasks):
        for task in main_tasks:
            if task == 'tag docker':
                self.tag_docker(image=self.config.docker_image, version=self.version, repo=self.config.docker_repo)
            elif task == 'version npm':
                self.npm_version(self.version)

    def parse_post_tasks(self):
        post_tasks = []
        if hasattr(self.config, 'post_tasks'):
            for task in self.config.post_tasks:
                try:
                    post_tasks.append(verify_task(Tasks.post_tasks.value, task))
                except ConfigValueError as msg:
                    logger.error(msg)
            return post_tasks
        return None

    def execute_post_tasks(self, post_tasks):
        for task in post_tasks:
            if task == 'publish npm':
                self.npm_publish(self.version)
            elif task == 'release versioner':
                self.api.make_release(project_name=self.config.project_name,
                                      version=self.version,
                                      type='Environment',
                                      text=self.args.build_type)
            elif task == 'trigger cd':
                if self.branch_from.lower() == 'development':
                    self.trigger_cd(ContinuousDeliveryEnum.dev.value)
                elif self.branch_from.lower() == 'master':
                    self.trigger_cd(ContinuousDeliveryEnum.stage.value)

    def parse_cli(self):
        if self.args.config is not None:
            self.config_path = self.args.config
        else:
            self.config_path = find_config()
        return self.config_path

    def setup(self):
        """
        Logs into docker and binds docker client.
        :return:
        """
        docker_user = environ.get('DOCKER_USER')
        docker_pass = environ.get('DOCKER_PASS')
        docker_email = environ.get('DOCKER_EMAIL')
        if None in [docker_email, docker_pass, docker_user]:
            logger.error('Environment Variable not set')
            raise_with_traceback(LookupError('Environment Variable not set'))
        self.docker = Client(base_url='unix://var/run/docker.sock', version='1.21')
        try:
            self.docker_auth = self.docker.login(username=docker_user,
                                                 password=docker_pass,
                                                 email=docker_email)
        except APIError as msg:
            logger.error(msg)
        self.config = VersionerConfig(self.parse_cli())

    def __init__(self, args):
        """
        Takes args from CLI and stores as a property. Calls setup and looks for docker auth environment variables.
        Looks for environment variables: CI_PULL_REQUEST, CIRCLE_BRANCH, VERSIONER_USER, VERSIONER_PASSWORD
        :param args:
        """
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
        requests.packages.urllib3.disable_warnings(SNIMissingWarning)
        requests.packages.urllib3.disable_warnings(InsecurePlatformWarning)
        self.args = args
        self.config = None
        self.config_path = None
        self.version = None
        self.build_type = self.args.build_type
        self.docker = None
        self.docker_auth = {}
        self.setup()
        self.pull_request = environ.get('CI_PULL_REQUEST', args.pull_request)
        self.branch_from = environ.get('CIRCLE_BRANCH', args.build_type)
        self.api = VersionerApi(endpoint=self.config.versioner_endpoint,
                                username=environ.get('VERSIONER_USER'),
                                password=environ.get('VERSIONER_PASSWORD'))
        pre_tasks = self.parse_pre_tasks()
        if pre_tasks is not None:
            self.execute_pre_tasks(pre_tasks)
        else:
            logger.warning('No pre tasks')
        main_tasks = self.parse_tasks()
        if main_tasks is not None:
            self.execute_main_tasks(main_tasks)
        else:
            logger.warning('No main tasks')
        post_tasks = self.parse_post_tasks()
        if post_tasks is not None:
            self.execute_post_tasks(post_tasks)
        else:
            logger.warning('No post tasks')
