from flask import render_template,redirect, request, url_for
from app.login import bp

@bp.route('/')
def load():
    print('here')
    return render_template('login.html')

'''
@bp.route('/handle_authentication', method=['POST'])
def authenticate():
    print('here2')
    return render_template('login.html')
'''