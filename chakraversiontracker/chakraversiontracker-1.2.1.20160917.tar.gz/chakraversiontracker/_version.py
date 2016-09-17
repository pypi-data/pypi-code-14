from datetime import datetime

__software_version__ = '1.2.1'
__data_date__ = datetime(year=2016, month=9, day=17)
__data_version__ = __data_date__.strftime('%Y%m%d')
__version__ = '{}.{}'.format(__software_version__, __data_version__)
