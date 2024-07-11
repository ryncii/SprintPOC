from config import Config

class Session:

    def __init__(self):
        self.username = None
        print('IN SESSION')

        # Temporary - POC does not require DB
        self.db = {}
        self.db['RyanC'] = {}
        self.db['RyanC']['Password'] = 'Enter123'
        self.db['RyanC']['SecretKey'] = 'ACCOUNTSECRETKEY01'
        self.db['Account1'] = {}
        self.db['Account1']['Password'] = 'Enter123'
        self.db['Account1']['SecretKey'] = 'ACCOUNTSECRETKEY01'

    def authenticate(self, username:str, password:str):
        print('Attempting Authentication: '+ username + ', ' + password)
        if username in self.db.keys() and self.db[username]['Password'] == password:
            Config.SECRET_KEY = self.db[username]['SecretKey']
            return True
        else:
            return False