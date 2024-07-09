from flask import Blueprint, render_template, request as flaskReq

bp = Blueprint('login', __name__)

@bp.route('/')
def load():
    return render_template('login.html')

@bp.route('/authenticate', methods=['POST'])
def authenticate():
    print(flaskReq.form['username'])
    return render_template('login.html')