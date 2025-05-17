

from flask import Flask, render_template, request, jsonify
from flask_restful import Resource, Api
from flask import Response
from datetime import datetime
import time
import platform
import random
from loremipsum import generate_sentence,generate_sentences,get_sentences,get_paragraphs


app = Flask(__name__)
api = Api(app)

def get_sleeping_time():
    global COUNTER
    # sleep_time = 0.5
    if COUNTER.value >= 50:
        return random.randint(60, 70)/10
    if COUNTER.value >= 40:
        return random.randint(45, 50)/10
    if COUNTER.value >= 30:
        return random.randint(35, 40)/10
    if COUNTER.value >= 20:
        return random.randint(20, 25)/10
    if COUNTER.value >= 10:
        return random.randint(10, 15)/10
    if COUNTER.value >= 0:
        return random.randint(1, 2)/10
    else:
        return 0.1


@app.route('/')
def index():
    return render_template('index.html')

class Hello(Resource):
    def get(self):
        return {"message": "Hello, World!"}


class InputAPI(Resource):
    def post(self):
        if request.is_json:
            json_data = request.get_json(force=True)
            input_value_1 = json_data.get('input_field_1')
            input_value_2 = json_data.get('input_field_2')
            input_language = json_data.get('language')
            return {
                'status': 'success',
                'input': f'{input_value_1} {input_value_2} {input_language}'
            }
        else:
            return {
                'status': 'error',
                'message': 'Content-Type not supported!'
            }, 400



from multiprocessing import Value
from functools import wraps
# import datetime
COUNTER = Value('i', 1)

def track_time_spent(name):
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            COUNTER.value += 1
            # start = datetime.now()
            int_msg = "counter: {}".format(COUNTER.value)
            print(int_msg)
            ret = f(*args, **kwargs)
            COUNTER.value -= 1
            # delta = datetime.now() - start
            # print(name, "took", delta.total_seconds(), "seconds")
            return ret
        return wrapped
    return decorator


class Perf_api_version(Resource):
    @track_time_spent("version")
    def get(self):
        response = {
            "version": "0.1",
            "deployed": datetime.today().strftime('%Y-%m-%d')
        }
        sleeping_time = random.randint(1, 150) / 1000
        time.sleep(sleeping_time)
        return jsonify(response), 200


class Perf_api_log(Resource):
    @track_time_spent("log")
    def get(self):
        size = COUNTER.value
        if size >= 15:
            return Response("Service unavailable", status=500, mimetype='application/json')
        response_msg = ".".join(get_paragraphs(size)).replace("'", "").replace("..", ". ")
        sleeping_time = random.randint(900, 1100) / 1000
        time.sleep(sleeping_time)
        return Response(response_msg, status=200, mimetype='application/json')

class Perf_api_sysinfo(Resource):
    @track_time_spent("sysinfo")
    def get(self):
        sleep_time = get_sleeping_time()
        time.sleep(sleep_time)
        response = {
            "platform": platform.machine(),
            "version": platform.version(),
            "system": platform.system(),
        }
        return jsonify(response), 200

class Perf_api_checkuser(Resource):
    @track_time_spent("check_user")
    def post(self):
        user_name = request.form.get("user")
        if user_name == "nik":
            time.sleep(0.5)
            return jsonify({"auth": "pass", "user": user_name}), 200
        return jsonify({"auth": "FAILED"}), 500






api.add_resource(InputAPI, '/submit', endpoint="submit")
api.add_resource(Hello, "/hello")
api.add_resource(Perf_api_version, "/version")
api.add_resource(Perf_api_log, "/log")
api.add_resource(Perf_api_sysinfo, "/sysinfo")
api.add_resource(Perf_api_checkuser, "/check_user")


if __name__ == '__main__':
    app.run(debug=True,
            host="0.0.0.0",
            port=5000,
            threaded=True)
