from flask import Blueprint, render_template, request as flaskReq, redirect, url_for, current_app
import core.authentication as authentication

bp = Blueprint('login', __name__)

@bp.route('/')
def load():
    return render_template('login.html')

@bp.route('/authenticate', methods=['POST'])
def authenticate():
    if authentication.authenticate(current_app, flaskReq.form['username'], flaskReq.form['password']):
        return redirect(url_for('home.load'))
    else:
        return redirect(url_for('login.load'))