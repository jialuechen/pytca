import pyodbc
import pandas as pd

def load_sqlserver_data(server, database, user, password, query):
    conn_str = (
        f"DRIVER={{SQL Server}};"
        f"SERVER={server};"
        f"DATABASE={database};"
        f"UID={user};"
        f"PWD={password};"
    )
    conn = pyodbc.connect(conn_str)
    df = pd.read_sql(query, conn)
    conn.close()
    return df
