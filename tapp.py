from flask import Flask, request
import psycopg2
import psycopg2.extras
from credfile import HOST, DATABASE, USER, PASSWORD, PORT_ID
import json
from datetime import datetime

app = Flask(__name__)

host=HOST
database=DATABASE
user=USER
password=PASSWORD
port_id=PORT_ID

try:
    print("Connecting")
    conn = psycopg2.connect(
            host=HOST,
            database=DATABASE,
            user=USER,
            password=PASSWORD,
            port=PORT_ID)
        
    print("Connection Established!")
except Exception as e:
    print(e)

@app.route('/vehicle-list', methods=['GET'])
def vehicle_list():
    '''
    Input - station_id : int
    Provides a list of all the vehicles along with their information for the specified station
    Output - vehicle_id, model_type, last_issued, battery_level, estimated_range 
    '''
    if request.method == 'GET':
        
        ## Uncomment this during integration
        #station_id = request. args. get("student_id")
        station_id = 7

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

@app.route('/report-vehicle', methods=['GET'])
def report_vehicle():
    '''
    Input - issue_type, user_id, vehicle_id, issue_description, vehicle_image, timestamp

    Inserts a record into the vehicle_issue table with the reported vehicle
    '''
    if request.method == 'GET':
        
        ## Uncomment this during integration
        #issue_type, user_id, vehicle_id, issue_description, timestamp = request.args

        issue_type = 'Battery Discharged'
        user_id = 4
        vehicle_id = 2
        issue_description = 'The battery is discharged'
        issue_reported_on = datetime(2022, 5, 5) 

        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        cur.execute(f"INSERT INTO vehicle_issue (vehicle_id, issue_active, issue_type, issue_description, issue_reported_on) values ({vehicle_id},'Y','{issue_type}','{issue_description}','{issue_reported_on}');")

        conn.commit()
        cur.close()
        conn.close()

    return "Row inserted in vehicle_issue table"

if __name__=='__main__':
    # Development Mode
    app.run(debug=True)