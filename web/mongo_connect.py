from flask import Flask
from flask_pymongo import PyMongo

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'connect_to_mongo'
app.config['MONGO_URI'] = 'mongodb://pretty:printed123@ds012889.mlab.com:12889/connect_to_mongo'

mongo = PyMongo(app)


@app.route('/add')
def add():
    user = mongo.db.users
    user.insert({'name': 'Akshit(AK) Gupta'})
    return 'Added User!'


if __name__ == "__main__":
    app.run(port=5000, debug=True)
