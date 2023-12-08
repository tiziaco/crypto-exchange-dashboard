import os
import unittest
from flask.cli import FlaskGroup
from flask_migrate import Migrate

from app.main import create_app, db

app = create_app(os.getenv('BOILERPLATE_ENV') or 'dev')
cli = FlaskGroup(app)
migrate = Migrate(app, db)

with app.app_context():
    from app.main.controllers import routes
    from app.main.controllers import user_routes
    # TODO: import dash app
    # from app.main.views.dash import demo

    # db.create_all()
    # TODO: initialize dash app
    # app = demo.init_dash(app)

@cli.command()
def run():
    app.run()

@cli.command()
def test():
    """Runs the unit tests."""
    tests = unittest.TestLoader().discover('app/test', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1

if __name__ == '__main__':
    cli()
