from flask import Flask

def create_app(test_config=None):
    app = Flask(__name__)
    from . import bp
    app.secret_key = 'xxiiieeaakrujrs'
    app.register_blueprint(bp.bp)
    return app
