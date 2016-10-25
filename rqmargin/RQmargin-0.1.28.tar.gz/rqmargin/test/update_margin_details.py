from rqmargin.store.store import *
from rqmargin.config import get_config_one
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("update_mode", help="input 'total' or 'daily' .'total':it means that"
                                        "it is the first time to update")
args = parser.parse_args()

database_url = get_config_one("config.json").get('tushare')
store_margin_details = StoringMarginDetails(database_url)
if args.update_mode == 'total':
    flag=input("are you sure to totally update ? it will drop the existed collection.(y/n)")
    if flag== 'y':
        store_margin_details.drop_margin_details()
        store_margin_details.create_index()
        store_margin_details.update_margin_details()
elif args.update_mode == 'daily':
    store_margin_details.update_margin_details()
else:
    raise RuntimeError("please add correct argument. 'total' or 'daily'.")
print('begin to fetch data..')
print('store successfully.')
