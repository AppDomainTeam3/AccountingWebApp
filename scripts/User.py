from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, id, username, email, usertype, firstname, lastname, avatarlink, password, isActive, isPasswordExpired, reactivateUserDate, failedLoginAttempts, passwordExpirationDate):
        self.id = id
        self.username = username
        self.email = email
        self.usertype = usertype
        self.firstname = firstname
        self.lastname = lastname
        self.avatarlink = avatarlink
        self.password = password
        self.isActive = isActive
        self.isPasswordExpired = isPasswordExpired
        self.reactivateUserDate = reactivateUserDate
        self.failedLoginAttempts = failedLoginAttempts
        self.passwordExpirationDate = passwordExpirationDate
    def __repr__(self): 
        return f"""<id: {self.id}, username: {self.username}, email: {self.email}, usertype: {self.usertype}, 
                    firstname: {self.firstname}, lastname: {self.lastname}, isActive: {self.isActive}, 
                    isPasswordExpired: {self.isPasswordExpired}, reactivateUserDate: {self.reactivateUserDate}>"""