from flask import Blueprint, request, jsonify
from app.models import Attendance, User
from app.extensions import db
from datetime import datetime
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.utils.decorators import hr_required

bp = Blueprint('attendance', __name__, url_prefix='/api/attendance')

@bp.route('/clock-in', methods=['POST'])
@jwt_required()
def clock_in():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if not user.employee_profile:
        return jsonify(msg="Employee profile not found"), 404
        
    today = datetime.utcnow().date()
    existing = Attendance.query.filter_by(employee_id=user.employee_profile.id, date=today).first()
    if existing:
        return jsonify(msg="Already clocked in today"), 400
        
    data = request.get_json()
    new_attendance = Attendance(
        employee_id=user.employee_profile.id,
        clock_in=datetime.utcnow(),
        location=data.get('location')
    )
    db.session.add(new_attendance)
    db.session.commit()
    return jsonify(msg="Clocked in successfully"), 201

@bp.route('/clock-out', methods=['POST'])
@jwt_required()
def clock_out():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    today = datetime.utcnow().date()
    attendance = Attendance.query.filter_by(employee_id=user.employee_profile.id, date=today).first()
    if not attendance:
        return jsonify(msg="No clock-in record found for today"), 400
    if attendance.clock_out:
        return jsonify(msg="Already clocked out today"), 400
    attendance.clock_out = datetime.utcnow()
    db.session.commit()
    return jsonify(msg="Clocked out successfully"), 200

@bp.route('/mark', methods=['POST'])
@jwt_required()
@hr_required()
def mark_attendance():
    data = request.get_json()
    emp_id = data.get('employee_id')
    date_str = data.get('date', datetime.utcnow().strftime('%Y-%m-%d'))
    status = data.get('status', 'Present') # Present, Absent, Half-Day, On Leave
    
    date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
    
    attendance = Attendance.query.filter_by(employee_id=emp_id, date=date_obj).first()
    if attendance:
        attendance.status = status
        if status == 'Present' and not attendance.clock_in:
            attendance.clock_in = datetime.utcnow()
    else:
        attendance = Attendance(
            employee_id=emp_id,
            date=date_obj,
            status=status,
            clock_in=datetime.utcnow() if status == 'Present' else None
        )
        db.session.add(attendance)
    
    db.session.commit()
    return jsonify(msg=f"Attendance status synced: {status}"), 200

@bp.route('/history', methods=['GET'])
@jwt_required()
def get_history():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    claims = get_jwt()
    current_role = claims.get('role')

    # If HR/Admin, allow viewing any employee's history if ID is provided
    target_id = request.args.get('employee_id')
    if target_id and current_role in ['admin', 'hr']:
        history = Attendance.query.filter_by(employee_id=target_id).order_by(Attendance.date.desc()).all()
    else:
        if not user.employee_profile:
             return jsonify(msg="Profile not found"), 404
        history = Attendance.query.filter_by(employee_id=user.employee_profile.id).order_by(Attendance.date.desc()).all()

    return jsonify([{
        'date': att.date.isoformat(),
        'clock_in': att.clock_in.isoformat() if att.clock_in else None,
        'clock_out': att.clock_out.isoformat() if att.clock_out else None,
        'status': att.status
    } for att in history]), 200
