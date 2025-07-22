import os
from dotenv import load_dotenv

flask_env = os.getenv('FLASK_ENV', 'development')  # set_default
dotenv_file = os.path.join(os.path.dirname(__file__), f'../.env.{flask_env}')

if os.path.exists(dotenv_file):
    load_dotenv(dotenv_file)
else:
    print(f"⚠️ Warning: {dotenv_file} not found! Using system environment variables.")

class Config(object):
    SECRET_KEY=os.environ.get("SECRET_KEY",os.urandom(24))
    MONGO_HOST=os.environ.get("MONGO_HOST","localhost")
    MONGO_PORT=os.environ.get("MONGO_PORT","27017")
    MONGO_USERNAME=os.environ.get("MONGO_USERNAME","admin")
    MONGO_PASSWORD=os.environ.get("MONGO_PASSWORD","<PASSWORD>")
    MONGO_DBNAME=os.environ.get("MONGO_DBNAME","db")


class ProductionConfig(Config):
    DEBUG = False
    MONGO_URI = f"mongodb://{Config.MONGO_USERNAME}:{Config.MONGO_PASSWORD}@{Config.MONGO_HOST}:{Config.MONGO_PORT}/{Config.MONGO_DBNAME}"

class DevelopmentConfig(Config):
    DEBUG = True
    MONGO_URI = f"mongodb://{Config.MONGO_HOST}:{Config.MONGO_PORT}/{Config.MONGO_DBNAME}"


