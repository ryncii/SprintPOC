from flask import Blueprint, render_template, request as flaskReq

bp = Blueprint('home', __name__)

@bp.route('/', methods=['POST'])
def load():
    print(flaskReq.form['username'])
    return render_template('home.html')
