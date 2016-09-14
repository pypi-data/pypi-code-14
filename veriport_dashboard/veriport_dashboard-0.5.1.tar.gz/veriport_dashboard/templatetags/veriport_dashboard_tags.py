from datetime import timedelta

from django import template

register = template.Library()


@register.filter
def get_duration_field(report, duration):
    """
    Returns the value of the field duration of the report given
    """
    seconds = report.durations.get(duration, 0)
    average = timedelta(seconds=seconds)
    return "%s.%s" % (average.days, average.seconds)
