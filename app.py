from flask import Flask, jsonify, request, Blueprint, url_for
from flask_restplus import Api, Resource, fields, abort

from available_tyks_info import *
from api_model_objects import *

app = Flask(__name__)
blueprint = Blueprint('api', __name__, url_prefix='/api')
api = Api(blueprint, doc='/doc/', version='3.0.1',
          description='Artificial Intelligence @ PrecisEd Online - API')


app.register_blueprint(blueprint)

api = api.namespace(
    'api', description='')


# set app properties
app.available_tyks = available_tyks_info
app.tyk_ids = [tyk['id'] for tyk in app.available_tyks]

app.tyk_ids_format_six = tyk_ids_format_six = [
    tyk['id'] for tyk in app.available_tyks if tyk['format'] == '6 - 3 Pros & 3 Cons']

app.tyk_ids_format_two = tyk_ids_format_two = [
    tyk['id'] for tyk in app.available_tyks if tyk['format'] == '2 - 1 Pros & 1 Cons']


''' Format Six'''


student_text_format_six_model = api.model(
    'student_text_format_six_model', student_text_format_six_model_object)

ai_predictions_format_six_model = api.model(
    'ai_predictions_format_six_model', ai_predictions_format_six_model)

tyk_format_six_model = api.model('tyk_format_six_model', {
    'tyk_id': fields.String(required=True, enum=app.tyk_ids_format_six),
    'student_id': fields.String(required=False),
    'user_id': fields.String(required=False),
    "student_text_format_six": fields.Nested(student_text_format_six_model, required=True),
    "ai_predictions_format_six": fields.Nested(ai_predictions_format_six_model, required=False),
    "ai_score": fields.Integer(required=False),
    "max_score": fields.Integer(required=False)
})


'''Format Two'''


student_text_format_two_model = api.model(
    'student_text_format_two_model', student_text_format_two_model_object)

ai_predictions_format_two_model = api.model(
    'ai_predictions_format_two_model', ai_predictions_format_two_model)

tyk_format_two_model = api.model('tyk_format_two_model', {
    'tyk_id': fields.String(required=True, enum=app.tyk_ids_format_two),
    'student_id': fields.String(required=False),
    'user_id': fields.String(required=False),
    "student_text_format_two": fields.Nested(student_text_format_two_model, required=True),
    "ai_predictions_format_two": fields.Nested(ai_predictions_format_two_model, required=False),
    "ai_score": fields.Integer(required=False),
    "max_score": fields.Integer(required=False)
})


@api.route('/tyk/format_six')
class format_six(Resource):
    @api.expect(tyk_format_six_model, validate=True)
    @api.response(200, 'Success')
    @api.response(400, 'Validation Error')
    def post(self):
        postedData = request.get_json()
        return jsonify(postedData)


@api.route('/tyk/format_two')
class format_two(Resource):
    @api.expect(tyk_format_two_model, validate=True)
    @api.response(200, 'Success')
    @api.response(400, 'Validation Error')
    def post(self):
        postedData = request.get_json()
        return jsonify(postedData)


if __name__ == "__main__":
    app.run(port=5000, debug=True)
