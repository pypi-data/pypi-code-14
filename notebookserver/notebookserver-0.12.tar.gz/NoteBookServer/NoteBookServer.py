#! /usr/bin/python
# -*- coding: utf-8 -*-
import json
import os

from flask import Flask
from flask import request

import GlobalValue
from GlobalValue import ZetModule
from NoteBookOperate import NoteBook_Operater
from Utils import Util

app = Flask(__name__)
_operater = NoteBook_Operater()
usrHome = GlobalValue.usr_home
curDIr = GlobalValue.currentDir

# 每次打开页面都要计算最小的notebook编号
@app.route('/noteBook/getFileCode', methods=['GET', 'POST'])
def getFileCode():
    filelist = [re.sub(r"Untitled", '', re.sub(".ipynb", '', fileName)) for fileName in
                [fn for fn in os.listdir(GlobalValue.usr_home) if fn.endswith(".ipynb")]]
    if(len(filelist)==0):
        code = 0
    else:
        code = min(filelist)
        if len(code)==0:
            code = 0
    notebook = "Untitled%s.ipynb" % (int(code)+1)
    print "[getFielCode] : get file code is %s" % notebook
    from jinja2 import Environment, PackageLoader
    env = Environment(loader=PackageLoader('NoteBookServer', 'templates/notebook'))
    templates = env.list_templates()
    for tmpl_file in templates:
        target_file = notebook
        tmpl = env.get_template(tmpl_file)
        with open(os.path.join(usrHome, target_file), "w") as f:
            f.write(tmpl.render())

    _respn = {}
    _respn["notebook"] = notebook
    return json.dumps(_respn)

# 用于把页面上填写的配置存成spec.json文件
@app.route('/noteBook/params', methods=['GET', 'POST'])
def storejson():
    if request.method == 'POST':
        params = request.get_data()
        uploadJson = json.loads(params)
        moudleName = uploadJson['Name']
        moudle_dir = '%s/upload/%s/tar' % (GlobalValue.currentDir, moudleName)
        Util.makedir(moudle_dir)
        with open('%s/upload/%s/%s' % (GlobalValue.currentDir, moudleName, "spec.json"), "w") as specfile:
            specfile.write(params)
        uploadJson["PARAM"] = {}
        uploadJson["GLOBAL_PARAM"] = {}
        with open('%s/upload/%s/tar/%s' % (GlobalValue.currentDir, moudleName, "spec.json"), "w") as globalfile:
            globalfile.write(json.dumps(uploadJson, indent=2, separators=(',', ': ')))
        _respn = {"result":"store success"}
        result_json = json.dumps(_respn, indent=2, separators=(',', ': '))
        print "[storejson] : store file to %s" % moudle_dir
        return result_json

# 存储上传的input文件：位置在
# 参数：moudleName，上传的文件
@app.route('/noteBook/upload', methods=['GET', 'POST'])
def upload_file():
    moudleName=request.form['moudleName']
    if request.method == 'POST':
        fs = request.files()
        for f in fs:
            Util.makedir('%s/upload/%s' % (curDIr,moudleName))
            f.save('%s/upload/%s/inputs/%s' % (curDIr,moudleName,f.filename))

    _respn = {"result":"upload file success"}
    return json.dumps(_respn)


# 用于填完spec.json后，在notebook的第一个cell中显示参数解析的语句
@app.route('/noteBook/gen1stCellFromspecJson', methods=['GET', 'POST'])
def gen1stCellFromspecJson():
    _notebookName = request.form['notebookName']
    _moudleName = request.form['moudleName']
    _operater.gen1stCellFromspecJson(_notebookName,_moudleName)
    print ("gen first cell to file : %s" % _notebookName)
    _respn = {"result":"gen 1st cell success"}
    return json.dumps(_respn)

# 整理notebook脚本，去除有错的python命令
# filepath：untitle.ipy文件名
@app.route('/noteBook/trimscript', methods=['GET', 'POST'])
def trimscript():
    _bookPath = "%s/%s" % (os.path.expandvars('$HOME'),request.form['notebookName'])
    _operater.collate_file(_bookPath)
    print ("[trimscript] trim file success : %s" % _bookPath)
    _respn = {"result":"trim file success"}
    return json.dumps(_respn)

# 提交模块
@app.route('/noteBook/submitmoudle', methods=['GET', 'POST'])
def submitmoudle():
    form = request.form
    moudleName = form['moudleName']
    templateType = form['templateType']
    fileName = form['notebookName']
    module_home = "upload/%s" % moudleName
    zm = ZetModule(module_home)
    _operater.generate_script(filepath= "%s/%s" %(usrHome,fileName),_moudleName=moudleName)
    tarfile = Util.tarballFiles(moudleName)
    res = Util.submit(zm,tarfile,templateType)
    os.remove("%s/%s" % (os.path.expandvars('$HOME'),fileName))
    _respn = {}
    _respn["result"] = res
    return json.dumps(_respn)

import re
if __name__ == '__main__':
    Util.makedir(GlobalValue.currentDir)
    app.run(debug=True,host='0.0.0.0')
