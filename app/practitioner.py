# /ayursutra/app/practitioner.py

from flask import (
    Blueprint, render_template, request, redirect, url_for, flash, session, g, jsonify
)
from app.decorators import practitioner_required
import pymysql

practitioner_bp = Blueprint('practitioner', __name__, url_prefix='/practitioner')


@practitioner_bp.route('/schedule')
@practitioner_required
def schedule():
    """Shows the practitioner's list of all appointments."""
    db = g.db_cursor
    
    query = """
        SELECT 
            appt.id, 
            appt.start_time, 
            appt.status, 
            th.name AS therapy_name, 
            u.first_name AS patient_first_name, 
            u.last_name AS patient_last_name,
            u.id AS patient_id  -- <-- !! MODIFIED: ADDED THIS LINE !!
        FROM Appointments appt
        JOIN Therapies th ON appt.therapy_id = th.id
        JOIN Users u ON appt.patient_id = u.id
        WHERE appt.practitioner_id = %s
        ORDER BY appt.start_time DESC
    """
    db.execute(query, (session['user_id'],))
    appointments = db.fetchall()
    
    return render_template('practitioner/schedule.html', appointments=appointments)


@practitioner_bp.route('/appointment/approve/<int:appointment_id>', methods=['POST'])
@practitioner_required
def approve(appointment_id):
    # ... (this function is unchanged) ...
    db = g.db_cursor
    try:
        db.execute(
            "UPDATE Appointments SET status = 'confirmed' WHERE id = %s AND practitioner_id = %s",
            (appointment_id, session['user_id'])
        )
        g.db_conn.commit()
        flash('Appointment confirmed successfully!', 'success')
    except pymysql.Error as e:
        flash(f'An error occurred: {e}', 'danger')
    return redirect(url_for('practitioner.schedule'))


@practitioner_bp.route('/appointment/cancel/<int:appointment_id>', methods=['POST'])
@practitioner_required
def cancel(appointment_id):
    # ... (this function is unchanged) ...
    db = g.db_cursor
    try:
        db.execute(
            "UPDATE Appointments SET status = 'cancelled' WHERE id = %s AND practitioner_id = %s",
            (appointment_id, session['user_id'])
        )
        g.db_conn.commit()
        flash('Appointment cancelled.', 'info')
    except pymysql.Error as e:
        flash(f'An error occurred: {e}', 'danger')
    return redirect(url_for('practitioner.schedule'))


# --- !! ADD THESE TWO NEW ROUTES !! ---

@practitioner_bp.route('/patient/<int:patient_id>/progress')
@practitioner_required
def patient_progress(patient_id):
    """Shows the progress chart page for a specific patient."""
    db = g.db_cursor
    # Get patient's name for the title
    db.execute("SELECT first_name, last_name FROM Users WHERE id = %s", (patient_id,))
    patient = db.fetchone()
    if patient is None:
        flash('Patient not found.', 'danger')
        return redirect(url_for('practitioner.schedule'))
        
    return render_template('practitioner/progress.html', patient=patient, patient_id=patient_id)


@practitioner_bp.route('/api/patient/<int:patient_id>/progress_data')
@practitioner_required
def patient_progress_data(patient_id):
    """Returns feedback data for a specific patient as JSON."""
    db = g.db_cursor
    
    # Get all feedback ratings for the specified patient
    db.execute(
        """
        SELECT DATE_FORMAT(created_at, '%%Y-%%m-%%d') AS date, rating
        FROM Feedback
        WHERE patient_id = %s
        ORDER BY created_at
        """,
        (patient_id,)
    )
    feedback_data = db.fetchall()
    
    # Format for Chart.js
    labels = [row['date'] for row in feedback_data]
    data = [row['rating'] for row in feedback_data]
    
    return jsonify({'labels': labels, 'data': data})