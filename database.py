import pymysql

def create_connection():
    
    config = {
        'user': 'admin',
        'password': 'x23301295-scalable-cloud-rds',
        'host': 'x23301295-scalable-cloud-rds.cizdihoh0eru.us-east-1.rds.amazonaws.com',  
        'database': 'scalable_cloud_rds'
    }
    try:
        conn = pymysql.connect(**config)
        print("Connection successful.")
        return conn
    except pymysql.MySQLError as err:
        print(f"Error: {err}")
        return None
