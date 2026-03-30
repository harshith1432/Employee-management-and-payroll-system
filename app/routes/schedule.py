from flask import Blueprint, request, jsonify
from app.models import Employee, Schedule
from app.extensions import db
from app.utils.decorators import hr_required, admin_required, employee_required
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime

bp = Blueprint('schedule', __name__, url_prefix='/api/schedule')

@bp.route('/assign', methods=['POST'])
@jwt_required()
@hr_required()
def assign_schedule():
    data = request.get_json()
    emp_id = data.get('employee_id')
    emp = Employee.query.get_or_404(emp_id)
    
    date_str = data.get('date', datetime.utcnow().date().isoformat())
    date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
    
    schedule = Schedule(
        employee_id=emp.id,
        date=date_obj,
        shift_start=data.get('shift_start', '09:00'),
        shift_end=data.get('shift_end', '18:00'),
        task_description=data.get('task', 'Standard Operational Duties'),
        status='assigned'
    )
    
    db.session.add(schedule)
    db.session.commit()
    
    return jsonify({
        "msg": "Mission sequence committed to personnel schedule",
        "employee": f"{emp.first_name} {emp.last_name}"
    }), 201

@bp.route('/my', methods=['GET'])
@jwt_required()
@employee_required()
def get_my_schedule():
    user_id = get_jwt_identity()
    emp = Employee.query.filter_by(user_id=user_id).first()
    if not emp:
        return jsonify({"error": "Profile not found"}), 404
        
    today = datetime.utcnow().date()
    schedules = Schedule.query.filter_by(employee_id=emp.id, date=today).all()
    
    return jsonify([{
        'id': s.id,
        'shift_start': s.shift_start,
        'shift_end': s.shift_end,
        'task': s.task_description,
        'status': s.status
    } for s in schedules]), 200

@bp.route('/employee/<int:id>', methods=['GET'])
@jwt_required()
@hr_required()
def get_employee_schedules(id):
    schedules = Schedule.query.filter_by(employee_id=id).order_by(Schedule.date.desc()).limit(10).all()
    return jsonify([{
        'date': str(s.date),
        'shift': f"{s.shift_start} - {s.shift_end}",
        'task': s.task_description,
        'status': s.status
    } for s in schedules]), 200
