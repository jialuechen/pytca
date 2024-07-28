import psycopg2
import pandas as pd

def load_pgsql_data(host, database, user, password, query):
    conn = psycopg2.connect(
        host=host,
        database=database,
        user=user,
        password=password
    )
    df = pd.read_sql(query, conn)
    conn.close()
    return df
