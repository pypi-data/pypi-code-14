#!/usr/bin/env python
# coding=utf-8
# get intraday data of eastmoney
import urllib2
import time
localtime = time.localtime(time.time())
file_object = open("intraday" + str(localtime.tm_year)+str(localtime.tm_mon)+str(localtime.tm_mday)+".txt", 'w+')
file_object.write('现价\t涨跌\t涨跌幅\t昨收\t开盘\t最高\t最低\t总量\t总额\t时间\t日期\n')
url = 'http://yunhq.sse.com.cn:32041/v1/sh1/line/000001?callback=&begin=0&end=-1&select=time%2Cprice%2Cvolume'
url_list = 'http://yunhq.sse.com.cn:32041/v1/sh1/list/self/000001?callback=&select=last%2Copen%2Cname%2Chigh%2Clow%2Cchange%2Cchg_rate%2Cprev_close%2Cvolume%2Camount%2Ctradephase'
num_row = 2

while((localtime.tm_hour*60 + localtime.tm_min)<9*60+30):
    localtime = time.localtime(time.time())
    time.sleep(15)
    print('当前时间：' + str(localtime.tm_hour) + ':' + str(localtime.tm_min) + ':' + str(localtime.tm_sec))

while(9*60+30<=(localtime.tm_hour*60 + localtime.tm_min)<=15*60+30):
    if num_row != 2:
        file_object = open("intraday" + str(localtime.tm_year)+str(localtime.tm_mon)+str(localtime.tm_mday)+".txt", 'a')
        file_object.seek(0, 2)
    Request = urllib2.Request(url_list)
    request_jquery = urllib2.urlopen(Request).read()
    data_dict = eval(request_jquery.decode('gb2312'))
    file_object.write(str(float(data_dict["list"][0][0]))+'\t'
                      +str(float(data_dict["list"][0][5]))+'\t'
                      +str(float(data_dict["list"][0][6]))+'\t'
                      +str(float(data_dict["list"][0][7]))+'\t'
                      +str(float(data_dict["list"][0][1]))+'\t'
                      +str(float(data_dict["list"][0][3]))+'\t'
                      +str(float(data_dict["list"][0][4]))+'\t'
                      +str(float(data_dict["list"][0][8]) / 10000.00)+'\t'
                      +str(float(data_dict["list"][0][9]) / 100000000.00)
                      +str(data_dict["time"])+'\t'
                      +str(data_dict["date"])+'\n')
    # ws.cell(column=1, row=num_row, value=float(data_dict["list"][0][0]))  # ws.cell(行，列，值)
    # ws.cell(column=2, row=num_row, value=float(data_dict["list"][0][5]))  # %
    # ws.cell(column=3, row=num_row, value=float(data_dict["list"][0][6]))  # %
    # ws.cell(column=4, row=num_row, value=float(data_dict["list"][0][7]))  # RMB
    # ws.cell(column=5, row=num_row, value=float(data_dict["list"][0][1])) # RMB
    # ws.cell(column=6, row=num_row, value=float(data_dict["list"][0][3]))  # RMB
    # ws.cell(column=7, row=num_row, value=float(data_dict["list"][0][4]))  # RMB
    # ws.cell(column=8, row=num_row, value=float(data_dict["list"][0][8]) / 10000.00)  # 万手
    # ws.cell(column=9, row=num_row, value=float(data_dict["list"][0][9]) / 100000000.00)  # 亿元
    # ws.cell(column=10, row=num_row, value=data_dict["time"])
    # ws.cell(column=11, row=num_row, value=data_dict["date"])

    num_row =  num_row + 1
    file_object.close()

    print('现价：' + str(data_dict["list"][0][0]))
    print('涨跌：' + str(data_dict["list"][0][5]) + '%')
    print('涨跌幅：' + str(data_dict["list"][0][6]) + '%')
    print('昨收：' + str(data_dict["list"][0][7]))
    print('开盘：' + str(data_dict["list"][0][1]))
    print('最高：' + str(data_dict["list"][0][3]))
    print('最低：' + str(data_dict["list"][0][4]))
    print('总量(万手)：' + str(data_dict["list"][0][8] / 10000.00))
    print('总额(亿元)：' + str(data_dict["list"][0][9] / 100000000.00))
    # print('时间：' + time.strptime(data_dict["time"], '%H%2M%2S'))
    # print('日期：' + time.strptime(data_dict["date"], '%Y%2m%2d'))
    print('时间：' + str(data_dict["time"]))
    print('日期：' + str(data_dict["date"]))
    localtime = time.localtime(time.time())
    print('当前时间：' + str(localtime.tm_hour)+':'+str(localtime.tm_min)+':'+str(localtime.tm_sec))
    print('\n'+'\n')
# time.strptime('2016-05-09 21:09:30', '%Y-%m-%d %H:%M:%S')
    time.sleep(15)
# ew.save(filename='000001_上证指数.xlsx'.decode('utf-8'))
