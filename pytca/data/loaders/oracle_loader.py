import cx_Oracle
import pandas as pd

def load_oracle_data(dsn, user, password, query):
    conn = cx_Oracle.connect(user=user, password=password, dsn=dsn)
    df = pd.read_sql(query, conn)
    conn.close()
    return df
