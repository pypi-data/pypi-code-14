
# -*- coding: UTF-8 -*-
import os.path
from log import logger as logging

class Orchestra(object):
    def __init__(self, topo_config , task_path=None):
        logging.info("init orchestra:{}".format(topo_config))
        self.topo_config_file = topo_config
        logging.debug("topo file:{}".format(topo_config))
        # 如果任务文件的路径 没有指定，假设和topo_config存放在同一目录下
        # TODO: 配置文件描述，每个task路径
        if task_path is None:
            self.path = os.path.abspath(os.path.dirname(topo_config))
        else:
            self.path = task_path
        logging.debug("topo path:{}".format(self.path))

        self.task_list = []

        self.read_topology(topo_config)

        self.task_list = [ os.path.join(self.path,x)  for x in  self.task_list ] 

    def read_topology(self,filename):
        """
        通过配置文件，获得拓扑顺序
        """
        try:
            with open(filename,"rb") as f:
                self.task_list = [ line.strip() for line in f.readlines() ]
                logging.debug("get task_list:{}".format(self.task_list))
        except:
            logging.debug("Execption",exc_info=True)
            logging.error("topo file open failed:",filename)


    def store_topology(self):
        pass

    def print_topology(self):
        for task in self.task_list:
            print(task)

    def topo_order_list(self):
        return self.task_list

if __name__ == "__main__":
    o1= Orchestra("../02-bugfix/SP1/patch.list")
    o1.print_topology()

