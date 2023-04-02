from __future__ import annotations
from typing import List

from flask_login import UserMixin
from app import db, login
from datetime import datetime
from sqlalchemy.orm import Mapped


IMAGE_FILE_EXT = ['.jpeg', '.jpg', '.png', '.gif']


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id: Mapped[int] = db.mapped_column(primary_key=True)
    email: Mapped[str] = db.mapped_column(db.String(255), nullable=False, unique=True)
    password: Mapped[str] = db.mapped_column(db.String(255), nullable=False)
    # username = db.Column(db.String(24), unique=True)
    # is_verified = db.Column(db.Boolean(), default=False)
    # last_active = db.Column(db.DateTime())
    # reset_token = db.Column(db.String(255))

    def __repr__(self) -> str:
        return f"<User {self.id}: {self.email}>"


@login.user_loader
def user_loader(user_id):
    return User.query.get(user_id)


class Department(db.Model):
    __tablename__ = "departments"
    id: Mapped[int] = db.mapped_column(primary_key=True)
    name: Mapped[str] = db.mapped_column(db.String(255), nullable=False, unique=True)
    events: Mapped[List['Event']] = db.relationship(back_populates='department')
    faculty: Mapped[List['Faculty']] = db.relationship(back_populates='department')

    def __repr__(self) -> str:
        return f"<Department {self.id}: {self.name}>"


class File(db.Model):
    __tablename__ = "files"
    id: Mapped[int] = db.mapped_column(primary_key=True)
    basename: Mapped[str] = db.mapped_column(db.String(255), nullable=False)
    extension: Mapped[str] = db.mapped_column(db.String(255), nullable=True)
    date_added: Mapped[datetime] = db.mapped_column(default=datetime.utcnow())

    @classmethod
    def image_files(cls) -> list['File']:
        return cls.query.filter(cls.extension.in_(IMAGE_FILE_EXT))

    @property
    def name(self) -> str:
        return f"{self.basename}{self.extension}"

    @property
    def is_image(self) -> bool:
        return self.extension in IMAGE_FILE_EXT

    def __repr__(self) -> str:
        return f"<File {self.id}: {self.basename}{self.extension}>"


class Faculty(db.Model):
    __tablename__ = "faculty"
    id: Mapped[int] = db.mapped_column(primary_key=True)
    first_name: Mapped[str] = db.mapped_column(db.String(255), nullable=False)
    middle_name: Mapped[str] = db.mapped_column(db.String(255), nullable=True)
    last_name: Mapped[str] = db.mapped_column(db.String(255), nullable=False)
    position: Mapped[str] = db.mapped_column(db.String(255), nullable=True)
    email: Mapped[str] = db.mapped_column(db.String(255), nullable=True)
    department_id: Mapped[int] = db.mapped_column(db.ForeignKey('departments.id'))
    department: Mapped['Department'] = db.relationship(back_populates='faculty')
    image_id: Mapped[int] = db.mapped_column(db.ForeignKey('files.id'), nullable=True)
    image: Mapped['File'] = db.relationship()

    def __repr__(self) -> str:
        return f"<Faculty {self.id}: {self.first_name} {self.last_name} ({self.department.name})>"


class Event(db.Model):
    __tablename__ = "events"
    id: Mapped[int] = db.mapped_column(primary_key=True)
    name: Mapped[str] = db.mapped_column(db.String(255), nullable=False)
    start_datetime: Mapped[datetime] = db.mapped_column(nullable=True)
    end_datetime: Mapped[datetime] = db.mapped_column(nullable=True)
    price: Mapped[float] = db.mapped_column(nullable=True)
    location: Mapped[str] = db.mapped_column(db.String(255), nullable=True)
    street: Mapped[str] = db.mapped_column(db.String(255), nullable=True)
    city: Mapped[str] = db.mapped_column(db.String(255), nullable=True)
    state: Mapped[str] = db.mapped_column(db.String(255), nullable=True)
    zip: Mapped[int] = db.mapped_column(nullable=True)
    country: Mapped[str] = db.mapped_column(db.String(255), nullable=True)
    department_id: Mapped[int] = db.mapped_column(db.ForeignKey('departments.id'))
    department: Mapped['Department'] = db.relationship(back_populates='events')

    def __repr__(self) -> str:
        return f"<Event {self.id}: {self.name}"
