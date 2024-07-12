from flask import Flask, session as flaskSession
import random
import pandas as pd

def authenticate(app: Flask, username:str, password:str):
    accounts = pd.read_csv('sample/db_accounts.csv', index_col='Username')
    if accounts.loc[username,'Password'] == password:
        app.config.update(SECRET_KEY = accounts.loc[username,'SecretKey'] + str(random.randint(0,100000)), SESSION_TYPE = 'filesystem')
        print('SHHHHHHH: ' + app.secret_key)
        flaskSession['Username'] = username
        return True
    else:
        return False
    