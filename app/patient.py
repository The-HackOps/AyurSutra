from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from app.decorators import login_required
from datetime import datetime

patient_bp = Blueprint('patient', __name__, url_prefix='/patient')

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
    return render_template('patient/schedule.html', appointments=MOCK_APPOINTMENTS)

@patient_bp.route('/book', methods=('GET', 'POST'))
@login_required
def book():
    if request.method == 'POST':
        flash('Appointment requested! You will be notified upon confirmation.', 'success')
        return redirect(url_for('patient.schedule'))

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
    return jsonify({
        'labels': ['2025-09-01', '2025-09-10', '2025-09-20'],
        'data': [4, 5, 8]
    })
@patient_bp.route('/feedback/<int:appointment_id>', methods=('GET', 'POST'))
@login_required
def feedback(appointment_id):
    """Handles the feedback submission for a specific appointment using mock data."""
    appointment = next((a for a in MOCK_APPOINTMENTS if a['id'] == appointment_id), None)

    if not appointment:
        flash('Appointment not found.', 'danger')
        return redirect(url_for('patient.schedule'))

    if request.method == 'POST':
        rating = request.form.get('rating')
        improvements = request.form.get('improvements')
        symptoms = request.form.get('symptoms')
        print(f"Feedback Received: Appt {appointment_id}, Rating {rating}")
        
        flash('Thank you for your feedback! Your practitioner has been notified.', 'success')
        return redirect(url_for('patient.schedule'))

    return render_template('patient/feedback.html', appointment=appointment, appointment_id=appointment_id)
