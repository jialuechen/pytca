import mysql.connector
import pandas as pd

def load_mysql_data(host, user, password, database, query):
    conn = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )
    df = pd.read_sql(query, conn)
    conn.close()
    return df
