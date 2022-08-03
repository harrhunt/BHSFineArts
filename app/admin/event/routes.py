from flask import render_template, redirect, url_for, request
from flask_login import login_required
from app.admin.event import bp
from app.models import Event, Department
from app.forms import EventForm
from app import db


@bp.route('/')
@login_required
def index():
    event = Event.query.all()
    return render_template("event/index.html", event=event)


@bp.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    form = EventForm()
    form.department.query = Department.query
    if form.validate_on_submit():
        new_event = Event()
        form.populate_obj(new_event)
        try:
            db.session.add(new_event)
            db.session.commit()
        except Exception as err:
            form.submit.errors.append(str(err))
        else:
            return redirect(url_for('admin.event.index'))
    return render_template("event/add.html", form=form)


@bp.route('/edit/<int:event_id>', methods=['GET', 'POST'])
@login_required
def edit(event_id):
    event = Event.query.filter(Event.id == event_id).first()
    form = EventForm(obj=event)
    form.department.query = Department.query
    if form.validate_on_submit():
        form.populate_obj(event)
        try:
            db.session.add(event)
            db.session.commit()
        except Exception as err:
            form.submit.errors.append(str(err))
        else:
            return redirect(url_for('admin.event.index'))
    return render_template("event/edit.html", form=form)


@bp.route('/<int:event_id>', methods=['GET', 'POST'])
@login_required
def view(event_id):
    if request.method == 'POST':
        delete_event_id = int(request.form.get('id'))
        if delete_event_id == event_id:
            event = Event.query.filter(Event.id == delete_event_id).first()
            if event:
                db.session.delete(event)
                db.session.commit()
                return redirect(url_for('admin.event.index'))
    event = Event.query.filter(Event.id == event_id).first()
    return render_template("event/view.html", event=event)
