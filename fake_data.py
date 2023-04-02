from faker import Faker
from faker.providers import person, internet, misc, date_time, address, company
from app import db
from app.models import Faculty, Event, File
from collections import OrderedDict
from flaskconf import DevelopmentConfig
import os.path
from datetime import date, datetime, timedelta

fake = Faker()
fake.add_provider(person)
fake.add_provider(internet)
fake.add_provider(misc)
fake.add_provider(date_time)
fake.add_provider(address)
fake.add_provider(company)


def fake_file(n=100):
    for _ in range(n):
        filename = fake.file_name(category="image", extension="png")
        basename, extension = os.path.splitext(filename)
        db.session.add(File(basename=basename, extension=extension))
    db.session.commit()
    for file in File.query.all():
        with open(os.path.join(DevelopmentConfig.UPLOAD_PATH, str(file.id)), "wb") as filestream:
            filestream.write(fake.image(image_format=file.extension[1:]))


def fake_faculty(n=50):
    for _ in range(n):
        db.session.add(Faculty(
            first_name=fake.first_name(),
            middle_name=fake.first_name() if fake.random_int(max=9) < 3 else '',
            last_name=fake.last_name(),
            position=fake.random_element(elements=OrderedDict([("Teacher", 0.8), ("Aid", 0.15), ("Accompanist", 0.05)])),
            email=fake.ascii_safe_email(),
            department_id=fake.random_int(min=1, max=7),
            image_id=fake.random_int(max=File.query.count() - 1)
        ))
    db.session.commit()


def fake_event(n=150):
    for _ in range(n):
        start_datetime = fake.date_time_this_decade(after_now=True)
        db.session.add(Event(
            name=fake.bs().title(),
            start_datetime=start_datetime,
            end_datetime=start_datetime + timedelta(
                days=fake.random_element(elements=OrderedDict([
                    (0, 0.5),
                    (1, 0.36),
                    (2, 0.05),
                    (3, 0.01),
                    (4, 0.01),
                    (5, 0.01),
                    (6, 0.01),
                    (7, 0.05)
                ])),
                hours=fake.random_element(elements=OrderedDict([
                    (0, 0.15),
                    (1, 0.35),
                    (2, 0.35),
                    (3, 0.05),
                    (4, 0.05),
                    (5, 0.05)
                ])),
                minutes=fake.random_element(elements=OrderedDict([
                    (0, 0.85),
                    (30, 0.15)
                ]))
            ),
            price=fake.random_int(max=150),
            location=fake.company(),
            street=fake.street_address(),
            city=fake.city(),
            state=fake.state(),
            zip=fake.postcode(),
            country=fake.country() if fake.random_int(max=9) < 1 else '',
            department_id=fake.random_int(min=1, max=7),
        ))
    db.session.commit()


def generate_fake():
    fake_event()
    fake_file()
    fake_faculty()


if __name__ == '__main__':
    generate_fake()
