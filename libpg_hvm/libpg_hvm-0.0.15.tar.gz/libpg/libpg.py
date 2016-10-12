import threading
import psycopg2
import psycopg2.extras

class PG(object):
    """
        psycopg2 wrapper object
    """

    LOG_LEVELS = {
        'error': 0,
        'warn': 1,
        'info': 2,
        'debug': 3,
    }

    def set_log_level(self, level):
        if level in PG.LOG_LEVELS:
            self.log_level = PG.LOG_LEVELS[level]

    def log(self, level, text):
        if level not in PG.LOG_LEVELS:
            raise RuntimeError("Invalid log level: %s" % (level))
        if PG.LOG_LEVELS[level] > self.log_level:
            return
        print(text)

    def debug(self, text):
        self.log('debug', text)

    def info(self, text):
        self.log('info', text)

    def warn(self, text):
        self.log('warn', text)

    def error(self, text, exception=None):
        self.log('error', text)
        if exception is not None:
            self.log('error', exception)

    def __init__(self, uselocks=True, tries=3, log_level='warn', **kargs):
        """
            available parameters:
                user, host, password, database/dbname
                uselocks: lock requests s.t. only 1 operation is allowed per connection
        """
        
        self.params = {
            'host': 'localhost',
            'port': 5432,
            'dbname': 'postgres',
            'user': 'postgres',
            'password': 'postgres',
        }
        self.params.update(kargs)
        
        if 'database' in self.params:
            self.params['dbname'] = self.params['database']
            del self.params['database']

        if 'log' in kargs and callable(kargs['log']):
            self.log = kargs['log']

        self.set_log_level(log_level)
        
        self.uselocks = uselocks
        if uselocks:
            self.lock = threading.Lock()

        self.tries = tries
        
        self.connect()
        
    def connect(self):
        try:
            self.conn.close()
        except:
            pass
            
        try:
            self.conn = psycopg2.connect(**self.params)
            self.cur = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        except Exception as e:
            self.conn = None
            self.error("failed to connect %s:%s to %s:%s" % (self.params['user'], self.params['password'],
                self.params['host'], self.params['port']), e)
        
    def execute(self, query, params, commit=1):
        if self.uselocks:
            self.lock.acquire()
            
        try:
            tries = self.tries
            while True:
                try:
                    self.cur.execute(query, params)
                    if commit:
                        self.conn.commit()
                    return True
                except Exception as e:
                    self.debug("query failed: [%s] with params %s" % (query, params))
                    self.error("query failure", e)

                    tries -= 1
                    if tries <= 0:
                        break

                    self.debug("retrying, %d attempts left" % (tries))
                    self.connect()
                    
            self.debug("query aborted after %d tries" % (self.tries))
            return False
        finally:
            if self.uselocks:
                self.lock.release()
        
    def get(self, query, params=[], commit=1):
        row = self.execute(query, params, commit) and self.cur.fetchone()
        if row:
            return row[0]
        return None
        
    def get_one(self, query, params=[], commit=1):
        return self.execute(query, params, commit) and self.cur.fetchone()
        
    def get_many(self, query, count, params=[], commit=1):
        rows = self.execute(query, params, commit) and self.cur.fetchall()
        if rows:
            return rows[:count]
        else:
            return None
            
    def get_list(self, query, params=[], commit=1):
        rows = self.execute(query, params, commit) and self.cur.fetchall()
        if rows:
            return [x[0] for x in rows]
        else:
            return None
        
    def get_all(self, query, params=[], commit=1):
        rows = self.execute(query, params, commit) and self.cur.fetchall()
        if rows:
            return rows
        else:
            return None