from flask import Blueprint, render_template, request as flaskReq, redirect, url_for

bp = Blueprint('login', __name__)

@bp.route('/')
def load():
    return render_template('login.html')

@bp.route('/authenticate', methods=['POST'])
def authenticate():
    print('inhere')
    if flaskReq.form['username'] == 'Hello':
        return redirect(url_for('home.load'), code=307)
    else:
        return redirect(url_for('login.load'))