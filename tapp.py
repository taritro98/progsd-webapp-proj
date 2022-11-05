from flask import Flask, request, jsonify
import psycopg2
import psycopg2.extras
from credfile import HOST, DATABASE, USER, PASSWORD, PORT_ID
import json
from datetime import datetime
from Config.DBConnection import *
from flask_cors import CORS
from CustomerDAO import *
from CommonDAO import *
from OperatorReport import fetch_operator, fetch_operator_perf_data
from VehicleReport import *
from OperatorManagement import *
from StationReport import *

app = Flask(__name__)
CORS(app)


@app.route('/login', methods=['GET', 'POST'])
def login():

    content = request.json

    response = login_dao(content['email_address'], content['pwd'])
    print(response)
    return jsonify(response)


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
        role = 'C'
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
        cur.execute(f"""INSERT INTO user_profile (first_name, last_name, pwd, role, address, phone_number, id_proof, id_proof_type, is_active, email_address, 
        created_datetime, last_usage_datetime) 
        values ('{first_name}','{last_name}','{pwd}','{role}','{address}','{phone_number}','{id_proof}','{id_proof_type}','{is_active}','{email_address}',
        (SELECT now()),(SELECT now()));""")
        conn.commit()

        ## Fetch user_id from unique email address
        cur.execute(f"SELECT user_id from user_profile where email_address='{email_address}';")
        user_id = cur.fetchone()[0]
        
        ## E-Wallet Insert Query
        cur.execute(f"""INSERT INTO ewallet (user_id, wallet_amount, card_number, expiry_month_yr, cvv, created_date, last_updateddate) 
        values ({user_id},{wallet_amount},{card_number},'{expiry_month_yr}',{cvv},(SELECT now()),(SELECT now()));""")
        conn.commit()
        cur.close()
        conn.close()
        response = {"Message": "User {first_name}{last_name} with email {email_address} and user_id {user_id} created"}
        return jsonify(response), 200

@app.route('/vehicle-list', methods=['POST'])
def vehicle_list():
    
    content = request.json
    station_id = content['station_id']
        
    response = fetch_vehicle_list(station_id)
    
    return response

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
        #issue_reported_on = rv_json["issue_reported_on"]

        conn = get_connection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        cur.execute(f"""INSERT INTO vehicle_issue (vehicle_id, issue_active, issue_type, issue_description, identified_by,issue_reported_on) 
        values ({vehicle_id},'Y','{issue_type}','{issue_description}','{user_id}',(SELECT now()));""")

        conn.commit()
        cur.close()
        conn.close()
    response = {'report_vehicle': 'Success'}
    return jsonify(response), 200


@app.route('/vtr/', methods = ['POST'])
def vehicle_type_report():
    
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

@app.route('/asr', methods = ['POST'])
def active_station_report():
    content = request.json
    from_date = content['from_date'].split(":")[1]
    to_date = content['to_date'].split(":")[1]
    station_name = content['station_name']
    generate_activestation_report(from_date, to_date, station_name)
    response = {'asr_report_generation_status': 'Success'}
    return jsonify(response), 200

@app.route('/srr', methods = ['POST'])
def station_revenue_report():
    content = request.json
    from_date = content['from_date'].split(":")[1]
    to_date = content['to_date'].split(":")[1]
    station_name = content['station_name']
    generate_stationrevenue_report(from_date, to_date, station_name)
    response = {'srr_report_generation_status': 'Success'}
    return jsonify(response), 200


@app.route('/fol/', methods = ['GET'])
def fetch_operator_list():
    response = fetch_operator()
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

@app.route('/mv', methods=['POST'])
def move_vehicle():
    
    content = request.json
    print(content)
    #from_station, to_station, vehicles
        
    move_vehicle_dao(content['from_station'], content['to_station'], content['vehicles'])
    response = {'move_vehicle': 'Success'}
    
    return response

@app.route('/mo', methods=['POST'])
def manage_operator():
    #address, phone_number, is_active, email_address, last_name, first_name
    content = request.json
    print(content)
    update_operator(content['address'], content['phone_number'], content['is_active'], content['email_address'], content['last_name'],content['first_name'])
    response = {'manage_operator': 'Success'}
    
    return jsonify(response), 200


@app.route('/io', methods=['POST'])
def insert_operator():
    
    content = request.json
    print(content)
    #first_name, last_name, pwd, role, address, phone_number, id_proof, id_proof_type, email_address
        
    insert_operator_dao(content['first_name'], content['last_name'], content['pwd'], content['role'], content['address'], content['phone_number'], content['id_proof'], content['id_proof_type'], content['email_address'])
    response = {'insert_operator': 'Success'}
    
    return jsonify(response), 200

@app.route('/active-tasks-list', methods=['GET'])
def active_tasks_list():
    '''
    Fetch tasks and their corresponding information which are active
    Returns : issue_id, vehicle_id, vehicle_modal issue_type, issue_reported_on, priority, issue_description
    '''
        
    active_tasks_dict = active_tasks_dao()
    
    response = {'active_tasks_dict': active_tasks_dict}
    
    return active_tasks_dict


@app.route('/rent-ride', methods=['GET', 'POST'])
def rent_ride():
    rent_ride_content = request.json
    print(rent_ride_content.get("user_id"))
    print(rent_ride_content.get("vehicle_id"))
    response = rent_ride_dao(rent_ride_content.get("user_id"), rent_ride_content.get("vehicle_id") )
    return jsonify(response), 200

@app.route('/load_data', methods=['POST'])
def load_data():
    
    content = request.json
    print(content)
    response = load_data_dao(content['user_id'])
    
    return jsonify(response), 200

if __name__=='__main__':
    # Development Mode
    app.run()