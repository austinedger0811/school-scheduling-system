from flask import Flask, jsonify
from flask_cors import CORS
from ClassScheduler import ClassScheduler


app = Flask(__name__)
CORS(app)

scheduler = ClassScheduler()


@app.route('/')
def hello():
    return 'Hello Word.'


@app.route('/api/v1/students', methods=['GET'])
def students():
    return jsonify(scheduler.get_students())


@app.route('/api/v1/courses', methods=['GET'])
def courses():
    return jsonify(scheduler.get_courses())
