from flask import Flask
from .api.v1.routes.note import note
from .config import SECRET_KEY, JWT_SECRET_KEY, JWT_ACCESS_TOKEN_EXPIRES, JWT_REFRESH_TOKEN_EXPIRES, JWT_TOKEN_LOCATION, JWT_QUERY_STRING_NAME
from flask_jwt_extended import JWTManager
from .api.v1.routes.auth import auth


def create_app():
    app = Flask(__name__)

    app.config.from_mapping(
        SECERT_KEY=SECRET_KEY,
        JWT_SECRET_KEY=JWT_SECRET_KEY,
        JWT_ACCESS_TOKEN_EXPIRES=JWT_ACCESS_TOKEN_EXPIRES,
        JWT_REFRESH_TOKEN_EXPIRES=JWT_REFRESH_TOKEN_EXPIRES,
        JWT_TOKEN_LOCATION=JWT_TOKEN_LOCATION,
        JWT_QUERY_STRING_NAME=JWT_QUERY_STRING_NAME
    )

    JWTManager(app)
    app.register_blueprint(note)
    app.register_blueprint(auth)
    return app