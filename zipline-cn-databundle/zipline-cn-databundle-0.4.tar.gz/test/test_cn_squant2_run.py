import matplotlib.pyplot as plt
from zipline.data.bundles import register
from zipline_cn_databundle.squant_source import squant_bundle
import pandas as pd
import os

from zipline.api import (
    schedule_function,
    symbol,
    order_target_percent,
    date_rules,
    record
)
import re
from zipline.algorithm import TradingAlgorithm
from zipline.finance.trading import TradingEnvironment
from zipline.utils.calendars import get_calendar, register_calendar
from zipline.finance import trading
from zipline.utils.factory import create_simulation_parameters
from zipline.data.bundles.core import load
from zipline.data.data_portal import DataPortal

from zipline_cn_databundle.loader import load_market_data

# register SHSZ

from cn_stock_holidays.zipline.default_calendar import shsz_calendar


bundle = 'cn_squant'

start_session_str = '2010-12-21'

register(
        bundle,
        squant_bundle,
        "SHSZ",
        pd.Timestamp(start_session_str, tz='utc'),
        pd.Timestamp('2016-10-31', tz='utc')
        )


bundle_data = load(
    bundle,
    os.environ,
    None,
)

prefix, connstr = re.split(
    r'sqlite:///',
    str(bundle_data.asset_finder.engine.url),
    maxsplit=1,
)

env = trading.environment = TradingEnvironment(asset_db_path=connstr,
                                               trading_calendar=shsz_calendar,
                                               bm_symbol='000001.SS',
                                               load=load_market_data)


first_trading_day = \
    bundle_data.equity_minute_bar_reader.first_trading_day
data = DataPortal(
    env.asset_finder, shsz_calendar,
    first_trading_day=first_trading_day,
    equity_minute_reader=bundle_data.equity_minute_bar_reader,
    equity_daily_reader=bundle_data.equity_daily_bar_reader,
    adjustment_reader=bundle_data.adjustment_reader,
)


def initialize(context):
    schedule_function(handle_daily_data, date_rules.every_day())

def handle_daily_data(context, data):
    sym = symbol('000001.SZ')
    # Save values for later inspection
    record(price=data.current(sym, 'price'),
           )

def analyze(context, perf):
    fig = plt.figure(figsize=(14,13))
    ax1 = fig.add_subplot(211)
    perf.portfolio_value.plot(ax=ax1, grid=True)
    ax1.set_ylabel('portfolio value in $')

    ax2 = fig.add_subplot(212)
    perf['GOOG'].plot(ax=ax2)
    perf[['short_mavg', 'long_mavg']].plot(ax=ax2)

    perf_trans = perf.ix[[t != [] for t in perf.transactions]]
    buys = perf_trans.ix[[t[0]['amount'] > 0 for t in perf_trans.transactions]]
    sells = perf_trans.ix[
        [t[0]['amount'] < 0 for t in perf_trans.transactions]]
    ax2.plot(buys.index, perf.short_mavg.ix[buys.index],
             '^', markersize=4, color='m')
    ax2.plot(sells.index, perf.short_mavg.ix[sells.index],
             'v', markersize=4, color='k')
    ax2.set_ylabel('price in $')
    plt.legend(loc=0)
    plt.show()
    plt.imsave("output.png")


if __name__ == '__main__':
    sim_params = create_simulation_parameters(
        start=pd.to_datetime(start_session_str + " 00:00:00").tz_localize("Asia/Shanghai"),
        end=pd.to_datetime("2011-01-01 00:00:00").tz_localize("Asia/Shanghai"),
        data_frequency="daily", emission_rate="daily", trading_calendar=shsz_calendar)

    algor_obj = TradingAlgorithm(initialize=initialize,
                                 handle_data=None,
                                 sim_params=sim_params,
                                 env=trading.environment,
                                 trading_calendar=shsz_calendar)
    # not use run method of TradingAlgorithm
    #perf_manual = algor_obj.run(data)
    #perf_manual.to_pickle('/tmp/perf.pickle')

    algor_obj.data_portal = data
    algor_obj._assets_from_source = \
            self.trading_environment.asset_finder.retrieve_all(
                    self.trading_environment.asset_finder.sids
                    )
    algor_obj.perf_tracker = None
    try:
        perfs = []
        for perf in self.get_generator():
                perfs.append(perf)
                print('-' * 40)
                print(perf)
                print('-' * 40)

        daily_stats = algor_obj._create_daily_stats(perfs)
        print('*' * 40)
        print('daily_stats')
        print('*' * 40)
        print(daily_stats)
        daily_stats.to_pickle('/tmp/perf.pickle')
    finally:
        algor_obj.data_portal = None
