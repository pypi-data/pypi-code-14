import os

from gbdx_task_template.test.test_base import TestBase, temp_env_var
from gbdx_task_template import InputPort, OutputPort
from gbdx_task_template.port import InvalidPortType, LocalPortValidationError, RemotePortValidationError


class TestPort(TestBase):

    def test_bad_port_type(self):
        try:
            InputPort(value='.', port_type='int')
        except InvalidPortType as e:
            assert 'Port has an invalid port type.' == e.message

    def test_none_port_value(self):
        np = InputPort(value=None)
        try:
            np.path
        except ValueError as e:
            assert 'Directory ports must be provided with a location' == e.message

    def test_port_cwd_shortcut(self):
        np = InputPort(value='.')
        np.name = 'hi'
        assert np.path == os.getcwd()
        nnp = InputPort(value='')
        nnp.name = 'ho'
        assert nnp.path != os.getcwd()
        nnp.value = os.getcwd()
        assert np != nnp

    def test_port_list_files(self):
        path = os.path.dirname(os.path.realpath(__file__))

        port = InputPort(value=path)
        all_files = port.list_files()
        self.assertIn(__file__, all_files)
        for f in all_files:
            self.assertTrue(os.path.isfile(f))

        py_files = port.list_files(extensions=".py")

        self.assertIn(__file__, py_files)

        pyc_files = port.list_files(extensions=".pyc")

        self.assertNotIn(__file__, pyc_files)

        self.assertGreater(len(all_files), len(py_files))
        self.assertGreater(len(all_files), len(pyc_files))

    def test_port_list_files_bad_path(self):
        bad_path = 'not/good/path'
        port = InputPort(value=bad_path)
        try:
            port.list_files()
        except ValueError as e:
            self.assertIn('Port %s' % bad_path, e.message)

    def test_port_list_files_good_remote_path(self):
        good_path = os.path.dirname(os.path.realpath(__file__))
        port = InputPort(value=good_path)
        port.name = 'test'
        all_files = port.list_files(extensions=".py")
        self.assertEqual(len(all_files), 5)

    def test_port_write_good_path(self):
        """
        Test write to a port, relative to the port
        """
        good_path = os.path.dirname(os.path.realpath(__file__))
        port = OutputPort(value=good_path)

        # Write to file relative to port path.
        port.write('test.txt', 'Hello World')

        file_name = os.path.join(good_path, 'test.txt')

        with open(file_name, 'r') as f:
            self.assertEqual('Hello World', f.read())

    def test_port_write_good_path_abs(self):
        """
        Test write to a port, with an absolute filename
        """
        good_path = os.path.dirname(os.path.realpath(__file__))
        file_name = os.path.join(good_path, 'test.txt')

        port = OutputPort(value=good_path)

        # Write to abs path
        try:
            port.write(file_name, 'Hello World')
        except ValueError as e:
            self.assertIn('File name must be relative', e.message)

    def test_port_write_bad_port(self):
        good_path = os.path.dirname(os.path.realpath(__file__))
        port = InputPort(value=good_path)
        try:
            port.write('test.txt', 'Hello World')
        except ValueError as e:
            self.assertIn('Only Output ports', e.message)

    def test_port_write_bad_port2(self):
        good_path = os.path.dirname(os.path.realpath(__file__))
        port = OutputPort(port_type='string', value=good_path)
        try:
            port.write('test.txt', 'Hello World')
        except ValueError as e:
            self.assertIn('Only Directory ports', e.message)

    @temp_env_var(REMOTE_WORK_PATH=os.getcwd())
    def test_port_write_remote_path(self):
        good_path = os.path.dirname(os.path.realpath(__file__))
        port = OutputPort(value=good_path)
        port.name = 'test_port'
        expected_path = os.path.join(os.getcwd(), 'output', 'dir_test_port')
        self.assertEquals(port.path, expected_path)

    def test_port_string(self):
        port = OutputPort(port_type='string')
        port.name = 'test_port'
        port.value = 10
        self.assertEquals(port.json['name'], 'str_test_port')
        self.assertEquals(port.type, 'string')

    def test_invalid_port_paths(self):
        port = OutputPort(value='hi')
        try:
            port.is_valid_filesys(port.path)
        except LocalPortValidationError as e:
            assert 'not a valid filesystem location' in e.message

        try:
            port.is_valid_s3_url(port.path)
        except RemotePortValidationError as e:
            assert 'not a valid s3 location' in e.message

    def tearDown(self):
        try:
            path = os.path.dirname(os.path.realpath(__file__))
            file_name = os.path.join(path, 'test.txt')
            os.remove(file_name)
        except Exception:
            pass
