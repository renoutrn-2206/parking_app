from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app(test_config: dict | None = None) -> Flask:
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///parking.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["TESTING"] = False

    if test_config:
        app.config.update(test_config)

    db.init_app(app)

    from .models import Client, Parking, ClientParking  # noqa
    from .routes import bp

    app.register_blueprint(bp)

    with app.app_context():
        db.create_all()

    return app
