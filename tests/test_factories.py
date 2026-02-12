from app.factories import ClientFactory, ParkingFactory

from app import db
from app.models import Client, Parking


def test_create_client_with_factory(app):
    with app.app_context():
        count_before = db.session.query(Client).count()
        client = ClientFactory()
        db.session.commit()

        assert client.id is not None
        count_after = db.session.query(Client).count()
        assert count_after == count_before + 1


def test_create_parking_with_factory(app):
    with app.app_context():
        count_before = db.session.query(Parking).count()
        parking = ParkingFactory()
        db.session.commit()

        assert parking.id is not None
        assert parking.count_available_places == parking.count_places
        count_after = db.session.query(Parking).count()
        assert count_after == count_before + 1
