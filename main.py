from flask import Flask, redirect, url_for, request, render_template
import plotly.express as px, plotly.utils as pUtils, json

app = Flask(__name__, template_folder='UI')

# Generic Functions
def squeezeThisTextIn():
    return 'Hello Everybody'

def buildSampleGraphImage():
    fig = px.scatter(x=range(10), y=range(10))
    return fig

# App Proper
@app.route('/')
def onStart():
    return render_template('login.html')

@app.route('/success', methods=['POST'])
def success():
    squeeze = squeezeThisTextIn()
    fig = buildSampleGraphImage()
    graphJSON = json.dumps(fig, cls=pUtils.PlotlyJSONEncoder)


    return render_template('success.html', INPUT = request.form['input'], SQSQ = squeeze, FIG1 = graphJSON)
    #return render_template('success.html', INPUT = request.form['input'], SQSQ = squeeze)


@app.route('/braindead')
def hello():
    return 'Well'

if __name__ == '__main__':
    app.run(debug=True)


'''
if request.method == 'POST':
        user = request.form['username']
        return redirect(url_for('success2'))
    else:
'''