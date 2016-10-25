from rqmargin.fetch.fetching import *
import rqdata


def handle_sh_margin_details(start=''):
    """
    handle the sh detail RQmargin data fetched from tushare.
    recalculate by getting closing price from rqdata and change
    some fields name.
    :param start:
    :param update_mode: the mode you want to update ,total or daily.
    :return: return a list
    """
    print("begin to fetch sh data..")
    sh_margin_details_df = fetch_sh_margin_details(start=start)
    margin_details = []
    if sh_margin_details_df.empty:
        return margin_details
    stock_list = list((sh_margin_details_df['stockCode'] + '.XSHG').unique())
    recent_day = date.today() + timedelta(days=-1)
    rqdata.init()
    closing_px_df = rqdata.get_price(stock_list,
                                     start_date='2010-03-31',
                                     end_date=str(recent_day), adjusted=False)['ClosingPx']
    sh_margin_details_dict = sh_margin_details_df.to_dict('records')
    for value in sh_margin_details_dict:
        closing_px = closing_px_df.loc[value['opDate'], value['stockCode'] + '.XSHG']
        one_margin_details = {'date': value['opDate'],
                              'stock_code': value['stockCode'] + '.XSHG',
                              'fin_value': value['rzye'],
                              'fin_buy_value': value['rzmre'],
                              'stock_value': value['rqyl'] * closing_px,
                              'stock_sell_value': value['rqmcl'] * closing_px}

        one_margin_details['margin_value'] = one_margin_details['fin_value'] \
                                             + one_margin_details['stock_value']

        margin_details.append(one_margin_details)
    return margin_details


def handle_sz_margin_details(start=''):
    """
    handle the sz data fetched fetched from tushare.
    recalculate by getting closing price from rqdata and
    change some fields' name.
    :param start:
    :param update_mode:the mode you want to update, total or daily.
    :return: return a list containing all of detail RQmargin-records in ShenZhen exchange.
    """
    print("\nbegin to fetch sz data..")

    sz_margin_details_df = fetch_sz_margin_details(start=start)
    sz_margin_details = []
    if sz_margin_details_df.empty:
        return sz_margin_details
    rqdata.init()
    recent_day = date.today() + timedelta(days=-1)

    closing_px_df = rqdata.get_price(stock_list,
                                     start_date='2010-03-31',
                                     end_date=str(recent_day), adjusted=False)['ClosingPx']
    sz_margin_details_dict = sz_margin_details_df.to_dict('records')
    for value in sz_margin_details_dict:
        closing_px = closing_px_df.loc[value['opDate'],
                                       value['stockCode'] + '.XSHE']
        one_margin_details = {'date': value['opDate'],
                              'stock_code': value['stockCode'] + '.XSHE',
                              'fin_value': value['rzye'],
                              'fin_buy_value': value['rzmre'],
                              'stock_value': value['rqye'],
                              'stock_sell_value': value['rqmcl'] * closing_px,
                              'margin_value': value['rzrqye']}

        sz_margin_details.append(one_margin_details)
    return sz_margin_details


def handle_sh_margins(start=None):
    """
    to add some fields and change some fields' name.
    :param start:
    :return:
    """
    print('begin to fetch sh data..')
    sh_margins_df = fetch_sh_margins(start=start)
    sh_margins_dict = sh_margins_df.to_dict('records')
    sz_margin_details = []
    for value in sh_margins_dict:
        one_margins = {'date': value['opDate'], 'fin_value': value['rzye'],
                       'fin_buy_value': value['rzmre'], 'stock_value': value['rqylje'],
                       'stock_sell': value['rqmcl'], 'margin_value': value['rzrqjyzl'],
                       'region':'XSHG'}

        sz_margin_details.append(one_margins)
    return sz_margin_details

def handle_sz_margins(start=None):
    """
    to add some fields and change some fields' name .
    :param start:
    :return:
    """
    print('begin to fetch sz data..')
    sz_margins_df = fetch_sz_margins(start=start)
    sh_margins_dict = sz_margins_df.to_dict('records')
    sz_margin_details = []
    for value in sh_margins_dict:
        one_margins = {'date': value['opDate'], 'fin_value': value['rzye'],
                       'fin_buy_value': value['rzmre'], 'stock_value': value['rqye'],
                       'stock_sell': value['rqmcl'], 'margin_value': value['rzrqye'],
                       'region':'XSHE'}

        sz_margin_details.append(one_margins)
    return sz_margin_details