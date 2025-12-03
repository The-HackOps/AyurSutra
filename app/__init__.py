from flask import Flask, g
from config import Config

# NOTE: Database imports are removed for Mock Mode
# import pymysql
# import pymysql.cursors

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # --- Database Connection Removed ---
    # We are using Mock Data in auth.py, so we don't need a DB connection here.

    @app.before_request
    def get_db_connection():
        # Just set these to None so the app doesn't crash if something checks them
        g.db_conn = None
        g.db_cursor = None

    @app.teardown_appcontext
    def close_db_connection(exception):
        pass

    # --- Register Blueprints ---
    from . import auth
    app.register_blueprint(auth.auth_bp)

    from . import main
    app.register_blueprint(main.main_bp)
    
    from . import patient
    app.register_blueprint(patient.patient_bp)
    
    from . import practitioner
    app.register_blueprint(practitioner.practitioner_bp)

    app.add_url_rule('/', endpoint='index')
    
    return app
