from app.controllers.notam_controller import NotamController
from app.extentions import notam_ns


def register_notam_routes():
    notam_ns.add_resource(NotamController,'')