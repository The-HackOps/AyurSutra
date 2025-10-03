# /ayursutra/app/auth.py

from flask import (
    Blueprint, render_template, request, redirect, url_for, flash, session, g
)
from werkzeug.security import check_password_hash, generate_password_hash
import pymysql

# Import our updated RegistrationForm
from .forms import RegistrationForm

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


@auth_bp.route('/register', methods=('GET', 'POST'))
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        db = g.db_cursor
        
        # Check if user already exists
        db.execute("SELECT id FROM Users WHERE email = %s", (form.email.data,))
        if db.fetchone() is not None:
            flash(f"User {form.email.data} is already registered.", 'warning')
            return redirect(url_for('auth.login'))

        # Insert the new user into the Users table using data from the form
        if form.password.data is None:
            flash("Password is required.", "danger")
            return render_template('auth/register.html', form=form)
        db.execute(
            "INSERT INTO Users (email, password_hash, first_name, last_name, role) VALUES (%s, %s, %s, %s, %s)",
            (form.email.data, generate_password_hash(form.password.data), form.first_name.data, form.last_name.data, form.role.data)
        )
        new_user_id = db.lastrowid
        
        # Insert into the correct role-specific table
        role = form.role.data
        if role == 'patient':
            db.execute("INSERT INTO Patients (user_id) VALUES (%s)", (new_user_id,))
        elif role == 'practitioner' or role == 'doctor': # Accept both terms
            db.execute("INSERT INTO Practitioners (user_id) VALUES (%s)", (new_user_id,))
        
        g.db_conn.commit()
        
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/register.html', form=form)


@auth_bp.route('/login', methods=('GET', 'POST'))
def login():
    # No changes needed here, but keeping it consistent
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