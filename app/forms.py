# /app/forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, HiddenField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError

# We have removed the line: from .models import User

class RegistrationForm(FlaskForm):
    # We've added first_name and last_name to the form itself
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password', message='Passwords must match')])
    role = HiddenField('Role', default='patient') # Set a default
    submit = SubmitField('Create Account')

    # We have removed the validate_email function because auth.py already handles it.