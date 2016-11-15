# encoding: utf-8
import os
import sys
import json
import ConfigParser
import time
from datetime import datetime
from nvd3 import *

# configParser = ConfigParser.RawConfigParser()
# configParser.read(os.path.join(os.path.abspath(os.path.dirname(__file__)), '.', 'config.cfg'))
#
# HEIGHT = configParser.get('Graph_config', 'height')
# WIDTH = configParser.get('Graph_config', 'width')
# DATE_FORMAT = configParser.get('Date_config', 'crud_api_format')
# X_AXIS_FORMAT = configParser.get('Graph_config', 'x_axis_format')
# BUYER_MANAGEMENT_ID_PREFIX = configParser.get('Date_config', 'buyer_management_id_prefix')


unicode_name_test = True


# [Graph_config]
width = 700
height = 450
x_axis_format = "%d %b %Y"
# [Date_config]
crud_api_format = "%Y-%m-%d"
buyer_management_id_prefix = "buyer_management:day:"
# [Chart_name_config]
personal_handle_success_history = "対応数/成約数" if not unicode_name_test else "personal_handle_success_history"
personal_revenue_profit_history = "見込販売額/見込粗利" if not unicode_name_test else "personal_revenue_profit_history"
personal_realtime_target_achieved = "今日目標達成率" if not unicode_name_test else "personal_realtime_target_achieved"
personal_productivity_history = "生産性" if not unicode_name_test else "personal_productivity_history"
top_k_revenue_profit = "Top 5 見込粗利率(見込粗利/見込販売額)" if not unicode_name_test else "top_k_revenue_profit"
top_k_handle_success = "Top 5 成約率(成約数/対応数)" if not unicode_name_test else "top_k_handle_success"
top_k_target_achieved = "Top 5 目標達成率" if not unicode_name_test else "top_k_target_achieved"
top_k_productivity = "Top 5 生産性(1h)" if not unicode_name_test else "top_k_productivity"
# [Top_K_config]
k = 5


HEIGHT = height
WIDTH = width
DATE_FORMAT = crud_api_format
X_AXIS_FORMAT = x_axis_format
BUYER_MANAGEMENT_ID_PREFIX = buyer_management_id_prefix


def build_personal_handle_success_line_chart(data, chart_id="personal_handle_success_history",
        height=HEIGHT, width=WIDTH, date_format=DATE_FORMAT,
        chart_title=personal_handle_success_history):

    xdata, ydata1, ydata2, ydata3, ydata4 = ([] for i in range(5))
    for date_result in data['data']:
        if not date_result.get('updated', None):

            day_result = date_result['results'][0]
            action_count = day_result['value']['achievement']['action_count']
            agreed_count = day_result['value']['achievement']['agreed_count']
            action_count_p = day_result['value']['personal_target']['action_count']
            agreed_count_p = day_result['value']['personal_target']['agreed_count']
            # if action_count:
            if True:
                ydata1.append(action_count)
                ydata2.append(agreed_count)
                ydata3.append(action_count_p)
                ydata4.append(agreed_count_p)

                d = datetime.strptime(date_result['_id']\
                    .replace(BUYER_MANAGEMENT_ID_PREFIX, ''), date_format)
                t = time.mktime(d.timetuple())
                xdata.append(t * 1000)

    # pretty_log({"xdata": xdata, "ydata1": ydata1})
    kwargs = {
        "margin_left": 60,
        "y_axis_format": ".f"
    }
    chart = stackedAreaChart(name=chart_id, height=height, width=width,
        x_is_date=True, x_axis_format=X_AXIS_FORMAT, **kwargs)

    chart.set_containerheader("\n\n<h2>{}</h2>\n\n".format(chart_title))

    chart.add_serie(y=ydata1, x=xdata, name='対応数')
    chart.add_serie(y=ydata2, x=xdata, name='成約数')
    chart.add_serie(y=ydata3, x=xdata, name='対応数(目標)')
    chart.add_serie(y=ydata4, x=xdata, name='成約数(目標)')

    chart.buildcontent()
    return chart.htmlcontent


