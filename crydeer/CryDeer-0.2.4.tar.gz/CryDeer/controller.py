#!/usr/bin/env python3
# _*_ coding:utf-8 _*_

import requests
from requests.exceptions import ConnectTimeout
import json
import os
import sys
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

com_names = {"quanjitong": "全际通", "shunfengen": "顺丰", "cces": "希伊艾斯(CCES)", "huaqikuaiyun": "华企快运", "datianwuliu": "大田物流", "yinjiesudi": "银捷速递", "jiayunmeiwuliu": "加运美", "sevendays": "七天连锁", "rufengda": "如风达快递", "upsen": "UPS", "fedexus": "Fedex-美国件-英文结果", "youzhengguoji": "邮政小包", "zhaijisong": "宅急送", "dsukuaidi": "D速快递", "ems": "E邮宝", "quanyikuaidi": "全一快递", "jixianda": "急先达", "emsguoji": "EMS--Chinese data", "yuanzhijiecheng": "元智捷诚", "feikuaida": "飞快达", "hkpost": "香港邮政", "debangwuliu": "德邦物流", "yitongfeihong": "一统飞鸿", "canpost": "加拿大邮政Canada Post", "huiqiangkuaidi": "汇强快递", "zhongyouwuliu": "中邮物流", "lijisong": "立即送", "baifudongfang": "百福东方", "youzhengguonei": "邮政小包", "kangliwuliu": "康力物流", "jinyuekuaidi": "晋越快递", "quanchenkuaidi": "全晨快递", "shunfeng": "顺丰", "quanritongkuaidi": "全日通", "chuanxiwuliu": "传喜物流", "coe": "中国东方", "dpex": "DPEX", "lejiedi": "乐捷递", "jindawuliu": "金大物流", "ganzhongnengda": "港中能达", "longlangkuaidi": "隆浪快递", "fedexcn": "Fedex-国际件-中文结果", "xinhongyukuaidi": "鑫飞鸿", "bht": "BHT", "emsinten": "EMS--Englilsh data", "menduimen": "门对门", "santaisudi": "三态速递", "kuaijiesudi": "快捷速递", "sxhongmajia": "山西红马甲", "xinbangwuliu": "新邦物流", "shangda": "上大物流", "yafengsudi": "亚风速递", "meiguokuaidi": "美国快递", "jiayiwuliu": "佳怡物流", "gls": "GLS", "canpostfr": "加拿大邮政Canada Post", "jialidatong": "嘉里大通", "anxindakuaixi": "安信达", "feibaokuaidi": "飞豹快递", "shenghuiwuliu": "盛辉物流", "haimengsudi": "海盟速递", "lianbangkuaidien": "联邦快递", "suer": "速尔物流", "dhlen": "DHL-国际件-英文结果", "tonghetianxia": "通和天下", "xinfengwuliu": "信丰物流", "guangdongyouzhengwuliu": "广东邮政", "guotongkuaidi": "国通快递", "feikangda": "飞康达物流", "tiandihuayu": "天地华宇", "youshuwuliu": "优速物流", "hengluwuliu": "恒路物流", "yuanweifeng": "源伟丰快递", "zhengzhoujianhua": "郑州建华", "ups": "UPS", "jietekuaidi": "捷特快递", "tnten": "TNT", "weitepai": "微特派", "suijiawuliu": "穗佳物流", "saiaodi": "赛澳递", "lianhaowuliu": "联昊通", "lanbiaokuaidi": "蓝镖快递", "quanfengkuaidi": "全峰快递", "bangsongwuliu": "邦送物流", "usps": "USPS", "disifang": "递四方", "longbanwuliu": "龙邦物流", "tiantian": "天天快递", "ontrac": "onTrac", "auspost": "澳大利亚邮政", "haiwaihuanqiu": "海外环球", "kuayue": "跨越物流", "wanjiawuliu": "万家物流", "yuanchengwuliu": "远成物流", "yuantong": "圆通速递", "aae": "AAE", "fengxingtianxia": "风行天下", "haihongwangsong": "山东海红", "jiajiwuliu": "佳吉物流", "mingliangwuliu": "明亮物流", "jinguangsudikuaijian": "京广速递", "huitongkuaidi": "汇通快运", "neweggozzo": "新蛋奥硕物流", "zhongxinda": "忠信达", "tnt": "TNT", "yuefengwuliu": "越丰物流", "wanxiangwuliu": "万象物流", "dhl": "DHL-中国件-中文结果", "xingchengjibian": "星晨急便", "yunda": "韵达快运", "zhongtong": "中通速递", "emsen": "EMS", "yuntongkuaidi": "运通快递", "zhongtianwanyun": "中天万运", "huaxialongwuliu": "华夏龙", "gongsuda": "共速达", "zhimakaimen": "芝麻开门", "yibangwuliu": "一邦速递", "dhlde": "DHL-德国件-德文结果", "shentong": "申通", "hebeijianhua": "河北建华", "fedex": "Fedex-国际件-英文结果", "lianbangkuaidi": "联邦快递", "shenganwuliu": "圣安物流", "yuananda": "源安达", "zhongsukuaidi": "中速快件", "shengfengwuliu": "盛丰物流", "yuanfeihangwuliu": "原飞航", "ocs": "OCS","baishiwuliu": "百世汇通"}


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
                    des = com_names[com_code] + "快递"
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
        except Exception as err:
            print(err)
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
