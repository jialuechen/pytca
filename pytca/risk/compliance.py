import numpy as np

def calculate_var(returns, confidence_level=0.95):
    sorted_returns = np.sort(returns)
    index = int((1 - confidence_level) * len(sorted_returns))
    return sorted_returns[index]

def compliance_check(transaction_data):
    suspicious_transactions = transaction_data[transaction_data['Amount'] > 10000]
    return suspicious_transactions
