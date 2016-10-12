# coding: utf-8

import csv

from home_electric_usage_recommendation_modules \
    import (SettingTemp, ReduceUsage, ChangeUsage)
from tests.test_modules import RowData


def get_input_rows_list():
    input_rows = []
    with open('test.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            input_rows.append(
                RowData(timestamp=row['timestamp'],
                        set_temperature=row['set_temperature'],
                        on_off=row['on_off']))
    return input_rows


if __name__ == "__main__":
    input_rows = get_input_rows_list()

    # SettingTemp
    st = SettingTemp(input_rows)
    st.calculate_running_time()

    # ReduceUsage
    du = ReduceUsage(input_rows)
    du.calculate_running_time()

    # ChangeUsage
    cu = ChangeUsage(input_rows)
    cu.calculate_running_time()
