#!/usr/bin/python3

import os
from flask import Flask, jsonify, request, Blueprint, url_for, send_from_directory, render_template
from flask_restplus import Api, Resource, fields, abort
from flask_pymongo import PyMongo
from wtforms import Form, StringField, PasswordField, validators

# Local imports
from available_tyks_info import tyk_info, tyk_ids, tyk_ids_format_six, tyk_ids_format_two
from api_model_objects import student_text_format_six_model_object, ai_predictions_format_six_model_object, student_text_format_two_model_object, ai_predictions_format_two_model_object
from forms import TykFormTwo, TykFormSix
from word2vector_model import w2v
from word2vec_api import get_index2word_set, get_word_rank, get_word_vector
from grader import channel_grader


# App init
app = Flask(__name__)

# Mongo DB
app.config['MONGO_DBNAME'] = 'connect_to_mongo'
app.config['MONGO_URI'] = 'mongodb://pretty:printed123@ds012889.mlab.com:12889/connect_to_mongo'
mongo = PyMongo(app)

# Api Blueprint
blueprint = Blueprint('api', __name__, url_prefix='/api')
api = Api(blueprint, doc='/doc/', version='3.0.1',
          description='Artificial Intelligence @ PrecisEd Online - API')
app.register_blueprint(blueprint)


# Set app properties
app.is_ready = False
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
        format_six_request.insert(postedData)
        return jsonify(postedData)


@api.route('/tyk/format_two')
class format_two(Resource):
    @api.expect(tyk_format_two_model, validate=True)
    @api.response(200, 'Success')
    @api.response(400, 'Validation Error')
    def post(self):
        postedData = request.get_json()
        # print(postedData)
        format_two_request = mongo.db.format_two_requests
        format_two_request.insert_one(postedData)
        print(postedData['_id'])
        return 'added!'


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

# Load
@app.route('/load_models')
def load_models():
    msg = ''
    if not app.is_ready:
        get_ready()
    if app.is_ready:
        msg = 'Loading complete...'
    return render_template('dashboard.html', available_tyks=tyk_info, msg=msg)

# Dashboard
@app.route('/dashboard')
def dashboard():
    warning = ''
    if not app.is_ready:
        # flash('AI models NOT loaded yet', 'warning')
        warning = 'AI models NOT loaded yet'
    return render_template('dashboard.html', available_tyks=tyk_info, warning=warning)

# Test Your Knowledge
@app.route('/tyk/<string:tyk_id>', methods=['GET', 'POST'])
def tyk_route(tyk_id):

    chosen_tyk = {}

    for tyk in tyk_info:
        if tyk_id == tyk['id']:
            chosen_tyk = tyk

    form = TykFormSix(request.form)
    if chosen_tyk and chosen_tyk['format'] == '2 - 1 Pros & 1 Cons':
        form = TykFormTwo(request.form)

    if request.method == 'POST' and form.validate():

        if chosen_tyk and chosen_tyk['format'] == '2 - 1 Pros & 1 Cons':
            pro_1 = form.pro_1.data
            con_1 = form.con_1.data

            response_text = [pro_1, con_1]

        else:
            pro_1 = form.pro_1.data
            pro_2 = form.pro_2.data
            pro_3 = form.pro_3.data
            con_1 = form.con_1.data
            con_2 = form.con_2.data
            con_3 = form.con_3.data

            response_text = [pro_1, pro_2, pro_3, con_1, con_2, con_3]

        if not app.is_ready:
            get_ready()

        if app.is_ready:
            # call grading method
            output = channel_grader(
                chosen_tyk['id'], response_text, app.index2word_set, app.WORDS, app)

            return render_template('tyk.html', form=form, chosen_tyk=chosen_tyk, msg=str(output))

        return render_template('tyk.html', form=form, chosen_tyk=chosen_tyk, msg=str(response_text))

    return render_template('tyk.html', form=form, chosen_tyk=chosen_tyk)


# Route to init the Google AI File
@app.route('/init/', methods=['GET'])
def get_ready():
    '''Default route'''

    if True:
        app.w2v_model, app.index2word_set, app.WORDS = w2v(app)

    else:
        app.index2word_set = get_index2word_set()
        app.WORDS = get_word_rank()

    app.is_ready = True

    output = ["READY"]

    return jsonify({'result': output})


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
