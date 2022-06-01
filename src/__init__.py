from flask import Flask
from .api.v1.routes.note import note
from .config.config import SECRET_KEY,JWT_SECRET_KEY
from flask_jwt_extended import JWTManager
from .api.v1.routes.auth import auth


def create_app():
    app = Flask(__name__)

    app.config.from_mapping(
        SECERT_KEY=SECRET_KEY,
        JWT_SECRET_KEY=JWT_SECRET_KEY
    )

    JWTManager(app)
    app.register_blueprint(note)
    app.register_blueprint(auth)
    return app