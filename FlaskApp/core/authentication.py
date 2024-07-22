from flask import session as flaskSession
import pandas as pd

def authenticate(username:str, password:str):
    accounts = pd.read_csv('sample/db_accounts.csv', index_col='Username')
    if accounts.loc[username,'Password'] == password:
        flaskSession['Username'] = username
        flaskSession['LocalID'] = accounts.loc[username,'LocalID']
        return True
    else:
        return False
    