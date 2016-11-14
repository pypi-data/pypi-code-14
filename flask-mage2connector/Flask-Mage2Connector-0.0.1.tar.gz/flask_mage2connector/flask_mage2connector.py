from flask import current_app

try:
    from flask import _app_ctx_stack as stack
except ImportError:
    from flask import _request_ctx_stack as stack

import MySQLdb


class Adaptor(object):
    """Adaptor contain MySQL cursor object.
    """

    def __init__(self, mySQLConn=None):
        self._mySQLConn = mySQLConn
        self._mySQLCursor = self._mySQLConn.cursor(MySQLdb.cursors.DictCursor)

    @property
    def mySQLCursor(self):
        """MySQL Server cursor object.
        """
        return self._mySQLCursor

    def disconnect(self):
        self._mySQLConn.close()


class Mage2Connector(object):
    """Magento 2 connection with functions.
    """

    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        # Use the newstyle teardown_appcontext if it's available,
        # otherwise fall back to the request context
        if hasattr(app, 'teardown_appcontext'):
            app.teardown_appcontext(self.teardown)
        else:
            app.teardown_request(self.teardown)

    def connect(self):
        """Initiate the connect with MySQL server.
        """
        mySQLConn = MySQLdb.connect(current_app.config['MAGE2DBSERVER'],
                                    current_app.config['MAGE2DBUSERNAME'],
                                    current_app.config['MAGE2DBPASSWORD'],
                                    current_app.config['MAGE2DB'],
                                    charset="utf8",
                                    use_unicode=False)
        log = "Open Mage2 DB connection"
        current_app.logger.info(log)
        return Adaptor(mySQLConn)

    def teardown(self, exception):
        ctx = stack.top
        if hasattr(ctx, 'mage2adaptor'):
            ctx.mage2adaptor.disconnect()

    @property
    def adaptor(self):
        ctx = stack.top
        if ctx is not None:
            if not hasattr(ctx, 'mage2adaptor'):
                ctx.mage2adaptor = self.connect()
            return ctx.mage2adaptor
