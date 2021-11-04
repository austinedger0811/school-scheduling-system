from flask import Flask, jsonify
from flask_cors import CORS
from ClassScheduler import ClassScheduler


app = Flask(__name__)
CORS(app)

scheduler = ClassScheduler()


@app.route('/')
def hello():
    return 'Hello Word.'


@app.route('/students')
def print_students():
    res = scheduler.get_students()
    return jsonify(res)
