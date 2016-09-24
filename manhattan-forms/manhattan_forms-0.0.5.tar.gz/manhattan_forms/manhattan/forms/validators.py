from wtforms.validators import Optional, Required

__all__ = ['RequiredIf']


class RequiredIf(object):
    """
    The `RequiredIf` validator allows the parent field to be flagged as required
    only if certain conditions are met.

    The set of conditions are specified using keywords when initializing the
    validator, for example:

        send_by = SelectField(
            'Send by',
            choices=[('sms', 'SMS'), ('email', 'Email')]
            )
        email = StringField('Email', [RequiredIf(send_by='email')])
        mobile_no = StringField('Mobile no.', [RequiredIf(send_by='sms')])
    """

    def __init__(self, **conditions):
        self.conditions = conditions

    def __call__(self, form, field):
        for name, value in self.conditions.items():

            assert name in form._fields, \
                'Condition field does not present in form.'

            # Check if the condition is met
            if form._fields.get(name).data == value:
                return Required()(form, field)

        Optional()(form, field)