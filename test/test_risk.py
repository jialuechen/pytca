import pytest
import numpy as np
from pytca.risk.compliance import calculate_var, compliance_check

def test_calculate_var():
    returns = np.array([-0.02, -0.01, 0.01, 0.02, 0.03, 0.05])
    confidence_level = 0.95
    expected_var = -0.01  # Expected VaR at 95% confidence level

    var = calculate_var(returns, confidence_level)

    assert np.isclose(var, expected_var, atol=1e-6), f"VaR calculation error: expected {expected_var}, got {var}"

def test_compliance_check():
    import pandas as pd
    transaction_data = pd.DataFrame({
        'TransactionID': [1, 2, 3, 4, 5],
        'Amount': [5000, 15000, 3000, 25000, 1000]
    })
    
    suspicious_transactions = compliance_check(transaction_data)
    
    expected_suspicious_ids = [2, 4]  # Transactions with Amount > 10000
    assert list(suspicious_transactions['TransactionID']) == expected_suspicious_ids, \
        f"Compliance check error: expected suspicious transactions {expected_suspicious_ids}, got {list(suspicious_transactions['TransactionID'])}"
