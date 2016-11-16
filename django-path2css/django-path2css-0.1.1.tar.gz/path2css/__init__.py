# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from functools import partial
from django.utils.encoding import force_text
from django.utils.functional import lazy
from django.utils.safestring import mark_safe
try:
    from collections import UserList
except ImportError:
    from UserList import UserList
from django.utils.six import python_2_unicode_compatible

__version_info__ = '0.1.1'
__version__ = '0.1.1'
version = '0.1.1'
VERSION = '0.1.1'
__all__ = ['get_version', 'generate_css_names_from_string',
           'request_path_to_css_names']

def get_version():
    return version  # pragma: no cover


def generate_css_names_from_string(item, split_on, prefix='', suffix='', midpoint=''):
    newpath = tuple(part for part in item.strip(split_on).split(split_on)
                    if part)
    # If the thing is empty, just return an empty tuple
    if not newpath:
        return ()
    newpath_length = len(newpath) + 1
    variations = (newpath[0:l] for l in range(1, newpath_length))
    # If there's a prefix and it doesn't end with a sensible separator (given
    # the valid names of CSS identifiers), add midpoint.
    if prefix and not prefix.endswith(('-', '_')):
        prefix = '%s%s' % (prefix, midpoint)
    # same as prefix, but start, rather than end
    if suffix and not suffix.startswith(('-', '_')):
        suffix = '%s%s' % (midpoint, suffix,)
    finalised_variations = (
        '%s%s%s' % (prefix, midpoint.join(variation), suffix)
        for variation in variations
    )
    return finalised_variations


request_path_to_css_names = partial(generate_css_names_from_string,
                                    split_on='/')



@python_2_unicode_compatible
class Output(UserList):
    def __str__(self):
        """
        Used when doing something like:
        {% path2css ... as OUTVAR %}
        {{ OUTVAR }}
        """
        return mark_safe(" ".join(force_text(x) for x in self.data))

    def __html__(self):
        """
        Used in {% path2css x y %} is used directly
        """
        return force_text(self)

    def __getitem__(self, item):
        """
        Used when doing something like:
        {% path2css ... as OUTVAR %}
        {% for x in OUTVAR %}{{ x }}{% endfor %}
        """
        return mark_safe(super(Output, self).__getitem__(item))



def context_processor(request):
    return {
        "PATH2CSS": Output(request_path_to_css_names(request.path, midpoint='-')),
    }
