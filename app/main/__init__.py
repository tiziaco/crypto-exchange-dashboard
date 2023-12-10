from flask import Flask
from flask_sqlalchemy import SQLAlchemy
# from flask_bcrypt import Bcrypt

from .config import config_by_name

db = SQLAlchemy()
# flask_bcrypt = Bcrypt()


def create_app(config_name: str) -> Flask:
    app = Flask(__name__, template_folder='views')
    app.config.from_object(config_by_name[config_name])
    db.init_app(app)
    with app.app_context():
        from .controllers.routes import views_blueprint
        from .controllers.user_routes import user_blueprint
        from .controllers.portfolio_routes import portfolio_blueprint

        app.register_blueprint(user_blueprint)
        app.register_blueprint(views_blueprint)
        app.register_blueprint(portfolio_blueprint)
    # flask_bcrypt.init_app(app)

    return app