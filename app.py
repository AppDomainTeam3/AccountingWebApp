from flask import Flask, render_template, redirect
import requests

from scripts.User import User
from scripts.CreateUser import UserCreationForm

app = Flask(__name__, static_folder='static')
app.config['SECRET_KEY'] = 'secret_key'

app_url = 'https://appdomainteam3.azurewebsites.net'
api_url = 'https://127.0.0.2:5000'

@app.route("/")
def index():
    user = {'username': 'user'}
    return render_template('index.html', title='Home', user=user)

@app.route("/users")
def DisplayAllUsers():
    response = requests.get(f"{api_url}/users")
    userList = []
    for user in response.json():
        userList.append(user)
    return render_template('users.html', title='All Users', userdata=userList)

@app.route("/add-user", methods=['GET', 'POST'])
def CreateUser():
    form = UserCreationForm()
    if (form.validate_on_submit()):
        response = requests.post(f"{api_url}/users/create-user")
        return redirect('/users')
    return render_template('create_user.html', title='Create User', form=form)

if __name__ == "__main__":
    app.run(debug=False)