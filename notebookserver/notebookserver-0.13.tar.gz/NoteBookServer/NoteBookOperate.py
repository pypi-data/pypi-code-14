# -*- coding: utf-8 -*-
import json
from collections import OrderedDict
import os

filepath2 = "/home/lj/Untitled.ipynb"

class NoteBook_Operater:

    def collate_file(self,filepath,delete1stCell=False):
        ''' purge wrong commond to jupiter notebook scripte'''
        with open(filepath, "r") as sj_in:
            ipynb = json.load(sj_in, object_pairs_hook=OrderedDict)
            _cells = ipynb['cells']
        list = []
        for i, el in enumerate(_cells):
            if delete1stCell:
             if el['execution_count'] == 0:   #删除生成脚本的第一行信息
                 list.append(i)
            _outputs = el["outputs"]
            if (len(_outputs) >= 1):
                if _outputs[0].__contains__("traceback") :
                    list.append(i)
        list.reverse()
        for i in list:
            _cells.__delitem__(i)
        ipynb["cells"] = _cells
        with open(filepath, "w") as sj_out:
            sj_out.write(json.dumps(ipynb, indent=2, separators=(',', ': ')))

    # _operater.generate_script("/home/lj/Untitled.ipynb","testlj")
    def generate_script(self,filepath,_moudleName):

        self.collate_file(filepath,delete1stCell=True)
        _usercode = ""
        _lineseparator = "\x20\x20\x20\x20"
        _spanseparator = "\x0a"

        with open(filepath, "r") as sj_in:
            ipynb = json.load(sj_in, object_pairs_hook=OrderedDict)
        _cells = ipynb['cells']
        for _cell in _cells:
            for _source in _cell["source"]:
                _usercode += _lineseparator + _source
            _usercode += _spanseparator

        obj = OrderedDict()
        obj['CMD'] = _usercode
        obj['Name'] = _moudleName

        from GlobalValue import currentDir
        target_path = "%s/upload/%s/tar" % (currentDir,obj['Name'].lower())
        # if os.path.exists(target_path):
        #     print("Path %s exist, can not create" % target_path)
        #     return
        # os.makedirs(target_path)

        from jinja2 import Environment, PackageLoader
        env = Environment(loader=PackageLoader('NoteBookOperate', 'templates/basic'))
        templates = env.list_templates()
        for tmpl_file in templates:
            target_file = os.path.splitext(tmpl_file)[0]   #mian.py.j2 to maion.py
            tmpl = env.get_template(tmpl_file)
            with open(os.path.join(target_path, target_file), "w") as f:
                f.write(tmpl.render(obj))

    #_operater.gen1stCellFromspecJson("Untitled.ipynb","testlj")
    def gen1stCellFromspecJson(self,_notebookName,_moudleName):
        '''把spec.json文件的参数解析出来，形成字符串作为第一个cell的内容，由用户点击执行。
           此前，需要把spec.json,global.json,上传的文件都准备好'''
        from GlobalValue import usr_home,currentDir
        _notebookDir = os.path.join(usr_home,_notebookName)
        _scpecPath = "%s/upload/%s/tar/spec.json" % (currentDir,_moudleName)
        _source = 'from NoteBookServer.Utils import Util \n_settings = Util.get_settings_from_file("%s")\nparams = _settings.Param\ninputs = _settings.Input\noutputs = _settings.Output' % _scpecPath
        with open(_notebookDir, "r") as sj_in:
            aa = json.load(sj_in, object_pairs_hook=OrderedDict)
        mydict = OrderedDict({
           "cell_type": "code",
           "execution_count": 0,
           "metadata": {},
           "outputs": [
            {
             "name": "stdout",
             "output_type": "stream",
             "text": [
              ""
             ]
            }
           ]
        })
        mydict["source"] = [_source]
        aa["cells"].append(mydict)
        with open(_notebookDir, "w") as sj_out:
            sj_out.write(json.dumps(aa, indent=2, separators=(',', ': ')))


if __name__ == "__main__":
    _operater = NoteBook_Operater()
    #_operater.collate_file("/home/lj/Untitled.ipynb")
    #_operater.gen1stCellFromspecJson("Untitled.ipynb","testlj")
    #_operater.generate_script("/home/lj/Untitled.ipynb","testlj")
    from Utils import Util
    Util.tarballFiles("testlj")
    #print os.path.join("/home/lj","aaa")