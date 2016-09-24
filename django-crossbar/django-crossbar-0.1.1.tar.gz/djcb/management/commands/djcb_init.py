from django.core.management.base import BaseCommand, CommandError
import os
import sys
from django.core import exceptions
from django.conf import settings
import subprocess

from django.template import Context, Engine
from django.utils.encoding import smart_str
import simplejson as json

class NotRunningInTTYException(Exception):
    pass


class NoCrossbarException(Exception):
    pass


class Command(BaseCommand):
    help = 'Sets up project for djcb.  Note: will add files to your project'

    def execute(self, *args, **options):
        self.stdin = options.get('stdin', sys.stdin)  # Used for testing
        return super(Command, self).execute(*args, **options)

    def handle(self, *args, **options):

        # if not self.check_crossbar_exists():
        #     self.stdout.write('Crossbar (.crossbar) directory not found in project root.')

        #     if hasattr(self.stdin, 'isatty') and not self.stdin.isatty():
        #         raise NotRunningInTTYException("Not running in a TTY")
        #     doinit = self.get_yn_input_data("y/n: ")
        #     if doinit.upper() == "Y":
        #         self.do_crossbar_init()
        #     elif doinit.upper() == "N":
        #         self.stderr.write("No crossbar config in project directory.  Please run $ crossbar init and try again.")
        #         return


        self.settingsdir = self.find_django_settings()

        self.stdout.write('Setting up project files')
        self.setup_project_files()
        # self.setup_cb_config_json()
        #self.place_file_from_tempalate("test", "test")
        #self.stdout.write('current file: "%s"' % settings.DJANGO_SETTINGS_MODULE)

    def get_yn_input_data(self, message, default=None):
        """
        Override this method if you want to customize data inputs or
        validation exceptions.
        """
        valid_response = False
        while valid_response is False:
            raw_value = raw_input(message)
            if raw_value.upper() == "Y":
                valid_response = True
            elif raw_value.upper() == "N":
                valid_response = True

        return raw_value

    def check_crossbar_exists(self):
        """
        Checks to see if the .crossbar/config.json exists in project BASE_DIR
        """
        if os.path.exists(os.path.join(settings.BASE_DIR, '.crossbar', 'config.json')):
            return True
        else:
            return False

    def do_crossbar_init(self):
        """
        Runs crossbar init from the project folder
        """

        process = subprocess.Popen(['crossbar init'], cwd=settings.BASE_DIR, shell=True,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)

        # wait for the process to terminate
        out, err = process.communicate()
        errcode = process.returncode

    def place_file_from_tempalate(self, template, destination):
        """
        Takes [template] files from _setup directory and puts them at destination
        """
        file = open(os.path.join(os.path.dirname(__file__), '_setup', template), 'r')

        file_template = file.read()
        file_contents = smart_str(Engine().from_string(file_template).render(Context({'projdir': self.settingsdir})))

        writefile = open(destination,"w")
        writefile.write(file_contents)
        writefile.close()

    def find_django_settings(self):
        for dirpath, dirnames, files in os.walk(settings.BASE_DIR):
            for name in files:
                if name.lower() == "settings.py":
                    return os.path.basename(dirpath)
        return False

    def check_setup_destination_exists(self, filename):
        """
        Checks to see if the .crossbar/config.json exists in project BASE_DIR
        """
        if os.path.exists(os.path.join(settings.BASE_DIR, self.settingsdir, filename)):
            return True
        else:
            return False

    def setup_project_files(self):
        """seup files needed for everything to work"""
        if not self.check_setup_destination_exists('celery.py'):
            print "writing celery.py to %s" % os.path.join(settings.BASE_DIR, self.settingsdir, 'celery.py')
        self.place_file_from_tempalate('celery.py.template', os.path.join(settings.BASE_DIR, self.settingsdir, 'celery.py'))
        self.place_file_from_tempalate('backend.py.template', os.path.join(settings.BASE_DIR, self.settingsdir, 'backend.py'))
        os.mkdir(os.path.join(settings.BASE_DIR, '.crossbar'))
        self.place_file_from_tempalate('config.json.template', os.path.join(settings.BASE_DIR, '.crossbar', 'config.json'))


    def setup_cb_config_json(self):
        file = open(os.path.join(settings.BASE_DIR, '.crossbar', 'config.json'), 'r')
        file_contents = file.read()
        config_json = json.loads(file_contents)
        print config_json
        for a in config_json["workers"]:
            print a["type"]