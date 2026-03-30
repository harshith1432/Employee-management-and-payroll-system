from datetime import datetime
from app.extensions import db

class Attendance(db.Model):
    __tablename__ = 'attendance'
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    date = db.Column(db.Date, default=lambda: datetime.now().date())
    clock_in = db.Column(db.DateTime)
    clock_out = db.Column(db.DateTime)
    status = db.Column(db.String(20), default='present') 
    location = db.Column(db.String(200))
    anomaly_flag = db.Column(db.Boolean, default=False)

class Payroll(db.Model):
    __tablename__ = 'payroll'
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    month = db.Column(db.Integer, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    basic_salary = db.Column(db.Float, nullable=False)
    allowances = db.Column(db.Float, default=0.0)
    bonuses = db.Column(db.Float, default=0.0)
    overtime = db.Column(db.Float, default=0.0)
    tax_deductions = db.Column(db.Float, default=0.0)
    pf_deductions = db.Column(db.Float, default=0.0)
    leave_deductions = db.Column(db.Float, default=0.0)
    net_salary = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default='pending')
    generated_at = db.Column(db.DateTime, default=datetime.now)
    paid_at = db.Column(db.DateTime)

class LeaveRequest(db.Model):
    __tablename__ = 'leave_requests'
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    leave_type = db.Column(db.String(50), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    reason = db.Column(db.Text)
    status = db.Column(db.String(20), default='pending')
    applied_on = db.Column(db.DateTime, default=datetime.now)
    approved_by = db.Column(db.Integer, db.ForeignKey('users.id'))

class PerformanceReview(db.Model):
    __tablename__ = 'performance_reviews'
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    reviewer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    rating = db.Column(db.Integer)
    feedback = db.Column(db.Text)
    review_date = db.Column(db.DateTime, default=datetime.now)

class Document(db.Model):
    __tablename__ = 'documents'
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    doc_name = db.Column(db.String(100), nullable=False)
    doc_type = db.Column(db.String(50))
    file_path = db.Column(db.String(200), nullable=False)
    uploaded_at = db.Column(db.DateTime, default=datetime.now)

class Schedule(db.Model):
    __tablename__ = 'schedules'
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    date = db.Column(db.Date, nullable=False, default=lambda: datetime.now().date())
    shift_start = db.Column(db.String(10), nullable=False, default="09:00")
    shift_end = db.Column(db.String(10), nullable=False, default="18:00")
    task_description = db.Column(db.Text)
    status = db.Column(db.String(20), default='assigned') # assigned, in_progress, completed
    created_at = db.Column(db.DateTime, default=datetime.now)

class DailyAgenda(db.Model):
    __tablename__ = 'daily_agendas'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, unique=True, nullable=False, default=lambda: datetime.now().date())
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.now)
