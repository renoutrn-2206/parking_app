from __future__ import annotations

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app(config: dict | None = None) -> Flask:
    app = Flask(__name__)

    if config:
        app.config.update(config)

    app.config.setdefault("SQLALCHEMY_DATABASE_URI", "sqlite:///parking.db")
    app.config.setdefault("SQLALCHEMY_TRACK_MODIFICATIONS", False)

    db.init_app(app)

    from .routes import bp

    app.register_blueprint(bp)

    return app
