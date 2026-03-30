from datetime import datetime, timedelta
from flask import Blueprint, render_template, request, jsonify
from app.models import Employee, Attendance, Payroll, LeaveRequest, User, DailyAgenda
from app.extensions import db
from sqlalchemy import func
from app.utils.decorators import hr_required, admin_required, employee_required
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

bp = Blueprint('dashboard', __name__)

@bp.route('/')
def index():
    return render_template('admin/dashboard.html')

@bp.route('/hr')
def hr_dashboard():
    return render_template('hr/dashboard.html')

@bp.route('/employee')
def employee_dashboard():
    return render_template('employee/dashboard.html')

@bp.route('/login')
def login():
    return render_template('auth/login.html')

@bp.route('/register')
def register():
    return render_template('auth/register.html')

@bp.route('/employees')
def employees():
    return render_template('admin/employees.html')

@bp.route('/attendance')
def attendance():
    return render_template('admin/attendance.html')

@bp.route('/payroll')
def payroll():
    return render_template('admin/payroll.html')

@bp.route('/leaves')
def leaves():
    return render_template('admin/leaves.html')

@bp.route('/transactions')
def transactions():
    return render_template('admin/transactions.html')

@bp.route('/api/dashboard/stats', methods=['GET'])
@jwt_required()
def get_stats():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    total_employees = Employee.query.count()
    dept_stats = db.session.query(Employee.department, func.count(Employee.id)).group_by(Employee.department).all()
    
    # Real-time Payroll: Distributed (net_salary) + Current Month Accumulations
    distributed_payroll = db.session.query(func.sum(Payroll.net_salary)).first()[0] or 0
    accumulated_payroll = db.session.query(func.sum(Employee.accumulated_pay)).first()[0] or 0
    total_payroll = distributed_payroll + accumulated_payroll
    
    user_accumulated = 0.0
    if user.employee_profile:
        user_accumulated = user.employee_profile.accumulated_pay
    
    # Present today - using Title Case 'Present'
    today = datetime.now().date()
    present_today = Attendance.query.filter_by(date=today, status='Present').count()
    
    # Today's Agenda
    agenda = DailyAgenda.query.filter_by(date=today).first()
    agenda_is_set = agenda is not None
    agenda_data = {
        'title': agenda.title if agenda_is_set else "No Agenda Set",
        'description': agenda.description if agenda_is_set else "HR has not assigned today's main agenda yet.",
        'is_set': agenda_is_set
    }
    
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
        'total_payroll_expense': round(total_payroll, 2),
        'distributed_payroll': round(distributed_payroll, 2),
        'pending_payload': round(accumulated_payroll, 2),
        'present_today': present_today,
        'attendance_trend': attendance_trend,
        'accumulated_pay': round(user_accumulated, 2),
        'today_agenda': agenda_data,
        'agenda_is_set': agenda_is_set
    }), 200
