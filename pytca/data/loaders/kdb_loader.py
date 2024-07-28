from qpython import qconnection
import pandas as pd

def load_kdb_data(host, port, query):
    with qconnection.QConnection(host=host, port=port) as q:
        data = q(query)
    return pd.DataFrame(data)
