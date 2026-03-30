from datetime import datetime, timedelta
from flask import Blueprint, render_template, request, jsonify
from app.models import Employee, Attendance, Payroll, LeaveRequest
from app.extensions import db
from sqlalchemy import func
from app.utils.decorators import hr_required, admin_required, employee_required
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from flask import redirect, url_for

bp = Blueprint('dashboard', __name__)

@bp.route('/')
def index():
    # If no login, sidebar script in base.html handles /login redirect
    # Root renders admin by default if role is admin
    return render_template('admin/dashboard.html')

@bp.route('/hr')
def hr_dashboard():
    return render_template('hr/dashboard.html')

@bp.route('/employee')
def employee_dashboard():
    return render_template('employee/dashboard.html')

@bp.route('/login')
def login_page():
    return render_template('auth/login.html')

@bp.route('/register')
def register_page():
    return render_template('auth/register.html')

@bp.route('/reset-password')
def reset_password_page():
    return render_template('auth/reset_password.html')

@bp.route('/employees')
def employee_list_page():
    return render_template('admin/employees.html')

@bp.route('/attendance')
def attendance_page():
    return render_template('admin/attendance.html')

@bp.route('/payroll')
def payroll_page():
    return render_template('admin/payroll.html')

@bp.route('/leaves')
def leave_page():
    return render_template('admin/leaves.html')

@bp.route('/api/dashboard/stats', methods=['GET'])
@jwt_required()
def get_stats():
    total_employees = Employee.query.count()
    dept_stats = db.session.query(Employee.department, func.count(Employee.id)).group_by(Employee.department).all()
    total_payroll = db.session.query(func.sum(Payroll.net_salary)).first()[0] or 0
    
    # Present today
    today = datetime.now().date()
    present_today = Attendance.query.filter_by(date=today, status='Present').count()
    
    # Attendance Trend (Last 7 days)
    attendance_trend = []
    for i in range(6, -1, -1):
        day = today - timedelta(days=i)
        count = Attendance.query.filter_by(date=day, status='Present').count()
        attendance_trend.append({
            'date': day.strftime('%b %d'),
            'count': count
        })
    
    return jsonify({
        'total_employees': total_employees,
        'department_distribution': {d: c for d, c in dept_stats},
        'total_payroll_expense': total_payroll,
        'present_today': present_today,
        'attendance_trend': attendance_trend
    }), 200
