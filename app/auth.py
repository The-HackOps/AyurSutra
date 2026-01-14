from flask import (
    Blueprint, render_template, request, redirect, url_for, flash, session, g
)
from .forms import RegistrationForm

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

MOCK_USERS = {
    1: {
        'id': 1, 
        'email': 'patient@test.com', 
        'password': '123', 
        'first_name': 'John', 
        'last_name': 'Doe', 
        'role': 'patient'
    },
    2: {
        'id': 2, 
        'email': 'doctor@test.com', 
        'password': '123', 
        'first_name': 'Ayur', 
        'last_name': 'Sutra', 
        'role': 'practitioner'
    }
}

@auth_bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = MOCK_USERS.get(user_id)

@auth_bp.route('/register', methods=('GET', 'POST'))
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash('Registration successful! (Prototype Mode: Please log in with patient@test.com)', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/register.html', form=form)

@auth_bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        error = None
        user = None

        if email == 'patient@test.com' and password == '123':
            user = MOCK_USERS[1]
        elif email == 'doctor@test.com' and password == '123':
            user = MOCK_USERS[2]
        
        if user is None:
            error = 'Invalid credentials. Try patient@test.com / 123'
        
        if error is None:
            session.clear()
            session['user_id'] = user['id']
            session['role'] = user['role']
            session['first_name'] = user['first_name']
            return redirect(url_for('main.dashboard'))

        flash(error, 'danger')
        
    return render_template('auth/login.html', form={})

@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))
