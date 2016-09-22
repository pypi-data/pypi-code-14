import logging


class UserError(Exception):
    """
    Custom custom_error for User
    """
    def __init__(self, code, **kwargs):
        self.code = {
            3000: "{}".format(kwargs),
            3001: "You must load an user before deleting it"
        }

        logging.error("ScrapperError({}): {}, args: {}".format(code, self.code[code], kwargs), stack_info=True)
        super(UserError, self).__init__(code)
