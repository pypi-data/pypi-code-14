import typing
from collections import OrderedDict

import flask_wtf
from capture0.forms import countries
from capture0_data.online_handles import IndexCompany
from capture0_data.online_messages import get_messages
from wtforms import RadioField
from wtforms import SelectField
from wtforms import StringField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Email


class BaseHomeForm(flask_wtf.Form):
    messages = get_messages()
    name = StringField('name', description=messages["question_name"], validators=[DataRequired()])
    country = SelectField('country', description=messages["question_country"], choices=countries.COUNTRIES)
    name = EmailField('name', description=messages["question_email"], validators=[Email()])


def form_empathy_question(company_name):
    return "How empathic is <b>%s</b>?" % company_name


def home_form_instance_factory(companies: typing.List[IndexCompany]) -> BaseHomeForm:
    messages = get_messages()

    EMPATHY_CHOICES = [
        (2, messages["option_2"]),
        (1, messages["option_1"]),
        (0, messages["option_0"]),
        (-1, messages["option_-1"]),
        (-2, messages["option_-2"]),
        (None, messages["option_unknown"]),
    ]

    new_form_elements = OrderedDict({
                                        c.company: RadioField(c.company,
                                                              description=form_empathy_question(c.display_name),
                                                              validators=[DataRequired()],
                                                              choices=EMPATHY_CHOICES)
                                        for c in companies})

    new_form = type("frm0", (BaseHomeForm,), new_form_elements)

    new_form.most_empathic = StringField('most_empathic',
                                         description=messages["question_most_empathic"],
                                         validators=[DataRequired()])

    new_form.least_empathic = StringField('least_empathic',
                                          description=messages["question_least_empathic"],
                                          validators=[DataRequired()])

    new_form.question_missing = StringField('question_missing',
                                            description=messages["question_missing"],
                                            validators=[DataRequired()])



    form_instance = new_form()
    return form_instance
