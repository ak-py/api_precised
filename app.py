from flask import Flask, jsonify, request, Blueprint, url_for
from flask_restplus import Api, Resource, fields, abort


app = Flask(__name__)
blueprint = Blueprint('api', __name__, url_prefix='/api')
api = Api(blueprint, doc='/doc/', version='3.0.1',
          description='Artificial Intelligence @ PrecisEd Online - API')


app.register_blueprint(blueprint)

api = api.namespace(
    'api', description='')


app.available_tyks = [
    {'id': '101', 'title': 'Pricing - High', 'avg_accuracy': '91%',
        'format': '6 - 3 Pros & 3 Cons', 'status': 'OK'},
    {'id': '102', 'title': 'Pricing - Low', 'avg_accuracy': '91%',
        'format': '6 - 3 Pros & 3 Cons', 'status': 'OK'},
    {'id': '103', 'title': 'Accounting - Cash', 'avg_accuracy': '94%',
        'format': '2 - 1 Pros & 1 Cons', 'status': 'OK'},
    {'id': '104', 'title': 'Accounting - Accrual', 'avg_accuracy': '94%',
        'format': '2 - 1 Pros & 1 Cons', 'status': 'OK'},
    {'id': '105', 'title': 'Location - Mid-Town', 'avg_accuracy': '92%',
        'format': '6 - 3 Pros & 3 Cons', 'status': 'OK'},
    {'id': '106', 'title': 'Location - North-End', 'avg_accuracy': '95%',
        'format': '6 - 3 Pros & 3 Cons', 'status': 'OK'},
    {'id': '107', 'title': 'Location - Strip Mall', 'avg_accuracy': '89%',
        'format': '6 - 3 Pros & 3 Cons', 'status': 'OK'},
    {'id': '108', 'title': 'Over-Ripe Tomatoes - BUYING', 'avg_accuracy': '90%',
        'format': '2 - 1 Pros & 1 Cons', 'status': 'OK'},
    {'id': '109', 'title': 'Over-Ripe Tomatoes - NOT BUYING',
        'avg_accuracy': '90%', 'format': '2 - 1 Pros & 1 Cons', 'status': 'OK'},
    {'id': '110', 'title': 'Uniform - PROVIDE', 'avg_accuracy': '84%',
        'format': '2 - 1 Pros & 1 Cons', 'status': 'OK'},
    {'id': '111', 'title': 'Uniform - NOT PROVIDE', 'avg_accuracy': '82%',
        'format': '2 - 1 Pros & 1 Cons', 'status': 'OK'},
]

app.tyk_ids = [tyk['id'] for tyk in app.available_tyks]


student_text_format_six_model = api.model('student_text_format_six_model', {
    "pro_1": fields.String(required=True),
    "pro_2": fields.String(required=True),
    "pro_3": fields.String(required=True),
    "con_1": fields.String(required=True),
    "con_2": fields.String(required=True),
    "con_3": fields.String(required=True),
})

ai_predictions_format_six_model = api.model('ai_predictions_format_six_model', {
    "pro_1": fields.Boolean(required=False),
    "pro_2": fields.Boolean(required=False),
    "pro_3": fields.Boolean(required=False),
    "con_1": fields.Boolean(required=False),
    "con_2": fields.Boolean(required=False),
    "con_3": fields.Boolean(required=False)
})


tyk_format_six_model = api.model('tyk_format_six_model', {
    'tyk_id': fields.String(required=True, enum=app.tyk_ids),
    'student_id': fields.String(required=False),
    'user_id': fields.String(required=False),
    "student_text_format_six": fields.Nested(student_text_format_six_model, required=True),
    "ai_predictions_format_six": fields.Nested(ai_predictions_format_six_model),
    "ai_score": fields.Integer(required=False),
    "max_score": fields.Integer(required=False)
})


@api.route('/')
class grade(Resource):
    @api.expect(tyk_format_six_model, validate=True)
    @api.response(200, 'Success')
    @api.response(400, 'Validation Error')
    def post(self):
        postedData = request.get_json()
        return jsonify(postedData)


if __name__ == "__main__":
    app.run(port=5000, debug=True)
