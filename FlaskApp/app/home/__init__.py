from flask import Blueprint, render_template, request as flaskReq
import plotly.express as px, plotly.utils as pUtils, json

bp = Blueprint('home', __name__)

# Generic Functions
def squeezeThisTextIn():
    return 'Hello Everybody'

def buildSampleGraphImage():
    fig = px.scatter(x=range(10), y=range(10))
    return fig


@bp.route('/', methods=['POST'])
def load():
    squeeze = squeezeThisTextIn()
    fig = buildSampleGraphImage()
    graphJSON = json.dumps(fig, cls=pUtils.PlotlyJSONEncoder)
    return render_template('home.html', username = flaskReq.form['username'], SQSQ = squeeze, FIG1 = graphJSON)
