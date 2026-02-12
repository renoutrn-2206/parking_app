import random

import factory
from faker import Faker

from app import db
from app.models import Client, Parking

fake = Faker("ru_RU")


class ClientFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Client
        sqlalchemy_session = db.session
        sqlalchemy_session_persistence = "flush"

    name = factory.LazyAttribute(lambda _: fake.first_name())
    surname = factory.LazyAttribute(lambda _: fake.last_name())
    credit_card = factory.Maybe(
        factory.LazyAttribute(lambda _: random.choice([True, False])),
        yes_declaration=factory.LazyAttribute(
            lambda _: fake.credit_card_number()
        ),
        no_declaration=None,
    )
    car_number = factory.LazyAttribute(lambda _: fake.license_plate())


class ParkingFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Parking
        sqlalchemy_session = db.session
        sqlalchemy_session_persistence = "flush"

    address = factory.LazyAttribute(lambda _: fake.address())
    opened = factory.LazyAttribute(lambda _: random.choice([True, False]))
    count_places = factory.LazyAttribute(lambda _: fake.random_int(min=1, max=100))

    @factory.lazy_attribute
    def count_available_places(self) -> int:
        return self.count_places