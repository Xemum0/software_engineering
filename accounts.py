from datetime import datetime, timedelta
from flask import Blueprint, request, jsonify
from schemas import RegisterSchema
from models import Branch, Company, Company_register, User, db
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token
from marshmallow.exceptions import ValidationError



add_blueprint = Blueprint('add', __name__)
bcrypt = Bcrypt()

@add_blueprint.route('/add_account/company', methods=['POST'])
def register():
    data = request.get_json()
    account_id=data('user_id')
    user1=User.query.filter_by(id=account_id,role=2).first()
    company=Company.query.filter_by(id=data.get('company_id')).first()
    if user1 and company:
        hashed_password= bcrypt.generate_password_hash(data['password']).decode('utf-8'),


        user = User(
            email=data['email'],
            password=hashed_password,
            name=data['name'],
            phone=data.get('phone'),
            role = 2,
            avatar = data.get('avatar'),
            created_at = datetime.now,
            company_id=data.get('company_id')
        )
        db.session.add(user)
        db.session.commit()

        token = create_access_token(identity=user.id, expires_delta=timedelta(hours=1))

        return jsonify({
        "user_id": user.id,
        "token": token,
        "expires_in": 3600
    }), 201
    else:
        if not user1:
            
            return jsonify({
        "msg":'unauthorized',

    }), 404
        else:
            return jsonify({
        "msg":'Company doesn"t exist',

    }), 404
            
            
            
            
            
            
    
    
    
    
    
    
    










@add_blueprint.route('/add_account/branch', methods=['POST'])
def register():
    data = request.get_json()
    account_id=data('user_id')
    user1=User.query.filter_by(id=account_id,role=2).first()
    user2=User.query.filter_by(id=account_id,role=3).first()
    branch=Branch.query.filter_by(id=data.get('branch_id')).first()
    if (user1 or user2) and branch:
        hashed_password= bcrypt.generate_password_hash(data['password']).decode('utf-8'),


        user = User(
            email=data['email'],
            password=hashed_password,
            name=data['name'],
            phone=data.get('phone'),
            role = 2,
            avatar = data.get('avatar'),
            created_at = datetime.now,
            branch_id=data.get('branch_id')
        )
        db.session.add(user)
        db.session.commit()

        token = create_access_token(identity=user.id, expires_delta=timedelta(hours=1))

        return jsonify({
        "user_id": user.id,
        "token": token,
        "expires_in": 3600
    }), 201
    else:
        if not user1:
            
            return jsonify({
        "msg":'unauthorized',

    }), 404
        else:
            return jsonify({
        "msg":'Branch doesn"t exist',

    }), 404
        
        
        
        
edit_blueprint = Blueprint('edit', __name__)
        
        
        
@edit_blueprint.route('/edit_account/edit', methods=['POST'])
def register():
    data = request.get_json()
    account_id=data('user_id')
    user=User.query.filter_by(id=account_id,role=2).first()
    if user:
        if data.get('name'):
            user.name= data.get('name')
        if data.get('password'):
            user.name= bcrypt.generate_password_hash(data.get('password')).decode('utf-8'),
        if data.get('email'):
            user.name= data.get('email')
        if data.get('phone'):
            user.name= data.get('phone')
        if data.get('avatar'):
            user.name= data.get('avatar')
        db.session.commit()
        return jsonify({
        "msg": 'user modified successfully',
    }), 201
    else:
        return jsonify({
        "msg":'user doesn"t exist',

    }), 404



