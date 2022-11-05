from Config.DBConnection import *
import psycopg2
import psycopg2.extras
import json
from datetime import date

from Vehicle import Vehicle


def fetch_vehicle_list(station_id):
    conn = get_connection()
    curr = conn.cursor()

    curr.execute(f"""SELECT v.vehicle_number, v.vehicle_type, vu.last_used_on, vu.vehicle_charge_percentage, vehicle_charge_percentage*2 as vehicle_ride_kms 
    FROM vehicle v right join vehicle_usage vu on v.vehicle_id = vu.vehicle_id where vu.is_active='Y' and vu.vehicle_current_station_id = {station_id};""")

    vehicle_list = []
    #vehicle_number, vehicle_type, last_used_on, percentage_of_charge
    for record in curr.fetchall():
        vehicle = Vehicle(record[0], record[1], record[2].strftime('%m/%d/%Y'), str(record[3]), record[4])
        vehicle_list.append(vehicle)
        print(record)
   
    curr.close()
    conn.close()
    res = [vl.to_json() for vl in vehicle_list]
    print(res)
    return res


def report_vehicle_dao(vehicle_number, issue_type, issue_description, from_station, priority):
    conn = get_connection()
    curr = conn.cursor()
    curr.execute(f"""INSERT INTO vehicle_issue (vehicle_id, issue_active, issue_type, issue_description, issue_reported_on, current_station, priority) values 
    ((select vehicle_id from vehicle where vehicle_number = '{vehicle_number}'),'Y','{issue_type}','{issue_description}',(SELECT CURRENT_DATE), 
    '{from_station}', '{priority}');""")

    conn.commit()
    curr.close()
    conn.close()

def move_vehicle_dao(from_station, to_station, vehicles):
    conn = get_connection()
    curr = conn.cursor()
    vehicle_list = vehicles.split(",")
   
    for vl in vehicle_list:
        curr.execute(f"""INSERT INTO vehicle_issue (vehicle_id, issue_active, issue_type, issue_description, issue_reported_on, current_station, move_to_station, priority) values 
        ((select vehicle_id from vehicle where vehicle_number = '{vl}'),'Y','Vehicle Movement','Move Vehicle between stations',(SELECT CURRENT_DATE),{from_station},
        '{to_station}', 'Normal');""")


    conn.commit()
    curr.close()
    conn.close()
    return True
    

def rent_ride(user_id, vehicle_id):
    return True
    
#move_vehicle(4, 5, "1007,1006")
#report_vehicle('1007', 'Puncture', 'Vehicle Punctured', '4', 'High')
fetch_vehicle_list('7')