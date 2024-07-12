from flask import Flask, session as flaskSession
import random
import pandas as pd

def authenticate(app: Flask, username:str, password:str):
    accounts = pd.read_csv('sample/db_accounts.csv', index_col='Username')
    if accounts.loc[username,'Password'] == password:
        flaskSession['Username'] = username
        flaskSession['LocalID'] = accounts.loc[username,'LocalID']
        return True
    else:
        return False
    