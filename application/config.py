import os


class Config(object):
    APPRISE_URL = os.environ.get("APPRISE_URL", "http://localhost:8000")


class DevelopmentConfig(Config):
    ENV = "development"
    DEVELOPMENT = True


class ProductionConfig(Config):
    DEBUG = False
