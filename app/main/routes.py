from flask import render_template, request, send_from_directory, abort, current_app as app
from app.main import bp
from app.models import Department, Event


@bp.route("/uploads/<path:filename>")
def uploads(filename):
    return send_from_directory(app.config["UPLOAD_PATH"], filename, as_attachment=True)


@bp.route("/")
def index():
    return render_template("index.html", departments=Department.query.all(), events=Event.query.order_by(Event.start_datetime).all())
