from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from app.decorators import login_required
from datetime import datetime

patient_bp = Blueprint('patient', __name__, url_prefix='/patient')

# --- MOCK DATA FOR PATIENT ---
MOCK_APPOINTMENTS = [
    {
        'id': 101,
        'start_time': datetime(2025, 10, 20, 10, 30),
        'status': 'confirmed',
        'therapy_name': 'Abhyanga (Massage)',
        'doc_first_name': 'Ayur',
        'doc_last_name': 'Sutra'
    },
    {
        'id': 102,
        'start_time': datetime(2025, 10, 25, 14, 00),
        'status': 'pending',
        'therapy_name': 'Shirodhara',
        'doc_first_name': 'Ayur',
        'doc_last_name': 'Sutra'
    }
]

@patient_bp.route('/schedule')
@login_required
def schedule():
    # We pass the mock list instead of querying the DB
    return render_template('patient/schedule.html', appointments=MOCK_APPOINTMENTS)

@patient_bp.route('/book', methods=('GET', 'POST'))
@login_required
def book():
    if request.method == 'POST':
        # Simulate a successful booking
        flash('Appointment requested! You will be notified upon confirmation.', 'success')
        return redirect(url_for('patient.schedule'))

    # Mock data for the dropdowns in the booking form
    therapies = [{'id': 1, 'name': 'Abhyanga'}, {'id': 2, 'name': 'Shirodhara'}]
    practitioners = [{'id': 2, 'first_name': 'Ayur', 'last_name': 'Sutra'}]
    
    return render_template('patient/book.html', therapies=therapies, practitioners=practitioners)

@patient_bp.route('/progress')
@login_required
def progress():
    return render_template('patient/progress.html')

@patient_bp.route('/api/progress_data')
@login_required
def progress_data():
    # Mock data for Chart.js
    return jsonify({
        'labels': ['2025-09-01', '2025-09-10', '2025-09-20'],
        'data': [4, 5, 8] # Recovery scores
    })
