import traceback
from datetime import timedelta
from dateutil import parser

from django.utils import timezone

from rest_framework.fields import DateTimeField


TIME_CORRECTION_THRESHOLD = 5 * 60 # threshold offset difference in seconds


class TrueDateTimeField(DateTimeField):
    '''
    Custom DateTimeField for serializers that offsets value
    to ensure bad device time is not saved
    '''

    def run_validation(self, data):
        validated_data = super(TrueDateTimeField, self).run_validation(data)
        return offset_time_field(validated_data, self)


def offset_time_field(validated_data, field_instance):
    '''
    Helper method to offset time value for custom DateTimeField
    '''
    try:
        if 'request' in field_instance.context:
            request = field_instance.context.get('request')
            device_time_string = request.META.get('HTTP_DEVICE_TIME')
            current_server_time = timezone.now()

            if device_time_string:
                device_time = parser.parse(device_time_string)
                device_time_offset = (current_server_time - device_time).total_seconds()

                if abs(device_time_offset) >= TIME_CORRECTION_THRESHOLD:
                    validated_data = validated_data + timedelta(seconds=device_time_offset)

    except Exception, excp:
        # Blanket exception handler
        print 'Time offset field error:', str(excp)
        print traceback.format_exc()

    return validated_data
