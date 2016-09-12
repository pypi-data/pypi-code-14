"""Auto-generated file, do not edit by hand. CW metadata"""
from ..phonemetadata import NumberFormat, PhoneNumberDesc, PhoneMetadata

PHONE_METADATA_CW = PhoneMetadata(id='CW', country_code=None, international_prefix=None,
    general_desc=PhoneNumberDesc(national_number_pattern='[19]\\d{2}', possible_number_pattern='\\d{3}'),
    toll_free=PhoneNumberDesc(national_number_pattern='NA', possible_number_pattern='NA'),
    premium_rate=PhoneNumberDesc(national_number_pattern='NA', possible_number_pattern='NA'),
    emergency=PhoneNumberDesc(national_number_pattern='112|911', possible_number_pattern='\\d{3}', example_number='112'),
    short_code=PhoneNumberDesc(national_number_pattern='1(?:12|76)|911', possible_number_pattern='\\d{3}', example_number='112'),
    standard_rate=PhoneNumberDesc(national_number_pattern='NA', possible_number_pattern='NA'),
    carrier_specific=PhoneNumberDesc(national_number_pattern='176', possible_number_pattern='\\d{3}'),
    short_data=True)
