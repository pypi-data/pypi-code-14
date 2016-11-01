#!/usr/bin/env python
'''
Copyright (c) 2016, nodewire.org
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
   This product includes software developed by nodewire.org.
4. Neither the name of nodewire.org nor the
   names of its contributors may be used to endorse or promote products
   derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY nodewire.org ''AS IS'' AND ANY
EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL nodewire.org BE LIABLE FOR ANY
DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
'''
import sys
import serial
import glob
from socket import *
import sys
import threading
from nodewire import getip2
import time
import paho.mqtt.client as paho
from queue import Queue as queue
from nodewire import ir
import configparser
import requests
from nodewire.splitter import split, getnode, getsender

config = configparser.RawConfigParser()
config.read('cp.cfg')

myAddress = 'cp'
publishmqtt = False

instancename = None
mqttbroker = None

user = str(config.get('user', 'account_name'))
password = str(config.get('user', 'password'))


nodes = []
routers = {}

tcpclients = [] # {'connection': con, 'nodename', node}
mqttclients = []
mqttmessages = [] # {'topic': payload}


ircmds = queue()

def serial_ports():
    """ Lists serial port names
        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
    """
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result

def openSerial():
    tries = 10
    print('searching for serial port...')
    while True:
        sys.stdout.write(".")
        sys.stdout.flush()
        ports = serial_ports()
        for port in ports:
            try:
                serialport = serial.Serial(port, timeout=1)
                serialport.write('any ping cp\n')
                time.sleep(20)
                msg = serialport.readline()
                if msg.startswith('cp ThisIs'):
                    print('serialport is on ' + port)
                    return serialport
            except:
                pass
        tries-=1
        if tries == 0:
            print('giving up on serial port. will not support serial devices in this run')
            return None
        # print ('could not find an PlainTalk compartible serial port. will try again in 30 seconds...')
        time.sleep(30)

ser = None #serial.Serial('/dev/ttyACM1', timeout =5)

def _readline():
    eol = b'\n'
    leneol = len(eol)
    line = bytearray()
    while True:
        c = ser.read(1)
        if c:
            line += c
            if line[-leneol:] == eol:
                break
    return bytes(line)

#uart loop
#handles the zigbee network.
def uart_loop():
    global buff, ser
    print('running uart thread')
    ser = openSerial()
    while True:
        if ser:
            cmd = _readline() # ser.readline()
            print("uart receive:" + cmd)
            # thread.start_new_thread(sendMQTT, (cmd,))
            #responses.put(cmd)
            if cmd.strip() != "":
                ProcessCommand(cmd)


sendqueue = queue()
def uart_send():
    while True:
        response = sendqueue.get()
        if ser:
            ser.write(response+'\n')
            print('uart:' + response+'\n')
        time.sleep(0.2)
        sendqueue.task_done()

#udp loop
responses = queue()
s2 = None
def udp_loop():
    global s2
    MYPORT = 50000
    s = socket(AF_INET, SOCK_DGRAM)
    s.bind(('', 0))
    s.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
    print('broadcasting my IP')
    t = time.time()
    while 1:
        if time.time()-t > 10:
            try:
                data = getip2.connectedip()
                s.sendto(('remote cp_ip ' + data + ' cp').encode(), ('<broadcast>', MYPORT))
                t = time.time()
            except Exception as ex1:
                # pass
                print ('udp error')
                print(ex1)
                time.sleep(30)
        try:
            response = responses.get_nowait()
            if publishmqtt and response[:response.find(' ')] in mqttclients or response[:response.find(' ')] =='remote':
                threading.Thread(target=sendMQTT, args=(response,)).start()
            responses.task_done()
        except:
            pass


def clearretained():
    mqtt_client = paho.Client()
    mqtt_client.connect(mqttbroker)
    for topic in mqttmessages:
        mqtt_client.publish(topic.items()[0][0], None, 0, True)


def sendMQTT(cmd):
    topic, message = plaintalk2mqtt(cmd)
    if topic:
        if message:
            try:
                mqtt_client = paho.Client()
                mqtt_client.connect(mqttbroker)
                mqtt_client.publish(topic, message, 0, 1)
            except:
                print('error sending mqtt message')
        '''else:
            mqtt_client = paho.Client()
            mqtt_client.connect(mqttbroker)
            print(topic)
            mqtt_client.publish(topic,'', 1) # all topics
            '''


