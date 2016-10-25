import tushare as ts
from datetime import *
import multiprocessing
import pandas as pd


def fetch_sh_margins(start=None, retry_count=3):
    """
    fetch summarized margin data in ShangHai exchange from tushare
    :param start:
    :param retry_count:
    :return:
    """
    sh_margins_df = ts.sh_margins(start=start,
                                  retry_count=retry_count)
    return sh_margins_df


def fetch_sh_margin_details(start='', retry_count=100):
    """
    fetch detailed  margin data in ShangHai exchange from tushare
    and tushare suggests that we should get one year data at most
    every time we call.
    :param start:
    :param retry_count:
    :return:
    """
    start_date = datetime.strptime(start, '%Y-%m-%d').date()
    today_date = date.today()
    if int((today_date - start_date).days) > 364:
        begin_date_str = start
        begin_date = datetime.strptime(begin_date_str, '%Y-%m-%d').date()
        today_date = date.today()
        years = int((today_date - begin_date).days / 365)
        sh_margin_details_df = pd.DataFrame()
        mgr = multiprocessing.Manager()
        dt = mgr.dict()
        dt['sh_margin_details_df'] = sh_margin_details_df
        processing_dict = []

        for i in range(years + 1):
            end_date = begin_date + timedelta(days=364)
            start = str(begin_date)
            end = str(end_date)
            p = multiprocessing.Process(target=multi_fetch_sh_margin_details,
                                        args=(dt, start, end, retry_count,
                                              ))
            p.start()
            processing_dict.append(p)
            begin_date = end_date + timedelta(days=1)
        for p in processing_dict:
            p.join()

        sh_margin_details_df = dt['sh_margin_details_df']

    else:
        today_date_str = str(today_date)
        sh_margin_details_df = ts.sh_margin_details(start=start, end=today_date_str,
                                                    retry_count=retry_count)
    return sh_margin_details_df


def fetch_sz_margins(start=None, retry_count=100):
    """
    fetch summarized margin data in ShenZhen exchange from tushare, and tushare
    suggest that we should get one year data at most every time we call.
    :param start:
    :param retry_count:
    :return:
    """
    start_date = datetime.strptime(start, '%Y-%m-%d').date()
    today_date_str = date.today()
    if int((today_date_str - start_date).days) > 364:
        begin_date_str = "2010-03-31"
        begin_date = datetime.strptime(begin_date_str, '%Y-%m-%d').date()
        today_date = date.today()
        years = int((today_date - begin_date).days / 365)
        sz_margins_df = pd.DataFrame()
        mgr = multiprocessing.Manager()
        dt = mgr.dict()
        dt['sz_margins_df'] = sz_margins_df
        processing_list = []
        for i in range(years + 1):
            end_date = begin_date + timedelta(days=364)
            start = str(begin_date)
            end = str(end_date)
            p = multiprocessing.Process(target=multi_fetch_sz_margins,
                                        args=(dt, start, end, retry_count,
                                              ))
            p.start()
            processing_list.append(p)
            begin_date = end_date + timedelta(days=1)
        for p in processing_list:
            p.join()
        sz_margins_df = dt['sz_margins_df']
    else:
        sz_margins_df = ts.sz_margins(start=start,
                                      retry_count=retry_count)

    return sz_margins_df


def fetch_sz_margin_details(start='', retry_count=100):
    """
     fetch detailed margin data in ShenZhen exchange from tushare, and tushare
    suggest that we should get one day data at most every time we call.
    :param start:
    :param retry_count:
    :param update_mode:
    :return:
    """
    begin_date_str = start
    begin_date = datetime.strptime(begin_date_str, '%Y-%m-%d').date()
    today_date = date.today()
    years = int((today_date - begin_date).days / 365)
    sz_margin_details_df = pd.DataFrame()
    mgr = multiprocessing.Manager()
    dt = mgr.dict()
    dt['sz_margin_details_df'] = sz_margin_details_df
    processing_list = []
    for i in range(years + 1):
        end_date = begin_date + timedelta(days=364)
        p = multiprocessing.Process(target=multi_fetch_sz_margin_details,
                                    args=(dt, begin_date, end_date, retry_count,
                                          ))
        p.start()
        processing_list.append(p)
        begin_date = end_date
    for p in processing_list:
        p.join()
    sz_margin_details_df = dt['sz_margin_details_df']
    return sz_margin_details_df


def multi_fetch_sz_margins(dt, start, end, retry_count):
    sz_one_margins_df = ts.sz_margins(start=start, end=end,
                                      retry_count=retry_count,
                                      )
    dt['sz_margins_df'] = dt['sz_margins_df'].append(sz_one_margins_df)


def multi_fetch_sh_margin_details(dt, start, end, retry_count):
    sh_one_margin_details_df = ts.sh_margin_details(start=start, end=end,
                                                    retry_count=retry_count,
                                                    )
    dt['sh_margin_details_df'] = dt['sh_margin_details_df'] \
        .append(sh_one_margin_details_df)


def multi_fetch_sz_margin_details(dt, begin_date, end_date, retry_count):
    days = int((end_date - begin_date).days)
    sz_margin_details_df = pd.DataFrame()
    for i in range(days):
        select_date = str(begin_date + timedelta(days=i + 1))
        sz_one_margin_details_df = ts.sz_margin_details(date=select_date,
                                                        retry_count=retry_count,
                                                        )
        sz_margin_details_df = sz_margin_details_df.append(sz_one_margin_details_df)
    dt['sz_margin_details_df'] = dt['sz_margin_details_df'] \
        .append(sz_margin_details_df)
