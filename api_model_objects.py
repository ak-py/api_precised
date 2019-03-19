from flask_restplus import fields

student_text_format_six_model_object = {
    "pro_1": fields.String(required=True),
    "pro_2": fields.String(required=True),
    "pro_3": fields.String(required=True),
    "con_1": fields.String(required=True),
    "con_2": fields.String(required=True),
    "con_3": fields.String(required=True),
}

ai_predictions_format_six_model = {
    "pro_1": fields.Boolean(required=False),
    "pro_2": fields.Boolean(required=False),
    "pro_3": fields.Boolean(required=False),
    "con_1": fields.Boolean(required=False),
    "con_2": fields.Boolean(required=False),
    "con_3": fields.Boolean(required=False)
}

student_text_format_two_model_object = {
    "pro_1": fields.String(required=True),
    "con_1": fields.String(required=True)
}

ai_predictions_format_two_model = {
    "pro_1": fields.Boolean(required=False),
    "con_1": fields.Boolean(required=False)
}
