from flask import Blueprint, render_template, request as flaskReq, current_app, session
from config import Config
import plotly.express as px, plotly.utils as pUtils, json, datetime as dt

from core.interfaceAPI import InterfaceAPI

bp = Blueprint('home', __name__)

@bp.route('/')
def load():
    interface = InterfaceAPI()
    interface.interfaceDataset()
    interface.calculateAccountFunds()
    interface.calculateBusinessState()
    interface.showTransactions()


    # Account Funds
    accountFund = {}
    accountFund['TOTALACCOUNT_VALUE'] = interface.accountFunds
    accountFund['TOTALACCOUNT_UNIT'] = interface.defaultCurrency
    accountFund['ACCOUNT_LS'] = interface.bankAccount_ls
    
    # Business Perfromance
    bizPerformance = {}
    bizPerformance['BIZHEALTH'] = interface.overallHealth
    bizPerformance['BIZREFERENCEMONTH'] = interface.overallHealthRefMonth
    bizPerformance['HEALTHGRAPH'] = interface.overallHealthGraph
    bizPerformance['CURRENTMONTHPACE'] = interface.currentMonthPace
    bizPerformance['PACEGRAPH'] = interface.paceGraph
    
    latestTransactions = {}
    latestTransactions['TRANSACTIONEVENTS'] = interface.eventsGraph
    latestTransactions['REFRESHTIME'] = dt.datetime.strftime(dt.datetime.now(), '%d %b %Y %H:%M:%S')
    
    campaignPerformance = {}
    campaignPerformance['Status'] = 'No active campaigns running'

    return render_template('home.html', username = session['Username'], ACCOUNTFUNDDATA = accountFund, BUSINESSPERFORMANCEDATA = bizPerformance, TRANSACTIONEVENTS = latestTransactions, CAMPAIGNPROGRESS=campaignPerformance)
