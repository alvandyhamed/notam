from flask_restx import fields

def get_request_models(namespace):
    get_notams_request=namespace.model("getNotamsRequest",{
        "retrieveLocIds":fields.List(fields.String,default=[],description="List of ICAO codes"),
        "flight_number":fields.String(description="Flight number"),
        "user_id":fields.String(description="User ID"),
        "date":fields.String(description="Date"),
        "rout":fields.String(description="Rout"),

    })
    namespace.models["getNotamsRequest"] = get_notams_request
    return {
        "get_notams_request":get_notams_request
    }