
from functools import wraps
from flask import session, redirect, url_for, g
from functools import wraps
from flask import session, redirect, url_for, g, flash

def login_required(view):
    @wraps(view)
    def wrapped_view(**kwargs):
        if 'user_id' not in session:
            return redirect(url_for('auth.login'))
        db = g.db_cursor
        if db:
            db.execute("SELECT * FROM Users WHERE id = %s", (session['user_id'],))
            g.user = db.fetchone()
        else:
            g.user = None
            
        return view(**kwargs)
    return wrapped_view

def practitioner_required(view):
    @wraps(view)
    def wrapped_view(**kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('auth.login'))
        
        if session.get('role') != 'practitioner':
            flash('You do not have permission to access this page.', 'danger')
            return redirect(url_for('main.dashboard'))
        db = g.db_cursor
        if db:
            db.execute("SELECT * FROM Users WHERE id = %s", (session['user_id'],))
            g.user = db.fetchone()
        else:
            g.user = None
            
        return view(**kwargs)
    return wrapped_view
