"""这是“xianshi.py”模块，提供了一个名为duocengdayin()的函数，这个函
数的作用是打印列表，其中有可能包含（也可能不包含）嵌套列表"""
def duocengdayin(a):
        """这个函数取一个位置参数，名为“a”,这可以是任何python列表
        （也可以是包含嵌套列表的列表）。所指定的列表中的每个数据项会
        （递归地）输出到屏幕上，各数据各占一行。"""
        for b in a:
                if isinstance(b,list):
                        duocengdayin(b)
                else:
                        print(b)
