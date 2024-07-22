from flask import Blueprint, render_template, current_app, session as flaskSession
from config import Config
import plotly.express as px, plotly.utils as pUtils, json, datetime as dt

from core.interfaceAPI import InterfaceAPI

bp = Blueprint('financialInsights', __name__)

@bp.route('/')
def load():

    generalInfo = {}
    generalInfo['Username'] = flaskSession['Username']
    generalInfo['ActivePage'] = "FinancialInsights"

    return render_template('financialInsights.html', GENERAL = generalInfo)
