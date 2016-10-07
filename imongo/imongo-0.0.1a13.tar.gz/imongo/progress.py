# 项目：标准数据库模块
# 模块：进度条
# 作者：黄涛
# License:GPL
# Email:huangtao.sh@icloud.com
# 创建：2016-08-30 14:49

from threading import *
lock=Lock()

class Progress:
    def __init__(self,maximum=100,base=0,owner=None,name='',
                 mode=0,updated=None):
        self.position=0       # 当前进度
        self.maximum=maximum  # 最大值
        self.base=base        # 本进度占用主进度的数量
        self.owner=owner      # 本进度所属的进度
        self.name=name        # 本进度的名称
        self.mode=mode        # 处理模式：0-子流程处理，1-主流程自行处理
        if updated:
            self.updated=updated

    def updated(self,name=None,position=0,msg=None):
        if position:
            print('\r%s\t%03.2f'%(name,position*100/self.maximum),
                  end='')
        if msg:
            print(msg)
    
    def do_update(self,position=0,msg=None):
        with lock:
            self.updated(self.name,position,msg)
                    
    def update(self,current=0,msg=None):
        if msg:
            self.do_update(msg=msg)
        if current:
            self.position+=current
            if self.position>=self.maximum:
                msg='\n%s 完成！'%(self.name)
            if self.owner:
                self.owner.update(current*self.base/self.maximum,msg)
            else:
                self.do_update(self.position,msg)
                        
    def new(self,maximum,base=1,name=''):
        owner=self if self.mode else None
        return Progress(maximum,base,owner=owner,name=name,
                        updated=self.updated)
