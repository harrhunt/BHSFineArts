from flask import Blueprint

bp = Blueprint('file', __name__, template_folder='templates')

from app.admin.file import routes
