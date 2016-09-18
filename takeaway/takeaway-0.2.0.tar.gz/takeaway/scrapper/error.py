import logging


class ScrapperError(Exception):
    """
    Custom custom_error for Scrapper
    """

    def __init__(self, code, **kwargs):
        self.code = {
            1000: "{}".format(kwargs),
            1001: "Impossible to retrieve the url for postcode {}. {}".format(
                kwargs.get('postcode'), kwargs.get('website_msg')),
            1002: "Improper response from {}.".format(kwargs.get('url')),
            1003: "No district provided. Available district in {} : {}".format(kwargs.get("city"),
                                                                               kwargs.get('district')),  #Vietnam
            1004: "{} is not a recognized city.".format(kwargs.get("city")),

            1101: "Impossible to check out with items from multiple restaurants.",
            1102: "No response from server during checkout, url: {}.".format(kwargs.get('url')),
            1103: "Impossible to check out with an empty basket.",
            1104: "Impossible to find items check online for restaurant {}".format(kwargs.get("restaurant_name")),
            1105: "Error during checkout: {}".format(kwargs.get('website_msg')),

            1201: "Impossible to find any restaurant for {}.".format(kwargs.get('postcode')),  # 1002
            1202: "Impossible to find meals for {}.".format(kwargs.get('restaurant_name')),  # 1005
            1203: "Impossible to find information page for {}.".format(kwargs.get('restaurant_name')),  # 1007

            1901: "Could not connect to {}.\nCheck your internet connection.".format(kwargs.get('url')),
            1902: "Could not connect to {}.\nCheck your internet connection.".format(kwargs.get('url')),
            1903: "Could not connect to {}.\nCheck your internet connection.".format(kwargs.get('url')),

            1999: "Country {} not yet implemented.".format(kwargs.get('country')),
        }
        logging.error("ScrapperError({}): {}, args: {}".format(code, self.code[code], kwargs), stack_info=True)
        super(ScrapperError, self).__init__(code)
