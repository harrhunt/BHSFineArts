from flask import render_template, abort
from app.department import bp
from app.models import Department, Event, Faculty
from app.department.helper import validate_department


@bp.route("/<string:dep>")
def home(dep):
    if department := validate_department(dep):
        department_events = Event.query.filter(Event.department_id == department.id).order_by(Event.start_datetime)
        return render_template("department/home.html", department=department, events=department_events)
    abort(404)


@bp.route("/<string:dep>/events")
def events(dep):
    if department := validate_department(dep):
        department_events = Event.query.filter(Event.department_id == department.id).order_by(Event.start_datetime)
        return render_template("department/events.html", department=department, events=department_events)
    abort(404)


@bp.route("/<string:dep>/faculty")
def faculty(dep):
    if department := validate_department(dep):
        faculty_members = Faculty.query.filter(Faculty.department_id == department.id).order_by(Faculty.last_name)
        return render_template("department/faculty.html", department=department, faculty=faculty_members)
    abort(404)


@bp.route("/<string:dep>/about")
def about(dep):
    if department := validate_department(dep):
        return render_template("department/about.html", department=department)
    abort(404)
