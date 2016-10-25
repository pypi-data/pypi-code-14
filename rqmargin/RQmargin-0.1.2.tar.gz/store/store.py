from pymongo import ASCENDING, DESCENDING
from store.mongosave import MongoSave
from handle.handling import *


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
            print(" \nsh summarized margin data is latest.no need to update")
        try:
            sz_margins_dict = handle_sz_margins(start=start)
            self._db.margins.insert_many(sz_margins_dict)
        except TypeError:
            print(" \nsz summarized margin data is latest.no need to update.")

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
            print("\nsh detailed margin data is latest.no need to update.")
        try:
            sz_margin_details_dict = handle_sz_margin_details(start=start)
            self._db.margin_details.insert_many(sz_margin_details_dict)
        except TypeError:
            print("sz detailed margin data is latest.no need to update.")



    def create_index(self):
        self._create_index(self._db.margin_details)

    def drop_margin_details(self):
        self._db.margin_details.drop()

