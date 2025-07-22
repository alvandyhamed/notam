from flask import Flask
from flask_pymongo import PyMongo
from werkzeug.middleware.proxy_fix import ProxyFix

from app.config import DevelopmentConfig
from app.routs import configure_routs


from app.extentions import mongo



def create_app(config_class=DevelopmentConfig):
    app = Flask(__name__, instance_relative_config=True)
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_port=1, x_prefix=1)
    app.config.from_object(config_class or DevelopmentConfig)
    app.config["JWT_TOKEN_LOCATION"] = ["headers"]
    app.config["JWT_HEADER_NAME"] = "Authorization"
    app.config["JWT_HEADER_TYPE"] = "Bearer"

    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config.from_object(config_class)

    mongo.init_app(app)
    configure_routs(app)


    return app

if __name__ == '__main__':
    print('Starting app...')

