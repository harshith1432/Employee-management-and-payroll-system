import calendar
from datetime import date
from app.models.core import Attendance, LeaveRequest

class PayrollService:
    @staticmethod
    def calculate_net_salary(employee, month, year, bonuses=0):
        basic_monthly = employee.salary_base
        num_days = calendar.monthrange(year, month)[1]
        daily_rate = basic_monthly / num_days
        
        # Calculate Working Days (Present or Approved Leave)
        start_date = date(year, month, 1)
        end_date = date(year, month, num_days)
        
        present_days = Attendance.query.filter(
            Attendance.employee_id == employee.id,
            Attendance.date >= start_date,
            Attendance.date <= end_date,
            Attendance.status == 'Present'
        ).count()
        
        approved_leaves = LeaveRequest.query.filter(
            LeaveRequest.employee_id == employee.id,
            LeaveRequest.start_date <= end_date,
            LeaveRequest.end_date >= start_date,
            LeaveRequest.status == 'Approved'
        ).all()
        
        # Count unique leave days within this month
        leave_days_count = 0
        for rel in approved_leaves:
            l_start = max(rel.start_date, start_date)
            l_end = min(rel.end_date, end_date)
            leave_days_count += (l_end - l_start).days + 1

        total_paid_days = present_days + leave_days_count
        absent_days = num_days - total_paid_days
        
        if total_paid_days > num_days: total_paid_days = num_days # Cap just in case
        
        # Financials
        earned_salary = total_paid_days * daily_rate
        leave_deductions = absent_days * daily_rate
        
        # Components (Applied on earned amount)
        allowances = earned_salary * 0.10
        tax = earned_salary * 0.05
        pf = earned_salary * 0.12
        
        net = earned_salary + allowances + bonuses - tax - pf
        
        return {
            'basic': earned_salary,
            'daily_rate': daily_rate,
            'paid_days': total_paid_days,
            'absent_days': absent_days,
            'allowances': allowances,
            'bonuses': bonuses,
            'deductions': leave_deductions,
            'tax': tax,
            'pf': pf,
            'net': net
        }
        
    @staticmethod
    def generate_monthly_payroll(db, Employee, Payroll, month, year):
        employees = Employee.query.all()
        for emp in employees:
            # Check if already generated
            existing = Payroll.query.filter_by(employee_id=emp.id, month=month, year=year).first()
            if existing: continue
            
            # Use accumulated_pay instead of recalculating from scratch
            # However, for consistency, we still calculate the standard components
            # But the 'basic_salary' for this month is the accumulated amount
            accumulated = emp.accumulated_pay
            if accumulated <= 0: continue # Skip if no earnings
            
            # Components applied on accumulated amount
            allowances = accumulated * 0.10
            tax = accumulated * 0.05
            pf = accumulated * 0.12
            net = accumulated + allowances - tax - pf
            
            pay = Payroll(
                employee_id=emp.id,
                month=month,
                year=year,
                basic_salary=accumulated,
                allowances=allowances,
                bonuses=0,
                overtime=0,
                tax_deductions=tax,
                pf_deductions=pf,
                leave_deductions=0, # Deductions already reflected in accumulation (or lack thereof)
                net_salary=net
            )
            db.session.add(pay)
            
            # Reset the accumulator for the next month
            emp.accumulated_pay = 0.0
        db.session.commit()