#Handles MQQT
def on_message(mosq, obj, msg):
    print(msg.topic + ' ' + str(msg.payload))
    #if msg.topic.split('/')[1] == 'cp':
    #if msg.retain==0:
    ProcessCommand(mqtt2plaintalk(msg.topic, msg.payload))


def mqqt_loop():
    global publishmqtt, mqttbroker, instancename
    while True:
        with requests.Session() as s:
            try:
                server = 'http://45.55.150.77:5001'
                #server = 'http://localhost:5000'
                res = s.post(server + '/login', data = {'email':user, 'pw':password})
                if res.url != unicode(server + '/login'):
                    r = s.get(server + '/config').json()
                    instancename = str(r['instance'])
                    mqttbroker = str(r['broker'])
                    publishmqtt = True
                break
            except:
                print('could not connect to cloud service. will retry after 30 seconds.')
                time.sleep(30)

    while publishmqtt:
        try:
            print('starting MQTT')
            mqtt_client = paho.Client()
            mqtt_client.on_message = on_message
            mqtt_client.connect(mqttbroker)
            mqtt_client.subscribe(instancename + '/#', 2)  # all topics

            #mqtt_client.publish(mqqttopic + '/node/any', 'any ping cp', 0)
            return_code = 0
            while return_code == 0:
                return_code = mqtt_client.loop()
            print('mqtt loop terminated. restarting ...')
                # time.sleep(200)
        except Exception as ex:
            print ('error in mqtt loop')
            print(ex)
            time.sleep(20)



#gsmloop
def gsm_loop():
    pass

#Handles LAN
def local_server():
    #local server
    myHost = ''  # server machine, '' means local host
    myPort = 10001  # listen on a non-reserved port number

    sockobj = socket(AF_INET, SOCK_STREAM)  # make a TCP socket object
    sockobj.bind((myHost, myPort))  # bind it to server port number
    sockobj.listen(5)  # allow up to 5 pending connects
    dispatcher(sockobj)


def handleClient(connection,addr): # in spawned thread: reply
    notlisted = True
    print('new connection from:' + str(addr))
    while True:
        try:
            command = connection.recv(1024)
            if notlisted:
                print('node name:' + command[command.rfind(' '):].strip())
                tcpclients.append({'connection': connection, 'node': command[command.rfind(' '):].strip()})
                notlisted = False
            ProcessCommand(command)
        except Exception as error:
            #print(str(error))
            item = filter(lambda i: i['connection']==connection, tcpclients)[0]
            print(item['node']+ ' disconnected')
            tcpclients.remove(item)
            break


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

        #thread.start_new_thread(handleClient, (connection, address,))
        threading.Thread(target=handleClient, args=(connection, address,)).start()


def sendtotcpclients(cmd):
    try:
        clients = filter(lambda c: c['node']==getnode(cmd), tcpclients)
        #cmd+='/r/n'
        for client in clients:
            try:
                client['connection'].sendall(cmd+'\r\n')
            except:
                client['connection'].close()
                clients.remove(client)
    except Exception as ex:
        print(ex)

