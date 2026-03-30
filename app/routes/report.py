from flask import Blueprint, send_file, request, jsonify
from app.models import Payroll, Employee
from app.services.pdf_service import PDFService
from flask_jwt_extended import jwt_required

bp = Blueprint('report', __name__, url_prefix='/api/report')

@bp.route('/salary-slip/<int:payroll_id>', methods=['GET'])
@jwt_required()
def download_slip(payroll_id):
    payroll = Payroll.query.get_or_404(payroll_id)
    employee = payroll.employee
    
    # Check permission (HR or the employee themselves)
    # Simplified for demo
    
    filepath = PDFService.generate_salary_slip(payroll, employee)
    return send_file(filepath, as_attachment=True)
