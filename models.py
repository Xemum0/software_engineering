from flask_sqlalchemy import SQLAlchemy
import uuid

from sqlalchemy import ForeignKey

db = SQLAlchemy()



class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    role = db.Column(db.Integer, ForeignKey('role.id'))              #0 for user, 1 for company, 2 for admin
    company_id=db.Column(db.String(130), ForeignKey('company.id'))
    branch_id = db.Column(db.String(130), ForeignKey('branch.id'))

    created_at = db.Column(db.String(120),nullable=False)
    avatar = db.Column(db.String(120),nullable=False)
    


class Company(db.Model):
    __tablename__ = 'company'

    id = db.Column(db.String(32), primary_key=True,default =lambda: str(uuid.uuid4))
    
    name = db.Column(db.String(32),unique=True,nullable=False)
    email = db.Column(db.String(132),unique=True,nullable=False)
    phone = db.Column(db.String(132),unique=True,nullable=True)
    description = db.Column(db.String(132),unique=True,nullable=False)
    website = db.Column(db.String(132),unique=True,nullable=False)
    business_registration = db.Column(db.String(132),unique=True,nullable=False)
    social_links = db.Column(db.String(132),unique=True,nullable=False)
    logo = db.Column(db.String(120),unique=True,nullable=False)
    category=db.Column(db.Integer,ForeignKey('category.id'))
    address = db.Column(db.String(120),nullable=False)
    created_at = db.Column(db.String(120),nullable=False)
    visits = db.Column(db.Integer, default=0) 
    verified = db.Column(db.Integer, default=0) 


    def __init__(self, name,email,phone,description,website,business_registration,social_links,logo,category,address,created_at):

        self.name = name
        self.email=email
        self.phone=phone
        self.description=description
        self.website=website
        self.business_registration=business_registration
        self.social_links=social_links
        self.email=email
        self.logo=logo
        self.category=category
        self.address = address
        self.created_at=created_at

class Branch(db.Model):
    __tablename__ = 'branch'

    id = db.Column(db.String(120), primary_key=True,default =lambda: str(uuid.uuid4()))
    company = db.Column(db.String(120),ForeignKey('company.id'))
    name = db.Column(db.String(120),nullable=False,unique=True)
    email = db.Column(db.String(120),nullable=False)
    phone=db.Column(db.String(120),nullable=False)
    address = db.Column(db.String(120),nullable=False)
    visits = db.Column(db.Integer, default=0) 



    def __init__(self, id,name,company,email,address,phone):
        self.id = id
        self.company = company
        self.name = name
        self.email=email
        self.address = address
        self.phone=phone

class Company_register(db.Model):
    __tablename__ = 'company_register'

    id = db.Column(db.String(32), primary_key=True,default =lambda: str(uuid.uuid4))
    name = db.Column(db.String(32),unique=True,nullable=False)
    email = db.Column(db.String(132),unique=True,nullable=False)
    admin_email = db.Column(db.String(132),unique=True,nullable=False)
    phone = db.Column(db.String(132),unique=True,nullable=True)
    description = db.Column(db.String(132),unique=True,nullable=False)
    website = db.Column(db.String(132),unique=True,nullable=False)
    business_registration = db.Column(db.String(132),unique=True,nullable=False)
    social_links = db.Column(db.String(132),unique=True,nullable=False)
    logo = db.Column(db.String(120),unique=True,nullable=False)
    category=db.Column(db.Integer,ForeignKey('category.id'))
    address = db.Column(db.String(120),nullable=False)



    def __init__(self, name,email,admin_email,phone,description,business_registration,social_links,website,logo,category,address):
        self.name = name
        self.admin_email=admin_email
        self.email=email
        self.phone=phone
        self.description=description
        self.website=website
        self.business_registration=business_registration
        self.social_links=social_links
        self.logo=logo
        self.category=category
        self.address = address

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "logo": self.logo,
            "category": self.category,
            "address": self.address
        }

class Category(db.Model):
    __tablename__ = "category"

    id = db.Column(db.Integer, primary_key = True, autoincrement = 'auto')
    name = db.Column(db.String(120),nullable=False,unique=True)

    def __init__(self, name):
        self.name = name

class Role(db.Model):
    __tablename__ = "role"

    id = db.Column(db.Integer, primary_key = True, autoincrement = 'auto')
    name = db.Column(db.String(120),nullable=False,unique=True)

    def __init__(self, name):
        self.name = name
        
        
        
        
        
        
        
        
        
        
        
class Review(db.Model):
    __tablename__ = 'review'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(120),ForeignKey('users.id'))
    branch_id = db.Column(db.String(120),ForeignKey('branch.id'))
    title = db.Column(db.String(120))
    description = db.Column(db.String(120))
    rating = db.Column(db.Float, nullable=False)
    staff_satisfaction = db.Column(db.Float, nullable=False)
    speed_satisfaction = db.Column(db.Float, nullable=False)
    reliability = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.String(120),nullable=False)
    tags = db.Column(db.String(120),nullable=False)
    
    
    
    
class Flagged(db.Model):
    __tablename__ = 'flagged'
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    review_id= db.Column(db.String(120))
    description= db.Column(db.String(120))
    user_id= db.Column(db.String(120),ForeignKey('users.id'))
    
