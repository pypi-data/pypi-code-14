#! /usr/bin/python
# -*- coding: utf-8 -*-
import json
import os

import uuid

from flask import Flask
from flask import request

import GlobalValue
from GlobalValue import ZetModule
from NoteBookOperate import NoteBook_Operater
from Utils import Util
import sqlite3

app = Flask(__name__)
_operater = NoteBook_Operater()
usrHome = GlobalValue.usr_home
curDIr = GlobalValue.currentDir

# sqlite3


# 每次打开页面都要计算最小的notebook编号
@app.route('/noteBook/getFileCode', methods=['GET', 'POST'])
def getFileCode():
    params = json.loads(request.get_data())
    username = params["username"]
    # 产生最小的Untitled编号
    # filelist = [re.sub(r"Untitled", '', re.sub(".ipynb", '', fileName)) for fileName in
    #             [fn for fn in os.listdir(GlobalValue.usr_home) if fn.endswith(".ipynb")]]
    # if(len(filelist)==0):
    #     code = 0
    # else:
    #     code = min(filelist)
    #     if len(code)==0:
    #         code = 0
    # notebook = "Untitled%s.ipynb" % (int(code)+1)
    conn = sqlite3.connect(os.path.join(os.path.dirname(os.path.realpath(__file__)),"remark.db"))
    conn.isolation_level = None
    cur = conn.cursor()
    cur.execute("SELECT * FROM USER_ID WHERE USER = '%s'" % username)
    res = cur.fetchall()
    if len(res) != 0:
        notebookId = res[0][1]
    else:
        notebookId = "%s.ipynb" % uuid.uuid1()
        insertsql = "INSERT INTO USER_ID(user,id) VALUES('%s','%s')" % (username, notebookId)
        conn.execute(insertsql)
        print "[insert sql: %s]" % insertsql

    conn.commit()
    print "[getFielCode] : get file code is %s" % notebookId
    from jinja2 import Environment, PackageLoader
    env = Environment(loader=PackageLoader('NoteBookServer', 'templates/notebook'))
    templates = env.list_templates()
    for tmpl_file in templates:
        target_file = notebookId
        tmpl = env.get_template(tmpl_file)
        with open(os.path.join(usrHome, target_file), "w") as f:
            f.write(tmpl.render())

    _respn = {}
    _respn["notebook"] = notebookId
    return json.dumps(_respn)

# 用于把页面上填写的配置存成spec.json文件
@app.route('/noteBook/params', methods=['GET', 'POST'])
def storejson():
    if request.method == 'POST':
        params = request.get_data()
        uploadJson = json.loads(params)
        username = uploadJson["username"]
        moudle_dir = '%s/upload/%s/tar' % (GlobalValue.currentDir, username)
        Util.makedir(moudle_dir)
        with open('%s/upload/%s/%s' % (GlobalValue.currentDir, username, "spec.json"), "w") as specfile:
            specfile.write(params)
        uploadJson["PARAM"] = {}
        uploadJson["GLOBAL_PARAM"] = {}
        with open('%s/upload/%s/tar/%s' % (GlobalValue.currentDir, username, "spec.json"), "w") as globalfile:
            globalfile.write(json.dumps(uploadJson, indent=2, separators=(',', ': ')))
        _respn = {"result":"store success"}
        result_json = json.dumps(_respn, indent=2, separators=(',', ': '))
        print "[storejson] : store file to %s" % moudle_dir
        return result_json

# 存储上传的input文件：位置在
# 参数：moudleName，上传的文件
@app.route('/noteBook/upload', methods=['GET', 'POST'])
def upload_file():
    moudleDir=json.loads(request.get_data())['username']
    if request.method == 'POST':
        fs = request.files()
        for f in fs:
            Util.makedir('%s/upload/%s' % (curDIr,moudleDir))
            f.save('%s/upload/%s/inputs/%s' % (curDIr,moudleDir,f.filename))

    _respn = {"result":"upload file success"}
    return json.dumps(_respn)


# 用于填完spec.json后，在notebook的第一个cell中显示参数解析的语句
# jupeter的docker里面需要有NoteBookServer模块
@app.route('/noteBook/gen1stCellFromspecJson', methods=['GET', 'POST'])
def gen1stCellFromspecJson():
    _notebookName = json.loads(request.get_data())['notebookName']
    _username = json.loads(request.get_data())['username']
    _operater.gen1stCellFromspecJson(_notebookName,_username)
    print ("gen first cell to file : %s" % _notebookName)
    _respn = {"result":"gen 1st cell success"}
    return json.dumps(_respn)

# 整理notebook脚本，去除有错的python命令
# filepath：untitle.ipy文件名
@app.route('/noteBook/trimscript', methods=['GET', 'POST'])
def trimscript():
    _bookPath = "%s/%s" % (usrHome,json.loads(request.get_data())['notebookName'])
    _operater.collate_file(_bookPath)
    print ("[trimscript] trim file success : %s" % _bookPath)
    _respn = {"result":"trim file success"}
    return json.dumps(_respn)

# 提交模块
# 部署NoteBookServer的用户虾米那要有.screwjack.cfg
@app.route('/noteBook/submitmoudle', methods=['GET', 'POST'])
def submitmoudle():
    form = json.loads(request.get_data())
    username = form['username']
    templateType = form['templateType']
    fileName = form['notebookName']
    module_home = "upload/%s" % username
    with open("%s/%s/tar/spec.json" % (curDIr,module_home), "r") as sp_in:
        moudleName = json.load(sp_in)["Name"]
    zm = ZetModule(module_home)
    zm.username = username
    _operater.generate_script(filepath= "%s/%s" %(usrHome,fileName),_moudleName=moudleName,_username=username)
    tarfile = Util.tarballFiles(username)
    res = Util.submit(zm,tarfile,templateType)
    if res.startswith("Successful"):
        os.remove("%s/%s" % (usrHome,fileName))
        #删除数据库里面对应的记录
        deluser2id(username)
    _respn = {}
    _respn["result"] = res
    return json.dumps(_respn)


def deluser2id(username):
    conn = sqlite3.connect(os.path.join(os.path.dirname(os.path.realpath(__file__)), "remark.db"))
    conn.isolation_level = None
    conn.execute("DELETE FROM USER_ID WHERE USER='%s'" % username)


@app.route('/noteBook/abandonedit', methods=['GET', 'POST'])
def abandonedit():
    form = json.loads(request.get_data())
    _username = form["username"]
    _pfileName = form["notebookName"]
    deluser2id(_username)
    os.remove("%s/%s" % (usrHome,_pfileName))
    moudleroot = '%s/upload/%s' % (GlobalValue.currentDir,_username)
    os.system("rm -rf %s" % moudleroot)
    print("delete file complete : %s" % moudleroot)



if __name__ == '__main__':
    conn = sqlite3.connect(os.path.join(os.path.dirname(os.path.realpath(__file__)),"remark.db"))
    conn.isolation_level = None
    conn.execute("CREATE TABLE IF NOT EXISTS user_id(user string,id string)")
    conn.commit()
    Util.makedir(GlobalValue.currentDir)
    app.run(debug=True,host='0.0.0.0',port=5001)

