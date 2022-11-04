import psycopg2
from credfile import HOST, DATABASE, USER, PASSWORD, PORT_ID

def get_connection():
    try:
        return psycopg2.connect(
            database=DATABASE,
            user=USER,
            password=PASSWORD,
            host=HOST,
            port=PORT_ID,
        )
    except:
        return False
  
