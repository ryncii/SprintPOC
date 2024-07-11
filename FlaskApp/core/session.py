from config import Config

class Session:

    def __init__(self):
        self.username = None
        print('IN SESSION')

        # Temporary - POC does not require DB
        self.db = {}
        self.db['Ryan'] = {}
        self.db['Ryan']['Password'] = 'Enter123'
        self.db['Ryan']['SecretKey'] = 'ACCOUNTSECRETKEY01'

    def authenticate(self, username:str, password:str):
        print('Attempting Authentication: '+ username + ', ' + password)
        if username in self.db.keys() and self.db[username]['Password'] == password:
            Config.SECRET_KEY = self.db[username]['SecretKey']
            return True
        else:
            return False