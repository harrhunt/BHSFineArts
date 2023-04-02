from flask import render_template, redirect, url_for, request
from flask_login import login_required
from app.admin.faculty import bp
from app.models import Faculty, Department, File
from app.forms import FacultyForm
from app import db


@bp.route('/')
@login_required
def index():
    faculty = Faculty.query.all()
    return render_template("faculty/index.html", faculty=faculty)


@bp.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    form = FacultyForm()
    form.department.query = Department.query
    form.image.query = File.query
    if form.validate_on_submit():
        new_faculty_member = Faculty()
        form.populate_obj(new_faculty_member)
        try:
            db.session.add(new_faculty_member)
            db.session.commit()
        except Exception as err:
            form.submit.errors.append(str(err))
        else:
            return redirect(url_for('admin.faculty.index'))
    return render_template("faculty/add.html", form=form)


@bp.route('/edit/<int:faculty_id>', methods=['GET', 'POST'])
@login_required
def edit(faculty_id):
    faculty_member = Faculty.query.filter(Faculty.id == faculty_id).first()
    form = FacultyForm(obj=faculty_member)
    form.department.query = Department.query
    if form.validate_on_submit():
        form.populate_obj(faculty_member)
        try:
            db.session.add(faculty_member)
            db.session.commit()
        except Exception as err:
            form.submit.errors.append(str(err))
        else:
            return redirect(url_for('admin.faculty.index'))
    return render_template("faculty/edit.html", form=form)


@bp.route('/<int:faculty_id>', methods=['GET', 'POST'])
@login_required
def view(faculty_id):
    if request.method == 'POST':
        delete_faculty_id = int(request.form.get('id'))
        if delete_faculty_id == faculty_id:
            faculty_member = Faculty.query.filter(Faculty.id == delete_faculty_id).first()
            if faculty_member:
                db.session.delete(faculty_member)
                db.session.commit()
                return redirect(url_for('admin.faculty.index'))
    faculty_member = Faculty.query.filter(Faculty.id == faculty_id).first()
    return render_template("faculty/view.html", faculty_member=faculty_member)
