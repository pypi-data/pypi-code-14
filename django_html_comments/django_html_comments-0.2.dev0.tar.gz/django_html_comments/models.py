from mezzanine.generic.models import ThreadedComment
from sanitize import sanitize

from django.contrib.comments.signals import comment_was_posted
from django.utils.module_loading import import_by_path
from django.conf import settings

comment_class = import_by_path(settings.COMMENT_CLASS)

def comment_sanitizer(sender, comment, request, **kwargs):
    comment.comment = sanitize(comment.comment)
    comment.save()
# comment_will_be_posted would be better, but mezzanine does not 
# seem to have that hooked up

# COMMENT_FILTER in your settings.py needs to be set to this function
# and you need to turn off autoescapting around the output of the 
# comment in your templates
def comment_filter(comment_text):
    return comment_text
comment_was_posted.connect(comment_sanitizer, sender=ThreadedComment)
