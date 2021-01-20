class User:
    types = ['administrator', 'manager', 'regular_user']

    type = 'null'
    name = 'null'

    def __init__(self, user_type, name):
        if (user_type not in self.types):
            print(f"User type \'{user_type}\' not found!")
            return None
        self.type = user_type
        self.name = name
        