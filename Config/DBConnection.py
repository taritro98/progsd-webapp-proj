import psycopg2
  
def get_connection():
    try:
        return psycopg2.connect(
            database="d8fka28kjhdh83",
            user="lvqdingxyjopfb",
            password="730fd28c3fc99b055f8462b39548ad66dd2eee8bd30e8f98b707aa1dc3975595",
            host="ec2-34-246-86-78.eu-west-1.compute.amazonaws.com",
            port=5432,
        )
    except:
        return False
  
