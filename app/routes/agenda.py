from flask import Blueprint, request, jsonify
from app.models import DailyAgenda, User
from app.extensions import db
from datetime import datetime
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.utils.decorators import hr_required

bp = Blueprint('agenda', __name__, url_prefix='/api/agenda')

@bp.route('/set', methods=['POST'])
@jwt_required()
@hr_required()
def set_agenda():
    user_id = get_jwt_identity()
    data = request.get_json()
    title = data.get('title')
    description = data.get('description')
    
    if not title:
        return jsonify(msg="Title is required"), 400
        
    today = datetime.now().date()
    agenda = DailyAgenda.query.filter_by(date=today).first()
    
    if agenda:
        agenda.title = title
        agenda.description = description
        agenda.created_by = user_id
    else:
        agenda = DailyAgenda(
            date=today,
            title=title,
            description=description,
            created_by=user_id
        )
        db.session.add(agenda)
    
    db.session.commit()
    return jsonify(msg="Today's agenda has been set successfully"), 200

@bp.route('/today', methods=['GET'])
@jwt_required()
def get_today_agenda():
    today = datetime.now().date()
    agenda = DailyAgenda.query.filter_by(date=today).first()
    
    if not agenda:
        return jsonify({
            'title': "No Agenda Set",
            'description': "HR has not assigned today's main agenda yet."
        }), 200
        
    return jsonify({
        'title': agenda.title,
        'description': agenda.description,
        'created_at': agenda.created_at.isoformat()
    }), 200
