from datetime import datetime
import uuid
import bcrypt
from flask import Blueprint, Response, jsonify, request
from flask_jwt_extended import get_jwt_identity
from models import Branch, Category, Company, Company_register, Review, User
from models import Company, db
import secrets
import string


response_blueprint = Blueprint('responses', __name__)

@response_blueprint.route('/get_responses', methods=['GET'])
def get_responses():
   responses = Response.query.all()
    
   responses_list = [company.to_dict() for company in responses]

   return jsonify({
        "companies": responses_list,
    }), 201
   
   
   
   
@response_blueprint.route('/add_response', methods=['POST'])
def add_response():
    data = request.get_json()
    account_id=get_jwt_identity()
    description=data.get('description')
    review_id=data.get('review_id')
    user=User.query.filter_by(id=account_id).first()
    review=Review.query.filter_by(id=review_id).first()
    branch=Branch.query.filter_by(id=review.branch_id)
    if user:
        if (user.role==2 and user.company_id==branch.company_id)  or (user.role==3 and review.branch_id==user.branch_id):
            response=Response(review_id=review_id,description=description,user_id=account_id)
            db.session.add(response)
            db.session.commit()
        
            
        else:
            return  jsonify({
                    'msg':'User not authorized or review no longer exists'
                }),300 
        
    else:
        return  jsonify({
                    'msg':'User does not exist'
                }),300    
        
        
        
        
        




@response_blueprint.route('/delete_response', methods=['POST'])
def add_response():
    data = request.get_json()
    account_id=get_jwt_identity()
    response_id=data.get('response_id')
    user=User.query.filter_by(id=account_id).first()
    response=Response.query.filter_by(id=response_id).first()
    review=Review.query.filter_by(id=response.review_id).first()
    branch=Branch.query.filter_by(id=review.branch_id)
    if user and response:
        if (user.role==2 and user.company_id==branch.company_id)  or (user.role==3 and review.branch_id==user.branch_id):
            db.session.delete(response)
            db.session.commit()
        
            
        else:
            return  jsonify({
                    'msg':'User not authorized or review no longer exists'
                }),300 
        
    else:
        return  jsonify({
                    'msg':'User/response does not exist'
                }),300    