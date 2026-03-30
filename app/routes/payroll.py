from flask import Blueprint, request, jsonify, send_file
from datetime import datetime
from app.models import Payroll, Employee, User
from app.services.payroll_service import PayrollService
from app.utils.pdf_utils import PDFGenerator
from app.extensions import db
from app.utils.decorators import hr_required
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

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

@bp.route('/distribute', methods=['POST'])
@jwt_required()
@hr_required() # Or admin_required if you prefer, but the user requested 'Admin button'
def distribute_salaries():
    now = datetime.now()
    month = now.month
    year = now.year
    
    employees = Employee.query.filter(Employee.accumulated_pay > 0).all()
    if not employees:
        return jsonify(msg="No pending salaries to distribute"), 400
        
    distributed_records = []
    for emp in employees:
        payroll = Payroll(
            employee_id=emp.id,
            month=month,
            year=year,
            basic_salary=emp.salary_base, # This is the monthly total
            net_salary=round(emp.accumulated_pay, 2), # This is what they earned this month so far
            status='paid',
            paid_at=now
        )
        db.session.add(payroll)
        
        # Log the payload for return/UI tracking
        distributed_records.append({
            "emp_id": emp.emp_id,
            "name": f"{emp.first_name} {emp.last_name}",
            "amount": round(emp.accumulated_pay, 2)
        })
        
        # Reset to zero
        emp.accumulated_pay = 0.0
    
    db.session.commit()
    
    return jsonify({
        "msg": f"Successfully distributed salaries to {len(employees)} employees.",
        "payload": distributed_records,
        "total_distributed": sum(r['amount'] for r in distributed_records)
    }), 200

@bp.route('/history', methods=['GET'])
@jwt_required()
def get_payroll_history():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    claims = get_jwt()
    current_role = claims.get('role')

    if current_role in ['admin', 'hr']:
        # If admin/hr, we can see all or filter by search/month/year
        month = request.args.get('month', type=int)
        year = request.args.get('year', type=int)
        query = Payroll.query
        if month: query = query.filter_by(month=month)
        if year: query = query.filter_by(year=year)
        history = query.order_by(Payroll.year.desc(), Payroll.month.desc()).all()
    else:
        history = Payroll.query.filter_by(employee_id=user.employee_profile.id).order_by(Payroll.year.desc(), Payroll.month.desc()).all()

    return jsonify([{
        'id': p.id,
        'emp_id': p.employee.emp_id,
        'name': f"{p.employee.first_name} {p.employee.last_name}",
        'month': p.month,
        'year': p.year,
        'net_salary': p.net_salary,
        'status': p.status
    } for p in history]), 200

@bp.route('/download-report', methods=['GET'])
@jwt_required()
@hr_required()
def download_report():
    month = request.args.get('month', type=int)
    year = request.args.get('year', type=int)
    if not month or not year:
        return jsonify(msg="Month and Year required"), 400
    
    payrolls = Payroll.query.filter_by(month=month, year=year).all()
    pdf_buffer = PDFGenerator.generate_monthly_report(payrolls, month, year)
    
    return send_file(
        pdf_buffer,
        as_attachment=True,
        download_name=f"Payroll_Report_{month}_{year}.pdf",
        mimetype='application/pdf'
    )

@bp.route('/download-slip/<int:payroll_id>', methods=['GET'])
@jwt_required()
def download_slip(payroll_id):
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    claims = get_jwt()
    current_role = claims.get('role')
    
    payroll = Payroll.query.get_or_404(payroll_id)
    
    # Security: Ensure only the owner or HR/Admin can download
    if current_role not in ['admin', 'hr'] and payroll.employee_id != user.employee_profile.id:
        return jsonify(msg="Unauthorized access to salary slip"), 403
        
    pdf_buffer = PDFGenerator.generate_salary_slip(payroll.employee, payroll)
    
    return send_file(
        pdf_buffer,
        as_attachment=True,
        download_name=f"Salary_Slip_{payroll.month}_{payroll.year}.pdf",
        mimetype='application/pdf'
    )
