from flask_wtf import Form
from wtforms import IntegerField, StringField
from wtforms.validators import DataRequired


class PersonForm(Form):
    name = StringField('name', validators=[DataRequired()])
    age = IntegerField('age')
