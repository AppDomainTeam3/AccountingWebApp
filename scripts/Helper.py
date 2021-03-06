from scripts.Journal import Journal
from scripts.Account import Account
from scripts.User import User
import requests

def populateJournalsListWithAllJournals(api_url):
    response = requests.get(f"{api_url}/journals")
    journalList = response.json()
    journals = []
    if response.status_code == 404:
        return None
    for journalDict in journalList:
        journals.append(Journal(Journal_ID=journalDict['Journal_ID'],
                                RequestorUserID=journalDict['RequestorUserID'],
                                SourceAccountName=journalDict['SourceAccountName'],
                                SourceAccountNumber=journalDict['SourceAccountNumber'],
                                DestAccountName=journalDict['DestAccountName'],
                                DestAccountNumber=journalDict['DestAccountNumber'],
                                Status=journalDict['Status'],
                                Debits=buildFloatArrayFromCommaDelimitedString(journalDict['Debits']),
                                Credits=buildFloatArrayFromCommaDelimitedString(journalDict['Credits']),
                                Message=journalDict['Message'],
                                Timestamp=journalDict['Timestamp']))
    return journals

def buildFloatArrayFromCommaDelimitedString(str):
    str = str.split(',')
    for i, value in enumerate(str):
        str[i] = "".join(str[i].split())
    arr = []
    for entry in str:
        arr.append(float(entry))
    return arr

def populateAccountsListByUserID(user_id, api_url):
    response = requests.get(f"{api_url}/users/{user_id}/accounts")
    accountList = response.json()
    accounts = []
    if response.status_code == 404:
        return None
    for accountDict in accountList:
        accounts.append(Account(id=accountDict['id'],
                                accountName=accountDict['AccountName'],
                                accountNumber=accountDict['AccountNumber'],
                                accountDesc=accountDict['AccountDesc'],
                                normalSide=accountDict['NormalSide'],
                                category=accountDict['Category'],
                                subcategory=accountDict['Subcategory'],
                                balance=accountDict['Balance'],
                                accountCreationDate=accountDict['CreationDate'],
                                accountOrder=accountDict['AccountOrder'],
                                statement=accountDict['Statement'],
                                comment=accountDict['Comment'],
                                isActive=accountDict['IsActive']))
    return accounts

def populateAccountByAccountNumber(account_number, api_url):
    response = requests.get(f"{api_url}/accounts/{account_number}")
    accountDict = response.json()
    if response.status_code == 404:
        return None
    account = Account(id=accountDict['id'],
                      accountName=accountDict['AccountName'],
                      accountNumber=accountDict['AccountNumber'],
                      accountDesc=accountDict['AccountDesc'],
                      normalSide=accountDict['NormalSide'],
                      category=accountDict['Category'],
                      subcategory=accountDict['Subcategory'],
                      balance=accountDict['Balance'],
                      accountCreationDate=accountDict['CreationDate'],
                      accountOrder=accountDict['AccountOrder'],
                      statement=accountDict['Statement'],
                      comment=accountDict['Comment'],
                      isActive=accountDict['IsActive'])
    return account

def populateEventsListByEndpoint(endpoint, api_url):
    response = requests.get(api_url + endpoint)
    if response.status_code == 404:
        return None
    eventList = []
    for event in response.json():
        eventList.append(event)
    return eventList

def sumBalanceEvents(balanceEvents, api_url):
    balance = 0.0
    for event in balanceEvents:
        balance += event['Amount']
    return balance

def updateUserList(users, api_url):
    response = requests.get(f"{api_url}/users")
    userList = response.json()
    users.clear()
    for x in range(len(userList)):
        userDict = userList[x]
        users.append(User(id=userDict['id'], 
                          username = userDict['username'],
                          email = userDict['email'],
                          usertype = userDict['usertype'],
                          firstname = userDict['firstname'],
                          lastname = userDict['lastname'],
                          avatarlink = userDict['avatarlink'],
                          password = userDict['hashed_password'],
                          isActive = userDict['is_active'],
                          isPasswordExpired = userDict['is_password_expired'],
                          reactivateUserDate = userDict['reactivate_user_date'],
                          failedLoginAttempts = userDict['failed_login_attempts'],
                          passwordExpirationDate = userDict['password_expiration_date']))
    return users

def getUserEditStatus(user, user_id):
    canEdit = False
    if user.usertype == 'administrator' or user.id == user_id:
        canEdit = True
    return canEdit