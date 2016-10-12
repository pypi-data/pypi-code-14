# condig: utf-8

from datetime import datetime, timedelta


def make_ranking_index(vlist):
    '''
    指定の配列におけるランキングをインデックス基準に返す
    >>> make_ranking_index([19, 21, 11, 38, 21, 13, 28])
    [3, 6, 1, 4, 0, 5, 2]
    '''
    dic = {}
    for i, v in enumerate(vlist):
        dic.setdefault(v, []).append(i)
    ret = []
    for k, v in reversed(sorted(dic.items())):
        while v:
            ret.append(v.pop(0))
    return ret


def convert_num_to_weekday(num, lang="ja"):
    '''
    曜日インデックスを日本語に変換するメソッド
    >>> convert_num_to_weekday(2)
    '火'
    >>> convert_num_to_weekday(2, 'en')
    'Tue'
    '''
    convert_dict = {
        "ja": ["日", "月", "火", "水", "木", "金", "土"],
        "en": ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]}
    return convert_dict[lang][num]


def back_1day_ago(the_time=datetime.now()):
    """
    >>> back_1day_ago(datetime(2016, 4, 1))
    datetime.datetime(2016, 3, 31, 0, 0)
    """
    return the_time - timedelta(days=1)


def make_days_last_timestamp(the_time=datetime.now()):
    return datetime(the_time.year, the_time.month, the_time.day,
                    23, 59, 59)


def make_delta_hour(start_dt, end_dt=datetime.now()):
    """
    >>> start_dt = datetime(2016, 4, 1, 10, 40, 0)
    >>> end_dt = datetime(2016, 4, 1, 15, 40, 0)
    >>> make_delta_hour(start_dt, end_dt)
    5.0
    """
    delta_seconds = (end_dt - start_dt).seconds
    return round((delta_seconds // 60) / 60, 1)
