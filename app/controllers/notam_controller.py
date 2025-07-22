import os
from flask import request
from flask_restx import Resource

from app.config import ProductionConfig
from app.extentions import notam_ns
from app.models.swagger_models.request_parsers import notam_search
from app.models.swagger_models.response_models import get_response_models
from app.utils.decorator import notam_decorato

response_models = get_response_models(notam_ns)

for model_name, model in response_models.items():
    notam_ns.models[model_name] = model


class BaseController(Resource):
    env=os.environ.get("FLASK_ENV", "development")
    if env == "production":
        config=ProductionConfig()


    def handle_request(self,context,operation,retrieveLocId=None):


        if operation == "get":
            return self._get_notam(context,retrieveLocId)

    def _get_notam(self,context,retrieveLocId):
        try:
            response, status_code=context.get_Notam(retrieveLocId)
            if status_code == 200:
                return response,status_code
            else:
                return response,status_code

        except Exception as e:
            print(e)
            return "There is an issue",500

@notam_decorato
class NotamController(BaseController):

    @notam_ns.expect(notam_search)
    @notam_ns.marshal_with(response_models["get_notam"])
    def get(self,context,**kwargs):
        retrieveLocId=request.args.get("retrieveLocId")
        return self.handle_request(context,"get",retrieveLocId=retrieveLocId)


