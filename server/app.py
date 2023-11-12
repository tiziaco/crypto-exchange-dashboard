import os
import unittest
from flask import Flask
from flask.cli import FlaskGroup
#from flask_migrate import Migrate

from main import create_app, db

app = create_app(os.getenv('BOILERPLATE_ENV') or 'dev')
with app.app_context():
    from main.controllers import routes
    # TODO: import dash app
    from main.views.dash import demo

    # TODO: initialize dash app
    app = demo.init_dash(app)

#migrate = Migrate(app, db)

# Create a FlaskGroup instead of a Manager
cli = FlaskGroup(app)

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
