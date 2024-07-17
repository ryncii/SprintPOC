from flask import session as flaskSession
from calendar import monthrange
import pandas as pd, numpy as np, datetime as dt, statistics as stats, math

# Custom Calls
import core.charts as customDraw

# Notes
# No currency conversion
# Need to handle empty dataframes or dataframes with size 1

class InterfaceAPI:

    def __init__(self):
        self.datasetAPI = {}
        self.accountFunds = None
        self.defaultCurrency = 'SGD'
        self.bankAccount_ls = []

        monthBinIndex = 4
        self.dateBinList = []
        while monthBinIndex <= 32:
            self.dateBinList.append(monthBinIndex)
            monthBinIndex += 4

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
            self.overallHealthGraph = None
        else:

            # Health
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

            self.overallHealthGraph = customDraw.plotOverallHealth(mvAvg_3month.loc[:, 'Amount'], mvAvg_3month.loc[dt.date(dt.datetime.today().year, dt.datetime.today().month, 1), 'Amount'])

            # Pacing
            monthDays = monthrange(dt.date.today().year, dt.date.today().month)[1]
            bins = 10 # a month will have its data devided into 10 bins (static)
            daysPerbins = monthDays / bins

            self.datasetAPI['Transaction']['Bin'] = [math.floor(timestamp.day/daysPerbins) for timestamp in self.datasetAPI['Transaction'].loc[:,'Timestamp']]
            self.datasetAPI['Transaction']['BinPos'] = [timestamp.day%daysPerbins for timestamp in self.datasetAPI['Transaction'].loc[:,'Timestamp']]
            multiIndex = pd.MultiIndex.from_product([list({x for x in self.datasetAPI['Transaction']['Month']}),list({x for x in self.datasetAPI['Transaction']['Bin']})], names=['Month', 'Bin'])
            avg_Bin = self.datasetAPI['Transaction'].groupby(['Month', 'Bin']).sum().reindex(multiIndex, fill_value=0).groupby(['Bin']).mean().loc[:, ['Amount']]
        
            progressBar = []
            for amt in list(avg_Bin['Amount']):
                if len(progressBar) == 0:
                    progressBar.append(amt)
                else:
                    progressBar.append(progressBar[-1] + amt)
            
            print(progressBar)
            avg_Bin['AvgProgress'] = progressBar

            #print(self.datasetAPI['Transaction'].groupby(['Month']).sum().iloc[-1:, 'Amount'])
            self.paceGraph = customDraw.plotPacingBar(list(avg_Bin['AvgProgress'])[-1], 200,0)
            print(avg_Bin)
            print(bins)
            #self.self.datasetAPI['Transaction']['MonthBin'] = [self._returnDateBin(ts) for ts in self.datasetAPI['Transaction']['Timestamp']]

    def view(self):
        for key in self.datasetAPI.keys():
            print(key)
            print(self.datasetAPI[key])

    # Support functions
    def _returnDateBin(self, timestamp:dt.datetime):
        print(monthrange(dt.date.today().year, dt.date.today().month))

        listInd = 0
        for ts in self.dateBinList:
            if timestamp.day < ts:
                return listInd
            
            listInd += 1

    