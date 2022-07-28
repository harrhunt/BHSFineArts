from flask_login import UserMixin
from app import db, login
from datetime import datetime


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    # username = db.Column(db.String(24), unique=True)
    # is_verified = db.Column(db.Boolean(), default=False)
    # last_active = db.Column(db.DateTime())
    # reset_token = db.Column(db.String(255))

    def __repr__(self):
        return f"<User {self.id}: {self.email}>"


@login.user_loader
def user_loader(user_id):
    return User.query.get(user_id)


class Department(db.Model):
    __tablename__ = "departments"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    events = db.relationship('Event', backref='department')
    faculty = db.relationship('Faculty', backref='department')

    def __repr__(self):
        return f"<Department {self.id}: {self.name}>"


class File(db.Model):
    __tablename__ = "files"
    id = db.Column(db.Integer, primary_key=True)
    basename = db.Column(db.String(255), nullable=False)
    extension = db.Column(db.String(255))
    date_added = db.Column(db.DateTime, default=datetime.utcnow())

    @classmethod
    def image_files(cls):
        return cls.query.filter(cls.extension.in_(['jpeg', 'jpg', 'png', 'gif']))

    def name(self):
        return f"{self.basename}.{self.extension}"

    def __repr__(self):
        return f"<File {self.id}: {self.basename}.{self.extension}>"


class Faculty(db.Model):
    __tablename__ = "faculty"
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255), nullable=False)
    middle_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255), nullable=False)
    position = db.Column(db.String(255))
    email = db.Column(db.String(255))
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'))

    def __repr__(self):
        return f"<Faculty {self.id}: {self.first_name} {self.last_name} ({self.department.name})>"


class Event(db.Model):
    __tablename__ = "events"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    start_datetime = db.Column(db.DateTime)
    end_datetime = db.Column(db.DateTime)
    price = db.Column(db.Float)
    street = db.Column(db.String(255))
    city = db.Column(db.String(255))
    state = db.Column(db.String(255))
    zip = db.Column(db.Integer)
    country = db.Column(db.String(255))
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'))

    def __repr__(self):
        return f"<Event {self.id}: {self.name}"
