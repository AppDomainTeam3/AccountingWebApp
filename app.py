from flask import Flask, render_template, request, redirect, url_for, session, g, flash
from flask_mail import Mail, Message
from datetime import datetime, timedelta
from werkzeug.security import check_password_hash
import requests

from scripts.Helper import populateAccountsListByUserID, populateAccountByAccountNumber, updateUserList
from scripts.FormTemplates import AccountCreationForm, UserCreationForm, UserPasswordChangeForm, UserPasswordChangeForm
from scripts.FormTemplates import AdminEmailForm, ForgotPasswordForm, AccountEditForm

app = Flask(__name__, static_folder='static')
app.config.from_object("config.DevelopementConfig")

app_url = 'https://appdomainteam3.herokuapp.com'
api_url = 'https://appdomainteam3api.herokuapp.com'

mail = Mail(app)

#adds userdata to list for user tracking and authentication
users = []
users = updateUserList(users, api_url)

def passwordExEmail(user):
    
    expirDateDateTime = datetime.strptime(user.passwordExpirationDate, '%Y-%m-%d')
    
    curTimePlusThreeDay = datetime.now() + timedelta(days=3)
    currentTime = datetime.now() 
    currentTime.strftime('%Y-%m-%d')
    curTimePlusThreeDay.strftime('%Y-%m-%d')

    if expirDateDateTime < curTimePlusThreeDay:
        timeLeft =expirDateDateTime - currentTime

        msg = Message('Hello from appdomainteam3!', recipients=[user.email])
        if timeLeft.days > 0:
            flash(f"Your password is expiring in {timeLeft.days} day(s)")
            msg.body = f"Your password is expiring in {timeLeft.days} day(s)"
            mail.send(msg)
        elif timeLeft.days == -1: 
            flash(f"Your password is expiring at 12:00 A.M. (EST)")
            msg.body = f"Your password is expiring at 12:00 A.M. (EST)" 
            mail.send(msg)
        elif timeLeft.days < -1: 
            flash(f"Your password has been expired")
            msg.body = f"Your password has been expired" 
            mail.send(msg)
        
def updataUserSessionData():
    global users
    users = updateUserList(users, api_url)
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
    global users
    users = updateUserList(users, api_url)
    if request.method == 'POST':
        session.pop('user_id',None)
        username = request.form['username'].lower()
        password = request.form['password']
        _user = None
        for user in users:
            if user.username.lower() == username:
                _user = user
                break
        if _user != None:
            if check_password_hash(_user.password, password):
                if _user.isActive == 'True':
                    session['user_id'] = _user.id
                    passwordExEmail(_user)
                    return redirect(url_for('index'))
                else:
                    flash(f"{_user.username} is disabled until {_user.reactivateUserDate}")
                    return redirect(url_for('login'))
            else:
                response = requests.post(f"{api_url}/users/{_user.id}/failed_login")
                return render_template('login.html',title = 'Login', url=app_url)
    return render_template('login.html',title = 'Login', url=app_url)

@app.route("/user-mail", methods=['GET', 'POST'])
def userMail():
    global users
    users = updateUserList(users, api_url)
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
        return render_template('login.html',title='login')
    return render_template('index.html', title='home', user=g.user)

@app.route("/users/")
def DisplayAllUsers():
    if g.user == None:
        return render_template('login.html')
    global users
    users = updateUserList(users, api_url)
    return render_template('users.html', title='All Users', userdata=users, user=g.user, url=app_url)

@app.route("/users/expired_passwords/")
def DisplayAllUsersWithExpiredPasswords():
    if g.user == None:
        return render_template('login.html')
    global users
    users = updateUserList(users, api_url)
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
    response = requests.get(f"{api_url}/users/{user_id}/accounts")
    accounts = []
    if response.status_code != 404:
        for entry in response.json():
            accounts.append(entry)
    canEdit = False
    if g.user.usertype == 'administrator' or g.user.id == user_id:
        canEdit = True
    return render_template('profile.html', user=g.user, title = 'User Profile Page',userData=users[user_id], accounts=accounts, url=app_url, api=api_url, canEdit=canEdit)

@app.route("/users/<int:user_id>/edit/", methods=['GET', 'POST'])
def EditUserProfile(user_id):
    if g.user == None:
        return render_template('login.html')
    response = requests.get(f"{api_url}/users/{user_id}")
    if response.status_code == 404:
        return render_template('error.html', user=g.user)
    global users
    users = updateUserList(users, api_url)

    accounts = populateAccountsListByUserID(user_id, api_url)
    user = users[user_id]
    form = UserCreationForm()
    canEdit = False
    if g.user.usertype == 'administrator' or g.user.id == user_id:
        canEdit = True
    return render_template('edit_user.html', title='edit ' + user.username, form=form, accounts=accounts, user=user, url=app_url, api=api_url, sessionUser=g.user, canEdit=canEdit)

@app.route("/users/<int:user_id>/accounts/edit", methods=['GET', 'POST'])
def UserAccountsEditView(user_id):
    if g.user == None:
        return render_template('login.html')
    response = requests.get(f"{api_url}/users/{user_id}")
    if response.status_code == 404:
        return render_template('error.html', user=g.user)
    global users
    users = updateUserList(users, api_url)
    user = users[user_id]
    accounts = populateAccountsListByUserID(user_id, api_url)
    canEdit = False
    if g.user.usertype == 'administrator' or g.user.id == user_id:
        canEdit = True
    return render_template('user_accounts_edit_view.html', title='Edit Accounts ' + user.username, accounts=accounts, user=g.user, canEdit=canEdit, sessionUser=g.user, app=app_url, api=api_url)

@app.route("/users/<int:user_id>/edit_password", methods=['GET', 'POST'])
def EditPassword(user_id):
    if g.user == None:
        return render_template('login.html')
    response = requests.get(f"{api_url}/users/{user_id}")
    if response.status_code == 404:
        return render_template('error.html', user=g.user)
    global users
    users = updateUserList(users, api_url)
    user = users[user_id]
    form = UserPasswordChangeForm()
    return render_template('edit_password.html', title=f"Update Password, {user.username}", form=form, user=user, url=app_url, api=api_url, sessionUser=g.user)

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

@app.route("/accounts/create", methods=['GET', 'POST'])
def CreateAccount():
    if g.user == None:
        return render_template('login.html')
    form = AccountCreationForm()
    return render_template('create_account.html', title='Open Account', form=form, api=api_url, user=g.user, sessionUser=g.user)

@app.route("/accounts/<int:account_number>", methods=['GET', 'POST'])
def AccountOverview(account_number):
    if g.user == None:
        return render_template('login.html')
    account = populateAccountByAccountNumber(account_number, api_url)
    return render_template('account_overview.html', title='Account Overview', account=account, api=api_url, user=g.user, sessionUser=g.user)

@app.route("/accounts/<int:account_number>/edit", methods=['GET', 'POST'])
def EditAccount(account_number):
    if g.user == None:
        return render_template('login.html')
    account = populateAccountByAccountNumber(account_number, api_url)
    form = AccountEditForm()
    return render_template('edit_account.html', title='Edit Account', form=form, api=api_url, account=account, user=g.user, sessionUser=g.user)

@app.route("/forgot_password/", methods=['GET', 'POST'])
def ForgotPassword():
    form = ForgotPasswordForm()
    return render_template('forgot_password.html', title='Forgot Password', form=form, api=api_url)

@app.errorhandler(404)
def page_not_found(error):
    return render_template('error.html', user=g.user), 404

if __name__ == "__main__":
    app.run(debug=False)
