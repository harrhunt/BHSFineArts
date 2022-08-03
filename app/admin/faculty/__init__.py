from flask import Blueprint

bp = Blueprint('faculty', __name__, template_folder='templates')

from app.admin.faculty import routes
