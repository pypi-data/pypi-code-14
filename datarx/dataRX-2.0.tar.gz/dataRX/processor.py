# dataRX : A simple extension used to view, clean, and process your data files
# Author : Rashad Alston <ralston@yahoo-inc.com>
# Python : 3.5.1
#
# License: BSD 3 Clause

import pandas as pd
import numpy as np
from scipy import stats
import warnings
import time
import os


class RX:
    """
    A simple extension used to view, clean, and process your data files

    Parameters
    ----------

    file : <string>
        Data file to be read and manipulated
    worksheet : <string>
        The worksheet name (if using .xlsx or .xls file)
    """

    def __init__(self, file, worksheet=None):

        self.file = file
        self.worksheet = worksheet

    def info(self):
        """
        Checks to make sure that the given path exists, and that
        the path leads to a file.

        Returns
        -------
            file_path, file_ext, file_size : The file's path, extension, and size

        Raises
        ------
            TypeError : If file is not an actual file
        """

        if not isinstance(self.file, str):
            raise TypeError("'file' param requires type str. Type %s given." % type(self.file))

        if os.path.exists(self.file):
            try:
                os.path.isfile(self.file)
            except:
                raise TypeError("A file is required. %s is not a file." % self.file)

            file_path, file_ext = os.path.splitext(self.file)
            # 1048576 bytes = 1 megabyte >> http://www.whatsabyte.com/P1/byteconverter.htm
            file_size = os.path.getsize(self.file) / 1048576

            return file_path, file_ext, file_size

        else:
            raise OSError("%s is not an existing file path." % self.file)

    def read(self, file_info, *args, **kwargs):
        """
        Reads file in using pandas libaray I/O.

        Parameters
        ----------
            file_info : <tuple>
                File path, file extension, file size returned by info()

        Returns
        -------
            frame : data stored in a pandas DataFrame object

        Raises
        ------
            TypeError : If file_ext type is not supported
        """

        file_path, file_ext, file_size = file_info

        start = time.time()

        # Set the appropriate I/O reader for the various file types
        if (file_ext == ".csv") or (file_ext == ".txt"):
            frame = pd.read_csv(self.file, *args, **kwargs)

        elif (file_ext == ".xlsx") or (file_ext == ".xls"):
            frame = pd.read_excel(self.file, sheetname=self.worksheet, *args, **kwargs)
        else:
            raise TypeError("File type must be .csv, .txt, .xls, .xlsx. Got type '%s'" % file_ext)

        dtypes = [str(type(frame[col].values[0])) for col in frame.columns.values]

        # Print log to console
        print("Importing data...\n")
        print("Data shape: %d samples x %d features\n" % frame.shape)
        print("Unique data types found:", np.unique(dtypes), "\n")
        print("File size: %7.6f megabytes\n" % file_size)
        print("Done! Import time: %.2f seconds\n" % (np.abs(time.time() - start)))

        return frame

    def report(self, data, save_as):
        """
        Generates a general report on the contents of the data file

        Parameters
        ----------
            data : <pd.DataFrame>
                DataFrame object returned by read()
            save_as : <string>
                Path on which to store the .csv report

        Returns
        -------
            report : <pd.DataFrame>
                DataFrame object with descriptive statistics of data set
            data : <pd.DataFrame>
                DataFrame object returned by read()

        Raises
        ------
            None
        """

        if not isinstance(data, pd.DataFrame):
            raise TypeError("'data' param requires type pd.DataFrame. Type %s given." % type(data))

        if not isinstance(save_as, str):
            raise TypeError("'save_as' param requires type str. Type %s given." % type(save_as))

        start = time.time()
        cols = data.columns.values

        print("Generating report...\n")

        names = ["Index","Name","Variance","Sigma","Mu","Median",
                 "Mode","Min","Max","25th-Percentile","50th-Percentile",
                 "75th-Percentile","Total Number of Nulls",
                 "Percent of Values Null","Total Uniques","Data Type"]

        report_frame = pd.DataFrame(columns=names)

        with warnings.catch_warnings():

            warnings.filterwarnings("ignore")

            for i, col in enumerate(cols):

                series = data[col]

                # The descriptive statistics only apply to types of int and float
                if (series.dtype == "int64") or (series.dtype == "float64"):

                    vals = [i, col, np.var(series), np.std(series), np.mean(series),
                            np.median(series), stats.mode(series)[0], np.amin(series),
                            np.amax(series), np.percentile(series, 25), np.percentile(series, 50),
                            np.percentile(series, 75), sum(series.isnull()),
                            (sum(series.isnull()) / len(series)), len(series.unique()), series.dtype]

                # For type objects, insert NA in place of statistical values
                elif (series.dtype !="int64") or (series.dtype != "float64"):

                    # stats.mode(series, nan_policy="omit")
                    vals = [i, col, "Object:NA", "Object:NA", "Object:NA",
                            "Object:NA", "Object:NA", "Object:NA",
                            "Object:NA", "Object:NA", "Object:NA", "Object:NA",
                            sum(series.isnull()), (sum(series.isnull()) / len(series)),
                            len(series.unique()), series.dtype]

                else:
                    raise TypeError("Column '%s' with type %s is not acceptable." % (col, series.type))

                print("Processing feature: %d/%d ..." % (i+1, len(cols)))
                
                report_frame.loc[i] = vals

        report_frame.to_csv(save_as, index=False)

        print("\nDone! Processing finished in %3.2f minutes" % (np.abs(time.time() - start) / 60))

        return report_frame, data


rx = RX(file="../../data_dump/ybn_data.csv")
info = rx.info()
data = rx.read(info, low_memory=False)
report, data = rx.report(data, "sample.csv")
