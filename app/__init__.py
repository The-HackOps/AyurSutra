# /ayursutra/app/__init__.py

import os
from flask import Flask, g
from config import Config
import pymysql
import pymysql.cursors

# --- Application Factory ---
def create_app(config_class=Config):
    """
    Application factory pattern.
    """
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # --- Database Config ---
    app.config['DB_CONFIG'] = {
        'host': app.config['DB_HOST'],
        'user': app.config['DB_USER'],
        'password': app.config['DB_PASSWORD'],
        'database': app.config['DB_NAME'],
        'cursorclass': pymysql.cursors.DictCursor,
        'autocommit': True # <-- IMPORTANT for our auth routes
    }

    # --- Database Connection Management ---
    @app.before_request
    def get_db_connection():
        """Create a new database connection for each request."""
        try:
            g.db_conn = pymysql.connect(**app.config['DB_CONFIG'])
            g.db_cursor = g.db_conn.cursor()
        except pymysql.Error as err:
            print(f"--- DB Connection Error: {err} ---")
            g.db_conn = None
            g.db_cursor = None

    @app.teardown_appcontext
    def close_db_connection(exception):
        """Close the database connection at the end of the request."""
        conn = g.pop('db_conn', None)
        cursor = g.pop('db_cursor', None)
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    # --- Register Blueprints ---
    
    from . import auth
    app.register_blueprint(auth.auth_bp)

    from . import main
    app.register_blueprint(main.main_bp)
    
    from . import patient
    app.register_blueprint(patient.patient_bp)
    
    # !! ADD THESE TWO LINES !!
    # Import and register the practitioner blueprint
    from . import practitioner
    app.register_blueprint(practitioner.practitioner_bp)

    # Make 'index' the default route
    app.add_url_rule('/', endpoint='index')
    
    return app