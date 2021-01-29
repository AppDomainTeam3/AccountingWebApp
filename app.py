from flask import Flask, render_template, request, redirect, url_for,session,flash,g
from flask_login import UserMixin
from flask_mail import Mail, Message
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
app.config.from_object("config.DevelopementConfig")

app_url = 'https://appdomainteam3.herokuapp.com'
api_url = 'https://appdomainteam3api.herokuapp.com'

mail = Mail(app)


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
        self.usertype = usertype
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
                          usertype = dataDict['usertype'],              ######This needs to be updated every time session values are changed
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

@app.route('/mail')
def test_mail():
    if g.user == None:
        return render_template('login.html')
    if g.user.usertype == 'administrator':
        msg = Message('Hello, you have clicked on the link', recipients=['netim11829@alicdh.com'])
        msg.body = f"Hello {g.user.username}, you are the choosen one"
        mail.send(msg)   
        return """<h1>message has been sent</h1>
            <a href='/'> Back To Main Page</a>"""   
    else:
        return '''<h1>You do not have access</h1>
                  <a href='/'> Back To Main Page</a>'''  

@app.route('/sign_out')
def sign_out():
    if g.user == None:
        return render_template('login.html')
    session.pop('user_id')
    return redirect(url_for('login'))
#index page ~ welcome if signed in / not signed in notification if not
@app.route("/")
def index():
    if g.user == None:
        return render_template('login.html')
    return render_template('index.html', title='home', user=g.user)

@app.route("/users")
def DisplayAllUsers():
    if g.user == None:
        return render_template('login.html')
    response = requests.get(f"{api_url}/users")
    userList = []
    for user in response.json():
        userList.append(user)
    return render_template('users.html', title='All Users', userdata=userList, user=g.user, url=app_url)

@app.route("/users/<int:user_id>")
def UserProfile(user_id):
    if g.user == None:
        return render_template('login.html')
    canEdit = False
    print(f"g.user.usertype={g.user.usertype}")
    if g.user.usertype == 'administrator' or g.user.id == user_id:
        canEdit = True
    response = requests.get(f"{api_url}/users/{user_id}").json()
    username = response[0]['username']
    usertype = response[0]['usertype']
    firstname = response[0]['firstname']
    lastname = response[0]['lastname']
    avatarlink = response[0]['avatarlink']
    return render_template('profile.html', title=username, usertype=usertype, id=user_id, firstname=firstname, lastname=lastname, avatarlink=avatarlink, url=app_url, canEdit=canEdit)

@app.route("/users/<int:user_id>/edit", methods=['GET', 'POST'])
def EditUserProfile(user_id):
    if g.user == None:
        return render_template('login.html')
    response = requests.get(f"{api_url}/users/{user_id}").json()
    username = response[0]['username']
    usertype = response[0]['usertype']
    firstname = response[0]['firstname']
    lastname = response[0]['lastname']
    avatarlink = response[0]['avatarlink']
    form = UserCreationForm()
    return render_template('edit_user.html', title=username, form=form, id=user_id, username=username, usertype=usertype, firstname=firstname, lastname=lastname, avatarlink=avatarlink, url=app_url, api=api_url, user=g.user)

@app.route("/add-user", methods=['GET', 'POST'])
def CreateUser():
    if g.user == None:
        return render_template('login.html')
    form = UserCreationForm()
    return render_template('create_user.html', title='Create User', form=form, api=api_url, user=g.user)

if __name__ == "__main__":
    app.run(debug=False)
