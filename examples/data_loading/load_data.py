# examples/load_data.py
from pytca import load_data

# Load data from a CSV file
csv_data = load_data('csv', file_path='path/to/data.csv')
print(csv_data.head())

# Load data from an Excel file
excel_data = load_data('excel', file_path='path/to/data.xlsx', sheet_name='Sheet1')
print(excel_data.head())

# Load data from a KDB database
kdb_data = load_data('kdb', host='localhost', port=5001, query='select from trade')
print(kdb_data.head())
