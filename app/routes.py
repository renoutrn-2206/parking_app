from datetime import datetime

from flask import Blueprint, abort, jsonify, request

from . import db
from .models import Client, ClientParking, Parking

bp = Blueprint("api", __name__)


@bp.get("/clients")
def get_clients():
    clients = Client.query.all()
    return jsonify(
        [
            {
                "id": c.id,
                "name": c.name,
                "surname": c.surname,
                "credit_card": c.credit_card,
                "car_number": c.car_number,
            }
            for c in clients
        ]
    )


@bp.get("/clients/<int:client_id>")
def get_client(client_id: int):
    client = Client.query.get_or_404(client_id)
    return jsonify(
        {
            "id": client.id,
            "name": client.name,
            "surname": client.surname,
            "credit_card": client.credit_card,
            "car_number": client.car_number,
        }
    )


@bp.post("/clients")
def create_client():
    data = request.json or {}
    client = Client(
        name=data["name"],
        surname=data["surname"],
        credit_card=data.get("credit_card"),
        car_number=data.get("car_number"),
    )
    db.session.add(client)
    db.session.commit()
    return jsonify({"id": client.id}), 201


@bp.post("/parkings")
def create_parking():
    data = request.json or {}
    count_places = data["count_places"]
    parking = Parking(
        address=data["address"],
        opened=data.get("opened", True),
        count_places=count_places,
        count_available_places=data.get("count_available_places", count_places),
    )
    db.session.add(parking)
    db.session.commit()
    return jsonify({"id": parking.id}), 201


@bp.post("/client_parkings")
def client_parking_in():
    data = request.json or {}
    client_id = data["client_id"]
    parking_id = data["parking_id"]

    client = Client.query.get_or_404(client_id)
    parking = Parking.query.get_or_404(parking_id)

    if not parking.opened:
        abort(400, description="Parking closed")
    if parking.count_available_places <= 0:
        abort(400, description="No available places")

    # проверка, что этот клиент уже не стоит на этой парковке
    existing = ClientParking.query.filter_by(
        client_id=client.id, parking_id=parking.id, time_out=None
    ).first()
    if existing:
        abort(400, description="Client already parked here")

    parking.count_available_places -= 1

    cp = ClientParking(client_id=client.id, parking_id=parking.id)
    db.session.add(cp)
    db.session.commit()

    return jsonify({"id": cp.id, "time_in": cp.time_in.isoformat()}), 201


@bp.delete("/client_parkings")
def client_parking_out():
    data = request.json or {}
    client_id = data["client_id"]
    parking_id = data["parking_id"]

    client = Client.query.get_or_404(client_id)
    parking = Parking.query.get_or_404(parking_id)

    if not client.credit_card:
        abort(400, description="No credit card on client")

    cp = ClientParking.query.filter_by(
        client_id=client.id, parking_id=parking.id, time_out=None
    ).first()
    if not cp:
        abort(400, description="Client is not parked here")

    now = datetime.utcnow()
    if cp.time_in and now < cp.time_in:
        abort(400, description="time_out earlier than time_in")

    cp.time_out = now
    parking.count_available_places += 1

    db.session.commit()

    return jsonify({"id": cp.id, "time_out": cp.time_out.isoformat()})
