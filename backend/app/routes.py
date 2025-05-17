from flask import jsonify, request, Blueprint, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from bson.objectid import ObjectId
import jwt
import datetime
import random
import string
from main import mongo, app, token_required
from models.models import create_user
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import re

# Create Blueprint
api = Blueprint('api', __name__)

# Store OTPs in-memory (for demo; use Redis or DB for production)
otp_store = {}

# Helper to send OTP email
def send_otp_email(recipient, otp):
    # Configure your SMTP server here
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    sender_email = 'ishansangani25@gmail.com'  # Replace with your email
    sender_password = 'your_app_password'   # Use app password or env var

    subject = 'Your AlzCare Registration OTP'
    body = f'Your OTP for registration is: {otp}'

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient, msg.as_string())
        server.quit()
        return True
    except Exception as e:
        print('Email send error:', e)
        return False

# OTP endpoint
@api.route('/send-otp', methods=['POST'])
def send_otp():
    data = request.get_json()
    email = data.get('email')
    if not email:
        return jsonify({'message': 'Email is required!'}), 400
    otp = ''.join(random.choices(string.digits, k=6))
    otp_store[email] = {'otp': otp, 'expires': datetime.datetime.utcnow() + datetime.timedelta(minutes=10)}
    if send_otp_email(email, otp):
        return jsonify({'message': 'OTP sent successfully'})
    else:
        return jsonify({'message': 'Failed to send OTP'}), 500

# Regex patterns for validation
EMAIL_REGEX = r"^[\w\.-]+@[\w\.-]+\.\w{2,}$"
PASSWORD_REGEX = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()_+\-=\[\]{};':\"\\|,.<>\/?]).{8,}$"

# Authentication routes
@api.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    # Email and password validation
    email = data.get('email', '')
    password = data.get('password', '')
    if not re.match(EMAIL_REGEX, email):
        return jsonify({'message': 'Invalid email format!'}), 400
    if not re.match(PASSWORD_REGEX, password):
        return jsonify({'message': 'Password must be at least 8 characters, include uppercase, lowercase, number, and special character!'}), 400

    # Check if device_id is provided
    if 'device_id' not in data or not data['device_id']:
        return jsonify({'message': 'Device ID is required!'}), 400

    # Check if device_id is already used in users or patients
    device_id = data['device_id']
    if mongo.db.users.find_one({'device_id': device_id}) or mongo.db.patients.find_one({'device_id': device_id}):
        return jsonify({'message': 'Device ID already in use!'}), 409

    # Check if user already exists
    if mongo.db.users.find_one({'email': email}):
        return jsonify({'message': 'User already exists!'}), 409

    # OTP verification
    otp = data.get('otp')
    if not otp or not email:
        return jsonify({'message': 'OTP and email required!'}), 400
    otp_entry = otp_store.get(email)
    if not otp_entry or otp_entry['otp'] != otp or otp_entry['expires'] < datetime.datetime.utcnow():
        return jsonify({'message': 'Invalid or expired OTP!'}), 400
    # Remove OTP after use
    otp_store.pop(email, None)

    # Remove username from data if present
    data.pop('username', None)

    # Create user document using model function
    user_id = create_user(data)

    # Optionally, create a patient record as well
    patient_name = data.get('patient_name')
    if patient_name:
        new_patient = {
            'name': patient_name,
            'caretaker_id': str(user_id),
            'device_id': data['device_id'],
            'created_at': datetime.datetime.utcnow()
        }
        mongo.db.patients.insert_one(new_patient)

    return jsonify({'message': 'User registered successfully!'}), 201

@api.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    user = mongo.db.users.find_one({'email': email})
    if not user:
        return jsonify({'message': 'Invalid credentials!'}), 401
    if check_password_hash(user['password'], password):
        token = jwt.encode({
            'user_id': str(user['_id']),
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
        }, app.config['SECRET_KEY'], algorithm="HS256")
        resp = make_response(jsonify({
            'user': {
                'id': str(user['_id']),
                'name': user['name'],
                'email': user['email'],
                'role': user['role']
            }
        }))
        resp.set_cookie('alz_token', token, httponly=True, samesite='Lax', max_age=24*3600)
        return resp
    return jsonify({'message': 'Invalid credentials!'}), 401

# Patient routes
@api.route('/patients', methods=['GET'])
@token_required
def get_patients(current_user):
    if current_user['role'] != 'caretaker':
        return jsonify({'message': 'Unauthorized!'}), 403
    
    patients = list(mongo.db.patients.find({'caretaker_id': str(current_user['_id'])}))
    
    # Convert ObjectId to string for JSON serialization
    for patient in patients:
        patient['_id'] = str(patient['_id'])
    
    return jsonify({'patients': patients})

@api.route('/patients', methods=['POST'])
@token_required
def add_patient(current_user):
    data = request.get_json()
    
    new_patient = {
        'name': data['name'],
        'age': data['age'],
        'device_id': data['device_id'],
        'caretaker_id': str(current_user['_id']),
        'created_at': datetime.datetime.utcnow()
    }
    
    patient_id = mongo.db.patients.insert_one(new_patient).inserted_id
    
    return jsonify({
        'message': 'Patient added successfully!',
        'patient_id': str(patient_id)
    }), 201

# Sensor data routes
@api.route('/sensor-data/<patient_id>', methods=['GET'])
@token_required
def get_sensor_data(current_user, patient_id):
    # Verify the patient belongs to the current caretaker
    patient = mongo.db.patients.find_one({'_id': ObjectId(patient_id), 'caretaker_id': str(current_user['_id'])})
    
    if not patient:
        return jsonify({'message': 'Patient not found or not authorized!'}), 404
    
    # Get latest sensor data
    latest_data = mongo.db.sensor_data.find_one(
        {'patient_id': patient_id},
        sort=[('timestamp', -1)]
    )
    
    if latest_data:
        latest_data['_id'] = str(latest_data['_id'])
        return jsonify({'data': latest_data})
    
    return jsonify({'message': 'No sensor data available'}), 404

# ML model prediction endpoint
@api.route('/predict/fall-detection', methods=['POST'])
@token_required
def predict_fall(current_user):
    data = request.get_json()
    
    # This endpoint would use the ML model to predict falls
    # For now, it's a placeholder
    
    # In a real implementation, you would:
    # 1. Load the joblib model
    # 2. Process sensor data
    # 3. Make predictions
    # 4. Return the results
    
    return jsonify({
        'prediction': 'fall_detected' if data['acceleration_z'] > 20 else 'normal',
        'confidence': 0.95
    })

# Register blueprint with app
app.register_blueprint(api, url_prefix='/api')
