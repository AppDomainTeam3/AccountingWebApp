from flask import Flask, render_template
import requests

from scripts.User import User

app = Flask(__name__, static_folder='static')

app_url = 'https://appdomainteam3.azurewebsites.net'
api_url = 'https://appdomainteam3api.azurewebsites.net'

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

if __name__ == "__main__":
    app.run(debug=False)