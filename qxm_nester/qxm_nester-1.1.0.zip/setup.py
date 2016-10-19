# 从Python发布工具导入“setup”函数
from distutils.core import setup

setup(
    # setup函数的参数
    name='qxm_nester',                                 # 包名
    version='1.1.0',                                    # 版本号
    py_modules=['nester'],                              # 将模块的元数据与setup函数中的参数关联
    author='qxm',                                        # 作者--可变动
    author_email='1223418981@qq.com',                  # 作者邮箱--可变动
    url='https://www.baidu.com/',                      # 获取地址--可变动
    description='A simple printer of nested lists',   # 代码作用描述--可变动
     )
