# examples/load_sql_data.py
from pytca import load_data

# Load data from MySQL
mysql_data = load_data('mysql', host='localhost', user='username', password='password', database='dbname', query='SELECT * FROM trades')
print(mysql_data.head())

# Load data from PostgreSQL
pgsql_data = load_data('pgsql', host='localhost', user='username', password='password', database='dbname', query='SELECT * FROM trades')
print(pgsql_data.head())
