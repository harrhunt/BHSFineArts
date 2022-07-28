from flask import render_template, request, send_from_directory, current_app as app
from app.main import bp
from app.models import Department


@bp.route("/uploads/<path:filename>")
def uploads(filename):
    return send_from_directory(app.config["UPLOAD_PATH"], filename, as_attachment=True)


@bp.route("/")
def index():
    return render_template("index.html", departments=Department.query.all())


# @bp.route("/test", methods=['GET', 'POST'])
# def test():
#     form = FacultyForm()
#     form.department.query = Department.query
#     if request.method == 'POST':
#         if form.validate_on_submit():
#             print("valid")
#     return render_template("test.html", form=form)


@bp.route("/art")
def art():
    return "Test"


@bp.route("/band")
def band():
    return "Test"


@bp.route("/choir")
def choir():
    return "Test"


@bp.route("/dance")
def dance():
    return "Test"


@bp.route("/drama")
def drama():
    return "Test"


@bp.route("/musical_theater")
def musical_theater():
    return "Test"


@bp.route("/orchestra")
def orchestra():
    return "Test"
