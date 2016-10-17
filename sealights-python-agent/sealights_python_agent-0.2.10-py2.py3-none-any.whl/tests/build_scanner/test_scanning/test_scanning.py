from pyfakefs import fake_filesystem_unittest, fake_filesystem

from python_agent.build_scanner.main import get_all_files
from python_agent.utils import get_top_relative_path


class TestScanning(fake_filesystem_unittest.TestCase):

    def setUp(self):
        self.setUpPyfakefs()
        self.fs.CreateDirectory("/opt")
        self.fs.CreateDirectory("/opt/python_agent")
        self.fs.CreateDirectory("/opt/python_agent/python_agent")
        self.fs.CreateFile("/opt/python_agent/python_agent/__init__.py")
        self.fs.CreateFile("/opt/python_agent/setup.py")
        self.fs.CreateFile("/opt/python_agent/__init__.py")
        self.fs.CreateFile("/opt/python_agent/foo.py")
        os_module = fake_filesystem.FakeOsModule(self.fs)
        os_module.chdir("/opt/python_agent/python_agent")

    def test_only_source(self):
        files = get_all_files(sources=["/opt/python_agent"], includes=None, excludes=None)
        self.assertEqual(
            set(["/opt/python_agent/setup.py", "/opt/python_agent/__init__.py",
             "/opt/python_agent/foo.py", "/opt/python_agent/python_agent/__init__.py"]),
            set(files)
        )

    def test_source_include(self):
        self.fs.CreateFile("/opt/python_agent/python_agent/ooo.py")
        files = get_all_files(sources=["/opt/python_agent"], includes=["*o.py"], excludes=None)
        self.assertEqual(
            set(["/opt/python_agent/foo.py", "/opt/python_agent/python_agent/ooo.py"]),
            set(files)
        )

    def test_source_exclude(self):
        self.fs.CreateFile("/opt/python_agent/python_agent/ooo.py")
        files = get_all_files(sources=["/opt/python_agent"], includes=None, excludes=["*o.py", "python_agent/*o.py"])
        self.assertEqual(
            set(["/opt/python_agent/setup.py", "/opt/python_agent/__init__.py", "/opt/python_agent/python_agent/__init__.py"]),
            set(files)
        )

    def test_source_include_exclude(self):
        files = get_all_files(sources=["/opt/python_agent"], includes=None, excludes=["*o.py", "python_agent/*o.py"])
        self.assertEqual(
            set(["/opt/python_agent/setup.py", "/opt/python_agent/__init__.py", "/opt/python_agent/python_agent/__init__.py"]),
            set(files)
        )

    def test_include_exclude(self):
        self.fs.CreateFile("/opt/python_agent/python_agent/ooo.py")
        self.fs.CreateFile("/opt/python_agent/python_agent/a.py")
        self.fs.CreateFile("/opt/python_agent/python_agent/b.py")
        self.fs.CreateFile("/opt/python_agent/python_agent/cd.py")
        files = get_all_files(
            sources=["/opt/python_agent"],
            includes=["/opt/python_agent/python_agent/*"],
            excludes=["python_agent/*o.py"]
        )
        self.assertEqual(
            set([
                "/opt/python_agent/python_agent/a.py",
                "/opt/python_agent/python_agent/b.py",
                "/opt/python_agent/python_agent/cd.py",
                "/opt/python_agent/python_agent/__init__.py"
            ]),
            set(files)
        )

    def test_relative_path(self):
        self.fs.CreateFile("/opt/python_agent/python_agent/ooo.py")
        self.fs.CreateFile("/opt/python_agent/python_agent/a.py")
        self.fs.CreateFile("/opt/python_agent/python_agent/b.py")
        self.fs.CreateFile("/opt/python_agent/python_agent/cd.py")
        self.fs.CreateFile("/opt/python_agent/python_agent/utils/cd.py")
        files = get_all_files(
            sources=["/opt/python_agent"],
            includes=["/opt/python_agent/python_agent/*"],
            excludes=["python_agent/*o.py"]
        )
        rel_paths = map(get_top_relative_path, files)

        self.assertEqual(
            set([
                "a.py",
                "b.py",
                "cd.py",
                "utils/cd.py",
                "__init__.py"
            ]),
            set(rel_paths)
        )