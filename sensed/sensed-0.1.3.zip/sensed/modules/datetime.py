import datetime
from dotmap import DotMap


class Datetime(object):
    def __init__(self, config: DotMap) -> None:
        if 'sensed-modules-datetime' not in config:
            self.config = DotMap({'formats': ['all']})
        else:
            self.config = config['sensed-modules-datetime']
        if 'formats' in self.config:
            if 'all' in self.config.formats:
                self.config.formats = ['unix', 'iso', '12h', '24h']
            elif 'none' in config.formats:
                self.config.formats = None
        else:
            self.config.formats = ['unix', 'iso', '12h', '24h']

    def get_data(self):
        datetimes = {}

        if self.config.formats:
            now = datetime.datetime.now()
            if 'unix' in self.config.formats:
                datetimes['unix'] = now.timestamp()
            if 'iso' in self.config.formats:
                datetimes['iso'] = now.isoformat()
            if '12h' in self.config.formats:
                datetimes['12h'] = now.strftime('%I:%M:%S%p')
            if '24h' in self.config.formats:
                datetimes['24h'] = now.strftime('%H:%M:%S')

        return datetimes

    def test(self):
        return self.get_data()

Sensor = Datetime
