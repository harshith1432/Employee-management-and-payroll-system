from datetime import datetime
from app.extensions import db, login_manager, bcrypt
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='employee')
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    must_change_password = db.Column(db.Boolean, default=False)
    
    employee_profile = db.relationship('Employee', backref='user', uselist=False, cascade="all, delete-orphan")

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

class Employee(db.Model):
    __tablename__ = 'employees'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True)
    emp_id = db.Column(db.String(20), unique=True, nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    department = db.Column(db.String(50))
    designation = db.Column(db.String(50))
    phone = db.Column(db.String(20))
    address = db.Column(db.Text)
    joining_date = db.Column(db.Date, default=datetime.utcnow().date)
    salary_base = db.Column(db.Float, default=0.0)
    profile_photo = db.Column(db.String(200))
    is_verified = db.Column(db.Boolean, default=False)
    
    attendance = db.relationship('Attendance', backref='employee', lazy=True, cascade="all, delete-orphan")
    payroll = db.relationship('Payroll', backref='employee', lazy=True, cascade="all, delete-orphan")
    leaves = db.relationship('LeaveRequest', backref='employee', lazy=True, cascade="all, delete-orphan")
    performance = db.relationship('PerformanceReview', backref='employee', lazy=True, cascade="all, delete-orphan")
    documents = db.relationship('Document', backref='employee', lazy=True, cascade="all, delete-orphan")
    schedules = db.relationship('Schedule', backref='employee', lazy=True, cascade="all, delete-orphan")
