import os
import tarfile
import shutil


from gbdx_task_template.test.test_base import TestBase
from gbdx_cloud_harness import TaskController


class TestApp(TestBase):

    def setUp(self):
        self.DIRS_TO_REMOVE = []
        self.FILES_TO_REMOVE = []

    def test_get_filename_pos(self):
        app = TaskController(None)

        # filename only.
        test_path1 = app._get_template_abs_path('app.py')
        exp_result1 = os.path.join(os.getcwd(), 'app.py')
        self.assertEqual(exp_result1, test_path1)

        # Test filename is absolute
        test_filename2 = os.path.abspath(__file__)
        test_path2 = app._get_template_abs_path(test_filename2)
        self.assertEqual(test_filename2, test_path2)

    def test_archive_pos_filter(self):
        test_path_dest = os.path.dirname(os.path.realpath(__file__))
        test_path_src = os.path.join(test_path_dest, 'input')

        filter_file = os.path.join(test_path_src, TaskController.IGNORE_FILES_NAME)
        self.FILES_TO_REMOVE.append(filter_file)
        with open(filter_file, 'a') as f:
            f.write('imgs/\n')
            f.write('README.md\n')

        TaskController._archive_source(test_path_src, test_path_dest)

        arch_tar = tarfile.open(os.path.join(test_path_dest, 'archive.tar.gz'))
        self.FILES_TO_REMOVE.append(arch_tar.name)
        filenames = arch_tar.getnames()
        self.assertIn('app.py', filenames)
        self.assertNotIn('README.md', filenames)
        self.assertIn('data/readme.txt', filenames)
        self.assertIn('data/subsub/test.rst', filenames)
        self.assertNotIn('imgs/tester.png', filenames)

    def test_archive_pos(self):

        test_path_dest = os.path.dirname(os.path.realpath(__file__))
        test_path_src = os.path.join(test_path_dest, 'input')

        TaskController._archive_source(test_path_src, test_path_dest)

        arch_tar = tarfile.open(os.path.join(test_path_dest, 'archive.tar.gz'))
        self.FILES_TO_REMOVE.append(arch_tar.name)
        filenames = arch_tar.getnames()
        self.assertIn('app.py', filenames)
        self.assertIn('README.md', filenames)
        self.assertIn('data/readme.txt', filenames)
        self.assertIn('data/subsub/test.rst', filenames)
        self.assertIn('imgs/tester.png', filenames)

    def test_create_neg(self):

        bad_dir_names = [
            '/new_test_app',  # abs paths not allowed
            'my/dir',  # No path seperators allowed.
        ]

        args = {
            '--destination': None,
            '--download': False,
            '--remote': False,
            '--upload': False,
            '--verbose': False,
            '<file_name>': None,
            'create': True,
            'run': False,
            'register': False
        }

        for baddir in bad_dir_names:
            args['<dir_name>'] = baddir
            app_ctrl = TaskController(args)

            try:
                app_ctrl.invoke()
                self.assertTrue(False)
            except ValueError as e:
                self.assertTrue('Directory name is invalid' in e.message)

    def test_create_pos(self):

        curr_path = os.getcwd()
        dir_name = 'new_test_dir'
        dir_path = os.path.join(curr_path, dir_name)
        self.DIRS_TO_REMOVE.append(dir_path)

        args = {
            '--destination': None,
            '--download': False,
            '--remote': False,
            '--upload': False,
            '--verbose': False,
            '<file_name>': None,
            '<dir_name>': dir_name,
            'create': True,
            'run': False,
            'register': False
        }

        app_ctrl = TaskController(args)
        app_ctrl.invoke()

        exp_result = os.path.join(dir_path, TaskController.DEFAULT_NEW_APP_FILENAME)

        self.assertTrue(os.path.isdir(dir_path))
        self.assertTrue(os.path.isfile(exp_result))

    def test_create_dest_neg(self):

        dir_name = 'new_test_dir'

        bad_destinations = [
            'relative/path',  # relative paths have to exist
            ''  # Empty string not allowed
        ]

        args = {
            '--download': False,
            '--remote': False,
            '--upload': False,
            '--verbose': False,
            '<file_name>': None,
            '<dir_name>': dir_name,
            'create': True,
            'run': False,
            'register': False
        }

        for baddest in bad_destinations:
            args['--destination'] = baddest
            app_ctrl = TaskController(args)

            try:
                app_ctrl.invoke()
                self.assertTrue(False)
            except ValueError as e:
                self.assertTrue('not a directory' in e.message or 'path is empty' in e.message)

    def test_create_dest_pos(self):
        # Test with relative destination.
        curr_path = os.path.dirname(os.path.abspath(__file__))
        dir_name = 'new_test_dir'
        dest_name = curr_path[len(os.getcwd()) + 1:]
        dir_path = os.path.join(curr_path, dir_name)
        self.DIRS_TO_REMOVE.append(dir_path)

        args = {
            '--destination': dest_name,
            '--download': False,
            '--remote': False,
            '--upload': False,
            '--verbose': False,
            '<file_name>': None,
            '<dir_name>': dir_name,
            'create': True,
            'run': False,
            'register': False
        }

        app_ctrl = TaskController(args)
        app_ctrl.invoke()

        exp_result = os.path.join(dir_path, TaskController.DEFAULT_NEW_APP_FILENAME)

        self.assertTrue(os.path.isdir(dir_path))
        self.assertTrue(os.path.isfile(exp_result))

    def test_create_dest_pos_abs(self):
        # Test with absolute destination.
        dir_name = 'new_test_dir'
        dest_name = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'input', 'data')
        dir_path = os.path.join(dest_name, dir_name)
        self.DIRS_TO_REMOVE.append(dir_path)

        args = {
            '--destination': dest_name,
            '--download': False,
            '--remote': False,
            '--upload': False,
            '--verbose': False,
            '<file_name>': None,
            '<dir_name>': dir_name,
            'create': True,
            'run': False,
            'register': False
        }

        app_ctrl = TaskController(args)
        app_ctrl.invoke()

        exp_result = os.path.join(dir_path, TaskController.DEFAULT_NEW_APP_FILENAME)

        self.assertTrue(os.path.isdir(dir_path))
        self.assertTrue(os.path.isfile(exp_result))

    def test_run_pos(self):

        filename = os.path.join('examples', 'echo_task', 'app.py')
        self.FILES_TO_REMOVE.append(
            os.path.join('examples', 'echo_task', '.cloud_harness_config.json')
        )

        args = {
            '--destination': None,
            '--download': False,
            '--remote': False,
            '--upload': False,
            '--verbose': True,
            '<file_name>': filename,
            '<dir_name>': None,
            'create': False,
            'run': True,
            'register': False
        }

        app_ctrl = TaskController(args)
        app_ctrl.invoke()
        self.assertTrue(True)  # Test passes if no exception raised...

        # test with filename the doesn't exist
        args['<file_name>'] = 'does_not_exist.py'

        app_ctrl = TaskController(args)

        try:
            app_ctrl.invoke()
        except ValueError as e:
            self.assertTrue('does not exist' in e.message)

    def tearDown(self):

        for filename in self.FILES_TO_REMOVE:
            self._remove_file(filename)

        for dirname in self.DIRS_TO_REMOVE:
            shutil.rmtree(dirname)

    @staticmethod
    def _remove_file(filename):

        if not os.path.isfile(filename):
            return

        os.remove(filename)
