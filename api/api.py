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
def get_students():
    return jsonify(scheduler.get_students())


@app.route('/api/v1/schedule/<sid>', methods=['GET'])
def get_schedule(sid):
    return jsonify(scheduler.get_schedule(sid))


@app.route('/api/v1/test', methods=['GET'])
def test():
    return jsonify(scheduler.schedule_students())
