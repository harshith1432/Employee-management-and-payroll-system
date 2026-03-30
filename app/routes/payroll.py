from flask import Blueprint, request, jsonify
from app.models import Payroll, Employee, User
from app.services.payroll_service import PayrollService
from app.extensions import db
from app.utils.decorators import hr_required
from flask_jwt_extended import jwt_required, get_jwt_identity

bp = Blueprint('payroll', __name__, url_prefix='/api/payroll')

@bp.route('/generate', methods=['POST'])
@jwt_required()
@hr_required()
def generate_payroll():
    data = request.get_json()
    month = data.get('month')
    year = data.get('year')
    if not month or not year:
        return jsonify(msg="Month and Year required"), 400
    PayrollService.generate_monthly_payroll(db, Employee, Payroll, month, year)
    return jsonify(msg="Payroll generated successfully"), 201

@bp.route('/history', methods=['GET'])
@jwt_required()
def get_payroll_history():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    history = Payroll.query.filter_by(employee_id=user.employee_profile.id).order_by(Payroll.year.desc(), Payroll.month.desc()).all()
    return jsonify([{
        'month': p.month,
        'year': p.year,
        'net_salary': p.net_salary,
        'status': p.status
    } for p in history]), 200
