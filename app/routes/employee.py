from flask import Blueprint, request, jsonify
from app.models import User, Employee
from app.utils.decorators import hr_required
from app.extensions import db
from flask_jwt_extended import jwt_required, get_jwt

bp = Blueprint('employee', __name__, url_prefix='/api/employee')

@bp.route('/', methods=['GET'])
@jwt_required()
@hr_required()
def get_employees():
    employees = Employee.query.all()
    output = []
    for emp in employees:
        user = User.query.get(emp.user_id)
        output.append({
            'id': emp.id,
            'emp_id': emp.emp_id,
            'name': f"{emp.first_name} {emp.last_name}",
            'department': emp.department,
            'designation': emp.designation,
            'salary': emp.salary_base,
            'is_active': user.is_active if user else False,
            'is_verified': emp.is_verified
        })
    return jsonify(output), 200

@bp.route('/<int:id>', methods=['GET'])
@jwt_required()
def get_employee(id):
    emp = Employee.query.get_or_404(id)
    return jsonify({
        'id': emp.id,
        'emp_id': emp.emp_id,
        'first_name': emp.first_name,
        'last_name': emp.last_name,
        'department': emp.department,
        'designation': emp.designation,
        'salary_base': emp.salary_base
    }), 200

@bp.route('/', methods=['POST'])
@jwt_required()
@hr_required()
def add_employee():
    data = request.get_json()
    claims = get_jwt()
    current_role = claims.get('role')
    
    required_fields = ['emp_id', 'email', 'first_name', 'last_name']
    for field in required_fields:
        if not data.get(field):
            return jsonify({"error": f"Field '{field}' is required"}), 400

    if Employee.query.filter_by(emp_id=data['emp_id']).first():
        return jsonify({"error": f"Employee ID '{data['emp_id']}' already exists"}), 400
        
    try:
        user = User.query.filter_by(email=data['email']).first()
        if user:
            if user.employee_profile:
                return jsonify({"error": "A profile already exists for this email address"}), 400
        else:
            temp_password = data.get('password') or 'Welcome@123'
            user = User(email=data['email'], role=data.get('role', 'employee'), must_change_password=True)
            user.set_password(temp_password)
            db.session.add(user)
            db.session.flush()

        is_verified = False
        target_role = data.get('role', 'employee')
        
        if current_role == 'hr':
            is_verified = True 
        elif current_role == 'admin':
            if target_role == 'hr':
                is_verified = True 
            else:
                is_verified = False 

        new_emp = Employee(
            user_id=user.id,
            emp_id=data['emp_id'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            department=data.get('department'),
            designation=data.get('designation'),
            salary_base=float(data.get('salary_base', 0)),
            is_verified=is_verified
        )
        
        db.session.add(new_emp)
        db.session.commit()
        
        msg = f"Personnel {new_emp.emp_id} onboarded successfully"
        return jsonify({"msg": msg, "verified": is_verified, "id": new_emp.id}), 201

    except Exception as e:
        db.session.rollback()
        print(f"ONBOARDING ERROR: {str(e)}") # Log for debugging
        return jsonify({"error": "Failed to onboard personnel", "details": str(e)}), 500

@bp.route('/verify/<int:id>', methods=['POST'])
@jwt_required()
@hr_required()
def verify_employee(id):
    emp = Employee.query.get_or_404(id)
    emp.is_verified = True
    db.session.commit()
    return jsonify({"msg": f"Employee {emp.emp_id} verified successfully"}), 200

@bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
@hr_required()
def update_employee(id):
    emp = Employee.query.get_or_404(id)
    data = request.get_json()
    
    if 'first_name' in data: emp.first_name = data['first_name']
    if 'last_name' in data: emp.last_name = data['last_name']
    if 'department' in data: emp.department = data['department']
    if 'designation' in data: emp.designation = data['designation']
    if 'salary_base' in data: emp.salary_base = float(data['salary_base'])
    
    db.session.commit()
    return jsonify({"msg": "Employee records updated successfully"}), 200

@bp.route('/<int:id>/status', methods=['PATCH'])
@jwt_required()
@hr_required()
def toggle_employee_status(id):
    emp = Employee.query.get_or_404(id)
    user = User.query.get(emp.user_id)
    if not user:
        return jsonify({"error": "Associated security account not found"}), 404
        
    user.is_active = not user.is_active
    db.session.commit()
    
    status_label = "ACTIVE" if user.is_active else "INACTIVE"
    return jsonify({"msg": f"Personnel account marked as {status_label}", "is_active": user.is_active}), 200

@bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
@hr_required()
def delete_employee(id):
    emp = Employee.query.get_or_404(id)
    user = User.query.get(emp.user_id)
    try:
        if user:
            db.session.delete(user)
        else:
            db.session.delete(emp)
        db.session.commit()
        return jsonify({"msg": "Personnel profile and history purged from matrix"}), 200
    except Exception as e:
        db.session.rollback()
        print(f"PURGE ERROR: {str(e)}") # Log for debugging
        return jsonify({"error": "Failed to purge record. This typically occurs if the personnel is referenced in active logs (e.g., as a reviewer or approver).", "details": str(e)}), 500

@bp.route('/<int:id>/history', methods=['GET'])
@jwt_required()
@hr_required()
def get_employee_history(id):
    emp = Employee.query.get_or_404(id)
    
    attendance = [{
        'date': str(att.date),
        'status': att.status
    } for att in emp.attendance]
    
    payroll = [{
        'month': pay.month,
        'year': pay.year,
        'net_salary': pay.net_salary,
        'status': pay.status,
        'generated_at': pay.generated_at.isoformat() if pay.generated_at else None
    } for pay in emp.payroll]
    
    schedules = [{
        'date': str(s.date),
        'shift_start': s.shift_start,
        'shift_end': s.shift_end,
        'task': s.task_description,
        'status': s.status
    } for s in emp.schedules]
    
    performance = [{
        'rating': r.rating,
        'feedback': r.feedback,
        'date': r.review_date.strftime('%Y-%m-%d') if r.review_date else None
    } for r in emp.performance]

    leaves = [{
        'type': l.leave_type,
        'start': str(l.start_date),
        'end': str(l.end_date),
        'status': l.status,
        'reason': l.reason
    } for l in emp.leaves]

    return jsonify({
        'attendance': attendance,
        'payroll': payroll,
        'schedules': schedules,
        'performance': performance,
        'leaves': leaves,
        'metadata': {
            'is_active': User.query.get(emp.user_id).is_active if emp.user_id else False,
            'is_verified': emp.is_verified
        }
    }), 200
