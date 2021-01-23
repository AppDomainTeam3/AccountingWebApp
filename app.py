from flask import Flask
import requests

from scripts.User import User

app = Flask(__name__, static_folder='static')

app_url = 'https://appdomainteam3.azurewebsites.net'
api_url = 'https://appdomainteam3api.azurewebsites.net'

@app.route("/")
def index():
    user1 = User('regular_user', 'User1')
    return f"<button onclick=\"window.location.href='users'\">Click me</button> <p>Hello, {user1.name}</p>"

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

@app.route("/add-user", methods=['GET', 'POST'])
def CreateUser():
    return """<html>
                <head>
                    <title>Create User</title>
                </head>
                
                <body>
                    <form method='POST' action='/add-user' enctype="multipart/form-data">
                        <input type='text' placeholder='username' name='username'></input>
                        <select name="user type" id="usertype">
                            <option value="regular_user">Basic</option>
                            <option value="manager">Manager</option>
                            <option value="administrator">Admin</option>
                        </select>
                        <input type='text' placeholder='first name' name='firstname'></input>
                        <input type='text' placeholder='last name' name='lastname'></input>
                        <input type='text' placeholder='avatar link' name='avatarlink'></input>
                        <button class='submit' name='upload' type='submit'>Submit</button>
                    </form>
                </body>
            </html>"""

if __name__ == "__main__":
    app.run(debug=False)