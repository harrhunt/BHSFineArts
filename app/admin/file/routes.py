from flask import render_template, redirect, url_for, request, current_app as app
from flask_login import login_required
from werkzeug.utils import secure_filename
from app.admin.file import bp
from app.models import File
from app.forms import FileForm
from app import db
import os


@bp.route('/')
@login_required
def index():
    file = File.query.all()
    return render_template("file/index.html", file=file)


@bp.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    form = FileForm()
    if form.validate_on_submit():
        uploaded_files = request.files.getlist(form.files.name)
        to_save = []
        for uploaded_file in uploaded_files:
            filename = secure_filename(uploaded_file.filename)
            if filename != '':
                basename, ext = os.path.splitext(filename)
                ext = ext.lower()
                if not len(app.config["EXTENSIONS_WHITELIST"]):
                    if ext in app.config["EXTENSIONS_BLACKLIST"]:
                        form.files.errors.append(f'{ext if ext else "Unknown"} file types are not allowed')
                        return render_template("file/add.html", form=form)
                else:
                    if ext not in app.config["EXTENSIONS_WHITELIST"]:
                        form.files.errors.append(f'{ext if ext else "Unknown"} file types are not allowed')
                        return render_template("file/add.html", form=form)
                new_file = File(basename=basename, extension=ext)
                db.session.add(new_file)
                to_save.append((uploaded_file, new_file))
            else:
                form.files.errors.append('Invalid filename')
                return render_template("file/add.html", form=form)
        try:
            db.session.commit()
        except Exception as err:
            form.submit.errors.append(str(err))
        else:
            for file in to_save:
                file[0].save(os.path.join(app.config["UPLOAD_PATH"], str(file[1].id)))
            return redirect(url_for('admin.file.index'))
    return render_template("file/add.html", form=form)


@bp.route('/edit/<int:file_id>', methods=['GET', 'POST'])
@login_required
def edit(file_id):
    file = File.query.filter(File.id == file_id).first()
    form = FileForm(obj=file)
    if form.validate_on_submit():
        form.populate_obj(file)
        try:
            db.session.add(file)
            db.session.commit()
        except Exception as err:
            form.submit.errors.append(str(err))
        else:
            return redirect(url_for('admin.file.index'))
    return render_template("file/edit.html", form=form)


@bp.route('/<int:file_id>', methods=['GET', 'POST'])
@login_required
def view(file_id):
    if request.method == 'POST':
        delete_file_id = int(request.form.get('id'))
        if delete_file_id == file_id:
            file = File.query.filter(File.id == delete_file_id).first()
            if file:
                db.session.delete(file)
                db.session.commit()
                os.remove(os.path.join(app.config["UPLOAD_PATH"], str(delete_file_id)))
                return redirect(url_for('admin.file.index'))
    file = File.query.filter(File.id == file_id).first()
    return render_template("file/view.html", file=file)
