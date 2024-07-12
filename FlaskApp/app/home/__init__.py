from flask import Blueprint, render_template, request as flaskReq, current_app, session
from config import Config
import plotly.express as px, plotly.utils as pUtils, json

from core.interfaceAPI import InterfaceAPI

bp = Blueprint('home', __name__)

# Generic Functions
def squeezeThisTextIn():
    print(Config.SECRET_KEY)
    return 'Hello Everybody'

def buildSampleGraphImage():
    fig = px.scatter(x=range(10), y=range(10))
    return fig


@bp.route('/')
def load():
    interface = InterfaceAPI()
    interface.interfaceDataset()
    interface.view()
    
    squeeze = squeezeThisTextIn()
    fig = buildSampleGraphImage()
    graphJSON = json.dumps(fig, cls=pUtils.PlotlyJSONEncoder)
    return render_template('home.html', username = session['Username'], SQSQ = squeeze, FIG1 = graphJSON)
