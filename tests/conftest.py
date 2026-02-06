import pytest

from app import create_app, db
from app.models import Client, Parking, ClientParking


@pytest.fixture(scope="session")
def app():
    app = create_app(
        {
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        }
    )
    with app.app_context():
        db.create_all()

        client = Client(
            name="Test",
            surname="User",
            credit_card="1234-5678",
            car_number="A123BC",
        )
        db.session.add(client)

        parking = Parking(
            address="Test street, 1",
            opened=True,
            count_places=10,
            count_available_places=10,
        )
        db.session.add(parking)
        db.session.commit()

        cp = ClientParking(
            client_id=client.id,
            parking_id=parking.id,
        )
        db.session.add(cp)
        db.session.commit()

        yield app

        db.drop_all()


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def db_session(app):
    return db.session
