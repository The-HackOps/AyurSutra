# /ayursutra/app/main.py

from flask import (
    Blueprint, render_template, session, redirect, url_for, g
)
# We removed the decorator code and added this import:
from app.decorators import login_required 

main_bp = Blueprint('main', __name__)

# --- Our Main Routes ---

@main_bp.route('/')
def index():
    # This will be our new homepage
    return render_template('index.html')

@main_bp.route('/dashboard')
@login_required  # <-- This still works!
def dashboard():
    # This is the main redirector
    if session['role'] == 'patient':
        return render_template('patient/dashboard.html')
    elif session['role'] == 'practitioner':
        return render_template('practitioner/dashboard.html')
    
    return "Error: Unknown role."