def isnumber(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


def plaintalk2mqtt(msg): #outgoing
    words = split(msg)
    address = words[0]
    command = words[1]
    params = words[2:-1]
    sender = words[-1]
    #router = 'cp'
    target = routers[address] if address in routers else None
    alternate = routers[sender] if sender in routers else None
    message = None

    if address != myAddress:
        topic = instancename + '/' + target if target else instancename + '/' + alternate
        if command == 'portvalue':
            topic+='/ports/'+params[0]
            message = params[1]
        elif command == 'RoutingVia':
            topic += '/routing'
            message = command + ' ' + params[0]
        elif command == 'setportvalue':
            topic = topic+'/ports/'+params[0] + '/input'
            message = params[1]
        elif command == 'noports':
            topic = topic+'/noports'
            message = params[0]
        elif command == 'ports':
            topic = topic+'/portslist'
            message = ' '.join(p for p in params)
            for p in params:
                sendqueue.put(sender + ' get properties ' + p + ' ' + myAddress + '\n')
        elif command == 'getportvalue':
            topic = topic+'/ports/'+params[0]
            payload = filter(lambda t: topic in t, mqttmessages)
            if len(payload) != 0:
                payload = payload[0][topic]
                sendtotcpclients(sender + ' portvalue ' + params[0] + ' ' + payload + ' ' + address)
        elif command == 'send':
            topic=topic+'/send'
            message = params[0]
        elif command.startswith('set'):
            topic = topic + '/port/' + command[3:] + '/input'
            message = params[0]
        elif command == 'properties':
            topic = topic+'/ports/'+params[0]+'/properties'
            message = ' '.join(p for p in params)
        elif command.startswith('get'):
            topic = topic+'/'+ command[3:]
            payload = filter(lambda t: topic in t, mqttmessages)
            if len(payload) != 0:
                payload = payload[0][topic]
                sendtotcpclients(sender + ' ' + command[3:]  + ' ' + payload + ' ' + address)
        else:
            print ('msg:' + msg)
            if params:
                topic = topic+'/'+params[0]
                payload = filter(lambda t: topic in t, mqttmessages)
                if len(payload) != 0:
                    payload = payload[0][topic]
                    sendtotcpclients(sender + ' ' + command + params[0] + ' ' + payload + ' ' + address)
        return topic, message
    else:
        return None, None


def mqtt2plaintalk(topic, msg=''): #incoming
    payload = filter(lambda t: topic in t, mqttmessages)
    if payload and len(payload) != 0:
        payload[0][topic] = msg
    else:
        mqttmessages.append({topic:msg})

    try:
        words = topic.split('/')
        node = words[2]

        if not node in mqttclients:
            if len(words)>3:
                command = words[3]
            else:
                command = None

            message = None
            #if node == self.address:
            if command == 'ports' and len(words)==6 and words[-1]=='input':
                message = node + ' setportvalue ' + words[4] + ' ' + msg + ' remote'
                '''
            elif command == 'ports' and len(words)==5:
                message =  'remote portvalue ' + words[4] + ' ' + msg + ' ' + node
                '''
            elif len(words) == 3 and msg:
                route = msg.split()
                if len(route) == 2 and route[0]=='RoutingVia':
                    message = 'cp mqttregister ' + node + ' ' + route[1] + ' ' + node
            else:
                print('mq2plain:' + topic + ' ' + msg)
            return message
    except Exception as ex:
        print('mq2plain error:' + str(ex))
        return None


def ProcessCommand(cmd):
    global sendqueue
    if cmd:
            words = split(cmd)
            print(words)
        #try:
            Address = words[0]
            Command = words[1]
            Params = words[2:-1]
            Sender = words[-1]

            #print Address
            #print Command
            #print Params
            #print Sender

            if Address == myAddress:
                print('consuming')
                print(cmd)
                if Command == 'ThisIs':
                    # ser.write(Sender + ' ack ' + myAddress + '\r')
                    if Sender not in nodes:
                        nodes.append(Sender)
                        routers[Sender] = 'cp/' + Sender
                        responses.put('remote RoutingVia cp/' + Sender + ' ' + Sender)
                    sendqueue.put(Sender + ' ack ' + myAddress + '\n')
                    sendqueue.put(Sender + ' getnoports remote\n')
                    sendqueue.put(Sender + ' get ports remote\n')
                    sendtotcpclients(Sender + ' ack ' + myAddress + '\n')
                elif Command == 'RoutingVia':
                    if Sender not in nodes:
                        nodes.append(Sender)
                        routers[Sender] = Params[0]
                    responses.put(Sender + ' ack ' + myAddress + '\n')
                    sendtotcpclients(Sender + ' ack ' + myAddress + '\n')
                    if not Sender in mqttclients:
                        mqttclients.append(Sender)
                elif Command == 'getrouter':
                    sendqueue.put(Sender + ' router ' + Params[0] + ' ' + routers[Params[0]] + ' ' + myAddress + '\n')
                    responses.put(Sender + ' router ' + Params[0] + ' ' + routers[Params[0]] + ' ' + myAddress + '\n')
                    sendtotcpclients(Sender + ' router ' + Params[0] + ' ' + routers[Params[0]] + ' ' + myAddress + '\n')
                elif Command == 'getip':
                    try:
                        ip = getip2.ipaddress(Params[0])
                        # ser.write(Sender + ' ' + ip + ' ' + myAddress + '\r')
                        sendqueue.put(Sender + ' ' + ip + ' ' + myAddress + '\n')
                    except:
                        pass
                elif Command == 'getnodes':
                    # clearretained()

                    print('getting nodes')
                    n = ' '.join(node for node in nodes)
                    print('got nodes:' + n)
                    # ser.write(Sender + ' nodes ' + n + ' cp')
                    sendqueue.put(Sender + ' nodes ' + n + ' cp')
                    responses.put(Sender + ' nodes ' + n + ' cp')
                    sendtotcpclients(Sender + ' nodes ' + n + ' cp')
                elif Command == 'sendir':
                    device_model = Params[0]
                    ircommand = Params[1]
                    IRNODE = 'IRBLAST01' # Params[2].strip()
                    div = len(ir.irdevices[device_model][ircommand])/(3 * 5)*5
                    cm1 = ir.irdevices[device_model][ircommand][:div]
                    cm2 = ir.irdevices[device_model][ircommand][div:2*div]
                    cm3 = ir.irdevices[device_model][ircommand][2*div:]
                    ircmds.put(IRNODE + ' SEND ' + cm1 + ' cp\n')
                    ircmds.put(IRNODE + ' SEND ' + cm2 + ' cp\n')
                    ircmds.put(IRNODE + ' sendgo ' + cm3 + ' cp\n')

                    #ircmds.put(IRNODE + ' go ' + ' cp\n')
                    #ircmds.put(IRNODE + ' print cp' + '\r\n')
                    cc = ircmds.get()
                    #sendqueue.put(cc)
                    responses.put(cc)
                    sendtotcpclients(cc)
                elif Command == 'received':
                    if ircmds.not_empty:
                        cc = ircmds.get()
                        #sendqueue.put(cc)
                        responses.put(cc)
                        sendtotcpclients(cc)
                elif Command == 'getirdevices':
                    devices = ir.irdevices.keys()
                    ds = reduce(lambda d, e1: d + ' ' + e1, devices)
                    response = Sender + ' irdevices ' + ds + ' cp'
                    sendqueue.put(response)
                    responses.put(response)
                    sendtotcpclients(response)
                elif Command == 'properties':
                    responses.put(cmd.replace('cp','remote'))
                elif Command == 'mqttregister':
                    if len(filter(lambda n: n==Address, nodes)) == 0:
                        nodes.append(Params[0])
                        routers[Params[0]] = Params[1]
                        mqttclients.append(Sender)
                elif Command == 'clearmqtt':
                    clearretained()
                    del mqttmessages[:]
                    print('cleared mqtt ghosts')
                elif Command == 'getinstance':
                    response = Sender + ' instance ' + instancename + ' cp'
                    sendqueue.put(response)
                    responses.put(response)
                    sendtotcpclients(response)
            elif Address != Sender:
                print('passing on')
                print(cmd)
                # sendqueue.put(cmd + '\r')
                responses.put(cmd)
                sendtotcpclients(cmd)
                if ser:
                    # ser.write(cmd + '\n')  # route
                    # print('putting')
                    sendqueue.put(cmd)
                else:
                    return False # serial port not found
            return True
            '''
            except Exception as e:
                print ('error while processing:' + cmd)
                print(e)
                return False
            '''

if __name__ == '__main__':
    print('NodeWire command processor')
    print('version 0.4 alpha')
    print('Copyright 2016 nodewire.org')
    print('starting...')
    #thread.start_new_thread(uart_send, ())
    #thread.start_new_thread(mqqt_loop, ())
    #thread.start_new_thread(udp_loop, ())
    #thread.start_new_thread(local_server, ())

    threading.Thread(target=uart_send).start()
    threading.Thread(target=mqqt_loop).start()
    threading.Thread(target=udp_loop).start()
    threading.Thread(target=local_server).start()
    uart_loop()
