from flask import Blueprint, render_template, request as flaskReq, redirect, url_for
from core.session import Session

bp = Blueprint('login', __name__)
userSession = Session()

@bp.route('/')
def load():
    return render_template('login.html')

@bp.route('/authenticate', methods=['POST'])
def authenticate():
    if userSession.authenticate(flaskReq.form['username'], flaskReq.form['password']):
        return redirect(url_for('home.load'), code=307)
    else:
        return redirect(url_for('login.load'))