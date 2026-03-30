from app import create_app, db
from app.models.user import User, Employee
from app.models.core import Attendance, LeaveRequest, Payroll
from datetime import datetime, timedelta
import random

app = create_app()

with app.app_context():
    # Only seed if employees don't exist
    if Employee.query.count() == 0:
        print("Seeding sample data...")
        
        departments = ['Engineering', 'HR', 'Marketing', 'Sales', 'Finance']
        designations = ['Manager', 'Developer', 'Designer', 'Analyst']
        
        for i in range(1, 6):
            name = f"Employee {i}"
            email = f"emp{i}@hrms.com"
            
            # Create User
            user = User(email=email, role='employee')
            user.set_password('Pass@123')
            db.session.add(user)
            db.session.flush()
            
            # Create Employee
            emp = Employee(
                user_id=user.id,
                first_name=name.split()[0],
                last_name=name.split()[1],
                emp_id=f"EMP00{i}",
                department=random.choice(departments),
                designation=random.choice(designations),
                joining_date=datetime.utcnow().date() - timedelta(days=365),
                salary_base=50000.0 + (i * 5000)
            )
            db.session.add(emp)
            db.session.flush()
            
            # Create some attendance records
            for d in range(5):
                date = datetime.utcnow() - timedelta(days=d)
                clock_in = datetime(date.year, date.month, date.day, 9, 0) + timedelta(minutes=random.randint(0, 30))
                clock_out = datetime(date.year, date.month, date.day, 17, 0) + timedelta(minutes=random.randint(0, 30))
                
                attendance = Attendance(
                    employee_id=emp.id,
                    date=date.date(),
                    clock_in=clock_in,
                    clock_out=clock_out,
                    status='Present'
                )
                db.session.add(attendance)
            
            # Create a leave request
            leave = LeaveRequest(
                employee_id=emp.id,
                leave_type='Sick Leave',
                start_date=(datetime.utcnow() + timedelta(days=10)).date(),
                end_date=(datetime.utcnow() + timedelta(days=12)).date(),
                reason='Health checkup',
                status='Pending'
            )
            db.session.add(leave)
            
            # Create Payroll Record
            payroll = Payroll(
                employee_id=emp.id,
                month=datetime.utcnow().month,
                year=datetime.utcnow().year,
                basic_salary=emp.salary_base,
                allowances=5000.0,
                net_salary=emp.salary_base + 5000.0,
                status='Paid'
            )
            db.session.add(payroll)
            
        db.session.commit()
        print("Seeding completed!")
    else:
        print("Data already exists, skipping seed.")
