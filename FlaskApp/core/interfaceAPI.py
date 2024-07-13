from flask import session as flaskSession
from config import Config
import pandas as pd

# Notes
# No currency conversion

class InterfaceAPI:

    def __init__(self):
        self.datasetAPI = {}
        self.accountFunds = None
        self.defaultCurrency = 'SGD'
        self.bankAccount_ls = []

    def interfaceDataset(self, partner:str = None):
        if partner == 'UOB':
            pass
        else:
            # Sample data for POC
            transaction = pd.read_csv('sample/api_transactionsSample.csv', index_col='LocalID')
            self.datasetAPI['Transaction'] = transaction.loc[flaskSession['LocalID']]
            bankInfo = pd.read_csv('sample/api_bankInformationSample.csv', index_col='LocalID')
            self.datasetAPI['BankInformation'] = bankInfo.loc[flaskSession['LocalID']]
            
            if isinstance(self.datasetAPI['BankInformation'], pd.Series):
                self.accountFunds = self.datasetAPI['BankInformation']['Balance']
                self.bankAccount_ls.append(self.datasetAPI['BankInformation'].to_dict())
            else:
                self.accountFunds = 0
                for index, bankS in self.datasetAPI['BankInformation'].iterrows():
                    self.accountFunds += float(bankS['Balance'])
                    self.bankAccount_ls.append(bankS.to_dict())
                    

            for ba in self.bankAccount_ls:
                print(ba['BankAccountID'])

    def view(self):
        for key in self.datasetAPI.keys():
            print(key)
            print(self.datasetAPI[key])
