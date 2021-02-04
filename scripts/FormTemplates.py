from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.fields.simple import TextAreaField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired

class UserCreationForm(FlaskForm):
    deactivate = DateField('Deactivate User until', format='%Y-%m-%d')
    username = StringField('Username', validators=[DataRequired('field is required.')])
    email = StringField('Email', validators=[DataRequired('field is required.')])
    usertype = SelectField('User Type', choices=[('regular_user', 'Basic'), ('manager', 'Manager'), ('administrator', 'Admin')], validators=[DataRequired('field is required.')])
    firstname = StringField('First Name', validators=[DataRequired('field is required.')])
    lastname = StringField('Last Name', validators=[DataRequired('field is required.')])
    avatarlink = StringField('Avatar Link')
    password = StringField('Password', validators=[DataRequired('field is required.')])
    submit = SubmitField('Submit')

class AdminEmailForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired('field is required.')])
    subject = StringField('Subject', validators=[DataRequired('field is required.')])
    message = TextAreaField('Message', validators=[DataRequired('field is required.')])
    submit = SubmitField('Send Message')