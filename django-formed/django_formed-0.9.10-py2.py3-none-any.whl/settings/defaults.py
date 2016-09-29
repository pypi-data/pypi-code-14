# coding=utf-8
from django import forms
from django.utils.translation import ugettext as _

from .. import form_fields

# Modules to search for field types:
FORMED_FORM_FIELD_MODULES = [
    form_fields,
    forms,
]

# Default prototype of a form field:
FORMED_FORM_FIELD = {
    # 'choices': False,
    'label': None,
    'help_text': '',
    'required': True,
    'widget_attributes': {
        'placeholder': True,
        # 'type': None,
        # 'class': None
    }
}

# A list of input types which are available in the editor
FORMED_FORM_FIELDS = {
    'text': {
        'type': 'CharField',
        'name': _('Text'),
        'component': {
            'name': 'text-input',
            'type': 'text'
        }
    },
    'textarea': {
        'type': 'TextareaField',
        'name': _('Textarea'),
        'component': {
            'name': 'textarea-input',
        },
    },
    'number': {
        'type': 'IntegerField',
        'name': _('Integer'),
        'component': {
            'name': 'text-input',
            'type': 'number',
        }
    },
    'email': {
        'type': 'EmailField',
        'name': _('E-mail'),
        'component': {
            'name': 'text-input',
            'type': 'email',
        }
    },
    'select': {
        'type': 'SelectField',
        'name': _('Select'),
        'choices': [],
        'widget_attributes': {
            'placeholder': False
        },
        'component': {
            'name': 'select-input',
        }
    },
    'radio': {
        'type': 'RadioField',
        'name': _('Radio buttons'),
        'choices': [],
        'widget_attributes': {
            'placeholder': False
        },
        'component': {
            'name': 'multiple-choice-input',
            'type': 'radio',
        }
    },
    'checkbox': {
        'type': 'BooleanField',
        'name': _('Single checkbox'),
        'widget_attributes': {
            'placeholder': False
        },
        'component': {
            'type': 'checkbox',
        }
    },
    'selectmultiple': {
        'type': 'MultipleChoiceField',
        'name': _('Multiple choice select'),
        'choices': [],
        'widget_attributes': {
            'placeholder': False
        },
        'component': {
            'name': 'select-input',
            'multiple': True
        }
    },
    'checkboxmultiple': {
        'type': 'MultipleChoiceCheckboxField',
        'name': _('Checkboxes'),
        'choices': [],
        'widget_attributes': {
            'placeholder': False
        },
        'component': {
            'name': 'multiple-choice-input',
            'type': 'checkbox',
        }
    },
    'url': {
        'type': 'URLField',
        'name': _('URL'),
        'component': {
            'name': 'text-input',
            'type': 'url'
        }
    },
    'tel': {
        'type': 'PhoneField',
        'name': _('Phone number'),
        'component': {
            'name': 'text-input',
            'type': 'tel'
        }
    },
    'date': {
        'type': 'DateField',
        'name': _('Date'),
        'component': {
            'name': 'text-input',
            'type': 'date'
        }
    },
    'datetime': {
        'type': 'DateTimeField',
        'name': _('Date & time'),
        'component': {
            'name': 'text-input',
            'type': 'datetime'
        }
    },

    # 'Person name' fields
    'first_name': {
        'type': 'FirstNameField',
        'name': _('First name'),
        'component': {
            'name': 'text-input',
            'type': 'text'
        }
    },
    'last_name_prefix': {
        'type': 'LastNamePrefixField',
        'name': _('Last name prefix'),
        'widget_attributes': {
            'class': {
                'small': _('Small')
            }
        },
        'component': {
            'name': 'text-input',
            'type': 'text'
        }
    },
    'last_name': {
        'type': 'LastNameField',
        'name': _('Last name'),
        'component': {
            'name': 'text-input',
            'type': 'text'
        }
    },

    # 'Form' fields
    'confirmation_email': {
        'type': 'ConfirmationEmailField',
        'name': _('Confirmation E-mail'),
        'component': {
            'name': 'text-input',
            'type': 'email',
        }
    }
}

FORMED_FORM_FIELD_CATEGORIES = {
    # Translators: The generic form field category
    _('Generic'): [
        'text',
        'textarea',
        'number',
        'email',
        'select',
        'radio',
        'checkbox',
        'url',
        'tel',
        'date',
        'datetime',
    ],
    # Translators: The 'multiple choice' form field category
    _('Multiple choice'): [
        'selectmultiple',
        'checkboxmultiple',
    ],
    # Translators: The person name form field category
    _('Name'): [
        'first_name',
        'last_name_prefix',
        'last_name',
    ],
    # Translators: The 'form' form field category
    _('Form'): [
        'confirmation_email'
    ]
}
