from flask_wtf import FlaskForm
from wtforms import validators, StringField, TextAreaField, SelectField, SubmitField
from wtforms.validators import DataRequired

class UserData(FlaskForm):
    name = StringField('Name', [validators.DataRequired()])
    email = StringField('Email', [validators.DataRequired(), validators.Email()])
    submit = SubmitField("Sign Up")