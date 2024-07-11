from config import Config
import pandas as pd

class InterfaceAPI:

    def __init__(self):
        self.datasetAPI = {}

    def interfaceDataset(self, partner:str = None):
        if partner == 'UOB':
            pass
        else:
            # Sample data for POC
            transaction = pd.read_csv('sample/api_transactionsSample.csv', index_col='SecretKey')
            self.datasetAPI['Transaction'] = transaction.loc[Config.SECRET_KEY]
            bankInfo = pd.read_csv('sample/api_bankInformationSample.csv', index_col='SecretKey')
            self.datasetAPI['BankInformation'] = bankInfo.loc[Config.SECRET_KEY]

    def view(self):
        for key in self.datasetAPI.keys():
            print(key)
            print(self.datasetAPI[key])
