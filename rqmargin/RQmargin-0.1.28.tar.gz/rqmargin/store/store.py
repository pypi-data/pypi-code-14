from pymongo import ASCENDING, DESCENDING
from rqmargin.store.mongosave import MongoSave
from rqmargin.handle.handling import *
from rqmargin.config import get_config_one

class StoringMargins(MongoSave):
    def __init__(self, mongo_config):
        super().__init__(mongo_config)

    def _create_index(self, collection):
        collection.create_index([("date", DESCENDING)],
                                )

    def update_margins(self):
        cursor = list(self._db.margins.find().sort('date', DESCENDING))
        if 0 == len(cursor):
            start = '2010-03-31'
        else:
            document=cursor[0]
            updated_date_str = document['date']
            updated_date = datetime.strptime(updated_date_str, '%Y-%m-%d').date()
            start = str(updated_date + timedelta(days=1))
        try:
            sh_margins_dict = handle_sh_margins(start=start)
            self._db.margins.insert_many(sh_margins_dict)
        except TypeError:
            print(" \nsh summarized RQmargin data is latest.no need to update")
        try:
            sz_margins_dict = handle_sz_margins(start=start)
            self._db.margins.insert_many(sz_margins_dict)
        except TypeError:
            print(" \nsz summarized RQmargin data is latest.no need to update.")

    def create_index(self):
        self._create_index(self._db.margins)

    def drop_margins(self):
        self._db.margins.drop()


class StoringMarginDetails(MongoSave):
    def __init__(self, margins_details_dict):
        super().__init__(margins_details_dict)
        self.create_index()

    def _create_index(self, collection):
        collection.create_index([('date', DESCENDING),
                                 ('stock_code', ASCENDING),
                                 ('fin_buy_value', DESCENDING)])

    def update_margin_details(self):
        cursor = list(self._db.margin_details.find().sort('date', DESCENDING))
        if 0 == len(cursor):
            start = '2010-03-31'
        else:
            document = cursor[0]
            updated_date_str = document['date']
            updated_date = datetime.strptime(updated_date_str, '%Y-%m-%d').date()
            start = str(updated_date + timedelta(days=1))
        try:
            sh_margin_details_dict = handle_sh_margin_details(start=start)
            self._db.margin_details.insert_many(sh_margin_details_dict)
        except TypeError:
            print("\nsh detailed RQmargin data is latest.no need to update.")
        try:
            sz_margin_details_dict = handle_sz_margin_details(start=start)
            self._db.margin_details.insert_many(sz_margin_details_dict)
        except TypeError:
            print("sz detailed RQmargin data is latest.no need to update.")



    def create_index(self):
        self._create_index(self._db.margin_details)

    def drop_margin_details(self):
        self._db.margin_details.drop()


def update_margin_details(update_mode):
    database_url = get_config_one("config.json").get('tushare')
    store_margin_details = StoringMarginDetails(database_url)
    if update_mode == 'total':
        flag = input("are you sure to totally update ? it will drop the existed collection.(y/n)")
        if flag == 'y':
            store_margin_details.drop_margin_details()
            store_margin_details.create_index()
            store_margin_details.update_margin_details()
    elif update_mode == 'daily':
        store_margin_details.update_margin_details()
    else:
        raise RuntimeError("please add correct argument. 'total' or 'daily'.")
    print('begin to fetch data..')
    print('store successfully.')


def update_margins(update_mode):
    database_url = get_config_one("config.json").get('tushare')
    store_margins = StoringMargins(database_url)
    if update_mode == 'total':
        flag = input("are you sure to totally update ? it will drop the existed collection.(y/n)")
        if flag == 'y':
            store_margins.drop_margins()
            store_margins.create_index()
            store_margins.update_margins()
    elif update_mode == 'daily':
        store_margins.update_margins()
    else:
        print("please add correct argument. 'total' or 'daily'.")
    print('begin to fetch data..')
    print('store successfully.')
