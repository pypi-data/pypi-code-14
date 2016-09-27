#!/usr/bin/env python
# _*_ coding=gbk _*_

u'''
基于UDP方式的通信协议
'''

import struct
import threading
import time
import socket
import binascii

CMD_SEARCH     = 0x01   # 获取设备信息
CMD_UPLOAD     = 0x02   # 上传数据
CMD_STARTUP    = 0x03   # 启动烧写升级
CMD_STATUS     = 0x04   # 获取操作状态

# 打印str供调试查看
def debug_str(data):
    print  ' '.join(map(hex,map(ord,list(data))))
    
# 按协议组包
def PackData(cmd, data=''):
    u'''按照协议格式打包数据'''
    # 包长度: 头部长加上数据长
    packlen = len(data)+11
    # 头部格式: 标志，命令，长度
    head = struct.pack('<IBH',0x55AA55AA,cmd,packlen)
    # 计算CRC校验: 头部+空白CRC占位+数据 一起计算校验
    crc = struct.pack('<I',binascii.crc32(head + struct.pack('<I',0) + data) & 0xffffffff)
    # 组合成最终包
    return head + crc + data

# 按协议解包
def UnPackData(data):
    u'''解包数据'''
    # 数据长度不能低于最小头部长度
    if not data or len(data)<11:
        return None
    rcrc = binascii.crc32(data[:7] + struct.pack('<I',0) + data[11:]) & 0xffffffff
    #debug_str(data)
    # 解析头部字段
    flag,cmd,datalen,crc = struct.unpack('<IBHI',data[:11])
    #print hex(rcrc),hex(crc)
    if flag!=0x55AA55AA or datalen!=len(data) or rcrc!=crc:
        return None
    # 验证通过后返回指令和数据部分
    return cmd,data[11:]
    
# 广播方式查找设备列表
def Search(listctrl):
    devlist = []
    try:
        # 获得当前主机名对应的IP
        addr = socket.getaddrinfo(socket.gethostname(),None)[-1][4][0]
        # 目的地址是广播
        dest = ('<broadcast>', 8081)
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(5)
        # 绑定当前IP才能自动使用当前网段发广播
        s.bind((addr, 0))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, True)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
        # 发送请求
        sendpack = PackData(0x01)
        #debug_str(sendpack)        
        s.sendto(sendpack, dest)
        n=0;
        while True:
            data, addr = s.recvfrom(1024)
            if data:
                rspcmd,data = UnPackData(data)
                if data and rspcmd==0x81:
                    # 搜索设备回应的设备信息
                    id,type,ver,sn,uuid = struct.unpack('<BBH16sI',data)
                    # print id,type,ver,sn,hex(uuid),hex(crc)
                    listctrl.InsertStringItem(n, str(id))
                    listctrl.SetStringItem(n, 1, str(hex(uuid)).upper())
                    listctrl.SetStringItem(n, 2, str(hex(ver))[2:])
                    listctrl.SetStringItem(n, 3, str(type))
                    listctrl.SetStringItem(n, 4, addr[0])
                    #listctrl.SetStringItem(n, 5, sn)
                    devlist.append((n,id,uuid,type,ver,sn,addr[0]))
                    n=n+1
        s.close()
    except:
        print 'err or timeout\n'
        s.close()
        pass
    print 'Search Finish.\n'
    return devlist

#上传文件时发送数据包
def sendpack(s,dest,i,data):
    try:
        data = struct.pack('<H',i) + data
        s.sendto(PackData(0x02,data), dest)
        data, addr = s.recvfrom(1024)
        if data:
            rspcmd,data = UnPackData(data)
            if data and rspcmd==0x82:
                num,result = struct.unpack('<HB',data)
                #print 'num=',num,'ret=',result
                if num==i and result==0:
                    return True
                else:
                    return False
    except:
        print "senddata fail\n"
        return False

# 上传文件数据
def Upload(addr,data):        
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(5)
        i = 0 #包序号
        # 循环截取数据发送,每段512字节
        while len(data) > 0:
            if len(data) >= 512:
                block = data[0:512]
            else:
                block = data
            #print 'pack=',i,'len=',len(block)
            if sendpack(s,(addr, 8081),i,block):                    
                i=i+1
                data = data[512:]
            else:
                #发送一包失败
                s.close()
                return False
        if len(data) == 0:#表示发送完了
            s.close()
            return True
    except:
        print 'send udp timeout or err\n'
        s.close()
        pass

# 启动固件更新
def StartUp(dest,key):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(5)
        # 发送请求
        sendpack = PackData(0x03,struct.pack('<B',1)+struct.pack('<I',key))
        #debug_str(sendpack)        
        s.sendto(sendpack, (dest,8081))
        while True:
            data, addr = s.recvfrom(1024)
            if data:
                rspcmd,data = UnPackData(data)
                if data and rspcmd==0x83:
                    result = struct.unpack('<B',data)
                    if result:
                        return True
                    else:
                        return False
        s.close()
    except:
        print 'err or timeout\n'
        s.close()
        return False

if __name__=="__main__":
    # 测试
    t=PackData(5,'abcdefg')
    print UnPackData(t)
    
    SearchThread()
    pass