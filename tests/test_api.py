import pytest


@pytest.mark.parametrize("url", ["/clients", "/clients/1"])
def test_get_endpoints_status_200(client, url):
    resp = client.get(url)
    assert resp.status_code == 200


def test_create_client(client):
    payload = {
        "name": "Ivan",
        "surname": "Ivanov",
        "credit_card": "1111-2222",
        "car_number": "B456CD",
    }
    resp = client.post("/clients", json=payload)
    assert resp.status_code == 201
    data = resp.get_json()
    assert "id" in data


def test_create_parking(client):
    payload = {
        "address": "Another street, 2",
        "opened": True,
        "count_places": 20,
    }
    resp = client.post("/parkings", json=payload)
    assert resp.status_code == 201
    data = resp.get_json()
    assert "id" in data


@pytest.mark.parking
def test_parking_in(client, db_session):
    payload = {"client_id": 1, "parking_id": 1}
    resp = client.post("/client_parkings", json=payload)
    assert resp.status_code == 201

    from app.models import Parking

    parking = db_session.get(Parking, 1)
    assert parking.count_available_places == 9  # было 10, стало 9


@pytest.mark.parking
def test_parking_out(client, db_session):
    client.post("/client_parkings", json={"client_id": 1, "parking_id": 1})

    resp = client.delete("/client_parkings", json={"client_id": 1, "parking_id": 1})
    assert resp.status_code == 200

    from app.models import ClientParking, Parking

    parking = db_session.get(Parking, 1)
    assert parking.count_available_places == 10  # вернулось место

    cp = (
        db_session.query(ClientParking)
        .filter_by(client_id=1, parking_id=1)
        .order_by(ClientParking.id.desc())
        .first()
    )
    assert cp.time_out is not None
    assert cp.time_out >= cp.time_in
