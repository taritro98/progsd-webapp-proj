from flask import Flask, jsonify, request
from CustomerProfile import *
from OperatorReport import fetch_operator, fetch_operator_perf_data
from VehicleReport import *
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def hello_world():
    return 'Hello World'

@app.route('/login/', methods = ['POST'])
def customer_login():
    content = request.json
    print(content['email_adress'])
    validate_userlogin(content['email_adress'], content['pwd'])
    return 'True'

@app.route('/vtr/', methods = ['POST'])
def vehicle_type_report():
    print("Here inside vehicle_type_report..")
    print(request, " ==> This is the request json..")
    content = request.json
    from_date = content['from_date'].split(":")[1]
    to_date = content['to_date'].split(":")[1]
    vehicle_type = content['vehicle_type']
    generate_vehiclerevenue_report(from_date, to_date, vehicle_type)
    response = {'vtr_report_generation_status': 'Success'}
    return jsonify(response), 200
    

@app.route('/vocr/', methods = ['POST'])
def vehicle_operational_cost_report():
    print("Here inside vehicle_operational_cost_report..")
    print(request, " ==> This is the request json..")
    content = request.json
    from_date = content['from_date'].split(":")[1]
    to_date = content['to_date'].split(":")[1]
    vehicle_type = content['vehicle_type']
    generate_vehicleoperationalcost_report(from_date, to_date, vehicle_type)
    response = {'vocr_report_generation_status': 'Success'}
    return jsonify(response), 200


@app.route('/fol/', methods = ['GET'])
def fetch_operator_list():
    print("Here inside fetch_operator_list..")
    print(request, " ==> This is the request json..")
    response = fetch_operator()
    print(response, " ==> Here..")
    return response

@app.route('/fpd/', methods = ['POST'])
def fetch_perf_data():
    print("Here inside fetch_perf_data..")
    print(request, " ==> This is the request json..")
    content = request.json
    from_date = content['from_date'].split(":")[1]
    to_date = content['to_date'].split(":")[1]
    operator_email = content['operator_email']
    fetch_operator_perf_data(from_date, to_date, operator_email)
    response = {'fpd_report_generation_status': 'Success'}
    return jsonify(response), 200



if __name__ == '__main__':
    app.run()