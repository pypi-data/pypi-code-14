import argparse


def get_parser():
    parser = argparse.ArgumentParser(description="Command line interface for pizza.be.")
    parser.add_argument('country', action="store", help="Your country (BE, EN, ...).", default=None,
                        metavar='country')
    parser.add_argument('postcode', action="store", help="""Your postcode (1000, "W1J 0", ...).""",
                        default=None, metavar='postcode')
    parser.add_argument('-i', action="store_true", default=False, dest="interactive",
                        help="Deactivate the interactive mode.")
    parser.add_argument('--checkout', action="store", default=False, const=True, dest="checkout", nargs="?",
                        help="Order your basket.", metavar="remarks", type=str)
    parser.add_argument('--confirm', action="store_true", default=False, dest="confirm",
                        help="Confirm the checkout.")
    parser.add_argument('--postcode', action="store", nargs=2, default=False, dest='new_postcode',
                        help="Use this to change current postcode.", metavar=('country', 'postcode'))
    parser.add_argument('--debug', action="store", default=False, const=True, nargs="?", dest="log_lvl",
                        metavar="level", help="Display debugging message and save to filename", type=int)

    group_search = parser.add_argument_group('Search')
    group_search.add_argument('-m', action="store", help="Search a meal (default is all).",
                              dest="search_meal", nargs='*', default=False, metavar='meal')
    group_search.add_argument('-c', action="store",
                              help="Search for a category(default is all).",
                              dest="search_cat", nargs='*', default=False, metavar="category")
    group_search.add_argument('-r', action="store",
                              help="Search for a restaurant (default is all).",
                              dest="search_rest", nargs='*', default=False, metavar="restaurant")
    group_search.add_argument('-v', action="count", default=1, dest='verbose',
                              help="Level of information to display. Use only with -r. 2 levels available.")
    group_search.add_argument('--time', action='store_true', default=False, dest="time",
                              help="Select only currently open restaurant")

    group_db = parser.add_argument_group('Database')
    group_db_me = group_db.add_mutually_exclusive_group()
    group_db_me.add_argument('--db-list', action="store", default=False, const="all", dest="db_list",
                             help='List all postcodes in the database.', nargs="?", metavar="country")
    group_db_me.add_argument('--db-del', action="store", default=False, dest="db_del", nargs=2,
                             help="Delete the postcode from the database.", metavar=('country', 'postcode'))
    group_db_me.add_argument('--db-make', action='store_true', default=False, dest="db_make",
                             help="Make the database for this postcode.")
    group_db_me.add_argument('--db-update', action='store', nargs='?', default=False, const=True,
                             dest="db_update", type=int, help="Update the database for this postcode.",
                             metavar="days")
    group_db_me.add_argument('--db-consolidate', action='store_true', default=False,
                             dest="db_consolidate", help="Consolidate the database for this postcode.", )

    group_basket = parser.add_argument_group('Basket')
    group_basket.add_argument('-a', action="store", default=False, dest="ba_add", nargs="+", type=int,
                              help="Index of item(s) to add to basket.", metavar='index')
    group_basket.add_argument('-d', action="store", default=False, dest="ba_del", nargs="+", type=int,
                              help="Index of item(s) to delete from the basket.", metavar="index")
    group_basket.add_argument('-l', action="store_true", default=False, dest="ba_list",
                              help="List all the item(s) in the basket.")
    group_basket.add_argument('--clear-basket', action="store_true", default=False, dest="ba_clear",
                              help="Clear all the item(s) in the basket")

    group_user = parser.add_argument_group('User')
    group_user.add_argument('-u', action="store", default=False, dest='u_name', metavar="user", nargs="?",
                            const=True,
                            help="User to use for checkout.")
    group_user.add_argument('--u-create', action="store", default=False, dest="u_new", metavar="user",
                            help="Create or modify an user.")
    group_user.add_argument('--u-list', action="store_true", default=False, dest="u_list",
                            help="List the users in the database.")
    group_user.add_argument('--u-del', action="store", default=False, dest="u_del", metavar="user", nargs="?",
                            const=True, help="Delete the user.")

    return parser

