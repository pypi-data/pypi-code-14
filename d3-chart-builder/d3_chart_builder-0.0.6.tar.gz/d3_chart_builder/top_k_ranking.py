# encoding: utf-8
import os
import sys
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
# TOP_K = int(configParser.get('Top_K_config', 'k'))


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
TOP_K = k


def build_revenue_profit_bar(data, chart_id="top_k_revenue_profit",
        height=HEIGHT, width=WIDTH, date_format=DATE_FORMAT, top_k=TOP_K,
        chart_title=top_k_revenue_profit, stacked=False):

    all_list = data['data'][0]['results']
    render_list = [u for u in all_list \
        if (u['group_id'] == "cc:tokyo" or u['group_id'] == "cc:tokushima")\
        and not u['value']['achievement']['sale_amount'] == 0]

    if top_k:
        render_list = sorted(render_list,
            key=lambda k: k['value']['achievement']['sale_amount'] ,reverse=True)[:top_k]

    # pretty_log(render_list)
    # pretty_log({"Number of members:": len(render_list)})

    kwargs = {
        "margin_left": 60,
        "y_axis_format": ".f"
    }
    chart = multiBarChart(name=chart_id, height=height, width=width,
        x_axis_format=None, stacked=stacked, **kwargs)
    xdata = [u['user_name'] for u in render_list]
    # pretty_log(xdata)

    chart.set_containerheader("\n\n<h2>{}</h2>\n\n".format(chart_title))


    ydata1 = [u['value']['achievement']['profit_rate'] for u in render_list]
    ydata2 = [u['value']['achievement']['sale_amount'] for u in render_list]
    ydata3 = [u['value']['achievement']['profit_amount'] for u in render_list]

    chart.add_serie(name="見込粗利率", x=xdata, y=ydata1)
    chart.add_serie(name="見込販売額", x=xdata, y=ydata2)
    chart.add_serie(name="見込粗利額", x=xdata, y=ydata3)

    chart.buildcontent()
    return chart.htmlcontent


def build_handle_success_bar(data, chart_id="top_k_handle_success",
    height=HEIGHT, width=WIDTH, date_format=DATE_FORMAT, top_k=TOP_K,
    chart_title=top_k_handle_success, stacked=True):

    all_list = data['data'][0]['results']
    render_list = [u for u in all_list \
        if (u['group_id'] == "cc:tokyo" or u['group_id'] == "cc:tokushima")\
        and not u['value']['achievement']['action_count'] == 0]

    if top_k:
        render_list = sorted(render_list,
            key=lambda k: k['value']['achievement']['agreed_rate'] , reverse=True)[:top_k]

    kwargs = {
        "margin_left": 60,
        "y_axis_format": ".f"
    }
    chart = multiBarChart(name=chart_id, height=height, width=width,
        x_axis_format=None, stacked=stacked, **kwargs)

    xdata = [u['user_name'] for u in render_list]
    # pretty_log(xdata)

    chart.set_containerheader("\n\n<h2>{}</h2>\n\n".format(chart_title))

    ydata1 = [u['value']['achievement']['agreed_rate'] for u in render_list]
    ydata2 = [u['value']['achievement']['action_count'] for u in render_list]
    ydata3 = [u['value']['achievement']['agreed_count'] for u in render_list]

    chart.add_serie(name="成約率", x=xdata, y=ydata1)
    chart.add_serie(name="対応数", x=xdata, y=ydata2)
    chart.add_serie(name="成約数", x=xdata, y=ydata3)

    chart.buildcontent()
    return chart.htmlcontent


def build_target_achieved_bar(data, chart_id="top_k_target_achieved",
    height=HEIGHT, width=WIDTH, date_format=DATE_FORMAT, top_k=TOP_K,
    chart_title=top_k_target_achieved, stacked=True):

    all_list = data['data'][0]['results']
    render_list = [u for u in all_list \
        if (u['group_id'] == "cc:tokyo" or u['group_id'] == "cc:tokushima")\
        and not u['value']['personal_target']['action_count'] == 0]

    if top_k:
        render_list = sorted(render_list,
            key=lambda k: float(k['value']['achievement']['agreed_rate']) \
            / k['value']['personal_target']['agreed_rate'] , reverse=True)[:top_k]

    chart = multiBarChart(name=chart_id, height=height, width=width,
        x_axis_format=None, stacked=stacked)

    xdata = [u['user_name'] for u in render_list]
    # pretty_log(xdata)

    chart.set_containerheader("\n\n<h2>{}</h2>\n\n".format(chart_title))

    # "personal_target": {
    # "additional_count": 4,

    ydata1 = [float(u['value']['achievement']['agreed_rate']) \
        / u['value']['personal_target']['agreed_rate'] for u in render_list]
    ydata2 = [float(u['value']['achievement']['action_count']) \
        / u['value']['personal_target']['action_count'] for u in render_list]
    ydata3 = [float(u['value']['achievement']['agreed_count']) \
        / u['value']['personal_target']['agreed_count'] for u in render_list]
    ydata4 = [float(u['value']['achievement']['profit_amount']) \
        / u['value']['personal_target']['profit_amount'] for u in render_list]


    chart.add_serie(name="成約率", x=xdata, y=ydata1)
    chart.add_serie(name="対応数", x=xdata, y=ydata2)
    chart.add_serie(name="成約数", x=xdata, y=ydata3)
    chart.add_serie(name="見込粗利率", x=xdata, y=ydata4)

    chart.buildcontent()
    return chart.htmlcontent


def build_productivity_bar(data, chart_id="top_k_productivity",
    height=HEIGHT, width=WIDTH, date_format=DATE_FORMAT, top_k=TOP_K,
    chart_title=top_k_productivity, stacked=True):

    all_list = data['data'][0]['results']
    render_list = [u for u in all_list \
        if (u['group_id'] == "cc:tokyo" or u['group_id'] == "cc:tokushima")\
        and not u['value']['achievement']['action_per_hour'] == 0]

    if top_k:
        render_list = sorted(render_list,
            key=lambda k: k['value']['achievement']['profit_per_hour'] , reverse=True)[:top_k]

    kwargs = {
        "margin_left": 60,
        "y_axis_format": ".f"
    }
    chart = multiBarChart(name=chart_id, height=height, width=width,
        x_axis_format=None, stacked=stacked, **kwargs)

    xdata = [u['user_name'] for u in render_list]
    # pretty_log(xdata)

    chart.set_containerheader("\n\n<h2>{}</h2>\n\n".format(chart_title))

    # "personal_target": {
    # "additional_count": 4,

    ydata1 = [ u['value']['achievement']['profit_per_hour'] for u in render_list]
    ydata2 = [ u['value']['achievement']['action_per_hour'] for u in render_list]
    ydata3 = [ u['value']['achievement']['agreed_per_hour'] for u in render_list]

    chart.add_serie(name="見込粗利(1h)", x=xdata, y=ydata1)
    chart.add_serie(name="対応数(1h)", x=xdata, y=ydata2)
    chart.add_serie(name="成約数(1h)", x=xdata, y=ydata3)

    chart.buildcontent()
    return chart.htmlcontent
