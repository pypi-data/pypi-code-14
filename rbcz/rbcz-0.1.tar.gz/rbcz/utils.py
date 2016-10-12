from decimal import *

money_regex = r"-?[0-9 ]+\.\d\d"

def to_decimal(s):
    return Decimal(s.replace(" ",""))
