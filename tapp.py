from flask import Flask, request, jsonify
import psycopg2
import psycopg2.extras
from credfile import HOST, DATABASE, USER, PASSWORD, PORT_ID
import json
from datetime import datetime
from Config.DBConnection import *
from flask_cors import CORS
from CustomerDAO import *
from OperatorReport import fetch_operator, fetch_operator_perf_data
from VehicleReport import *

app = Flask(__name__)
CORS(app)

@app.route('/sign-up', methods=['POST'])
def sign_up():
    '''
    Input - station_id : int
    Email_id, first_name, last_name, pwd (encrypted), role, address, phone_number, id_proof, id_proof_type, wallet_amount, card_number, expiry_month_yr, cvv
    Output - User is created and ewallet initiated with amount
    '''
    if request.method == 'POST':
        
        ## Signup Json
        signup_content = request.json
        ####### User Details ##########
        first_name = signup_content.get("first_name")
        last_name = signup_content.get("last_name")
        pwd = signup_content.get("pwd")
        role = signup_content.get("role")
        address = signup_content.get("address")
        phone_number = signup_content.get("phone_number")
        id_proof = signup_content.get("id_proof")
        id_proof_type = signup_content.get("id_proof_type")
        is_active = "Y"
        email_address = signup_content.get("email_address")
        ####### EWallet ##########
        wallet_amount = signup_content.get("wallet_amount")
        card_number = signup_content.get("card_number")
        expiry_month_yr = signup_content.get("expiry_month_yr")
        cvv = signup_content.get("cvv")

        conn = get_connection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        ## User Profile Insert Query
        cur.execute(f"INSERT INTO user_profile (first_name, last_name, pwd, role, address, phone_number, id_proof, id_proof_type, is_active, email_address, created_datetime, last_usage_datetime) values ('{first_name}','{last_name}','{pwd}','{role}','{address}','{phone_number}','{id_proof}','{id_proof_type}','{is_active}','{email_address}',(SELECT now()),(SELECT now()));")
        conn.commit()

        ## Fetch user_id from unique email address
        cur.execute(f"SELECT user_id from user_profile where email_address='{email_address}';")
        user_id = cur.fetchone()[0]
        
        ## E-Wallet Insert Query
        cur.execute(f"INSERT INTO ewallet (user_id, wallet_amount, card_number, expiry_month_yr, cvv, created_date, last_updateddate) values ({user_id},{wallet_amount},{card_number},'{expiry_month_yr}',{cvv},(SELECT now()),(SELECT now()));")
        conn.commit()
        cur.close()
        conn.close()

        return f"User {first_name}{last_name} with email {email_address} and user_id {user_id} created"

@app.route('/vehicle-list', methods=['GET'])
def vehicle_list():
    '''
    Input - station_id : int
    Provides a list of all the vehicles along with their information for the specified station
    Output - vehicle_id, model_type, last_issued, battery_level, estimated_range 
    '''
    if request.method == 'GET':
        
        station_id = request.json["station_id"]
        print("station id", station_id)

        conn = get_connection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        cur.execute('SELECT * FROM vehicle;')

        for record in cur.fetchall():
            print(record['vehicle_type'])

        cur.execute(f"SELECT v.vehicle_id, v.vehicle_type, v.vehicle_number, vu.last_modified_on, vu.vehicle_charge_percentage FROM vehicle v right join vehicle_usage vu on v.vehicle_id = vu.vehicle_id where vu.vehicle_current_station_id = {station_id};")

        ## Vehicle List Json
        veh_lst_json = json.dumps([dict(idx) for idx in cur.fetchall()])
        print(veh_lst_json)

        cur.close()
        conn.close()

    return veh_lst_json

@app.route('/report-vehicle', methods=['POST'])
def report_vehicle():
    '''
    Input - issue_type, user_id, vehicle_id, issue_description, vehicle_image, timestamp

    Inserts a record into the vehicle_issue table with the reported vehicle
    '''
    if request.method == 'POST':
        
        rv_json = request.json
        issue_type = rv_json["issue_type"]
        user_id = rv_json["user_id"]
        vehicle_id = rv_json["vehicle_id"]
        issue_description = rv_json["issue_description"]
        issue_reported_on = rv_json["issue_reported_on"]

        conn = get_connection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        cur.execute(f"INSERT INTO vehicle_issue (vehicle_id, issue_active, issue_type, issue_description, issue_reported_on) values ({vehicle_id},'Y','{issue_type}','{issue_description}','{issue_reported_on}');")

        conn.commit()
        cur.close()
        conn.close()

    return "Row inserted in vehicle_issue table"


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
    content = request.json
    from_date = content['from_date'].split(":")[1]
    to_date = content['to_date'].split(":")[1]
    vehicle_type = content['vehicle_type']
    generate_vehicleoperationalcost_report(from_date, to_date, vehicle_type)
    response = {'vocr_report_generation_status': 'Success'}
    return jsonify(response), 200


@app.route('/fol/', methods = ['GET'])
def fetch_operator_list():
    response = fetch_operator()
    print(response, " ==> Here..")
    return response

@app.route('/fpd/', methods = ['POST'])
def fetch_perf_data():
    content = request.json
    from_date = content['from_date'].split(":")[1]
    to_date = content['to_date'].split(":")[1]
    operator_email = content['operator_email']
    fetch_operator_perf_data(from_date, to_date, operator_email)
    response = {'fpd_report_generation_status': 'Success'}
    return jsonify(response), 200


# @app.route('/vehicle-list', methods=['POST'])
# def vehicle_list():
    
#     content = request.json
#     station_id = content['station_id']
        
#     response = fetch_vehicle_list(station_id)
    
#     return response

@app.route('/mv', methods=['POST'])
def move_vehicle():
    
    content = request.json
    print(content)
    #from_station, to_station, vehicles
        
    move_vehicle_dao(content['from_station'], content['to_station'], content['vehicles'])
    response = {'move_vehicle': 'Success'}
    
    return response

if __name__=='__main__':
    # Development Mode
    app.run(debug=True)