from Config.DBConnection import *


def validate_userlogin(emaill_address, pwd):
    
    conn = get_connection()
    curr = conn.cursor()
    select_query = """SELECT first_name, last_name, role FROM 
                        user_profile where email_adress = '""" + emaill_address + """' and pwd = '""" + pwd + """'"""
    curr.execute(select_query)
    for x in curr.fetchall():
        print(x)
    
    return True
    

