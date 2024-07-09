from flask import render_template, request
from app.home import bp

@bp.route('/')
def load():
    #squeeze = squeezeThisTextIn()
    #fig = buildSampleGraphImage()
    #graphJSON = json.dumps(fig, cls=pUtils.PlotlyJSONEncoder)
    return render_template('home.html', INPUT = request.form['username'])
