from flask import Flask
from config import Config

def create_app(configuration=Config):
    app = Flask(__name__)
    app.config.from_object(configuration)

    from app.login import bp as login_bp
    app.register_blueprint(login_bp)

    from app.home import bp as home_bp
    app.register_blueprint(home_bp, url_prefix='/home')

    @app.route('/test/')
    def testrun():
        return "<p>HELLO AGAIN</p>"
    
    return app