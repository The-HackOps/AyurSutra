from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from app.decorators import practitioner_required
from datetime import datetime

practitioner_bp = Blueprint('practitioner', __name__, url_prefix='/practitioner')

# --- MOCK DATA FOR DOCTOR ---
MOCK_APPOINTMENTS = [
    {
        'id': 101,
        'patient_id': 1,
        'start_time': datetime(2025, 10, 20, 10, 30),
        'status': 'pending',
        'therapy_name': 'Abhyanga',
        'patient_first_name': 'John',
        'patient_last_name': 'Doe'
    },
    {
        'id': 102,
        'patient_id': 1,
        'start_time': datetime(2025, 10, 22, 14, 00),
        'status': 'confirmed',
        'therapy_name': 'Shirodhara',
        'patient_first_name': 'John',
        'patient_last_name': 'Doe'
    }
]

# Mock Feedback for the doctor to "View"
MOCK_FEEDBACK = [
    {
        'patient_name': 'John Doe',
        'therapy': 'Abhyanga',
        'rating': 5,
        'improvements': 'Feeling much lighter and less stressed.',
        'symptoms': 'None'
    }
]

@practitioner_bp.route('/schedule')
@practitioner_required
def schedule():
    """Renders the schedule with mock appointments."""
    return render_template('practitioner/schedule.html', appointments=MOCK_APPOINTMENTS)

@practitioner_bp.route('/appointment/approve/<int:appointment_id>', methods=['POST'])
@practitioner_required
def approve(appointment_id):
    """Simulates approving an appointment."""
    flash(f'Appointment #{appointment_id} confirmed successfully!', 'success')
    return redirect(url_for('practitioner.schedule'))

@practitioner_bp.route('/patient/<int:patient_id>/progress')
@practitioner_required
def patient_progress(patient_id):
    """Renders the progress page for a specific patient."""
    # We use a static mock patient for the demo
    patient = {'first_name': 'John', 'last_name': 'Doe'}
    return render_template('practitioner/progress.html', patient=patient, patient_id=patient_id)

@practitioner_bp.route('/api/patient/<int:patient_id>/progress_data')
@practitioner_required
def patient_progress_data(patient_id):
    """Provides the JSON data for the Chart.js graph in progress.html."""
    return jsonify({
        'labels': ['Oct 01', 'Oct 05', 'Oct 10', 'Oct 15', 'Oct 20'],
        'data': [2, 3, 3, 4, 5] # Mock recovery scores
    })

@practitioner_bp.route('/feedback')
@practitioner_required
def view_feedback():
    """New route to view patient feedback comments."""
    return render_template('practitioner/feedback_list.html', feedbacks=MOCK_FEEDBACK)
