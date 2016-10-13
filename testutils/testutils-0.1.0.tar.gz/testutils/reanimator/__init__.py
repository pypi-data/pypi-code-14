import logging
from .default_webdriver import default_wd_func, default_wd_kwargs


class WebDriverReanimator(object):

    def __init__(self, wd_func=default_wd_func, wd_kwargs=default_wd_kwargs,
            filename='session_id.txt'):
        self.webdriver = wd_func(**wd_kwargs)
        logging.debug('new session_id: {}'.format(self.webdriver.session_id))
        self.filename = filename


    def __enter__(self):
        new_session_id = self.webdriver.session_id
        saved_session_id = self._load_session_id(self.filename)
        self.webdriver.session_id = saved_session_id
        try:
            # TODO: Come up with a more robust way
            #       to validate session_id.
            self.webdriver.find_element_by_xpath("//body")
            logging.debug('loaded session_id is valid; ' \
                    + 'throwing away newly opened browser')
            self.webdriver.session_id = new_session_id
            self.webdriver.close()
            self.webdriver.session_id = saved_session_id
            self.skip = True
        except:
            logging.debug('using new session_id')
            self.webdriver.session_id = new_session_id
            self.skip = False
        return self


    def __exit__(self, exc_type, exc_value, exc_tb):
        self._save_session_id(self.filename, self.webdriver.session_id)


    def _load_session_id(self, filename):
        try:
            with open(filename) as f:
                session_id = f.read()
            logging.debug('loaded session_id: {}'.format(session_id))
        except IOError:
            session_id = None
            logging.debug('failed to load session_id from file')
        return session_id


    def _save_session_id(self, filename, session_id):
        with open(filename, 'w') as f:
            f.write(session_id)
        logging.debug('saved session_id: {}'.format(self.webdriver.session_id))

