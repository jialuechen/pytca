from arctic import Arctic
import pandas as pd

def load_arctic_data(host, library, symbol):
    store = Arctic(host)
    lib = store[library]
    df = lib.read(symbol).data
    return df
