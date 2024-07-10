from flask import Blueprint, render_template, request as flaskReq, redirect, url_for

bp = Blueprint('login', __name__)

accounts = {}
accounts['Ryan'] = 'Enter123'

@bp.route('/')
def load():
    return render_template('login.html')

@bp.route('/authenticate', methods=['POST'])
def authenticate():
    if flaskReq.form['username'] in accounts.keys() and accounts[flaskReq.form['username']] == flaskReq.form['password']:
        return redirect(url_for('home.load'), code=307)
    else:
        return redirect(url_for('login.load'))