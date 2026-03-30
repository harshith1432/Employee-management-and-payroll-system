from flask import Blueprint, request, jsonify
from app.models import LeaveRequest, User
from app.extensions import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.utils.decorators import hr_required
from datetime import datetime

bp = Blueprint('leave', __name__, url_prefix='/api/leave')

@bp.route('/apply', methods=['POST'])
@jwt_required()
def apply_leave():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    data = request.get_json()
    new_request = LeaveRequest(
        employee_id=user.employee_profile.id,
        leave_type=data['leave_type'],
        start_date=datetime.strptime(data['start_date'], '%Y-%m-%d').date(),
        end_date=datetime.strptime(data['end_date'], '%Y-%m-%d').date(),
        reason=data.get('reason')
    )
    db.session.add(new_request)
    db.session.commit()
    return jsonify(msg="Leave applied successfully"), 201

@bp.route('/my-requests', methods=['GET'])
@jwt_required()
def my_requests():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    requests = LeaveRequest.query.filter_by(employee_id=user.employee_profile.id).all()
    return jsonify([{
        'id': r.id,
        'type': r.leave_type,
        'start': r.start_date.isoformat(),
        'end': r.end_date.isoformat(),
        'status': r.status
    } for r in requests]), 200

@bp.route('/pending', methods=['GET'])
@jwt_required()
@hr_required()
def pending_requests():
    requests = LeaveRequest.query.filter_by(status='pending').all()
    return jsonify([{
        'id': r.id,
        'emp_name': f"{r.employee.first_name} {r.employee.last_name}",
        'type': r.leave_type,
        'start': r.start_date.isoformat(),
        'end': r.end_date.isoformat(),
        'reason': r.reason
    } for r in requests]), 200

@bp.route('/action/<int:id>', methods=['POST'])
@jwt_required()
@hr_required()
def handle_leave(id):
    data = request.get_json()
    req = LeaveRequest.query.get_or_404(id)
    req.status = data['status'] 
    req.approved_by = get_jwt_identity()
    db.session.commit()
    return jsonify(msg=f"Leave {data['status']}"), 200
