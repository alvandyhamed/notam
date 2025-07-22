from flask_pymongo import PyMongo
from flask_restx import Namespace

notam_ns=Namespace("notam", description="Notam API")

mongo = PyMongo()
