from select import select
from Config.DBConnection import *
import matplotlib.pyplot as plt

def fetch_data(select_query):
    conn = get_connection()
    curr = conn.cursor()
    print(select_query)
    curr.execute(select_query)
   
    date_list = []
    count_list = []
    indx = 0

    for record in curr.fetchall():
        x_date = record[1].strftime('%m/%d/%Y')
        y_count = record[0]
        date_list.append(x_date)
        count_list.append(y_count)
        indx = indx + 1

    date_time = {}
    date_time["Date"] = date_list
    date_time["Count"] = count_list
    
    return date_list, count_list

def generate_stationrevenue_report(start_date, end_date, station_name):
    select_query = """select sum(cast(payment_amount as numeric)), drop_time  from customer_vehicle_usage cvu  where drop_time >= '""" +start_date+"""' 
    and drop_time <= '""" +end_date+"""' and pick_up_location = '"""+station_name+"""' group by drop_time;"""
    date_list, count_list = fetch_data(select_query)
 
    plt.plot(date_list, count_list)
    plt.show()


def generate_activestation_report(start_date, end_date, station_name):
    select_query = """select count(*), pick_up_time  from customer_vehicle_usage cvu where pick_up_time >= '""" +start_date+"""' 
    and pick_up_time <= '""" +end_date+"""' and cast(pick_up_location as numeric) in (select station_id from station where station_name = '"""+station_name+"""')
     group by pick_up_time;"""
    date_list, count_list = fetch_data(select_query)
 
    plt.plot(date_list, count_list)
 
    plt.show()


vocr = generate_activestation_report('2022-10-01', '2022-10-04', 'college lands')
print(vocr)

