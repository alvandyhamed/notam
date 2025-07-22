import os


class Config(object):
    SECRET_KEY=os.environ.get("SECRET_KEY","your-secret-key")
    MONGO_HOST=os.environ.get("MONGO_HOST","localhost")
    MONGO_PORT=os.environ.get("MONGO_PORT","27017")
    MONGO_USERNAME=os.environ.get("MONGO_USERNAME","admin")
    MONGO_PASSWORD=os.environ.get("MONGO_PASSWORD","<PASSWORD>")
    MONGO_DBNAME=os.environ.get("MONGO_DBNAME","db")

class ProductionConfig(Config):
    DEBUG = False
class DevelopmentConfig(Config):
    DEBUG = True
