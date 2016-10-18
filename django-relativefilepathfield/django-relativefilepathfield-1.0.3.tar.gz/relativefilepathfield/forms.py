from __future__ import absolute_import
import os
from django.forms.fields import FilePathField

class RelativeFilePathField(FilePathField):
    def __init__(self, path, *args, **kwargs):
        super(RelativeFilePathField, self).__init__(path, *args, **kwargs)
        
        if not self.required:
            choices = [self.choices[0]]  # don't handle default empty option
            start_from = 1
        else:
            choices = []
            start_from = 0

        for abs_path, name in self.choices[start_from:]:
            choices.append((os.path.relpath(abs_path, path), name))
        self.choices = choices
