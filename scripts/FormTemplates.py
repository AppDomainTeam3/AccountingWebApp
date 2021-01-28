from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired

class UserCreationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    usertype = SelectField('User Type', choices=[('regular_user', 'Basic'), ('manager', 'Manager'), ('administrator', 'Admin')], validators=[DataRequired()])
    firstname = StringField('First Name', validators=[DataRequired()])
    lastname = StringField('Last Name', validators=[DataRequired()])
    avatarlink = StringField('Avatar Link')
    submit = SubmitField('Submit')

class UserUpdateUsertypeForm(FlaskForm):
    usertype = SelectField('User Type', choices=[('regular_user', 'Basic'), ('manager', 'Manager'), ('administrator', 'Admin')], validators=[DataRequired()])
    submit = SubmitField('Submit')