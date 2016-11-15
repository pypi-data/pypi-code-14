import json
import os
import subprocess

pwd = os.path.abspath(os.curdir)
basecmd = 'docker run -e KRBUSER={krbuser} -v {keytab}:/auth/krb.keytab -v {pwd}:{pwd} -w {pwd} --rm -i cernjiracurl'.format(
    krbuser = 'lheinric', keytab = '/Users/lukas/lheinric.keytab', pwd = pwd
)

def create(summary, description, parent = None):
    createtask = {
        "fields": {
           "issuetype": {"name": "Task"},
           "project": {"key": "RCST"},
           "summary": summary,
           "description": description,
       }
    }
    if parent:
        createtask['fields']['issuetype'] = {"name":"Sub-task"}
        createtask['fields']['parent'] = {"key":parent}

    p = subprocess.Popen(
        '{base} {cmd}'.format(base = basecmd, cmd = 'create.sh'),
        shell = True, stdin = subprocess.PIPE, stdout = subprocess.PIPE
    )
    out, err = p.communicate(json.dumps(createtask))
    response = json.loads(out)
    print response
    return response

def attach(data,task,remotename):
    p = subprocess.Popen(
        '{base} {cmd}'.format(base = basecmd, cmd = 'attach.sh {} {}'.format(task,remotename)),
        shell = True, stdin = subprocess.PIPE, stdout = subprocess.PIPE
    )
    out, err = p.communicate(json.dumps(dict(data)))
    response = json.loads(out)
    return response

def getissue(task):
    p = subprocess.Popen(
        '{base} {cmd}'.format(base = basecmd, cmd = 'getissue.sh {}'.format(task)),
        shell = True, stdin = subprocess.PIPE, stdout = subprocess.PIPE
    )
    out, err = p.communicate()
    response = json.loads(out)
    return response

def resolve(task,sucess,publishdata = None):
    cmd = 'done.sh' if sucess else 'wontdo.sh'
    p = subprocess.Popen(
        '{base} {cmd}'.format(base = basecmd, cmd = '{} {}'.format(cmd,task)),
        shell = True, stdin = subprocess.PIPE, stdout = subprocess.PIPE
    )
    out, err = p.communicate()
    if publishdata:
        attach(publishdata,task,'published.json')

def getfile(task,filename):
    taskdata = getissue(task)
    attdata = {x['filename']:x['content'] for x in taskdata['fields']['attachment']}
    url = attdata[filename]
    p = subprocess.Popen(
        '{base} {cmd}'.format(base = basecmd, cmd = 'getatt.sh {}'.format(url)),
        shell = True, stdin = subprocess.PIPE, stdout = subprocess.PIPE
    )
    out, err = p.communicate()
    response = json.loads(out)
    return response

def getstatus(task):
    data = getissue(task)
    return  data['fields']['resolution']

def submit(name,spec,parameters,context,parent):
    data = create('manual packtivity {}'.format(name),'this is a description',parent)
    taskid = data['key']
    attach(parameters,taskid,'parameters.json')
    attach(spec,taskid,'spec.json')
    attach(context,taskid,'context.json')
    taskdata = getissue(taskid)
    return taskid


# workflowtask = create('workflow request #{}'.format(1234),'this is a description')
# taskid =  submit('first',{'this':'is a first spec'},{'and':'two','param':'values'},{'a first':'context'},workflowtask['key'])
# taskid =  submit('second',{'this':'is a another spec'},{'and':'two','param':'values'},{'another':'context'},workflowtask['key'])

# resolve(taskid,True,{'a':'response'})
# print getfile(taskid,'published.json')
