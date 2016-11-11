import pandas as pd
from IPython.core.display import display, HTML

def data(data,keyword,n):
    
    this_year = int(pd.datetime.today().strftime("%Y"))

    l = [keyword,n,
    data.reach_score.sum(),
    float(data.egg_account.sum()) / 500 * 100,
    float(data.created_at.dt.year[data.created_at.dt.year == this_year].value_counts()[this_year]) / 500 * 100,
    pd.datetime.today().strftime("%mth %b %Y %H:%M:%S")]

    return l
    
def table(data):

    display(HTML("<style type=\"text/css\"> .tg {border-collapse:collapse;border-spacing:0;} .tg td{font-family:Arial, sans-serif;font-size:14px;padding:25px 5px;border-style:solid;border-width:0px;overflow:hidden;word-break:normal;} .tg th{font-family:Arial, sans-serif;font-size:14px;font-weight:normal;padding:10px 5px;border-style:solid;border-width:0px;overflow:hidden;word-break:normal;} .tg .tg-uyoa{font-weight:bold;font-size:20px;color:#333333;text-align:center} .tg .tg-7ttm{font-size:36px;text-align:center} .tg .tg-5cgy{font-size:36px;color:#f8a102;text-align:center} .tg .tg-p7ly{font-weight:bold;font-size:20px;text-align:center} .tg .tg-huh2{font-size:15px;text-align:center} .tg .tg-6nwz{font-size:14px;text-align:center;vertical-align:top} .tg .tg-dc8z{font-size:36px;color:#cb0000;text-align:center} </style> <table class=\"tg\" style=\"undefined;table-layout: fixed; width: 950px; border-style: hidden; border-collapse: collapse;\"> <colgroup> <col style=\"width: 140px\"> <col style=\"width: 120px\"> <col style=\"width: 220px\"> <col style=\"width: 140px\"> <col style=\"width: 140px\"> <col style=\"width: 190px\"> </colgroup> <tr> <th class=\"tg-huh2\">keyword</th> <th class=\"tg-huh2\">sample</th> <th class=\"tg-huh2\">reach</th> <th class=\"tg-huh2\">egg_accounts(%)</th> <th class=\"tg-huh2\">new_accounts(%)</th> <th class=\"tg-huh2\">time</th> </tr> <tr> <td class=\"tg-uyoa\">" + str(data[0]) + "</td> <td class=\"tg-7ttm\">" + str(data[1]) + "</td> <td class=\"tg-7ttm\">" + str(data[2]) + "</td> <td class=\"tg-dc8z\">" + str(data[3]) + "</td> <td class=\"tg-5cgy\">" + str(data[4]) + "</td> <td class=\"tg-p7ly\">" + str(data[5]) + "</td> </tr> </table> <hr align=\"left\", width=\"950\">"))
