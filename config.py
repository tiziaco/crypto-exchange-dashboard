from os import environ


class Config:
    """Flask configuration variables."""

    # General Config
    APP_NAME = environ.get("APP_NAME")
    DEBUG = environ.get("FLASK_DEBUG")
    SECRET_KEYS = environ.get("SECRET_KEYS")

    # Static Assets
    STATIC_FOLDER = "static"
    TEMPLATE_FOLDER = "templates"