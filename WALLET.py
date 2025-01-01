## CONECTA A UNA BASE DE DATOS ORACLE 
## AUTONOMOUS DATABASE USANDO EL WALLET

import oracledb


# Oracle Autonomous Database connection details
username = ''
password = ''
dsn = ''
wallet_dir = '/wallet'
wallet_password = ''

oracledb.init_oracle_client(
    config_dir=wallet_dir
)

connection = oracledb.connect(
    user=username,
    password=password,
    dsn=dsn
)

with connection.cursor() as cursor:
    sql = """SELECT * FROM customers360 INNER JOIN SALES360 ON customers360.CUST_ID = SALES360.CUST_ID WHERE ROWNUM <= 10""" 
    for row in cursor.execute(sql):
        print(row)