import os
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from datetime import datetime
import io

class PDFGenerator:
    ORG_NAME = "HRMS STRATEGIC SOLUTIONS"
    ORG_SUBTITLE = "Global Enterprise Workforce Management"
    
    @staticmethod
    def _get_header(elements, styles, title):
        # Professional Header with Subtitle
        header_style = ParagraphStyle(
            'HeaderStyle', 
            parent=styles['Heading1'], 
            alignment=1, 
            fontSize=24, 
            fontName='Helvetica-Bold',
            textColor=colors.hexColor("#0f172a"),
            spaceAfter=2
        )
        subtitle_style = ParagraphStyle(
            'SubtitleStyle', 
            parent=styles['Normal'], 
            alignment=1, 
            fontSize=10, 
            fontName='Helvetica-Bold',
            textColor=colors.hexColor("#64748b"),
            spaceAfter=20,
            letterSpacing=1
        )
        elements.append(Paragraph(PDFGenerator.ORG_NAME, header_style))
        elements.append(Paragraph(PDFGenerator.ORG_SUBTITLE.upper(), subtitle_style))
        
        title_style = ParagraphStyle(
            'TitleStyle', 
            parent=styles['Heading2'], 
            alignment=1, 
            fontSize=16, 
            textColor=colors.hexColor("#1e293b"),
            spaceAfter=20,
            borderPadding=10,
            backColor=colors.hexColor("#f1f5f9")
        )
        elements.append(Paragraph(title, title_style))
        elements.append(Spacer(1, 0.2 * inch))

    @staticmethod
    def generate_salary_slip(employee, payroll):
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)
        styles = getSampleStyleSheet()
        elements = []

        # Header
        PDFGenerator._get_header(elements, styles, f"OFFICIAL SALARY SLIP - {datetime(payroll.year, payroll.month, 1).strftime('%B %Y')}")

        # Employee Info Section
        emp_data = [
            [Paragraph("<b>EMPLOYEE DETAILS</b>", styles['Normal']), ""],
            ["Employee ID:", employee.emp_id],
            ["Full Name:", f"{employee.first_name} {employee.last_name}"],
            ["Department:", employee.department],
            ["Designation:", employee.designation],
            ["Registration Date:", employee.joining_date or "N/A"]
        ]
        t_info = Table(emp_data, colWidths=[1.5 * inch, 4 * inch])
        t_info.setStyle(TableStyle([
            ('SPAN', (0, 0), (1, 0)),
            ('BACKGROUND', (0, 0), (1, 0), colors.hexColor("#1e293b")),
            ('TEXTCOLOR', (0, 0), (1, 0), colors.white),
            ('FONTNAME', (0, 1), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('GRID', (0, 0), (-1, -1), 0.25, colors.hexColor("#e2e8f0")),
        ]))
        elements.append(t_info)
        elements.append(Spacer(1, 0.4 * inch))

        # Financial Breakdown
        data = [
            [Paragraph("<b>EARNINGS</b>", styles['Normal']), "AMOUNT", Paragraph("<b>DEDUCTIONS</b>", styles['Normal']), "AMOUNT"],
            ["Basic Salary", f"{payroll.basic_salary:,.2f}", "Tax Component", f"{payroll.tax_deductions:,.2f}"],
            ["Allowances", f"{payroll.allowances:,.2f}", "Provident Fund", f"{payroll.pf_deductions:,.2f}"],
            ["Performance Bonus", f"{payroll.bonuses:,.2f}", "Leave Adjustments", f"{payroll.leave_deductions:,.2f}"],
            ["", "", "", ""],
            [Paragraph("<b>TOTAL EARNINGS</b>", styles['Normal']), f"<b>{(payroll.basic_salary + payroll.allowances + payroll.bonuses):,.2f}</b>", 
             Paragraph("<b>TOTAL DEDUCTIONS</b>", styles['Normal']), f"<b>{(payroll.tax_deductions + payroll.pf_deductions + payroll.leave_deductions):,.2f}</b>"]
        ]
        
        t_pay = Table(data, colWidths=[1.4 * inch, 1.2 * inch, 1.4 * inch, 1.2 * inch])
        t_pay.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.hexColor("#f8fafc")),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.hexColor("#1e293b")),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
            ('ALIGN', (3, 0), (3, -1), 'RIGHT'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.hexColor("#cbd5e1")),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        elements.append(t_pay)
        elements.append(Spacer(1, 0.4 * inch))

        # Net Total Highlight
        net_box_data = [[
            Paragraph("<b>NET SALARY PAYOUT (INR)</b>", styles['Normal']),
            Paragraph(f"<font size=16><b>{payroll.net_salary:,.2f}</b></font>", styles['Normal'])
        ]]
        t_net = Table(net_box_data, colWidths=[3 * inch, 2.2 * inch])
        t_net.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.hexColor("#0f172a")),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.white),
            ('ALIGN', (1, 0), (1, 0), 'RIGHT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 20),
            ('RIGHTPADDING', (0, 0), (-1, -1), 20),
            ('TOPPADDING', (0, 0), (-1, -1), 15),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 15),
        ]))
        elements.append(t_net)

        # Compliance Footer
        elements.append(Spacer(1, 1.5 * inch))
        footer_style = ParagraphStyle('FooterStyle', parent=styles['Normal'], alignment=1, fontSize=8, textColor=colors.hexColor("#94a3b8"), leading=12)
        elements.append(Paragraph("<b>CONFIDENTIAL DOCUMENT</b><br/>This payroll statement is electronically generated and verified by the HRMS Strategic System.<br/>No manual signature is required for validity.", footer_style))
        elements.append(Paragraph(f"Reference ID: {payroll.id} | Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", footer_style))

        doc.build(elements)
        buffer.seek(0)
        return buffer

    @staticmethod
    def generate_monthly_report(payrolls, month, year):
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=30, leftMargin=30, topMargin=40, bottomMargin=40)
        styles = getSampleStyleSheet()
        elements = []

        # Header
        PDFGenerator._get_header(elements, styles, f"CONSOLIDATED PAYROLL REPORT - {datetime(year, month, 1).strftime('%B %Y')}")

        # Summary Table Header
        data = [["EMP ID", "FULL NAME", "BASE SALARY", "ALLOWANCES", "DEDUCTIONS", "NET PAYOUT"]]
        
        total_payout = 0
        for p in payrolls:
            emp = p.employee
            total_payout += p.net_salary
            data.append([
                emp.emp_id,
                f"{emp.first_name} {emp.last_name}",
                f"{p.basic_salary:,.0f}",
                f"{p.allowances:,.0f}",
                f"{p.tax_deductions + p.pf_deductions + p.leave_deductions:,.0f}",
                f"{p.net_salary:,.0f}"
            ])

        # Add Summary Row
        data.append(["", "TOTAL DISBURSEMENT", "", "", "", f"INR {total_payout:,.0f}"])

        t = Table(data, repeatRows=1, colWidths=[0.8*inch, 1.8*inch, 1.1*inch, 1.1*inch, 1.1*inch, 1.1*inch])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.hexColor("#0f172a")),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('ALIGN', (2, 1), (-1, -1), 'RIGHT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 9),
            ('GRID', (0, 0), (-1, -1), 0.25, colors.hexColor("#e2e8f0")),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
            ('BACKGROUND', (0, -1), (-1, -1), colors.hexColor("#f1f5f9")),
            ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
            ('ROWBACKGROUNDS', (0, 1), (-1, -2), [colors.white, colors.hexColor("#f8fafc")])
        ]))
        
        elements.append(t)
        doc.build(elements)
        buffer.seek(0)
        return buffer
        
        elements.append(t)
        doc.build(elements)
        buffer.seek(0)
        return buffer
