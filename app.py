from flask import Flask, render_template, request, redirect, url_for,session,flash,g
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import requests
from scripts.User import User
from scripts.FormTemplates import UserCreationForm, UserUpdateUsertypeForm
from scripts.LoginUser import UserLoginForm
import re
import json
import flask_login
import flask


app = Flask(__name__, static_folder='static')
app.config['SECRET_KEY'] = 'secret_key'

app_url = 'https://appdomainteam3.herokuapp.com'
api_url = 'https://appdomainteam3api.herokuapp.com'

response = requests.get(f"{api_url}/users")

class User(UserMixin):
    def __init__(self, id, username, usertype, firstname, lastname, avatarlink, password):
        self.id = id
        self.username = username
        self.usertype = usertype
        self.firstname = firstname
        self.lastname = lastname
        self.avatarlink = avatarlink
        self.password = password
    def __repr__(self): 
        return f'<User: {self.username}>'

dataList = response.json()
users = []
#adds id, username, and hashed_password to list for user tracking and authentication
def update_user_list():
    for x in range(len(dataList)):
        dataDict = dataList[x]
        users.append(User(id=dataDict['id'], 
                          username = dataDict['username'],
                          usertype = dataDict['usertype'],
                          firstname = dataDict['firstname'],
                          lastname = dataDict['lastname'],
                          avatarlink = dataDict['avatarlink'],
                          password = dataDict['hashed_password']))
update_user_list()

#checks if user is logged in
@app.before_request
def before_request():
    g.user = None
    if 'user_id' in session:
        user = [x for x in users if x.id == session['user_id']][0]
        g.user = user

#starts the session/checks for auth
@app.route('/login/', methods=['GET', 'POST'])
def login():
    form = UserLoginForm()
    if request.method == 'POST':
        session.pop('user_id',None)
        username = request.form['username']
        password = request.form['password']
        try:
            user = [x for x in users if x.username == username][0]
        except Exception:
            return redirect(url_for('login'))
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            return redirect(url_for('index'))
        return redirect(url_for('login'))
    return render_template('login.html',title = 'Login', url=app_url)

#random page ~ home
@app.route('/home')
def home():
    if not g.user:
        return '<h1> You are not logged in </h1>'
    else:
        return f'''<h1> Welcome: {g.user.username} </h1>
                   <a href="{url_for('sign_out')}"> Sign Out </a>'''

@app.route('/sign_out')
def sign_out():
    session.pop('user_id')
    return redirect(url_for('login'))
#index page ~ welcome if signed in / not signed in notification if not
@app.route("/")
def index():
    if 'user_id' in session:
        return render_template('index.html',title='home')
    return 'You are not signed in!'

@app.route("/users")
def DisplayAllUsers():
    response = requests.get(f"{api_url}/users")
    userList = []
    for user in response.json():
        userList.append(user)
    return render_template('users.html', title='All Users', userdata=userList)

@app.route("/users/<int:user_id>")
def UserProfile(user_id):
    response = requests.get(f"{api_url}/users/{user_id}").json()
    username = response[0]['username']
    usertype = response[0]['usertype']
    firstname = response[0]['firstname']
    lastname = response[0]['lastname']
    avatarlink = response[0]['avatarlink']
    return render_template('profile.html', title=username, usertype=usertype, id=user_id, firstname=firstname, lastname=lastname, avatarlink=avatarlink, url=app_url, user=g.user)

@app.route("/users/<int:user_id>/edit")
def EditUserProfile(user_id):
    response = requests.get(f"{api_url}/users/{user_id}").json()
    username = response[0]['username']
    usertype = response[0]['usertype']
    firstname = response[0]['firstname']
    lastname = response[0]['lastname']
    avatarlink = response[0]['avatarlink']
    form = UserCreationForm()
    return render_template('edit_user.html', title=username, form=form, id=user_id, username=username, usertype=usertype, firstname=firstname, lastname=lastname, avatarlink=avatarlink, url=app_url, user=g.user)

@app.route("/add-user", methods=['GET', 'POST'])
def CreateUser():
    form = UserCreationForm()
    return render_template('create_user.html', title='Create User', form=form, api=api_url)

if __name__ == "__main__":
    app.run(debug=False)
