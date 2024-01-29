from flask_wtf import FlaskForm
from wtforms import validators, StringField, TextAreaField, SelectField, SubmitField
from wtforms.validators import DataRequired

class userData(FlaskForm):
    name = StringField('name', [validators.DataRequired()])
    email = StringField('email', [validators.DataRequired(), validators.Email()])
    submit = SubmitField("Sign Up")