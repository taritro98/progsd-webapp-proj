from Config.DBConnection import *

def login_dao(email_address, pwd):
    
    conn = get_connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    user = "SELECT email_address, pwd FROM USER_PROFILE"

    cursor.execute(user)

    count = 0

    for record in cursor.fetchall():
        if record[0] == email_address:
            user_id = record[0]
            print(user_id)
            pas = "SELECT pwd, user_id, role FROM USER_PROFILE WHERE EMAIL_ADDRESS = '" + email_address+"';"
            count = 1
            break

    
    if count == 1:
        cursor.execute(pas)
        for record in cursor.fetchall():
            if record[0] == pwd:
                response = {'login_status': 'Success', 'user_id': record[1], 'role': record[2]}
            else:
                response = {'login_status': 'Wrong Password', 'user_id': 'Blank'}
    else:
        response = {'login_status': 'Wrong Email', 'user_id': 'Blank'}
    conn.commit()
    cursor.close()
    conn.close()
    return response

#print(login_dao('newoperator2@tringtring.com', 'sdf'))