from Config.DBConnection import *
from datetime import datetime
from createdict import Create_dict

def active_tasks_dao():
    set_updates = ''
        
    select_query = """SELECT vi.issue_id, vi.vehicle_id, v.vehicle_type, vi.issue_type, vi.issue_reported_on, vi.priority, vi.issue_description from vehicle_issue vi left join vehicle v on vi.vehicle_id = v.vehicle_id where vi.issue_active = 'Y';"""
    conn = get_connection()
    curr = conn.cursor()
    curr.execute(select_query)

    # Call custom dict class constructor
    active_tasks_dict = Create_dict()

    for record in curr.fetchall():
        active_tasks_dict.add(record[0],({"issue_id":record[0],"vehicle_id":record[1],"vehicle_type":record[2],"issue_type":record[3],"issue_reported_on":record[4],"priority":record[5],"issue_description":record[6]}))

    print(active_tasks_dict)
    conn.commit()
    conn.close()

    return active_tasks_dict

def update_operator(address, phone_number, is_active, email_address, last_name, first_name):
    set_updates = ''
    
    if address != "" and address is not None:
        set_updates += """address = '"""+address+"""',"""
    if phone_number != "" and phone_number is not None:
        set_updates += """phone_number = '"""+phone_number+"""',"""
    if last_name != "" and last_name is not None:
        set_updates += """last_name = '"""+last_name+"""',"""
    if is_active != "" and is_active is not None:
        set_updates += """is_active = '"""+is_active+"""',"""
    if first_name != "" and first_name is not None:
        set_updates += """first_name = '"""+first_name+"""',"""

    set_updates += """last_usage_datetime = (select now())"""
    
    update_query = """update user_profile set """ + set_updates + """ where email_address = '"""+str(email_address)+"""'"""
    print(update_query, " ==> this is the update operator")
    conn = get_connection()
    curr = conn.cursor()
    curr.execute(update_query)
    conn.commit()
    conn.close()


def insert_operator_dao(first_name, last_name, pwd, role, address, phone_number, id_proof, id_proof_type, email_address):
    '''INSERT INTO public.user_profile
(first_name, last_name, pwd, "role", address, phone_number, id_proof, id_proof_type, id_proof_doc, is_active, last_usage_datetime, created_datetime, email_adress)
VALUES('Punitha', 'Sakthivel', '3sdf', 'O', 'UKn Belvista', '7259722847', '4564', 'Passport', NULL, '1', '2022-11-02 00:00:00.000', '2022-11-02 00:00:00.000', 
'msams.punitha@gmail.com');
The is_active should be set to 1 always, while inserting. last_usage_datetime, created_datetime should be set to current date time.
'''
    conn = get_connection()
    curr = conn.cursor()
    now=datetime.now()
    curr.execute("""SELECT * from user_profile where user_profile.email_address = '"""+(email_address)+"""'""")
    if curr.fetchall():
        print("USER ALREADY EXIST")
    else:
        is_active=str('1')
        last_usage_datetime=now.strftime("%Y-%m-%d %H:%M:%S")
        created_datetime=now.strftime("%Y-%m-%d %H:%M:%S")
        insert_query=("""INSERT INTO user_profile (first_name, last_name, pwd, role, address, phone_number, id_proof, id_proof_type, is_active, last_usage_datetime, 
        created_datetime, email_address)
        VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""")
        records=(first_name, last_name, pwd, role, address, phone_number, id_proof, id_proof_type, is_active, last_usage_datetime, created_datetime, email_address)
        curr.execute(insert_query,records)
        conn.commit()
        curr.close()
    return True

#update_operator("AECS Layout, D Block", '997212458', None, None, 5 )

#insert_operator('New','Customer','abc','C','202 Thruso','123456789','pass123','passport','rnc@gmail.com')