from flask_wtf import FlaskForm
from wtforms import validators,FileField, StringField, SubmitField
from wtforms.validators import DataRequired, InputRequired, Email

class UserData(FlaskForm):
    name = StringField('Name', [validators.DataRequired()])
    email = StringField('Email', [validators.DataRequired(), validators.Email()])
    fimg = FileField("Upload Fingerprint",validators=[InputRequired()])
    submit = SubmitField("Sign Up")