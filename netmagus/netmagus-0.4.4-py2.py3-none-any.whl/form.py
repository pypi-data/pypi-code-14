# coding=utf-8
"""
NetMagus Python Library
Copyright (C) 2016 Intelligent Visbility, Inc. - Richard Collins <richardc@intelligentvisibility.com>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
from __future__ import absolute_import, unicode_literals, print_function, division

import json


class FormComponent(object):
    """
    Parent class for all valid types of form elements.  This should be subclassed for each new type of component
    created in NetMagus forms.  This class is not intended for direct instantiation.

    The NetMagus app may choose to use or ignore values depending upon type of control.  The base class is set to
    provide all current attributes with a default value.  Sub-classes should over-ride defaults as necessary for each
    control type implemented.

    :param component:  Valid form component string value
    :param editable: Boolean to control if form component may be edited by user
    :param label: String rendered to left of the form component
    :param description: String rendered below the form component
    :param placeholder: String rendered inside the component before user inputs their own data
    :param options: List containing choices for checkboxes, dropdowns, etc.
    :param required: Boolean that controls if user must provide a value for this form component
    :param validation: String passed to NetMagus for certain component types to enforce user input validation
    validation examples: number=[number], email=[email], url=[url],  none=/.*/
    """

    def __init__(self, component='', editable=True, label='', description='', placeholder='', options=None,
                 required=False, validation='/.*/', value=None):
        # common attrs for all components
        self.component = component
        self.editable = editable
        self.index = 0
        self.label = label
        self.description = description
        self.required = required
        if options is None:
            self.options = []
        else:
            self.options = options
        self.placeholder = placeholder
        self.validation = validation
        self.value = value

    def __repr__(self):
        return json.dumps(self, sort_keys=True, default=lambda o: o.__dict__)

    @property
    def as_dict(self):
        return self.__dict__


class TextArea(FormComponent):
    def __init__(self, editable=True, label='', description='', placeholder='', required=False):
        super(TextArea, self).__init__(component='textArea', editable=editable, label=label,
                                       description=description, required=required, placeholder=placeholder)


class TextInput(FormComponent):
    def __init__(self, editable=True, label='', description='', placeholder='', required=False,
                 validation='/.*/'):
        super(TextInput, self).__init__(component='textInput', editable=editable, label=label,
                                        description=description, required=required, placeholder=placeholder,
                                        validation=validation)


class CheckBox(FormComponent):
    def __init__(self, editable=True, label='', description='', options=None, required=False, value=None):
        super(CheckBox, self).__init__(component='checkbox', editable=editable, label=label,
                                       description=description, options=options, required=required,
                                       value=value)


class RadioButton(FormComponent):
    def __init__(self, editable=True, label='', description='', options=None, required=False, value=None):
        super(RadioButton, self).__init__(component='radio', editable=editable, label=label,
                                          description=description, options=options, value=value, required=required)


class DropDownMenu(FormComponent):
    def __init__(self, editable=True, label='', description='', options=None, value=None, required=False):
        super(DropDownMenu, self).__init__(component='select', editable=editable, label=label,
                                           description=description, options=options, value=value, required=required)


class PasswordInput(FormComponent):
    def __init__(self, editable=True, label='', description='', placeholder='', required=False):
        super(PasswordInput, self).__init__(component='password', editable=editable, label=label,
                                            description=description, required=required, placeholder=placeholder)
