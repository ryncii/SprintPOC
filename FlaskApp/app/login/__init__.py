from flask import Blueprint, render_template

bp = Blueprint('login', __name__)

@bp.route('/')
def load():
    return render_template('login.html')