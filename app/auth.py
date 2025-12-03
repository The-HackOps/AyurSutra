from flask import (
    Blueprint, render_template, request, redirect, url_for, flash, session, g
)
from .forms import RegistrationForm

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

# --- MOCK DATA FOR PROTOTYPE ---
# This dictionary simulates your database. 
# It contains one Patient and one Doctor.
MOCK_USERS = {
    1: {
        'id': 1, 
        'email': 'patient@ayursutra.com', 
        'password': '123', 
        'first_name': 'John', 
        'last_name': 'Doe', 
        'role': 'patient'
    },
    2: {
        'id': 2, 
        'email': 'doctor@ayursutra.com', 
        'password': '123', 
        'first_name': 'Ayur', 
        'last_name': 'Sutra', 
        'role': 'doctor'
    }
}

# --- IMPORTANT: LOADS USER INTO NAVBAR ---
# This runs before every request to check if a user is logged in.
# It replaces the database lookup for g.user
@auth_bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        # Simulate fetching user from DB
        g.user = MOCK_USERS.get(user_id)

@auth_bp.route('/register', methods=('GET', 'POST'))
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        # --- BYPASS DB INSERT ---
        # In a real app, we would insert into MySQL here.
        # For prototype, we just pretend it worked.
        
        flash('Registration successful! (Prototype Mode: Please log in with patient@ayursutra.com)', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/register.html', form=form)


@auth_bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        error = None
        
        user = None

        # --- BYPASS DB SELECT ---
        # Check against our hardcoded Mock Users
        if email == 'patient@ayursutra.com' and password == '123':
            user = MOCK_USERS[1]
        elif email == 'doctor@ayursutra.com' and password == '123':
            user = MOCK_USERS[2]
        
        if user is None:
            error = 'Invalid credentials. Try patient@ayursutra.com (Password: 123)'
        
        if error is None:
            # Login successful
            session.clear()
            session['user_id'] = user['id']
            session['role'] = user['role']
            session['first_name'] = user['first_name']
            
            flash(f"Welcome back, {user['first_name']}!", 'success')
            return redirect(url_for('main.dashboard'))

        flash(error, 'danger')
        
    return render_template('auth/login.html', form={})


@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))
