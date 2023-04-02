from app import create_app, db
from app.models import User, Department, Faculty, Event, File
from werkzeug.security import generate_password_hash
# noinspection PyPackageRequirements
import sass
from fake_data import generate_fake

sass.compile(dirname=('app/static/styles/sass', 'app/static/styles/css'), output_style='compressed')

app = create_app()


def set_up_db():
    db.create_all()
    departments = [
        Department(name="Art"),
        Department(name="Band"),
        Department(name="Choir"),
        Department(name="Dance"),
        Department(name="Drama"),
        Department(name="Musical Theater"),
        Department(name="Orchestra")
    ]
    db.session.add_all(departments)
    admin = User(email=app.config["ADMIN_EMAIL"], password=generate_password_hash(app.config["ADMIN_PASSWORD"]))
    db.session.add(admin)
    db.session.commit()


@app.shell_context_processor
def make_shell_context():
    return {'db': db,
            'User': User,
            'Department': Department,
            'File': File,
            'Faculty': Faculty,
            'Event': Event,
            'set_up_db': set_up_db,
            'generate_fake': generate_fake
            }
