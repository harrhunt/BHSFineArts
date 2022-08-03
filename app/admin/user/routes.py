from flask import render_template, redirect, url_for
from flask_login import login_required
from werkzeug.security import generate_password_hash
from app.admin.user import bp
from app.models import User
from app.forms import SignUpForm
from app import db


@bp.route('/')
@login_required
def index():
    user = User.query.all()
    return render_template("user/index.html", user=user)


@bp.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    form = SignUpForm()
    if form.validate_on_submit():
        new_user = User()
        form.populate_obj(new_user)
        new_user.password = generate_password_hash(new_user.password)
        try:
            db.session.add(new_user)
            db.session.commit()
        except Exception as err:
            form.submit.errors.append(str(err))
        else:
            return redirect(url_for('admin.user.index'))
    return render_template("user/add.html", form=form)


@bp.route('/edit/<int:user_id>', methods=['GET', 'POST'])
@login_required
def edit(user_id):
    user = User.query.filter(User.id == user_id).first()
    form = SignUpForm(obj=user)
    if form.validate_on_submit():
        form.populate_obj(user)
        user.password = generate_password_hash(user.password)
        try:
            db.session.add(user)
            db.session.commit()
        except Exception as err:
            form.submit.errors.append(str(err))
        else:
            return redirect(url_for('admin.user.index'))
    return render_template("user/edit.html", form=form)


@bp.route('/<int:user_id>')
@login_required
def view(user_id):
    user = User.query.filter(User.id == user_id).first()
    return render_template("user/view.html", user=user)
