class Account():
    def __init__(self, id, accountName, accountNumber, accountDesc, normalSide, category, subcategory, balance, accountCreationDate, accountOrder, statement, comment, isActive):
        self.id = id
        self.accountName = accountName
        self.accountNumber = accountNumber
        self.accountDesc = accountDesc
        self.normalSide = normalSide
        self.category = category
        self.subcategory = subcategory
        self.balance = balance
        self.accountCreationDate = accountCreationDate
        self.accountOrder = accountOrder
        self.statement = statement
        self.comment = comment
        self.isActive = isActive
    def __repr__(self): 
        return f"""{{'id': {self.id}, 'accountNumber': {self.accountNumber}, 'accountName': '{self.accountName}', 'accountDesc': '{self.accountDesc}', 'normalSide': '{self.normalSide}',
         'category': '{self.category}', 'subcategory': '{self.subcategory}', 'balance': {self.balance}, 'accountCreationDate': '{self.accountCreationDate}',
         'accountOrder': {self.accountOrder}, 'statement': '{self.statement}', 'comment': '{self.comment}', 'isActive': '{self.isActive}'}}"""