#!/usr/bin/env python3
# _*_ coding:utf-8 _*_

import requests
from requests.exceptions import ConnectTimeout
import json
import os
import pickle
import subprocess
import random
from .database import Database
from prettytable import PrettyTable

state = [
    "在途",
    "揽件",
    "疑难",
    "签收",
    "退签",
    "派件",
    "退回"
]


def get_random_proxy():
    jsonPath = os.path.expanduser("~") + "/" + ".valid_proxy.json"
    if os.path.exists(jsonPath):
        jsonFile = open(jsonPath, "r")
        proxies = json.loads(jsonFile.read())
        jsonFile.close()
        if len(proxies) > 0:
            index = random.randint(0, len(proxies) - 1)
            proxy = {"http" : proxies[index]}
            return proxy
        else:
            return None
    else:
        return None

class Controller():

    db = Database()
    session = requests.Session()

    def __init__(self):
        pass

    def list(self, nu="all"):
        query = self.db.get_item_query()
        ptable = PrettyTable(["运单号", "描述", "状态", "最后一次更新时间", "最后一次更新信息"])
        for item in query:
            columns = os.get_terminal_size().columns - 70
            i = columns
            info = item.lastUpdateInfo
            info_gbk = info.encode("gbk")
            while i < len(info_gbk):
                info = info[:(i+1)//2] + "\n" + info[(i+1)//2:]
                i = i + columns + 1
            ptable.add_row([item.nu, item.description, state[item.state], item.lastUpdateTime, info])
        print(ptable)

    def show_info(self, s_nu):
        nus = self.db.get_full_nu(s_nu)
        if nus:
            if len(nus) > 1:
                print("匹配到多个单号，请选择:")
                for i in range(1, len(nus) + 1):
                    print(str(i) + "---" + self.db.find_item(nus[i-1]).description + "(" + nus[i-1] + ")")
                print("选择：", end="")
                choice = int(input())
                if (choice <= len(nus)):
                    nu = nus[choice - 1]
                else:
                    print("选择错误")
                    return
            else:
                nu = nus[0]
            item = self.db.find_item(nu)
            print(item.description + "(" + nu + ")  " + state[item.state])
            query = self.db.get_info_query(nu)
            ptable = PrettyTable(["时间", "信息"])
            for info in query:
                ptable.add_row([info.time, info.context])
            print(ptable)
        else:
            print("单号不存在")

    def get_com_code(self, nu):
        url = "http://www.kuaidi100.com/autonumber/autoComNum?text=" + nu
        data = self.session.get(url).text
        jsonData = json.loads(data)
        return jsonData["auto"][0]["comCode"]

    def new_item(self, nu, des=None):
        try:
            if not self.db.has_item(nu):
                com_code = self.get_com_code(nu)
                if not des:
                    des = com_code + "快递"
                url = "http://www.kuaidi100.com/query?type=" + com_code + "&postid=" + nu;
                try:
                    data = self.session.get(url, timeout=6, proxies=get_random_proxy()).text
                except:
                    data = self.session.get(url, timeout=6, proxies=get_random_proxy()).text
                jsonData = json.loads(data)
                if jsonData["status"] != "200":
                    print("快递不存在，或未更新,请检查运单号是否有错误。仍然添加？(y/n)", end="")
                    choice = input()
                    if choice == "y":
                        self.db.insert_item(self.db.get_new_item_id(), nu, des, "unknown", 2, 0, "unknown", "unknown")
                    elif choice == "n":
                        print("中断添加")
                        return
                    else:
                        print("选择错误,中断添加")
                        return
                    return
                status = jsonData["status"]
                state_code = int(jsonData["state"])
                data = jsonData["data"]
                for info in data:
                    time = info["time"]
                    context = info["context"]
                    # time = time[:10] + " " + time[11:15] + time[15:]
                    self.db.insert_info(self.db.get_new_info_id(), nu, time, context)
                last_time = data[0]["time"]
                # last_time = last_time[:10] + " " + last_time[11:14] + last_time[15:]
                last_context = data[0]["context"]
                self.db.insert_item(self.db.get_new_item_id(), nu, des, com_code, state_code, status, last_time, last_context)
                print(des + "(" + nu + ") " + last_time + " " + last_context)
            else:
                print("已存在")
        except:
            print("网络错误")

    def delete_item(self, nu):
        self.db.delete_item(nu)
        self.db.delete_info(nu)

    def update_all(self):
        for nu in self.db.get_all_nu():
            try:
                url = "http://www.kuaidi100.com/query?type=" + self.get_com_code(nu) + "&postid=" + nu;
                try:
                    data = self.session.get(url, timeout=6, proxies=get_random_proxy()).text
                except:
                    data = self.session.get(url, timeout=6, proxies=get_random_proxy()).text
                if not data:
                    continue
                jsonData = json.loads(data)
                if jsonData["status"] != "200":
                    continue
                try:
                    status = jsonData["status"]
                    state_code = int(jsonData["state"])
                    data = jsonData["data"]
                except KeyError:
                    self.update_all()
                for info in data:
                    time = info["time"]
                    context = info["context"]
                    self.db.insert_info(self.db.get_new_info_id(), nu, time, context)
                last_time = data[0]["time"]
                last_context = data[0]["context"]
                item = self.db.find_item(nu)
                if item.lastUpdateTime != last_time:
                    self.db.update_item(nu, state_code, status, last_time, last_context)
                    self.send_update_noti(nu, item.description, last_time, last_context);
                else:
                    print(item.description + "(" + nu + ")没有更新")
            except Exception as e:
                print(e)
                print("网络错误")

    def send_update_noti(self, nu, des, last_time, last_context):
        message = des + "(" + nu + ") 已更新：" + last_time + " " + last_context
        print(message)
        subprocess.call(['notify-send', "快递信息更新", message, "--urgency=critical"])

    def delete_item(self, s_nu):
        nus = self.db.get_full_nu(s_nu)
        if nus:
            if len(nus) > 1:
                print("匹配到多个单号，请选择:")
                for i in range(1, len(nus) + 1):
                    print(str(i) + "---" + self.db.find_item(nus[i-1]).description + "(" + nus[i-1] + ")")
                print("选择：", end="")
                choice = int(input())
                if (choice <= len(nus)):
                    nu = nus[choice - 1]
                else:
                    print("选择错误")
                    return
            else:
                nu = nus[0]
            self.db.delete_item(nu)
            self.db.delete_info(nu)
        else:
            print("无法匹配到任何单号，请检查你的输入")

if __name__ == "__main__":
    control = Controller()
    control.new_item("883967786411363996")
    control.new_item("610100445741")
    control.new_item("883909315041897319")
    control.update_all()
