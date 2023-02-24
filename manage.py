import logging

from application import create_app

gunicorn_logger = None
if __name__ != "__main__":
    gunicorn_logger = logging.getLogger("gunicorn.error")

app = create_app(gunicorn_logger)

if __name__ == "__main__":
    app.run()
