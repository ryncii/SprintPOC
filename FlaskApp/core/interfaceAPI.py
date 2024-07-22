from flask import session as flaskSession
from calendar import monthrange
import pandas as pd, numpy as np, datetime as dt, statistics as stats, math, copy

# Custom Calls
import core.charts as customDraw

# Notes
# No currency conversion
# Need to handle empty dataframes or dataframes with size 1
# Under Overall health - need to fix historicalMonth in event of no data
# 13 month lookback not completed for Business Performance

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
            self.datasetAPI['Transaction'] = copy.copy(transaction.loc[flaskSession['LocalID']])
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
            monthlySales = self.datasetAPI['Transaction'].groupby(['Month']).sum()
            referenceMonth = monthlySales[monthlySales.index == (dt.date.today().replace(day=1) - dt.timedelta(days=1)).replace(day=1)] # last Month
            self.overallHealthRefMonth = dt.date.strftime(referenceMonth.index[0], '%b %Y')
            historicalMonths = monthlySales[monthlySales.index < referenceMonth.index[0]]
            sDev = stats.stdev(list(historicalMonths.loc[:,'Amount']))
            meanAmt = stats.mean(list(historicalMonths.loc[:,'Amount']))
            if monthlySales.loc[dt.date.today().replace(day=1), 'Amount'] > meanAmt + sDev:
                self.overallHealth = 'Excellent'
            elif monthlySales.loc[dt.date.today().replace(day=1), 'Amount'] < meanAmt - sDev:
                self.overallHealth = 'Warning'
            else:
                self.overallHealth = 'Stable'

            self.overallHealthGraph = customDraw.plotOverallHealth(list(historicalMonths.loc[:, 'Amount']), round(referenceMonth['Amount'][0],2))

            # Pacing
            monthDays = monthrange(dt.date.today().year, dt.date.today().month)[1]
            bins = 10 # a month will have its data devided into 10 bins (static)
            daysPerbins = monthDays / bins
            paceIndex = math.floor(dt.date.today().day / daysPerbins)
            self.currentMonthPace = dt.date.strftime(dt.date.today(), '%b %Y')

            referenceMonth = monthlySales[monthlySales.index == dt.date.today().replace(day=1)]
            historicalMonths = copy.copy(self.datasetAPI['Transaction'][self.datasetAPI['Transaction']['Month'] < dt.date.today().replace(day=1)])
            historicalMonths['Bin'] = [math.floor(ts.day/daysPerbins) for ts in historicalMonths.loc[:,'Timestamp']]

            multiIndex = pd.MultiIndex.from_product([list({x for x in historicalMonths['Month']}),list({x for x in historicalMonths['Bin']})], names=['Month', 'Bin'])
            avg_Bin = historicalMonths.groupby(['Month', 'Bin']).sum().reindex(multiIndex, fill_value=0).groupby(['Bin']).mean().loc[:, ['Amount']]
        
            progressBar = []
            for amt in list(avg_Bin['Amount']):
                if len(progressBar) == 0:
                    progressBar.append(amt)
                else:
                    progressBar.append(progressBar[-1] + amt)
            
            avg_Bin['AvgProgress'] = progressBar
            self.currentMonthPace
            self.paceGraph = customDraw.plotPacingBar(list(avg_Bin['AvgProgress'])[-1], referenceMonth['Amount'][0], round(avg_Bin.loc[paceIndex, 'AvgProgress'], 2))

    def showTransactions(self):
        if isinstance(self.datasetAPI['Transaction'], pd.Series):
            pass
        else:

            latest100 = copy.copy(self.datasetAPI['Transaction'].sort_values(['Timestamp'], ascending=False)[:50])
            self.eventsGraph = customDraw.plotLastTransactions(latest100)



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

