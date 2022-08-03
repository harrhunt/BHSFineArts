from flask import Blueprint

bp = Blueprint('admin', __name__, template_folder='templates')

from app.admin import routes

from app.admin.user import bp as user_bp
bp.register_blueprint(user_bp, url_prefix='/user')

from app.admin.faculty import bp as faculty_bp
bp.register_blueprint(faculty_bp, url_prefix='/faculty')

from app.admin.event import bp as event_bp
bp.register_blueprint(event_bp, url_prefix='/event')

from app.admin.file import bp as file_bp
bp.register_blueprint(file_bp, url_prefix='/file')
