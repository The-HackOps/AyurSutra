from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from app.decorators import practitioner_required
from datetime import datetime

practitioner_bp = Blueprint('practitioner', __name__, url_prefix='/practitioner')

# --- MOCK DATA FOR DOCTOR ---
MOCK_PATIENT_LIST = [
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
        'patient_id': 2,
        'start_time': datetime(2025, 10, 21, 09, 00),
        'status': 'confirmed',
        'therapy_name': 'Shirodhara',
        'patient_first_name': 'Jane',
        'patient_last_name': 'Smith'
    }
]

@practitioner_bp.route('/schedule')
@practitioner_required
def schedule():
    return render_template('practitioner/schedule.html', appointments=MOCK_PATIENT_LIST)

@practitioner_bp.route('/appointment/approve/<int:appointment_id>', methods=['POST'])
@practitioner_required
def approve(appointment_id):
    flash(f'Appointment {appointment_id} confirmed successfully!', 'success')
    return redirect(url_for('practitioner.schedule'))

@practitioner_bp.route('/patient/<int:patient_id>/progress')
@practitioner_required
def patient_progress(patient_id):
    # In a real app, find patient by ID. For prototype, we use a generic mock.
    patient = {'first_name': 'John', 'last_name': 'Doe'}
    return render_template('practitioner/progress.html', patient=patient, patient_id=patient_id)

# --- NEW: ROUTE FOR CHART DATA ---
@practitioner_bp.route('/api/patient/<int:patient_id>/progress_data')
@practitioner_required
def patient_progress_data(patient_id):
    """Returns mock feedback data for the Chart.js line graph."""
    return jsonify({
        'labels': ['Day 1', 'Day 3', 'Day 5', 'Day 7'],
        'data': [2, 3, 4, 5]  # Mock recovery ratings
    })
