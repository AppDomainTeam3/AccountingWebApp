from flask import Flask
import requests

from scripts.User import User

app = Flask(__name__, static_folder='static')

api_url = 'http://127.0.0.2:5000'

@app.route("/")
def index():
    user1 = User('regular_user', 'User1')
    return f"Hello, {user1.name}"

@app.route("/users")
def DisplayAllUsers():
    response = requests.get(f"{api_url}/users")
    userList = ''
    for user in response.json():
        username = user['username']
        firstName = user['firstname']
        lastName = user['lastname']
        avatarLink = user['avatarlink']

        userList += f"<p>{username}: {firstName}, {lastName}<p>"
    return f"Users: {userList}"

if __name__ == "__main__":
    app.run(debug=False)