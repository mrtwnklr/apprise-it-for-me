import logging
from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config.from_object('application.config.Config')

    logging.basicConfig(format='%(message)s', level=app.config['LOGLEVEL'])
    app.logger.info('delegating notification requests to %s', app.config['APPRISE_URL'])

    with app.app_context():
        from application.routes import health
        from application.routes import notify

    return app
