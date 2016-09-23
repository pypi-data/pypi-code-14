# 递归的遍历一个List，并打印所有元素，包括缩进
def print_lol(the_list, level):
    for each in the_list:
        if isinstance(each, list):
            print_lol(each, level+1)
        else:
            for tab_stop in range(level):
                print('\t', end='')
            print(each)
'''
本地发布：
1. 在所在目录下创建setup.py文件
2. 构建发布文件，使用命令行工具cd到目录下，执行：
    python3 setup.py sdist
3. 将发布安装到Python本地副本中，可以直接import，执行：
    python3 setup.py install

发布到PyPI社区:
4. 想PyPI上传发布，第一次上传时需要进行一次注册
    python3 setup.py register
5. 上传发布：
    python3 setup.py sdist upload
'''
