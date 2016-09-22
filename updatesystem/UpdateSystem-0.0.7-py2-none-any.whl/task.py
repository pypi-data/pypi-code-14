
import subprocess
import shlex
from log import logger as logging
import os

class Task(object):
    def __init__(self,*argv,**kwargv):
        pass


class PatchTask(Task):
    """

    """
    def __init__(self, path, script="test.sh"):
        self.path = path
        # need to change
        self.script = script
        self._father = "father"
        self._children = "child"
        logging.info("init patchtask:{}".format(path))

    def check(self):
        file = os.path.join(self.path,self.script)
        if os.path.isfile(file):
            logging.debug("patch script:{} ".format(file)) 
            return True
        else:
            logging.error("patch script ({}) not exists".format(file))
            return False


    def run(self):
        cmd = "bash {}".format(os.path.join(self.path,self.script))
        #cmd_list = shlex.split(cmd)
        logging.debug("excute cmd ({})".format(cmd))
        try:
            output = subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=True)
            logging.debug(output)
            return True
        except subprocess.CalledProcessError , e:
            logging.debug("Exception",exc_info=True)
            logging.error("execute {} failed".format(cmd))
            logging.error("execute output: {} ".format(e.output))
            return False
        except:
            logging.debug("Exception",exc_info=True)
            logging.error("execute {} failed".format(cmd))
            return False

    def __str__(self):
        """ content of PatchTask
            return string 
        """
        return "father: {}\nchild :{}\npath {}\n".format(self._father,self._children,
                self.path)

    def revert(self):
        pass

    @property
    def father(self):
        return self._father

    @father.setter
    def father(self,father):
        self._father = father

    @property
    def children(self):
        return self._children

    @children.setter
    def children(self,children):
        self._children=  children

    @property
    def status(self):
        return self._status


if __name__ == "__main__":
    a = PatchTask(path="/root/project/ansible/update-system/02-bugfix/SP1/021/")
    a.father = "base"
    a.child = "039"
    a.run()
    a.check()
    print(a)


