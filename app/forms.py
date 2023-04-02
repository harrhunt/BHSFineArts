from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import StringField, PasswordField, BooleanField, DecimalField, IntegerField, MultipleFileField, SubmitField, DateTimeLocalField  # DateField, TimeField
from wtforms.validators import InputRequired, Email, NumberRange, Optional, EqualTo
from wtforms_sqlalchemy.fields import QuerySelectField
from wtforms.widgets import NumberInput
# from app.models import User, Department, Faculty, Event


class UserForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Email('Invalid Email'), ])
    password = PasswordField('Password', validators=[InputRequired()])
    submit = SubmitField('Submit')


class LoginForm(UserForm):
    remember = BooleanField('Remember me')
    submit = SubmitField('Login')


class SignUpForm(UserForm):
    password_confirm = PasswordField(
        'Confirm Password',
        validators=[InputRequired(), EqualTo('password', message='Passwords must match')]
    )


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
    image = QuerySelectField(get_label='name')
    submit = SubmitField('Submit')


class EventForm(FlaskForm):
    name = StringField('Name', validators=[InputRequired()])
    start_datetime = DateTimeLocalField('Start Date and Time', format="%Y-%m-%dT%H:%M")
    end_datetime = DateTimeLocalField('End Date and Time', format="%Y-%m-%dT%H:%M")
    # start_date = DateField('Start Date')
    # start_time = TimeField('Start Time')
    # end_date = DateField('End Date')
    # end_time = TimeField('End Time')
    price = DecimalField(
        'Price',
        places=None,
        validators=[NumberRange(min=0, message='Must be greater than or equal to %(min)s')],
        widget=NumberInput(0.01, min=0)
    )
    location = StringField('Location Name', validators=[Optional()])
    street = StringField('Street Address', validators=[Optional()])
    city = StringField('City', validators=[Optional()])
    state = StringField('State', validators=[Optional()])
    zip = IntegerField('Zip', validators=[Optional()])
    country = StringField('Country', validators=[Optional()])
    department = QuerySelectField(get_label='name')
    submit = SubmitField('Submit')


class FileForm(FlaskForm):
    files = MultipleFileField('File', validators=[InputRequired()])
    submit = SubmitField('Submit')


# FacultyFormTest = model_form(Faculty, db_session=db.session, base_class=FlaskForm)
