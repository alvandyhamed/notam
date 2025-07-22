from flask_restx import Api

from app.extentions import notam_ns
from app.routs.notam import register_notam_routes


def configure_routs(app):
    api=Api(
        app,
        title="Routs Of Notam",
        version="1.0",
        description="Notam API For flysepehran"

    )

    api.add_namespace(notam_ns,path="/api/v1/notam")

    register_notam_routes()
