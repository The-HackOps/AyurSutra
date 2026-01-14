from flask import Flask, g
from config import Config

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    @app.before_request
    def get_db_connection():
        g.db_conn = None
        g.db_cursor = None

    @app.teardown_appcontext
    def close_db_connection(exception):
        pass
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
