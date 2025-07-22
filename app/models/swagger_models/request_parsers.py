from flask_restx import reqparse

notam_search=reqparse.RequestParser()
notam_search.add_argument("retrieveLocId", type=int)