# /ayursutra/app/patient.py

from flask import (
    Blueprint, render_template, request, redirect, url_for, flash, session, g
)
from app.decorators import login_required
import pymysql

patient_bp = Blueprint('patient', __name__, url_prefix='/patient')


@patient_bp.route('/schedule')
@login_required
def schedule():
    """Shows the patient's list of appointments."""
    db = g.db_cursor
    
    # Query to get all appointments for the logged-in patient
    # We JOIN with other tables to get the names
    query = """
        SELECT 
            appt.start_time, 
            appt.status, 
            th.name AS therapy_name, 
            u.first_name AS doc_first_name, 
            u.last_name AS doc_last_name
        FROM Appointments appt
        JOIN Therapies th ON appt.therapy_id = th.id
        JOIN Users u ON appt.practitioner_id = u.id
        WHERE appt.patient_id = %s
        ORDER BY appt.start_time DESC
    """
    db.execute(query, (session['user_id'],))
    appointments = db.fetchall()
    
    return render_template('patient/schedule.html', appointments=appointments)


@patient_bp.route('/book', methods=('GET', 'POST'))
@login_required
def book():
    """Shows a form to book a new appointment."""
    db = g.db_cursor
    
    if request.method == 'POST':
        # --- Handle the form submission ---
        therapy_id = request.form['therapy_id']
        practitioner_id = request.form['practitioner_id']
        start_time = request.form['start_time']
        
        try:
            # Insert the new 'pending' appointment
            db.execute(
                """
                INSERT INTO Appointments (patient_id, practitioner_id, therapy_id, start_time, status)
                VALUES (%s, %s, %s, %s, 'pending')
                """,
                (session['user_id'], practitioner_id, therapy_id, start_time)
            )
            g.db_conn.commit()
            flash('Appointment requested! You will be notified upon confirmation.', 'success')
            return redirect(url_for('patient.schedule'))
        except pymysql.Error as e:
            flash(f'An error occurred: {e}', 'danger')

    # --- Handle the GET request (show the form) ---
    # Fetch all therapies
    db.execute("SELECT id, name FROM Therapies")
    therapies = db.fetchall()
    
    # Fetch all practitioners
    db.execute("SELECT id, first_name, last_name FROM Users WHERE role = 'practitioner'")
    practitioners = db.fetchall()
    
    return render_template('patient/book.html', therapies=therapies, practitioners=practitioners)
@patient_bp.route('/feedback/<int:appointment_id>', methods=('GET', 'POST'))
@login_required
def feedback(appointment_id):
    """Shows a form to submit feedback for a specific appointment."""
    db = g.db_cursor
    
    if request.method == 'POST':
        # --- Handle the form submission ---
        rating = request.form['rating']
        symptoms = request.form['symptoms']
        improvements = request.form['improvements']
        
        try:
            # Insert the new feedback
            db.execute(
                """
                INSERT INTO Feedback (appointment_id, patient_id, rating, symptoms, improvements)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (appointment_id, session['user_id'], rating, symptoms, improvements)
            )
            g.db_conn.commit()
            flash('Thank you for your feedback!', 'success')
            return redirect(url_for('patient.schedule'))
        except pymysql.Error as e:
            # Check for duplicate entry (if they already submitted feedback)
            if e.args[0] == 1062: # Duplicate entry error
                flash('You have already submitted feedback for this appointment.', 'warning')
            else:
                flash(f'An error occurred: {e}', 'danger')
            return redirect(url_for('patient.schedule'))

    # --- Handle the GET request (show the form) ---
    # Get appointment details to show on the page
    db.execute(
        "SELECT th.name AS therapy_name, appt.start_time FROM Appointments appt "
        "JOIN Therapies th ON appt.therapy_id = th.id WHERE appt.id = %s",
        (appointment_id,)
    )
    appointment = db.fetchone()
    
    if appointment is None:
        flash('Appointment not found.', 'danger')
        return redirect(url_for('patient.schedule'))

    return render_template('patient/feedback.html', appointment=appointment, appointment_id=appointment_id)

# /ayursutra/app/patient.py
# ... (at the bottom of the file) ...
from flask import jsonify

@patient_bp.route('/progress')
@login_required
def progress():
    """Shows the patient's progress chart page."""
    return render_template('patient/progress.html')


@patient_bp.route('/api/progress_data')
@login_required
def progress_data():
    """Returns feedback data as JSON for the chart."""
    db = g.db_cursor
    
    # Get all feedback ratings for the logged-in patient, ordered by date
    db.execute(
        """
        SELECT DATE_FORMAT(created_at, '%%Y-%%m-%%d') AS date, rating
        FROM Feedback
        WHERE patient_id = %s
        ORDER BY created_at
        """,
        (session['user_id'],)
    )
    feedback_data = db.fetchall()
    
    # Format for Chart.js
    labels = [row['date'] for row in feedback_data]
    data = [row['rating'] for row in feedback_data]
    
    return jsonify({'labels': labels, 'data': data})