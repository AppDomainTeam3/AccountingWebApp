from flask import Flask
from scripts.User import User

app = Flask(__name__, static_folder='static')

@app.route("/")
def index():
    user1 = User('regular_user', 'User1')
    return f"Hello, {user1.name}"

if __name__ == "__main__":
    app.run()