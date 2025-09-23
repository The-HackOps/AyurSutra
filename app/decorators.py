# /ayursutra/app/decorators.py

from functools import wraps
from flask import session, redirect, url_for, g
from functools import wraps
from flask import session, redirect, url_for, g, flash

def login_required(view):
    @wraps(view)
    def wrapped_view(**kwargs):
        if 'user_id' not in session:
            # If user is not logged in, redirect to login page
            return redirect(url_for('auth.login'))
        
        # If user is logged in, load their info into 'g'
        # This makes g.user available in all protected templates
        db = g.db_cursor
        
        # Add a check in case db_cursor is None
        if db:
            db.execute("SELECT * FROM Users WHERE id = %s", (session['user_id'],))
            g.user = db.fetchone()
        else:
            g.user = None # or handle error
            
        return view(**kwargs)
    return wrapped_view

def practitioner_required(view):
    @wraps(view)
    def wrapped_view(**kwargs):
        # First, check if they are logged in at all
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('auth.login'))
        
        # Then, check if they are a practitioner
        if session.get('role') != 'practitioner':
            flash('You do not have permission to access this page.', 'danger')
            return redirect(url_for('main.dashboard')) # Send them to their own dashboard
        
        # If they are logged in and are a practitioner, load their data
        db = g.db_cursor
        if db:
            db.execute("SELECT * FROM Users WHERE id = %s", (session['user_id'],))
            g.user = db.fetchone()
        else:
            g.user = None
            
        return view(**kwargs)
    return wrapped_view