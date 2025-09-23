# /ayursutra/app/auth.py

from flask import (
    Blueprint, render_template, request, redirect, url_for, flash, session, g
)
from werkzeug.security import check_password_hash, generate_password_hash
import pymysql

# 'auth' is the name of this blueprint.
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        # Get form data
        email = request.form['email']
        password = request.form['password']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        role = request.form['role'] # 'patient' or 'practitioner'
        
        # Get database cursor
        db = g.db_cursor
        error = None

        # --- Validation ---
        if not email:
            error = 'Email is required.'
        elif not password:
            error = 'Password is required.'
        elif not role:
            error = 'Please select a role.'
        
        if error is None:
            try:
                # Check if user already exists
                db.execute("SELECT id FROM Users WHERE email = %s", (email,))
                if db.fetchone() is not None:
                    error = f"User {email} is already registered."
                else:
                    # Insert the new user into the Users table
                    db.execute(
                        "INSERT INTO Users (email, password_hash, first_name, last_name, role) VALUES (%s, %s, %s, %s, %s)",
                        (email, generate_password_hash(password), first_name, last_name, role)
                    )
                    # Get the new user's ID
                    new_user_id = db.lastrowid
                    
                    # Insert into the correct role-specific table
                    if role == 'patient':
                        db.execute("INSERT INTO Patients (user_id) VALUES (%s)", (new_user_id,))
                    elif role == 'practitioner':
                         db.execute("INSERT INTO Practitioners (user_id) VALUES (%s)", (new_user_id,))
                    
                    g.db_conn.commit() # Commit the changes
            except pymysql.Error as e:
                error = f"Database error: {e}"
            else:
                # Success! Redirect to login page
                flash('Registration successful! Please log in.', 'success')
                return redirect(url_for('auth.login'))
        
        # If an error occurred, show it to the user
        flash(error, 'danger')

    # If GET request, just show the page
    return render_template('auth/register.html')


@auth_bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        db = g.db_cursor
        error = None
        
        db.execute("SELECT * FROM Users WHERE email = %s", (email,))
        user = db.fetchone()

        if user is None:
            error = 'Incorrect email.'
        elif not check_password_hash(user['password_hash'], password):
            error = 'Incorrect password.'

        if error is None:
            # Login successful!
            # Store user data in the session
            session.clear()
            session['user_id'] = user['id']
            session['role'] = user['role']
            session['first_name'] = user['first_name']
            return redirect(url_for('main.dashboard'))

        flash(error, 'danger')

    return render_template('auth/login.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))