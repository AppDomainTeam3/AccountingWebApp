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

class AccountCreationForm(FlaskForm):
    accountHolderUsername = StringField('Username', validators=[DataRequired('field is required.')])
    accountName = StringField('Account Name', validators=[DataRequired('field is required.')])
    accountDesc = StringField('Description', validators=[DataRequired('field is required.')])
    normalSide = StringField('Normal Side', validators=[DataRequired('field is required.')])
    category = SelectField('Category', choices=[('Checking', 'Checking'), ('Savings', 'Savings')], validators=[DataRequired('field is required.')])
    submit = SubmitField('Submit')

class AccountEditForm(FlaskForm):
    accountName = StringField('Account Name', validators=[DataRequired('field is required.')])
    accountDesc = StringField('Description', validators=[DataRequired('field is required.')])
    normalSide = StringField('Normal Side', validators=[DataRequired('field is required.')])
    category = SelectField('Category', choices=[('Checking', 'Checking'), ('Savings', 'Savings')], validators=[DataRequired('field is required.')])
    subcategory = StringField('Subcategory', validators=[DataRequired('field is required.')])
    accountOrder = StringField('Account Order', validators=[DataRequired('field is required.')])
    comment = StringField('Comment', validators=[DataRequired('field is required.')])
    submit = SubmitField('Submit')

class JournalEntryForm(FlaskForm):
    AccountNumber = StringField('Account Number', validators=[DataRequired('field is required.')])
    Debits = StringField('Debits (separated by commas)', validators=[DataRequired('field is required.')])
    Credits = StringField('Credits (separated by commas)', validators=[DataRequired('field is required.')])
    submit = SubmitField('Submit')

class UserPasswordChangeForm(FlaskForm):
    currentPassword = StringField('Current Password', validators=[DataRequired('field is required.')])
    newPassword = StringField('New Password', validators=[DataRequired('field is required.')])
    newPasswordVerification = StringField('Verify New Password', validators=[DataRequired('field is required.')])
    submit = SubmitField('Submit')

class AdminEmailForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired('field is required.')])
    subject = StringField('Subject', validators=[DataRequired('field is required.')])
    message = TextAreaField('Message', validators=[DataRequired('field is required.')])
    submit = SubmitField('Send Message')

class ForgotPasswordForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired('field is required.')])
    email = StringField('Email', validators=[DataRequired('field is required.')])
    submit = SubmitField('Submit')