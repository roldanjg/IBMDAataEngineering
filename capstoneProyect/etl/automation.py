import datetime 

# Import libraries required for connecting to mysql
import mysql.connector
# Import libraries required for connecting to DB2
import ibm_db
# Connect to MySQL
connection = mysql.connector.connect(user='root', password='Mzc2NC1qb2FxdWlu',host='127.0.0.1',database='sales')

# create cursor

cursor = connection.cursor()

# Connect to DB2
dsn_hostname = "824dfd4d-99de-440d-9991-629c01b3832d.bs2io90l08kqb1od8lcg.databases.appdomain.cloud" # e.g.: "dashdb-txn-sbox-yp-dal09-04.services.dal.bluemix.net"
dsn_uid = "rcn99047"        # e.g. "abc12345"
dsn_pwd = "n37LuvST1kQDueAu"      # e.g. "7dBZ3wWt9XN6$o0J"
dsn_port = "30119"                # e.g. "50000" 
dsn_database = "bludb"            # i.e. "BLUDB"
dsn_driver = "{IBM DB2 ODBC DRIVER}" # i.e. "{IBM DB2 ODBC DRIVER}"           
dsn_protocol = "TCPIP"            # i.e. "TCPIP"
dsn_security = "SSL"              # i.e. "SSL"

#Create the dsn connection string
dsn = (
    "DRIVER={0};"
    "DATABASE={1};"
    "HOSTNAME={2};"
    "PORT={3};"
    "PROTOCOL={4};"
    "UID={5};"
    "PWD={6};"
    "SECURITY={7};").format(dsn_driver, dsn_database, dsn_hostname, dsn_port, dsn_protocol, dsn_uid, dsn_pwd, dsn_security)

# create connection
conn = ibm_db.connect(dsn, "", "")
print ("Connected to database: ", dsn_database, "as user: ", dsn_uid, "on host: ", dsn_hostname)

# Find out the last rowid from DB2 data warehouse
# The function get_last_rowid must return the last rowid of the table sales_data on the IBM DB2 database.

def get_last_rowid():
    SQL = """SELECT ROWID FROM sales_data ORDER BY ROWID DESC LIMIT 1"""
    select_last_row = ibm_db.exec_immediate(conn, SQL)
    return ibm_db.fetch_tuple(select_last_row)[0]

last_row_id = get_last_rowid()
print("Last row id on production datawarehouse = ", last_row_id)

# List out all records in MySQL database with rowid greater than the one on the Data warehouse
# The function get_latest_records must return a list of all records that have a rowid greater than 
# the last_row_id in the sales_data table in the sales database on the MySQL staging data warehouse.

def get_latest_records(rowid):
	last_records = []
	SQL = "SELECT * FROM sales_data where rowid>{}".format(rowid)
	cursor.execute(SQL)
	for row in cursor.fetchall():
		last_records.append(row)
	return last_records

new_records = get_latest_records(last_row_id)
print("New rows on staging datawarehouse = ", len(new_records))

# Insert the additional records from MySQL into DB2 data warehouse.
# The function insert_records must insert all the records passed to it into the sales_data table in IBM DB2 database.

def insert_records(records):
	SQL = "INSERT INTO sales_data(ROWID,PRODUCT_ID,CUSTOMER_ID,PRICE,QUANTITY,TIMESTAMP)  VALUES(?,?,?,?,?,?);"
	stmt = ibm_db.prepare(conn, SQL)
	for new_record in records:
#lets imagine that every article cost 15 $
		now = datetime.datetime.now()
		time_now = now.strftime('%Y-%m-%d %H:%M:%S')
		ibm_db.execute(
		stmt, 
		(new_record[0],new_record[1],new_record[2],new_record[3]*15,new_record[3],time_now)
		)

insert_records(new_records)
print("New rows inserted into production datawarehouse = ", len(new_records))

# disconnect from mysql warehouse
# close connection
connection.close()
# disconnect from DB2 data warehouse
# close connection
ibm_db.close(conn)
# End of program
