from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, id, username, email, usertype, firstname, lastname, avatarlink, password, isactive, ispasswordexpired):
        self.id = id
        self.username = username
        self.email = email
        self.usertype = usertype
        self.firstname = firstname
        self.lastname = lastname
        self.avatarlink = avatarlink
        self.password = password
        self.isactive = isactive
        self.ispasswordexpired = ispasswordexpired
    def __repr__(self): 
        return f'<User: {self.username}>'