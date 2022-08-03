from flask import request, render_template, redirect, url_for
from flask_login import login_required, current_user, login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from app.admin import bp
from app.forms import LoginForm
from app.models import User


@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'GET':
        if current_user.is_authenticated:
            return redirect(url_for("admin.index"))
        else:
            return render_template("admin/login.html", form=form)
    elif request.method == 'POST':
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user:
                if check_password_hash(user.password, form.password.data):
                    login_user(user, remember=form.remember.data)
                    next_loc = request.args.get('next')
                    if next_loc is not None:
                        return redirect(url_for(next_loc))
                    else:
                        return redirect(url_for("admin.index"))
            form.password.errors.append("Invalid username and password combination!")
        if "csrf_token" in form.errors:
            form = LoginForm()
            # return render_template("admin/login.html", form=form)
        return render_template("admin/login.html", form=form)


@bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.index"))


@bp.route('/')
@login_required
def index():
    return render_template("admin/admin.html")
