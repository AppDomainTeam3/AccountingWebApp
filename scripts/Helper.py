from scripts.Account import Account
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