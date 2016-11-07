"""!nr show new relic info"""
from dateutil.parser import parse
from io import BytesIO 
import os
import re
import requests


import matplotlib
# need to call this before importing pyplot
matplotlib.use('Agg')
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import pandas as pd
from pandas.io.json import json_normalize
import seaborn as sns

# if I decide to go back to pandas:
#from pandas.io.json import json_normalize
#df = json_normalize(data["metric_data"]['metrics'][0]['timeslices'])

NR_API_KEY = os.environ.get("NR_API_KEY")
sns.set(font_scale=1.5, style="darkgrid")

def response_time():
    # requests doesn't let you do multiple params with the same name using the
    # dict syntax; instead pass it a byte param
    rpm = requests.get('https://api.newrelic.com/v2/applications/30301056/metrics/data.json',
            headers={'X-Api-Key': NR_API_KEY},
            params=b'names[]=HttpDispatcher&values[]=average_response_time&values[]=min_response_time&values[]=max_response_time')
    data = rpm.json()

    df = json_normalize(data["metric_data"]['metrics'][0]['timeslices'])

    # convert from to a datetime, then to a matplotlib date number
    df['from'] = pd.to_datetime(df['from'])
    df['from'] = df['from'].apply(mdates.date2num)

    # rename the columns (TODO: don't assume column name order)
    df.columns = ['from', 'to', 'avg', 'max', 'min']

    # add a column with variable type (unpivot):
    # from:
    # from avg min max
    # 1    2   3   4
    # 2    3   4   5
    #
    # to:
    # from response time
    # 1    avg      2
    # 1    min      3
    # 1    max      4
    # 2    avg      3
    # 2    min      4
    # 2    max      5
    df = pd.melt(df, id_vars=['from'], value_vars=['avg', 'min', 'max'],
            var_name="response", value_name="ms")

    fig, ax = plt.subplots()
    sns.tsplot(data=df, time="from", condition="response", value="ms", unit="response")
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))

    imgbuf = BytesIO()
    img = fig.savefig(imgbuf, format='png')

    imgbuf.seek(0)
    return imgbuf

def throughput():
    rpm = requests.get('https://api.newrelic.com/v2/applications/30301056/metrics/data.json',
            headers={'X-Api-Key': NR_API_KEY},
            params={'names[]': 'HttpDispatcher', 'values[]': 'requests_per_minute'})
    data = rpm.json()

    # date2num converts from datetime to matplotlib's particular date format
    # http://matplotlib.org/api/dates_api.html
    pts = [(x['values']['requests_per_minute'], mdates.date2num(parse(x['from'])))
            for x in data["metric_data"]['metrics'][0]['timeslices']]
    ds, ts = zip(*pts)

    fig, ax = plt.subplots()
    sns.tsplot(ds, ts, ax=ax, value='Requests Per Minute')
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))

    imgbuf = BytesIO()
    img = fig.savefig(imgbuf, format='png')

    imgbuf.seek(0)
    return imgbuf

charts = {
    "throughput": throughput,
    "response_time": response_time,
}

def nr(chart):
    return charts.get(chart, charts["throughput"])()

def on_message(msg, server):
    text = msg.get("text", "")
    match = re.findall(r"!nr(.*)?", text)
    if not match:
        return

    if not NR_API_KEY:
        return "New Relic API key not found. Please set the NR_API_KEY " \
               "environment variable to your New Relic API key"

    chart = match[0].strip()
    img = nr(chart)

    r = server.slack.api_call("files.upload",
        post_data={"channels": msg["channel"]},
        files={'file': ('graph.png', img, 'image/png')})

    # don't return any messages via RTM
    return ""
