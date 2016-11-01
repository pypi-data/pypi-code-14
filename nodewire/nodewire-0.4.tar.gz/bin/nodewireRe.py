#!/usr/bin/env python
'''
Copyright (c) 2016, Nigcomsat I&D
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:
1. Redistributions of source code must retain the above copyright
   notice, this list of conditions and the following disclaimer.
2. Redistributions in binary form must reproduce the above copyright
   notice, this list of conditions and the following disclaimer in the
   documentation and/or other materials provided with the distribution.
3. All advertising materials mentioning features or use of this software
   must display the following acknowledgement:
   This product includes software developed by Nigcomsat I&D.
4. Neither the name of Nigcomsat I&D nor the
   names of its contributors may be used to endorse or promote products
   derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY Nigcomsat I&D ''AS IS'' AND ANY
EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL Nigcomsat I&D BE LIABLE FOR ANY
DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
'''
import time
from socket import *
from nodewire import IoTComm
import thread
import sys
import re
import configparser
import json
import ast
import operator as op



class whendo():
    def __init__(self, when, do):
        self.when = when
        self.do = do

class ScripingEnging():
    def __init__(self, comm):
        self.whendos = []
        self.variables = {}
        self.comm = comm

        self.operators = {ast.Add: op.add, ast.Sub: op.sub, ast.Mult: op.mul, ast.Mod: op.mod,
                     ast.Div: op.truediv, ast.Pow: op.pow, ast.BitXor: op.xor,
                     ast.And: op.and_, ast.Or: op.or_, ast.Not: op.not_,
                     ast.Gt: op.gt, ast.GtE: op.ge, ast.Eq: op.eq, ast.Lt: op.lt, ast.LtE: op.le,
                     ast.USub: op.neg}

    def reset(self):
        #self.variables.clear()
        del self.whendos[:]

    def engine_process(self, script):
        if ' do ' in script:
            parts = script.split(' do ')
            when, do = parts[0].replace('when ',''), parts[1]
            whendo1 = whendo(when, do)
            self.whendos.append(whendo1)
        elif script.strip() != '':
            return self.evaluate(script)

    def engine_execution_loop(self): #todo event driven execution
        for whendo in self.whendos:
            if self.evaluate(whendo.when):
                if ';' in whendo.do:
                    dos = whendo.do.split(';')
                    for do in dos:
                        self.evaluate(do)
                else:
                    self.evaluate(whendo.do)
            time.sleep(0.3)

    def eval_(self, node):
        if isinstance(node, ast.Num):  # <number>
            return node.n
        elif isinstance(node, ast.Str):  # string
            return node.s
        elif isinstance(node, ast.BinOp):  # <left> <operator> <right>
            return self.operators[type(node.op)](self.eval_(node.left), self.eval_(node.right))
        elif isinstance(node, ast.UnaryOp):  # <operator> <operand> e.g., -1
            return self.operators[type(node.op)](self.eval_(node.operand))
        elif isinstance(node, ast.Name):
            if node.id in self.variables.keys():
                return self.variables[node.id]
            elif node.id == 'time':
                return time.time()
            else:
                raise Exception('undefined variable: ' + str(node.id))
        elif isinstance(node, ast.Subscript):
            thevar = node.value.id + '[' + (('"' + node.slice.value.s + '"') if isinstance(node.slice.value, ast.Str) else str(node.slice.value.n) + ']')
            if thevar in self.variables.keys():
                return self.variables[thevar]
            elif node.value.id == 'time':
                index = ('"' + node.slice.value.s + '"') if isinstance(node.slice.value, ast.Str) else str(node.slice.value.n)
                if index == '"hour"':
                    exp = time.localtime(time.time()).tm_hour
                elif index == '"minute"':
                    exp = time.localtime(time.time()).tm_min
                elif index == '"second"':
                    exp = time.localtime(time.time()).tm_sec
                elif index == '"year"':
                    exp = time.localtime(time.time()).tm_year
                elif index == '"month"':
                    exp = time.localtime(time.time()).tm_mon
                elif index == '"mday"':
                    exp = time.localtime(time.time()).tm_mday
                elif index == '"wday"':
                    exp = time.localtime(time.time()).tm_wday
                elif index == '"yday"':
                    exp = time.localtime(time.time()).tm_yday
                return exp
            else:
                raise Exception('undefined variable: ' + thevar)
        elif isinstance(node, ast.Compare):
            return self.operators[type(node.ops[0])](self.eval_(node.left), self.eval_(node.comparators[0]))
        elif isinstance(node, ast.BoolOp):
            return self.operators[type(node.op)](self.eval_(node.values[0]), self.eval_(node.values[1]))
        else:
            raise TypeError(node)

    def evaluate(self, exp):
        if '=' in exp and exp[exp.index('='):exp.index('=')+2] !='==':
            lr = exp.split('=')
            lhs, rhs = lr[0].strip(),lr[1].strip()
            theval = self.evaluate(rhs)
            if (lhs not in self.variables.keys()) or (self.variables[lhs] != theval): #todo correction to variable check
                ll = lhs.split('[')
                if len(ll)!=1:
                    node = ll[0]
                    index = ll[1][:-1] #todo check if this is node
                    #if theval != self.variables[lhs]:
                    comm.send(node, 'setportvalue', index, str(self.evaluate(rhs)))
                self.variables[lhs] = theval.strip('"') if isinstance(theval, basestring) else theval
                try: # todo check the logic of this
                    self.variables[lhs] = float(self.variables[lhs])
                except:
                    pass
            return self.variables[lhs]
        else:
            result = self.eval_(ast.parse(exp, mode='eval').body)
            if isinstance(result, basestring):
                return '"' + result + '"'
            else:
                return result

    def addscript(self, script):
        for line in script.splitlines():
            self.engine_process(line.strip())

    def addinteractive(self, line):
        return self.engine_process(line.strip())

    def ProcessCommand(self, cmd):
        try:
            Command = cmd['command']
            Params = cmd['params']
            Sender = cmd['sender']

            if Command == 'portvalue':
                try:
                    self.variables[Sender + '[' + Params[0] + ']'] = float(Params[1])
                except ValueError:
                    self.variables[Sender + '[' + Params[0] + ']'] = Params[1]
            elif Command == 'temperature' or Command == 'humidity':
                self.variables[Sender + "['" + Command +"']"] = Params[0]
            elif Command == 'send':
                self.reset()
                list = json.loads(Params[0])
                for line in list:
                    self.addinteractive(line)
            elif len(Params) == 1:
                self.variables[Sender + "['" + Command + "']"] = Params[0]
        except Exception as ex:
            pass


