from datetime import datetime
from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity
from models import Review, Flagged, User, Notification, Branch, db

review_blueprint = Blueprint('reviews', __name__)

# Submit a Review (Only Normal Users)
@review_blueprint.route('/submit_review', methods=['POST'])
def submit_review():
    user_id = get_jwt_identity()
    data = request.get_json()

    # Ensure the user exists and is a normal user
    user = User.query.get(user_id)
    if not user:
        return jsonify({"msg": "User not found"}), 404
    if user.role != 1:  # Normal user role
        return jsonify({"msg": "Only normal users can submit reviews"}), 403

    # Validate input
    required_fields = ['title', 'description', 'rating', 'branch_id']
    for field in required_fields:
        if not data.get(field):
            return jsonify({"msg": f"{field} is required"}), 400

    try:
        rating = float(data['rating'])
        if not (0 <= rating <= 5.0):
            return jsonify({"msg": "Rating must be between 0 and 5"}), 400
    except ValueError:
        return jsonify({"msg": "Rating must be a valid number"}), 400

    branch = Branch.query.get(data['branch_id'])
    if not branch:
        return jsonify({"msg": "Branch not found"}), 404

    # Create and save the review
    review = Review(
        user_id=user_id,
        branch_id=data['branch_id'],
        title=data['title'],
        description=data['description'],
        rating=rating,
        staff_satisfaction=data.get('staff_satisfaction', 0.0),
        speed_satisfaction=data.get('speed_satisfaction', 0.0),
        reliability=data.get('reliability', 0.0),
        created_at=datetime.now(),
        tags=data.get('tags', ''), 
        active=0  # Default active status
    )
    db.session.add(review)
    db.session.commit()

    notify_company_admins(f"New review submitted by User ID {user_id}")

    return jsonify({"msg": "Review submitted successfully", "review_id": review.id}), 201


# Flag a Review (Only Admins or Reviewers)
@review_blueprint.route('/flag_review/<string:review_id>', methods=['POST'])
def flag_review(review_id):
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if not user:
        return jsonify({"msg": "User not found"}), 404

    # Ensure the user is a company_admin, branch_admin, or reviewer
    if user.role not in [1, 3, 4]:  # Reviewer, Company Admin, Branch Admin roles
        return jsonify({"msg": "You are not authorized to flag reviews"}), 403

    review = Review.query.get(review_id)
    if not review or review.active == 1:
        return jsonify({"msg": "Review not found or inactive"}), 404

    # Check if the user has already flagged this review
    existing_flag = Flagged.query.filter_by(user_id=user_id, review_id=review_id).first()
    if existing_flag:
        return jsonify({"msg": "You have already flagged this review"}), 400

    # Add a flag entry
    flagged = Flagged(
        review_id=review_id,
        user_id=user_id,
        description=request.json.get('description', '')
    )
    db.session.add(flagged)
    db.session.commit()

    notify_company_admins(f"Review ID {review_id} was flagged by User ID {user_id}")

    return jsonify({"msg": "Review flagged successfully"}), 200


# Admin Action on Flagged Review
@review_blueprint.route('/review_action/<string:flagged_id>', methods=['POST'])
def review_action(flagged_id):
    data = request.json
    action = data.get('action')  # "approve" or "deactivate"
    flagged = Flagged.query.get(flagged_id)

    if not flagged:
        return jsonify({"msg": "Flagged review not found"}), 404

    review = Review.query.get(flagged.review_id)
    if not review:
        return jsonify({"msg": "Associated review not found"}), 404

    if action == "approve":
        # Approve review (remove flag)
        db.session.delete(flagged)
        db.session.commit()
        return jsonify({"msg": "Review approved successfully"}), 200

    elif action == "deactivate":
        # Mark review as inactive instead of deleting
        review.active = 1  # Mark as inactive
        
        db.session.commit()
        return jsonify({"msg": "Review deactivated successfully"}), 200

    return jsonify({"msg": "Invalid action"}), 400


# Notify Admins
def notify_company_admins(company_id, message):
    # Fetch company and branch admins
    admins = User.query.filter(
        (User.role.in_([3, 4])) &  # Role 3: Company Admin, Role 4: Branch Admin
        (User.company_id == company_id)
    ).all()

    for admin in admins:
        notification = Notification(user_id=admin.id, message=message)
        db.session.add(notification)
    db.session.commit()



# Notifications for Users
@review_blueprint.route('/notifications', methods=['GET'])
def get_notifications():
    user_id = get_jwt_identity()
    notifications = Notification.query.filter_by(user_id=user_id).all()
    return jsonify([{
        "id": notification.id,
        "message": notification.message,
        "created_at": notification.created_at
    } for notification in notifications]), 200
