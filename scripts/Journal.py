class Journal():
    def __init__(self, Journal_ID, RequestorUserID, SourceAccountName, SourceAccountNumber, DestAccountName,
                    DestAccountNumber, Status, Debits, Credits, Message, SourceFile, Timestamp):
        self.Journal_ID = Journal_ID
        self.RequestorUserID = RequestorUserID
        self.SourceAccountName = SourceAccountName
        self.SourceAccountNumber = SourceAccountNumber
        self.DestAccountName = DestAccountName
        self.DestAccountNumber = DestAccountNumber
        self.Status = Status
        self.Debits = Debits
        self.Credits = Credits
        self.Message = Message
        self.SourceFile = SourceFile
        self.Timestamp = Timestamp
    def __repr__(self): 
        return f"""{{'Journal_ID': {self.Journal_ID}, 'RequestorUserID': {self.RequestorUserID}, 'SourceAccountName': '{self.SourceAccountName}',
        'SourceAccountNumber': {self.SourceAccountNumber}, 'DestAccountName': '{self.DestAccountName}', 'DestAccountNumber': {self.DestAccountNumber},
        'Status': '{self.Status}', 'Debits': {self.Debits}, 'Credits': {self.Credits}, 'Message': '{self.Message}', 'SourceFile': '{self.SourceFile}', 
        'Timestamp': '{self.Timestamp}'}}"""