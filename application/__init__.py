import logging
import os
from flask import Flask

def create_app():
    app = Flask(__name__)
    environment_configuration = os.environ.get('APP_SETTINGS', __package__ + '.config.DevelopmentConfig')
    app.config.from_object(environment_configuration)

    logging.basicConfig(format='%(message)s', level=app.config['LOGLEVEL'])
    app.logger.info('delegating notification requests to %s', app.config['APPRISE_URL'])

    with app.app_context():
        from application.routes import health
        from application.routes import notify

    return app
