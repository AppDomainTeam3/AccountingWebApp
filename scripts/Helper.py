from scripts.Account import Account
from scripts.User import User
import requests

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
                                accountCreationDate=accountDict['AccountCreationDate'],
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
                      accountCreationDate=accountDict['AccountCreationDate'],
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