def build_personal_revenue_line_chart(data, chart_id="personal_revenue_profit_history",
        height=HEIGHT, width=WIDTH, date_format=DATE_FORMAT,
        chart_title=personal_revenue_profit_history):

    xdata, ydata1, ydata2, ydata3, ydata4 = ([] for i in range(5))
    for date_result in data['data']:
        if not date_result.get('updated', None):

            day_result = date_result['results'][0]
            action_count = day_result['value']['achievement']['sale_amount']
            agreed_count = day_result['value']['achievement']['profit_amount']
            # action_count_p = day_result['value']['personal_target']['sale_amount']
            agreed_count_p = day_result['value']['personal_target']['profit_amount']
            # if action_count:
            if True:
                ydata1.append(action_count)
                ydata2.append(agreed_count)
                # ydata3.append(action_count_p)
                ydata4.append(agreed_count_p)

                d = datetime.strptime(date_result['_id']\
                    .replace(BUYER_MANAGEMENT_ID_PREFIX, ''), date_format)
                t = time.mktime(d.timetuple())
                xdata.append(t * 1000)

    # pretty_log({"xdata": xdata, "ydata1": ydata1})

    kwargs = {
        "margin_left": 60,
        "y_axis_format": ".f"
    }
    # chart = lineChart(name=chart_id, height=height, width=width,
    chart = lineWithFocusChart(name=chart_id, height=height, width=width,
        x_is_date=True, x_axis_format=X_AXIS_FORMAT, **kwargs)

    chart.set_containerheader("\n\n<h2>{}</h2>\n\n".format(chart_title))

    chart.add_serie(y=ydata1, x=xdata, name='見込販売額')
    chart.add_serie(y=ydata2, x=xdata, name='見込粗利')
    # chart.add_serie(y=ydata3, x=xdata, name='見込販売額(目標)')
    chart.add_serie(y=ydata4, x=xdata, name='見込粗利(目標)')

    chart.buildcontent()
    return chart.htmlcontent


def build_realtime_target_achieved_bar(data, chart_id="personal_realtime_target_achieved",
    height=HEIGHT, width=WIDTH, date_format=DATE_FORMAT,
    chart_title=personal_realtime_target_achieved, stacked=False):

    render_list = data['data'][0]['results']
    achievement = render_list[0]['value']['achievement']
    personal_target = render_list[0]['value']['personal_target']

    kwargs = {
        "margin_left": 60,
        "y_axis_format": ".2f"
    }
    chart = multiBarChart(name=chart_id, height=height, width=width,
        x_axis_format=None, stacked=stacked, **kwargs)
    chart.set_containerheader("\n\n<h2>{}</h2>\n\n".format(chart_title))

    xdata = list()
    if not personal_target['agreed_rate'] == 0:
        ydata1 = [float(u['value']['achievement']['agreed_rate']) \
            / u['value']['personal_target']['agreed_rate'] for u in render_list]
        xdata.append("成約率達成率")
        chart.add_serie(name="成約率達成率", x=xdata, y=ydata1)

    if not personal_target['action_count'] == 0:
        ydata2 = [float(u['value']['achievement']['action_count']) \
            / u['value']['personal_target']['action_count'] for u in render_list]
        xdata.append("対応数達成率")
        chart.add_serie(name="対応数達成率", x=xdata, y=ydata2)

    if not personal_target['agreed_count'] == 0:
        ydata3 = [float(u['value']['achievement']['agreed_count']) \
            / float(u['value']['personal_target']['agreed_count']) for u in render_list]
        xdata.append("成約数達成率")
        chart.add_serie(name="成約数達成率", x=xdata, y=ydata3)

    if not personal_target['profit_amount'] == 0:
        ydata4 = [float(u['value']['achievement']['profit_amount']) \
            / u['value']['personal_target']['profit_amount'] for u in render_list]
        xdata.append("見込粗利率達成率")
        chart.add_serie(name="見込粗利率達成率", x=xdata, y=ydata4)

    chart.buildcontent()
    return chart.htmlcontent



# todo
def build_productivity_bar(data, chart_id="personal_productivity_history",
    height=HEIGHT, width=WIDTH, date_format=DATE_FORMAT,
    chart_title=personal_productivity_history, stacked=False):

    render_list = data['data'][0]['results']

    kwargs = {
        "margin_left": 60,
        "y_axis_format": ".2f"
    }
    chart = multiBarChart(name=chart_id, height=height, width=width,
        x_axis_format=None, stacked=stacked, **kwargs)

    xdata = ["見込粗利(1h)", ]


    chart.set_containerheader("\n\n<h2>{}</h2>\n\n".format(chart_title))


    ydata1 = [ u['value']['achievement']['profit_per_hour'] for u in render_list]

    chart.add_serie(name="見込粗利(1h)", x=xdata, y=ydata1)

    chart.buildcontent()
    return chart.htmlcontent
