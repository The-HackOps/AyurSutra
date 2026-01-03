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
    patient = {'first_name': 'John', 'last_name': 'Doe'}
    return render_template('practitioner/progress.html', patient=patient, patient_id=patient_id)
