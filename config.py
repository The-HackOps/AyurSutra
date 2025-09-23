# /ayursutra/config.py

import os
from dotenv import load_dotenv

# Find the .env file
basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

# (The debug print line is GONE)

class Config:
    """Base configuration."""
    SECRET_KEY = os.environ.get('SECRET_KEY')
    DEBUG = True
    
    # Database configuration
    DB_HOST = os.environ.get('DB_HOST')
    DB_USER = os.environ.get('DB_USER')
    DB_PASSWORD = os.environ.get('DB_PASSWORD')
    DB_NAME = os.environ.get('DB_NAME')