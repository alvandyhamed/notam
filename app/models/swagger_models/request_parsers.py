

from flask_restx import reqparse

notam_search=reqparse.RequestParser()
notam_search.add_argument("retrieveLocId", type=str)
notam_search.add_argument("flight_number", type=str)
notam_search.add_argument("user_id", type=str)
notam_search.add_argument("date", type=str)
notam_search.add_argument("rout", type=str)

