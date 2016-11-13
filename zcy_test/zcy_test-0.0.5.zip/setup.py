from setuptools import setup, find_packages
setup(
      name="zcy_test",
      version="0.0.5",
      description="My test module",
      author="zcy",
      author_email="zcy19941015@qq.com",
      url="http://www.csdn.net",
      license="LGPL",
      packages= find_packages(),
      scripts=["zcy_test/test1.py"],
      entry_points={
        "console_scripts":[
            "zcy_test = zcy_test.test1:test_print"
            ]
      }
      )