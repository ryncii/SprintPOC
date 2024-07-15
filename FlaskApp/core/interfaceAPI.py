from flask import session as flaskSession
from config import Config
import pandas as pd, numpy as np, datetime as dt, statistics as stats
import core.charts as customDraw

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
            self.datasetAPI['Transaction']['Timestamp'] = [dt.datetime.strptime(ts, '%d/%m/%y %H:%M') for ts in self.datasetAPI['Transaction'].loc[:,'Timestamp']]
            bankInfo = pd.read_csv('sample/api_bankInformationSample.csv', index_col='LocalID')
            self.datasetAPI['BankInformation'] = bankInfo.loc[flaskSession['LocalID']]
    
    def calculateAccountFunds(self):
        if isinstance(self.datasetAPI['BankInformation'], pd.Series):
            self.accountFunds = self.datasetAPI['BankInformation']['Balance']
            self.bankAccount_ls.append(self.datasetAPI['BankInformation'].to_dict())
        else:
            self.accountFunds = 0
            for index, bankS in self.datasetAPI['BankInformation'].iterrows():
                self.accountFunds += float(bankS['Balance'])
                self.bankAccount_ls.append(bankS.to_dict())

    def calculateBusinessState(self):
        if isinstance(self.datasetAPI['BankInformation'], pd.Series):
            # Return Insufficient Data
            self.overallHealth = 'Unknown'
        else:
            self.datasetAPI['Transaction']['Month'] = [dt.date(timestamp.year, timestamp.month, 1) for timestamp in self.datasetAPI['Transaction'].loc[:,'Timestamp']]
            mvAvg_3month = self.datasetAPI['Transaction'].groupby(['Month']).sum().rolling(window=3).mean()
            sDev = stats.stdev([income for income in mvAvg_3month.loc[:,'Amount'] if income >= 0])
            meanAmt = stats.mean([income for income in mvAvg_3month.loc[:,'Amount'] if income >= 0])
            if mvAvg_3month.loc[dt.date(dt.datetime.today().year, dt.datetime.today().month, 1), 'Amount'] > meanAmt + sDev:
                self.overallHealth = 'Excellent'
            elif mvAvg_3month.loc[dt.date(dt.datetime.today().year, dt.datetime.today().month, 1), 'Amount'] < meanAmt - sDev:
                self.overallHealth = 'Danger'
            else:
                self.overallHealth = 'Stable'

            print(self.overallHealth)
            self.overallHealthGraph = customDraw.plotOverallHealth(mvAvg_3month.loc[:, 'Amount'], mvAvg_3month.index)

    def view(self):
        for key in self.datasetAPI.keys():
            print(key)
            print(self.datasetAPI[key])
