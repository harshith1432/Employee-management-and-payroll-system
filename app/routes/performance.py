from flask import Blueprint, request, jsonify
from app.models import Employee, PerformanceReview
from app.extensions import db
from app.utils.decorators import hr_required
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime

bp = Blueprint('performance', __name__, url_prefix='/api/performance')

@bp.route('/review/<int:id>', methods=['POST'])
@jwt_required()
@hr_required()
def add_review(id):
    data = request.get_json()
    emp = Employee.query.get_or_404(id)
    reviewer_id = get_jwt_identity()
    
    review = PerformanceReview(
        employee_id=emp.id,
        reviewer_id=reviewer_id,
        rating=data.get('rating'),
        feedback=data.get('feedback'),
        review_date=datetime.utcnow()
    )
    
    db.session.add(review)
    db.session.commit()
    
    return jsonify({
        "msg": "Performance appraisal successfully committed to historical record",
        "employee": f"{emp.first_name} {emp.last_name}"
    }), 201

@bp.route('/employee/<int:id>', methods=['GET'])
@jwt_required()
@hr_required()
def get_reviews(id):
    reviews = PerformanceReview.query.filter_by(employee_id=id).order_by(PerformanceReview.review_date.desc()).all()
    return jsonify([{
        'id': r.id,
        'rating': r.rating,
        'feedback': r.feedback,
        'date': str(r.review_date)
    } for r in reviews]), 200
