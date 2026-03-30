from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os
from flask import current_app

class PDFService:
    @staticmethod
    def generate_salary_slip(payroll, employee):
        filename = f"salary_slip_{employee.emp_id}_{payroll.month}_{payroll.year}.pdf"
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        
        c = canvas.Canvas(filepath, pagesize=letter)
        width, height = letter
        
        # Header
        c.setFont("Helvetica-Bold", 16)
        c.drawString(50, height - 50, "AI Powered Employee Management & Payroll System")
        c.setFont("Helvetica", 12)
        c.drawString(50, height - 70, f"Salary Slip for {payroll.month}/{payroll.year}")
        
        # Employee Details
        c.line(50, height - 85, width - 50, height - 85)
        c.drawString(50, height - 110, f"Employee Name: {employee.first_name} {employee.last_name}")
        c.drawString(50, height - 125, f"Employee ID: {employee.emp_id}")
        c.drawString(50, height - 140, f"Department: {employee.department}")
        c.drawString(50, height - 155, f"Designation: {employee.designation}")
        
        # Salary Details
        c.line(50, height - 175, width - 50, height - 175)
        c.drawString(50, height - 200, f"Basic Salary: {payroll.basic_salary}")
        c.drawString(50, height - 215, f"Allowances: {payroll.allowances}")
        c.drawString(50, height - 230, f"Bonus: {payroll.bonuses}")
        c.drawString(50, height - 245, f"Overtime: {payroll.overtime}")
        
        c.drawString(300, height - 200, f"Tax Deductions: {payroll.tax_deductions}")
        c.drawString(300, height - 215, f"PF Deductions: {payroll.pf_deductions}")
        c.drawString(300, height - 230, f"Leave Deductions: {payroll.leave_deductions}")
        
        c.line(50, height - 265, width - 50, height - 265)
        c.setFont("Helvetica-Bold", 14)
        c.drawString(50, height - 290, f"Net Salary: {payroll.net_salary}")
        
        c.save()
        return filepath
