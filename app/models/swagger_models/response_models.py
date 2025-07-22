from flask_restx import fields


def get_response_models(namespace):
    notam_model = namespace.model("notam", {
        "notam_id": fields.String,
        "issued_for": fields.List(fields.String, description=""),
        "main_content": fields.String,
        "until_date": fields.String,
        "created_date": fields.String,
    })

    get_notam_model=namespace.model("get_notam",{
        "status": fields.String(description="وضعیت درخواست"),
        "message": fields.String(description="پیام پاسخ"),
        "total_notams":fields.Integer(description="تعداد نوتام"),
        "notams":fields.List(fields.Nested(notam_model),description="")
    })

    namespace.models["get_notam"] = get_notam_model

    return {
        "get_notam": get_notam_model,
    }