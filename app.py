

from flask import Flask, render_template, request, jsonify,json
from flask_restful import Resource, Api,reqparse
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
        content_type = request.form.get('Content-Type')
        request_result=request.form
        if (content_type == 'application/json'):
            input_value_1 = request_result.get('input_field_1')
            input_value_2 = request_result.get('input_field_2')
            input_language = request_result.get('language')
            # Do something with input_value
            # return jsonify({'status': 'success', 'input': '{}'.format(json_data)})
            # json_data = request.get_json(force=True)
            # print(json_data)
            return {'status': 'success', 'input': '{} {} {}'.format(input_value_1, input_value_2,input_language)}
        else:
            return 'Content-Type not supported!'



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
        response_msg = '{"version": "0.1", "deployed": '+datetime.today().strftime('%Y-%m-%d')+'}'
        sleeping_time = random.randint(1, 150)/1000
        time.sleep(sleeping_time)
        return Response(response_msg, status=200, mimetype='application/json')


class Perf_api_log(Resource):
    @track_time_spent("log")
    def get(self):
        size = COUNTER.value
        if size >= 15:
            return Response("Service unavailable", status=500, mimetype='application/json')
        response_msg = ".".join(get_paragraphs(size)).replace("'","").replace("..",". ")
        slleping_time = random.randint(900,1100) / 1000
        time.sleep(slleping_time)
        return Response(response_msg, status=200, mimetype='application/json')

class Perf_api_sysinfo(Resource):
    @track_time_spent("sysinfo")
    def get(self):
        sleep_time = get_sleeping_time()
        time.sleep(sleep_time)
        response_msg = '{"platform":' + platform.machine() + ', "version": ' + platform.version() + ', "system": ' + platform.system() + '}'
        return Response(response_msg, status=200, mimetype='application/json')

class Perf_api_checkuser(Resource):
    @track_time_spent("check_user")
    def post(self):
        # content_type = request.form.get('Content-Type')
        # request_result = request.form
        # # print(request_result)
        user_name = request.form["user"]
        # print(user_name)
        if user_name == "nik":
            response_msg = '{"auth": "pass", "user": ' + user_name + ' }'
            time.sleep(0.5)
            return Response(response_msg, status=200, mimetype='application/json')
        else:
            response_msg = '{"auth": "FAILED"}'
            return Response(response_msg, status=500, mimetype='application/json')






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
