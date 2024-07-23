from flask import Flask
from config import Config

def create_app(configuration=Config):
    app = Flask(__name__)
    app.config.from_object(configuration)

    from app.login import bp as login_bp
    app.register_blueprint(login_bp)

    from app.home import bp as home_bp
    app.register_blueprint(home_bp, url_prefix='/Home')

    from app.businessInsights import bp as bizInsights_bp
    app.register_blueprint(bizInsights_bp, url_prefix='/BusinessInsights')

    from app.aiAnalyst import bp as aiAnalyst_bp
    app.register_blueprint(aiAnalyst_bp, url_prefix='/AIAnalyst')

    @app.route('/test/')
    def testrun():
        return "<p>HELLO AGAIN</p>"
    
    return app