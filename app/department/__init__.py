from flask import Blueprint

bp = Blueprint('department', __name__, template_folder='templates')

from app.department import routes
