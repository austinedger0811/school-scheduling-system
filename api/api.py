from flask import Flask, jsonify, request
from flask.wrappers import Request
from flask_cors import CORS
from ClassScheduler import ClassScheduler


app = Flask(__name__)
CORS(app)

scheduler = ClassScheduler()


@app.route('/api/v1/semesters', methods=['GET'])
def get_semesters():
    return jsonify(scheduler.get_semesters())


@app.route('/api/v1/students', methods=['GET'])
def get_students():
    return jsonify(scheduler.get_students())


@app.route('/api/v1/schedule/', methods=['GET', 'POST'])
def get_schedule():
    data = request.json
    sid = int(data['sid'])
    semester = data['semester']
    year = int(data['year'])
    return jsonify(scheduler.get_student_schedule(sid, semester, year))


@app.route('/api/v1/clear_schedule', methods=['POST'])
def clear_schedule():
    data = request.json
    semester = data['semester']
    year = data['year']
    scheduler.clear_schedule(semester, year)


@app.route('/api/v1/test', methods=['GET'])
def test():
    return jsonify(scheduler.get_takes())
