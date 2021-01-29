from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired

class UserCreationForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired('field is required.')])
    email = StringField('Email', validators=[InputRequired('field is required.')])
    usertype = SelectField('User Type', choices=[('regular_user', 'Basic'), ('manager', 'Manager'), ('administrator', 'Admin')], validators=[InputRequired('field is required.')])
    firstname = StringField('First Name', validators=[InputRequired('field is required.')])
    lastname = StringField('Last Name', validators=[InputRequired('field is required.')])
    avatarlink = StringField('Avatar Link')
    submit = SubmitField('Submit')