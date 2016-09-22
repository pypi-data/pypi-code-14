import logging


class BasketError(Exception):
    """
    Custom custom_error for Basket
    """

    def __init__(self, code, **kwargs):
        self.code = {
            2000: "{}".format(kwargs),
            2001: "{} not in the basket".format(kwargs.get('meal')),  # delete
            2002: "No meals with this index.",  # add delete
        }
        logging.error("ScrapperError({}): {}, args: {}".format(code, self.code[code], kwargs), stack_info=True)
        super(BasketError, self).__init__(code)