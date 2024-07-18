from flask import Blueprint, render_template, request as flaskReq, current_app, session
from config import Config
import plotly.express as px, plotly.utils as pUtils, json

from core.interfaceAPI import InterfaceAPI

bp = Blueprint('home', __name__)

@bp.route('/')
def load():
    interface = InterfaceAPI()
    interface.interfaceDataset()
    interface.calculateAccountFunds()
    interface.calculateBusinessState()
    # interface.view()
    
    return render_template('home.html', username = session['Username'], TOTALACCOUNT_VALUE = interface.accountFunds, TOTALACCOUNT_UNIT = interface.defaultCurrency, ACCOUNT_LS=interface.bankAccount_ls, BIZHEALTH = interface.overallHealth, FIG1 = interface.overallHealthGraph, FIG2 = interface.paceGraph)
