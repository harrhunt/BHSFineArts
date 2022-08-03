from flask import Blueprint

bp = Blueprint('event', __name__, template_folder='templates')

from app.admin.event import routes
