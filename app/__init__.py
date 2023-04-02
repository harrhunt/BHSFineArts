from flask import Flask, redirect, url_for, request
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flaskconf import SELECTED_CONFIG


db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'admin.login'


@login.unauthorized_handler
def unauthorized():
    return redirect(url_for('admin.login', next=request.endpoint))


def create_app(flask_configuration=SELECTED_CONFIG):
    app = Flask(__name__)
    app.config.from_object(flask_configuration)

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.department import bp as department_bp
    app.register_blueprint(department_bp)

    from app.admin import bp as admin_bp
    app.register_blueprint(admin_bp, url_prefix='/admin')

    return app


from app import models
