import logging


class DatabaseError(Exception):
    """
    Custom custom_error for Database
    """
    def __init__(self, code, **kwargs):
        self.code = {
            4000: "{}".format(kwargs),
            4001: "Could not find {} {} in the database.".format(kwargs.get('country'), kwargs.get('postcode')),
            4002: "Could not find user {} in the database.".format(kwargs.get('username')),
        }

        logging.error("ScrapperError({}): {}, args: {}".format(code, self.code[code], kwargs), stack_info=True)
        super(DatabaseError, self).__init__(code)
