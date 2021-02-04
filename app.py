from flask import Flask, render_template, request, redirect, url_for, session, g
from flask_mail import Mail, Message
from werkzeug.security import check_password_hash, generate_password_hash
import requests
from scripts.User import User
from scripts.FormTemplates import UserCreationForm
from scripts.FormTemplates import UserPasswordChangeForm
from scripts.FormTemplates import AdminEmailForm
from scripts.LoginUser import UserLoginForm

app = Flask(__name__, static_folder='static')
app.config.from_object("config.DevelopementConfig")

app_url = 'http://127.0.0.1:5000/'
api_url = 'https://appdomainteam3api.herokuapp.com'

mail = Mail(app)

userList = []
users = []
#adds userdata to list for user tracking and authentication
def update_user_list():
    response = requests.get(f"{api_url}/users")
    userList = response.json()
    users.clear()
    for x in range(len(userList)):
        userDict = userList[x]
        users.append(User(id=userDict['id'], 
                          username = userDict['username'],
                          email = userDict['email'],
                          usertype = userDict['usertype'],
                          firstname = userDict['firstname'],
                          lastname = userDict['lastname'],
                          avatarlink = userDict['avatarlink'],
                          password = userDict['hashed_password'],
                          isActive = userDict['is_active'],
                          isPasswordExpired = userDict['is_password_expired'],
                          reactivateUserDate = userDict['reactivate_user_date']))
update_user_list()

def updataUserSessionData():
    update_user_list()
    for userIndex in range(len(users)):
        if g.user.id == users[userIndex].id:
            g.user = users[userIndex]

#checks if user is logged in
@app.before_request
def before_request():
    g.user = None
    if 'user_id' in session:
        user = [x for x in users if x.id == session['user_id']][0]
        g.user = user

#starts the session/checks for auth
@app.route("/login/", methods=['GET', 'POST'])
def login():
    update_user_list()
    if request.method == 'POST':
        session.pop('user_id',None)
        username = request.form['username'].lower()
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

@app.route("/user-mail", methods=['GET', 'POST'])
def userMail():
    update_user_list()
    form = AdminEmailForm()
    if g.user == None:
        return render_template('login.html')
    elif g.user.usertype == 'administrator':
        #username = 'cheese'
        return render_template('userMail.html',user=g.user,title = 'Admin Email', form=form)
    else:
        return """ <h1>You don't have access to this page</h1>
                   <a href = "/">Return Home</a> """

@app.route("/send_message", methods=['GET','POST'])
def send_message():
    if request.method == "POST":
        username = request.form['username']
        subject = request.form['subject']
        msg = request.form['message']
        eList = []
        if username.lower() == 'all':
            for userIndex in range(len(users)):
                eList.append(users[userIndex].email)
        
        for userIndex in range(len(users)):
            if users[userIndex].username == username:
                username = users[userIndex].email 
                eList.append(username)
        try:
            message = Message(subject = subject, recipients = eList)
            message.body = msg
            mail.send(message)
            return """<h1>Message has been sent</h1>
                  <a href = "/">Return home</a>
                  <a href = "/user-mail">Send Another Message</a>"""
        except Exception:
            return """<h1>user does not exist</h1>
                      <a href = "/user-mail">Send Another Message</a>"""

@app.route("/sign_out/")
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

@app.route("/users/")
def DisplayAllUsers():
    if g.user == None:
        return render_template('login.html')
    update_user_list()
    return render_template('users.html', title='All Users', userdata=users, user=g.user, url=app_url)

@app.route("/users/expired_passwords/")
def DisplayAllUsersWithExpiredPasswords():
    if g.user == None:
        return render_template('login.html')
    update_user_list()
    expiredUsers = []
    for user_ in users:
        if users[user_.id].isPasswordExpired == 'True':
            expiredUsers.append(user_)
    return render_template('expired_passwords.html', title='Expired Passwords Report', userdata=expiredUsers, user=g.user, url=app_url)

@app.route("/users/<int:user_id>/")
def UserProfile(user_id):
    if g.user == None:
        return render_template('login.html')
    updataUserSessionData()
    response = requests.get(f"{api_url}/users/{user_id}")
    if response.status_code == 404:
        return render_template('error.html', user=g.user)
    user = users[user_id]
    canEdit = False
    if g.user.usertype == 'administrator' or g.user.usertype == 'manager' or g.user.id == user_id:
        canEdit = True
    return render_template('profile.html', user=g.user, title = 'User Profile Page',userData=users[user_id], url=app_url, canEdit=canEdit)

@app.route("/users/<int:user_id>/edit/", methods=['GET', 'POST'])
def EditUserProfile(user_id):
    if g.user == None:
        return render_template('login.html')
    response = requests.get(f"{api_url}/users/{user_id}")
    if response.status_code == 404:
        return render_template('error.html', user=g.user)
    update_user_list()
    user = users[user_id]
    form = UserCreationForm()
    return render_template('edit_user.html', title='edit ' + user.username, form=form, user=user, url=app_url, api=api_url, sessionUser=g.user)

@app.route("/users/<int:user_id>/update_password", methods=['GET', 'POST'])
def UpdatePassword(user_id):
    if g.user == None:
        return render_template('login.html')
    response = requests.get(f"{api_url}/users/{user_id}")
    if response.status_code == 404:
        return render_template('error.html', user=g.user)
    update_user_list()
    user = users[user_id]
    form = UserPasswordChangeForm()
    return render_template('update_password.html', title=f"Update Password, {user}" + user.username, form=form, user=user, url=app_url, api=api_url, sessionUser=g.user)

@app.route("/add-user/", methods=['GET', 'POST'])
def CreateUser():
    if g.user == None:
        return render_template('login.html')
    form = UserCreationForm()
    return render_template('create_user.html', title='Create User', form=form, api=api_url, user=g.user)

@app.route("/new_account/", methods=['GET', 'POST'])
def NewAccount():
    form = UserCreationForm()
    return render_template('new_account.html', title='New Account', form=form, api=api_url)

if __name__ == "__main__":
    app.run(debug=False)
