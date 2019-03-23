import os
from flask import Flask, jsonify, request, Blueprint, url_for, send_from_directory, render_template
from flask_restplus import Api, Resource, fields, abort
from flask_pymongo import PyMongo
from bson.json_util import dumps

# Local imports
from available_tyks_info import tyk_info, tyk_ids, tyk_ids_format_six, tyk_ids_format_two
from api_model_objects import student_text_format_six_model_object, ai_predictions_format_six_model_object, student_text_format_two_model_object, ai_predictions_format_two_model_object


# App init
app = Flask(__name__)
blueprint = Blueprint('api', __name__, url_prefix='/api')
api = Api(blueprint, doc='/doc/', version='3.0.1',
          description='Artificial Intelligence @ PrecisEd Online - API')
app.register_blueprint(blueprint)

# Mongo DB
app.config['MONGO_DBNAME'] = 'connect_to_mongo'
app.config['MONGO_URI'] = 'mongodb://pretty:printed123@ds012889.mlab.com:12889/connect_to_mongo'
mongo = PyMongo(app)


# Set app properties
app.tyk_info = tyk_info
app.tyk_ids = tyk_ids
app.tyk_ids_format_six = tyk_ids_format_six
app.tyk_ids_format_two = tyk_ids_format_two


''' Format Six'''


student_text_format_six_model = api.model(
    'student_text_format_six_model', student_text_format_six_model_object)

ai_predictions_format_six_model = api.model(
    'ai_predictions_format_six_model', ai_predictions_format_six_model_object)

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
    'ai_predictions_format_two_model', ai_predictions_format_two_model_object)

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
        format_six_request = mongo.db.format_six_requests
        result = format_six_request.insert(postedData)
        return dumps(postedData)


@api.route('/tyk/format_two')
class format_two(Resource):
    @api.expect(tyk_format_two_model, validate=True)
    @api.response(200, 'Success')
    @api.response(400, 'Validation Error')
    def post(self):
        postedData = request.get_json()
        # print(postedData)
        format_two_request = mongo.db.format_two_requests
        result = format_two_request.insert(postedData)
        print(postedData['_id'])
        return dumps(postedData['_id'])


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/about')
def about():
    return render_template('home.html')


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
