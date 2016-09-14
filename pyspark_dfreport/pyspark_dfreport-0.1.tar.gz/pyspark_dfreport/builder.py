import pandas as pd
from pyspark.sql import DataFrame


class DataFrameReport(object):

    def __init__(self, report_path):
        assert(isinstance(report_path, str) and (report_path.endswith(".xlsx"))), "report path must be of type string" \
                                                                                  " and end with .xlsx"
        self.report_path = report_path
        self.report_writer = pd.ExcelWriter(self.report_path)
        self.df_count = 0

    def __del__(self):
        self.report_writer.close()

    def save_df(self, pyspark_df, name=None, header=True, index=False):
        """
        Save PySpark DataFrame to Excel File
        :param pyspark_df: Pyspark DF Object
        :param name: Name of sheet within Excel File to save DF to
        :param header: Boolean, save with header (col labels)
        :param index: Boolean, save with index (row labels)
        :return: None
        """
        assert(isinstance(pyspark_df, DataFrame)), "Not a PySpark DataFrame"
        self.df_count += 1
        if name is None:
            name = "DF_{}".format(self.df_count)
        pandas_df = pyspark_df.toPandas()
        pandas_df.to_excel(self.report_writer, sheet_name=name, header=header, index=index, encoding="utf-8")
        self.report_writer.save()
        return None
