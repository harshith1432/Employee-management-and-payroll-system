from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.models.user import User
from app import db, bcrypt
from datetime import timedelta

bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    if User.query.filter_by(email=data.get('email')).first():
        return jsonify({"msg": "User already exists"}), 400
        
    user = User(
        email=data.get('email'),
        role=data.get('role', 'employee')
    )
    user.set_password(data.get('password'))
    
    db.session.add(user)
    db.session.commit()
    
    return jsonify({"msg": "User registered successfully"}), 201

@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data.get('email')).first()
    
    if user and user.check_password(data.get('password')):
        if not user.is_active:
            return jsonify({"msg": "Your account is deactivated. Please contact support."}), 403
            
        access_token = create_access_token(
            identity=str(user.id), 
            additional_claims={"role": user.role},
            expires_delta=timedelta(days=1)
        )
        return jsonify(
            access_token=access_token, 
            role=user.role, 
            user_id=user.id,
            must_change_password=user.must_change_password
        ), 200
        
    return jsonify({"msg": "Bad email or password"}), 401

@bp.route('/reset-password', methods=['POST'])
@jwt_required()
def reset_password():
    data = request.get_json()
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    new_password = data.get('password')
    if not new_password:
        return jsonify({"msg": "Password is required"}), 400
        
    user.set_password(new_password)
    user.must_change_password = False
    db.session.commit()
    
    return jsonify({"msg": "Password updated successfully"}), 200

@bp.route('/me', methods=['GET'])
@jwt_required()
def get_me():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    return jsonify({
        "id": user.id,
        "email": user.email,
        "role": user.role
    }), 200
