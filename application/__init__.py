import os

from flask import Flask


def create_app(logger_override=None):
    app = Flask(__name__)

    if logger_override:
        app.logger.handlers = logger_override.handlers
        app.logger.setLevel(logger_override.level)

    environment_configuration = os.environ.get(
        "APP_SETTINGS", __package__ + ".config.DevelopmentConfig"
    )
    app.config.from_object(environment_configuration)

    app.logger.info(
        "delegating notification requests to %s", app.config["APPRISE_URL"]
    )

    with app.app_context():
        import application.routes.health  # noqa: F401
        import application.routes.notify  # noqa: F401

    return app
