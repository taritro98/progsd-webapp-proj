from Config.DBConnection import *
import psycopg2
import psycopg2.extras
import json

from datetime import datetime

from Vehicle import Vehicle


def fetch_vehicle_list(station_id):
    conn = get_connection()
    curr = conn.cursor()

    curr.execute(f"""SELECT v.vehicle_number, v.vehicle_type, vu.last_used_on, vu.vehicle_charge_percentage, vehicle_charge_percentage*2 as vehicle_ride_kms 
    FROM vehicle v right join vehicle_usage vu on v.vehicle_id = vu.vehicle_id where vu.is_active='N' and is_currently_defective='N' and vu.vehicle_current_station_id = {station_id};""")

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


def topup_dao(user_id, topup_amount, card_number, expiry_month_yr, cvv):
    conn = get_connection()
    curr = conn.cursor()
    select_query = f"""select wallet_amount from ewallet where user_id = {user_id}"""
    curr.execute(select_query)
    for record in curr.fetchall():
        topup_amount = int(topup_amount) + int(record[0])
    print(topup_amount, expiry_month_yr)
    update_query = f"""update ewallet set wallet_amount  = """+str(topup_amount)+""", card_number = """+str(card_number)+""", 
    last_updateddate = (select now()), expiry_month_yr = """+expiry_month_yr+""", cvv = """+cvv+"""where user_id = """ + str(user_id)
    curr.execute(update_query)

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
    

def rent_ride_dao(user_id, vehicle_id):
   
    conn = get_connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    
    
    sql = "Select vehicle_id, is_active, vehicle_current_station_id from vehicle_usage where vehicle_id = (select vehicle_id from vehicle where vehicle_number = '{}')".format(vehicle_id)
    cursor.execute(sql)
    for record in cursor.fetchall():
        if record[1] == 'Y':
            response = {'rent_status': 'Ride in use'}
        else:
            stat = record[2]
            now=datetime.now()
            vehicle_id = record[0]
            created_datetime=now.strftime("%Y-%m-%d %H:%M:%S")

            sql2 ="""INSERT INTO customer_vehicle_usage(user_id, 
            vehicle_id, payment_Mode, is_returned, pick_up_time, pick_up_location) Values({}, {}, 'Card', 'N','{}', {});""".format(user_id, vehicle_id, created_datetime, stat)
            cursor.execute(sql2)
            conn.commit()
            sql = "UPDATE vehicle_usage SET is_active = 'Y' where vehicle_id = {}".format(vehicle_id)
            cursor.execute(sql)
            conn.commit()
            response = {'rent_status': 'Success'}
    return response
    
#move_vehicle(4, 5, "1007,1006")
#report_vehicle('1007', 'Puncture', 'Vehicle Punctured', '4', 'High')
#fetch_vehicle_list('7')

#rent_ride_dao(1, 'RX450j')

#user_id, topup_amount, card_number, expiry_month_yr, cvv
topup_dao(1, "1000", "234212352", "10/2025", "234")
