from flask import render_template,redirect, request, url_for
from app.login import bp

@bp.route('/')
def load():
    return render_template('login.html')
