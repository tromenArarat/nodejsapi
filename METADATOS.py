## FUNCIÓN PARA OBTENER LOS METADATOS DE UNA TABLA Y 
## CONSTRUIR UNA API REST CON FLASK
### LOS METADATOS SE VAN A UTILIZAR PARA CREAR EL INDEX.HTML

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

try:
    connection = oracledb.connect(user=username, password=password, dsn=dsn)
    print("Database connection successful!")
except Exception as e:
    print(f"Error connecting to database: {e}")

from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, marshal_with, fields
import oracledb

# Flask app setup
app = Flask(__name__)
api = Api(app)



# Define the Customers360 model manually
class Customers360:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

# Define fields for marshalling
customer_fields = {
    'CUST_ID': fields.Integer,
    'CUST_FIRST_NAME': fields.String,
    'CUST_LAST_NAME': fields.String,
    'CUST_GENDER': fields.String,
    'CUST_YEAR_OF_BIRTH': fields.Integer,
    'CUST_MARITAL_STATUS': fields.String,
    'CUST_STREET_ADDRESS': fields.String,
    'CUST_POSTAL_CODE': fields.String,
    'CUST_CITY': fields.String,
    'CUST_CITY_ID': fields.Integer,
    'CUST_STATE_PROVINCE': fields.String,
    'CUST_STATE_PROVINCE_ID': fields.Integer,
    'COUNTRY_ID': fields.Integer,
    'CUST_MAIN_PHONE_NUMBER': fields.String,
    'CUST_INCOME_LEVEL': fields.String,
    'CUST_CREDIT_LIMIT': fields.Float,
    'CUST_EMAIL': fields.String,
    'CUST_TOTAL': fields.String,
    'CUST_TOTAL_ID': fields.Integer,
    'CUST_SRC_ID': fields.Integer,
    'CUST_EFF_FROM': fields.String,
    'CUST_EFF_TO': fields.String,
    'CUST_VALID': fields.String
}

# Parse incoming request data
customer_args = reqparse.RequestParser()
customer_args.add_argument('CUST_FIRST_NAME', type=str, required=True)
customer_args.add_argument('CUST_LAST_NAME', type=str, required=True)
customer_args.add_argument('CUST_GENDER', type=str, required=True)
customer_args.add_argument('CUST_YEAR_OF_BIRTH', type=int, required=True)
customer_args.add_argument('CUST_MARITAL_STATUS', type=str, required=False)
customer_args.add_argument('CUST_STATE_PROVINCE_ID', type=int, required=False)
customer_args.add_argument('COUNTRY_ID', type=int, required=False)
customer_args.add_argument('CUST_MAIN_PHONE_NUMBER', type=str, required=False)
customer_args.add_argument('CUST_INCOME_LEVEL', type=str, required=False)
customer_args.add_argument('CUST_CREDIT_LIMIT', type=float, required=False)
customer_args.add_argument('CUST_EMAIL', type=str, required=False)
customer_args.add_argument('CUST_TOTAL', type=str, required=False)
customer_args.add_argument('CUST_TOTAL_ID', type=int, required=False)
customer_args.add_argument('CUST_SRC_ID', type=int, required=False)
customer_args.add_argument('CUST_EFF_FROM', type=str, required=False)
customer_args.add_argument('CUST_EFF_TO', type=str, required=False)
customer_args.add_argument('CUST_VALID', type=str, required=False)

# Add other fields as necessary

# Resources for API
class Customers(Resource):
    @marshal_with(customer_fields)
    def get(self):
        query = "SELECT * FROM CUSTOMERS360 WHERE ROWNUM <= 25"
        cursor = connection.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        columns = [col[0] for col in cursor.description]
        customers = [Customers360(**dict(zip(columns, row))) for row in rows]
        cursor.close()
        return customers

    @marshal_with(customer_fields)
    def post(self):
        args = customer_args.parse_args()
        query = """INSERT INTO CUSTOMERS360 (
            CUST_FIRST_NAME, CUST_LAST_NAME, CUST_GENDER, CUST_YEAR_OF_BIRTH, CUST_MARITAL_STATUS
        ) VALUES (:1, :2, :3, :4, :5)"""
        cursor = connection.cursor()
        cursor.execute(query, (
            args['CUST_FIRST_NAME'], args['CUST_LAST_NAME'], 
            args['CUST_GENDER'], args['CUST_YEAR_OF_BIRTH'], 
            args.get('CUST_MARITAL_STATUS')
        ))
        connection.commit()
        cursor.close()
        return {}, 201

class Customer(Resource):
    @marshal_with(customer_fields)
    def get(self, cust_id):
        query = "SELECT * FROM CUSTOMERS360 WHERE CUST_ID = :1"
        cursor = connection.cursor()
        cursor.execute(query, [cust_id])
        row = cursor.fetchone()
        cursor.close()
        if not row:
            abort(404, message="Customer not found")
        columns = [col[0] for col in cursor.description]
        customer = Customers360(**dict(zip(columns, row)))
        return customer

    @marshal_with(customer_fields)
    def delete(self, cust_id):
        query = "DELETE FROM CUSTOMERS360 WHERE CUST_ID = :1"
        cursor = connection.cursor()
        cursor.execute(query, [cust_id])
        connection.commit()
        cursor.close()
        return {}, 204

# Add resources
api.add_resource(Customers, '/api/customers')
api.add_resource(Customer, '/api/customers/<int:cust_id>')

# Run the application
if __name__ == '__main__':
    app.run(debug=True)


## FUNCIÓN PARA OBTENER LOS METADATOS DE UNA TABLA

##def get_table_metadata(connection, schema_name='ADMIN', table_name=None):
##   query = """
##    SELECT TABLE_NAME, COLUMN_NAME, DATA_TYPE, NULLABLE
##    FROM ALL_TAB_COLUMNS
##    WHERE OWNER = :schema_name
##    """
##    params = {'schema_name': schema_name}
##    if table_name:
##        query += " AND TABLE_NAME = :table_name"
##        params['table_name'] = table_name##
##
##    with connection.cursor() as cursor:
##        cursor.execute(query, params)
##        return cursor.fetchall()

# Example: Get metadata for all tables
## tables_metadata = get_table_metadata(connection)