import datetime
from select import select
from Config.DBConnection import *
import matplotlib.pyplot as plt
import pandas as pd

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
    conn.close()
    
    return date_time

def generate_vehiclerevenue_report(start_date, end_date, vehicle_type):
    select_query = """select sum(cast(payment_amount as numeric)), pick_up_time  from customer_vehicle_usage cvu  where pick_up_time >= '""" +start_date+"""' 
    and pick_up_time <= '""" +end_date+"""' and vehicle_id in (select vehicle_id from vehicle where vehicle_type = '"""+vehicle_type+"""') group by pick_up_time;"""
    date_time = fetch_data(select_query)
    df = pd.DataFrame.from_dict(date_time)

    plt.bar(x=df["Date"], height=df["Count"])
    file_name = datetime.datetime.now()
    #plt.savefig("Vehicel_Revenue_"+str(file_name.timestamp()).split(".")[0]+".png")
    plt.show()
    


def generate_vehicleoperationalcost_report(start_date, end_date, vehicle_type):
    select_query = """select count(*), issue_reported_on  from vehicle_issue vi where issue_reported_on >= '""" +start_date+"""' 
    and issue_reported_on <= '""" +end_date+"""' and vehicle_id in (select vehicle_id from vehicle where vehicle_type = '"""+vehicle_type+"""') group by issue_reported_on;"""
    date_time = fetch_data(select_query)
    df = pd.DataFrame.from_dict(date_time)

    plt.bar(x=df["Date"], height=df["Count"])
    file_name = datetime.datetime.now()
    #plt.savefig("Vehicel_OperationalCost_"+str(file_name.timestamp()).split(".")[0]+".png")
    plt.show()



#vtr = generate_vehiclerevenue_report('2022-10-01', '2022-10-03', 'PB')
#print(vtr)

#vocr = generate_vehicleoperationalcost_report('2022-10-01', '2022-10-04', 'GB')
#print(vocr)

