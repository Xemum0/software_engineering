from datetime import datetime, timedelta
from flask import Blueprint, request, jsonify
from schemas import RegisterSchema
from models import Company, Company_register, User, db
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token
from marshmallow.exceptions import ValidationError



auth_blueprint = Blueprint('auth', __name__)
bcrypt = Bcrypt()

@auth_blueprint.route('/add_account/company', methods=['POST'])
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

@auth_blueprint.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    remember_me = data.get('remember_me', False)

    if not email or not password:
        return jsonify({"msg": "Missing email or password"}), 400

    user = User.query.filter_by(email=email).first()

    if user and bcrypt.check_password_hash(user.password, password):
        expires_in =3600 if not remember_me else 86400
        access_token = create_access_token(
            identity={
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "role": user.role,
            },
            expires_delta=timedelta(seconds=expires_in)
        )

        return jsonify({
            "token": access_token,
            "expires_in": expires_in,
            "user": {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "role": user.role,
                "company_id": user.company_id,
                "branch_id": user.branch_id
            }
        }), 200

    return jsonify({"msg": "Invalid email or password"}), 401

