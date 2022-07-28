from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, FloatField, DateField, TimeField, FileField, SubmitField
from wtforms.validators import InputRequired, Email, NumberRange, Optional
from wtforms_sqlalchemy.fields import QuerySelectField
from app.models import User, Department, Faculty, Event
from app import db


class UserForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Email('Invalid Email'), ])
    password = PasswordField('Password', validators=[InputRequired()])
    submit = SubmitField('Submit')


class LoginForm(UserForm):
    remember = BooleanField('Remember me')
    submit = SubmitField('Login')


class DepartmentForm(FlaskForm):
    name = StringField('Name', validators=[InputRequired()])
    submit = SubmitField('Submit')


class FacultyForm(FlaskForm):
    first_name = StringField('First Name', validators=[InputRequired()])
    middle_name = StringField('Middle Name', validators=[Optional()])
    last_name = StringField('Last Name', validators=[InputRequired()])
    position = StringField('Position')
    email = StringField('Email', validators=[Email()])
    department = QuerySelectField(get_label='name')
    submit = SubmitField('Submit')


class EventForm(FlaskForm):
    name = StringField('Name', validators=[InputRequired()])
    start_date = DateField('Start Date')
    start_time = TimeField('Start Time')
    end_date = DateField('End Date')
    end_time = TimeField('End Time')
    price = FloatField('Price', validators=[NumberRange(min=0, message='Must be greater than or equal to %(min)s')])
    street = StringField('Street Address')
    city = StringField('City')
    state = StringField('State')
    zip = StringField('Zip')
    country = StringField('Country')
    department = QuerySelectField(get_label='name')
    submit = SubmitField('Submit')


class FileForm(FlaskForm):
    file = FileField('File', validators=[InputRequired()])
    submit = SubmitField('Submit')


# FacultyFormTest = model_form(Faculty, db_session=db.session, base_class=FlaskForm)
