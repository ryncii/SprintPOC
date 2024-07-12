from flask import session as flaskSession
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
            transaction = pd.read_csv('sample/api_transactionsSample.csv', index_col='LocalID')
            self.datasetAPI['Transaction'] = transaction.loc[flaskSession['LocalID']]
            bankInfo = pd.read_csv('sample/api_bankInformationSample.csv', index_col='LocalID')
            self.datasetAPI['BankInformation'] = bankInfo.loc[flaskSession['LocalID']]

    def view(self):
        for key in self.datasetAPI.keys():
            print(key)
            print(self.datasetAPI[key])
