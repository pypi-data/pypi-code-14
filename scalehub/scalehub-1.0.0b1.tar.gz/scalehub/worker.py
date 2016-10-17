import sys


class Worker:
    def __init__(self, config):
        """
        type driver: str
        """
        self.id = config['id']
        self.endless = config['endless'] if 'endless' in config else False
        self.run_priority = int(config['run_priority']) if 'run_priority' in config else sys.maxint  # noqa
        self.config = config
        driver_klass = config['driver_class']
        driver_config =\
            config['driver_config'] if 'driver_config' in config else {}
        driver_config['id'] = config['id']
        self.driver = driver_klass(driver_config)

    def init(self):
        self.driver.init()

    def start_test(self):
        self.driver.start_test()

    def stop_test(self):
        self.driver.stop_test()

    def status(self):
        return self.driver.status()

    def collect_results(self):
        return self.driver.collect_results()
