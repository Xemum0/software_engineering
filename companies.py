from datetime import datetime
import uuid
import bcrypt
from flask import Blueprint, jsonify, request
from models import Branch, Company, Company_register, User
from models import Company, db
import secrets
import string


companies_blueprint = Blueprint('companies', __name__)

@companies_blueprint.route('/companies/<string:company_name>/visit', methods=['POST'])
def increment_visits(company_name):
    company = Company.query.filter_by(name=company_name).first()
    if not company:
        return jsonify({"msg": "Company not found"}), 404

    company.visits += 1
    db.session.commit()

    return jsonify({
        "msg": "Visit count updated",
        "company_id": company.id,
        "visits": company.visits
    }), 200



















@companies_blueprint.route('/company_register', methods=['POST'])
def company_register():
    data = request.get_json()
    name = data.get('name')
    logo = data.get('logo')
    category = data.get('category')
    address = data.get('address')
    email = data.get('email')
    admin_email = data.get('admin_email')
    website = data.get('website')
    description = data.get('description')
    phone = data.get('phone')
    business_registration = data.get('business_registration')
    social_links = data.get('social_links')


    if not name or not category:
        return jsonify({"msg": "Missing name or category"}), 400

    company = Company.query.filter_by(name=name).first()

    if company :
        return jsonify({"msg": "Name already exists"}), 400

    company = Company_register(
        name,email,admin_email,phone,description,business_registration,social_links,website,logo,category,address
    )
    db.session.add(company)
    db.session.commit()


    return jsonify({
        "company_id": company.id,
    }), 201

@companies_blueprint.route('/get_company_register', methods=['GET'])
def get_company_register():
    companies = Company_register.query.all()
    
    companies_list = [company.to_dict() for company in companies]

    return jsonify({
        "companies": companies_list,
    }), 201
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

@companies_blueprint.route('/company_register/validate', methods=['POST'])
def company_validate():
    data = request.get_json()
    validated = data.get("validated")
    company_id = data.get("company_id")
    company = Company_register.query.filter_by(id = company_id).first()
    if company:
        if User.query.filter_by(email=company.admin_email).first():
            return jsonify({"msg": "Admin email already exists"}), 400
        if validated:
            db.session.add(Company(name= company.name,email= company.email,phone= company.phone,website=company.website,description= company.description,social_links= company.social_links,business_registration= company.business_registration, logo=company.logo, category=company.category, address= company.address, created_at=datetime.now))
            admin_password = generate_password()
            db.session.add(User(email=company.admin_email, password=bcrypt.generate_password_hash(admin_password).decode('utf-8'), name = f"company.name admin", role = 2, company_id = company.id) )
        db.session.delete(company)
        db.session.commit()
    
        if validated:
            return jsonify ({"msg": "company validated and admin account created", 
                             "company": {
                                 "id": company.id,
                                 "admin_password": admin_password
                             }
                             }), 201
        else :
            return jsonify ({"msg": "Company registration rejected"}), 200
    else :
        return jsonify ({"msg": "Company not found"}), 404
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
@companies_blueprint.route('/company/<string:company_admin_name>/add_branch', methods=['POST'])
def add_branch(company_admin_name):
    user=User.query.filter_by(name=company_admin_name,role=2)
    if user:
        data = request.get_json()
        name = data.get('name')
        category = data.get('category')
        address = data.get('address')
        email = data.get('email')
        phone = data.get('phone')
        company_id = data.get('company_id')



        if not name or not category:
            return jsonify({"msg": "Missing name or category"}), 400
        company = Company.query.filter_by(id=company_id).first()
        if not company :
            return jsonify({"msg": "No company exists"}), 400
        branch = Branch.query.filter_by(name=name).first()

        if branch :
            return jsonify({"msg": "Name already exists"}), 400

        branch = Branch(
            name,email,company_id,email,address,phone)
        db.session.add(branch)
        db.session.commit()
        return jsonify({
        "msg": "Branch added successfully.",
        "branch_id": branch.id
    }), 201
    else:
        return jsonify({
        "msg": "unothorized user.",

    }), 301
        
        
    # name = data.get('name')
    # email = data.get('email')
    # phone = data.get('phone')
    # address = data.get('address')

    # if not name or not email or not phone or not address:
    #     return jsonify({"msg": "Missing required branch details."}), 400

    # company = Company.query.filter_by(id=company_id).first()
    # if not company:
    #     return jsonify({"msg": "Company not found."}), 404

    # if Branch.query.filter_by(name=name).first():
    #     return jsonify({"msg": "Branch name already exists."}), 400

    # branch = Branch(
    #     id=str(uuid.uuid4()),
    #     company=company_id,
    #     name=name,
    #     email=email,
    #     phone=phone,
    #     address=address
    # )

    # db.session.add(branch)
    # db.session.commit()

    # return jsonify({
    #     "msg": "Branch added successfully.",
    #     "branch_id": branch.id
    # }), 201


















def generate_password(length=12):
    """Generates a secure random password with at least one uppercase, lowercase, digit, and special character."""
    if length < 8:
        raise ValueError("Password length should be at least 8 characters.")

    # Define character pools
    uppercase = string.ascii_uppercase  # A-Z
    lowercase = string.ascii_lowercase  # a-z
    digits = string.digits              # 0-9
    special_chars = "!@#$%^&*()-_=+"

    # Ensure the password contains at least one of each required type
    password = [
        secrets.choice(uppercase),
        secrets.choice(lowercase),
        secrets.choice(digits),
        secrets.choice(special_chars),
    ]

    # Fill the rest of the password length with a mix of all character types
    all_chars = uppercase + lowercase + digits + special_chars
    password += [secrets.choice(all_chars) for _ in range(length - 4)]

    # Shuffle the password to avoid predictable patterns
    secrets.SystemRandom().shuffle(password)

    # Convert list to string
    return ''.join(password)

