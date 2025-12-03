import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config:
    # This 'or' part fixes the CSRF Error by providing a backup key
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-fallback-key-123'
    DEBUG = True
    
    # We leave these here, but they won't be used by the app right now
    DB_HOST = os.environ.get('DB_HOST')
    DB_USER = os.environ.get('DB_USER')
    DB_PASSWORD = os.environ.get('DB_PASSWORD')
    DB_NAME = os.environ.get('DB_NAME')