script = ''

#Handles LAN
def local_server():
    #local server
    myHost = ''  # server machine, '' means local host
    myPort = 10002  # listen on a non-reserved port number

    sockobj = socket(AF_INET, SOCK_STREAM)  # make a TCP socket object
    sockobj.bind((myHost, myPort))  # bind it to server port number
    sockobj.listen(5)  # allow up to 5 pending connects
    dispatcher(sockobj)

def handleClient(connection,addr): # in spawned thread: reply
    connection.sendall('Welcome to IoTScript\n>>')
    while True:
        try:
            command = connection.recv(1024)
            #print('tcp:'+command)
            if command.strip() == 'quit':
                break
            else:
                resp = se.addinteractive(command)
                if resp != None:
                    connection.send(str(resp))
                connection.sendall('\n>>')
        except Exception as error:
            print(error)
            connection.sendall(str(error) + '\n')

    connection.close()


def dispatcher(sockobj): # listen until process killed
    print('starting local TCP server ... \n')
    while True: # wait for next connection,
        connection, address = sockobj.accept() # pass to thread for service

        if len(sys.argv) >= 2 and sys.argv[1] == 'Secure':
            connection = ssl.wrap_socket(connection,
                                         certfile="cert.pem",
                                         ssl_version=ssl.PROTOCOL_SSLv23,
                                         server_side=True)

        thread.start_new_thread(handleClient, (connection, address,))

config = configparser.RawConfigParser()
config.read('cp.cfg')
user = str(config.get('user', 'account_name'))
password = str(config.get('user', 'password'))

comm = IoTComm(account=user, password=password)
comm.debug = True
se = ScripingEnging(comm)
comm.process = se.ProcessCommand
comm.address = 're'
if comm.publishmqtt:
    comm.startMqttListener()
else:
    print('failed to start mqtt')

se.addscript(script)
thread.start_new_thread(local_server, ())
while True:
    try:
        se.engine_execution_loop()
    except Exception as ex:
        pass
    #time.sleep(0.2)