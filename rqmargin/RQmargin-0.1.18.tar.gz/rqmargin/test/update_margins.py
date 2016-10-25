
from rqmargin.store.store import *
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("update_mode", help="input 'total' or 'daily' .'total':it means that"
                                        "it is the first time to update")
args = parser.parse_args()

database_url = get_config_one("../config.json").get('tushare')
store_margins = StoringMargins(database_url)
if args.update_mode == 'total':
    flag = input("are you sure to totally update ? it will drop the existed collection.(y/n)")
    if flag == 'y':
        store_margins.drop_margins()
        store_margins.create_index()
        store_margins.update_margins()
elif args.update_mode == 'daily':
    store_margins.update_margins()
else:
    print("please add correct argument. 'total' or 'daily'.")
print('begin to fetch data..')
print('store successfully.')

