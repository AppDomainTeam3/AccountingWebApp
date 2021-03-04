class Journal():
    def __init__(self, Journal_ID, RequestorUserID, AccountName, AccountNumber, Status, Debits, Credits, Message):
        self.Journal_ID = Journal_ID
        self.RequestorUserID = RequestorUserID
        self.AccountName = AccountName
        self.AccountNumber = AccountNumber
        self.Status = Status
        self.Debits = Debits
        self.Credits = Credits
        self.Message = Message
    def __repr__(self): 
        return f"""<Journal_ID: {self.Journal_ID}, RequestorUserID: {self.RequestorUserID}, AccountName: {self.AccountName}, AccountNumber: {self.AccountNumber},
         Status: {self.Status}, Debits: {self.Debits}, Credits: {self.Credits}, Message: {self.Message}>"""