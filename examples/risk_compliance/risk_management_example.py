import numpy as np
from pytca.risk.compliance import calculate_var, compliance_check
import pandas as pd

# Example data: Returns of a portfolio over a period
portfolio_returns = np.array([-0.02, -0.01, 0.01, 0.02, 0.03, 0.05, -0.03, 0.04, 0.02, -0.02])

# Calculate Value at Risk (VaR) at 95% confidence level
confidence_level = 0.95
var = calculate_var(portfolio_returns, confidence_level)
print(f"Value at Risk (VaR) at {confidence_level * 100}% confidence level: {var:.4f}")

# Example transaction data for compliance check
transaction_data = pd.DataFrame({
    'TransactionID': [1, 2, 3, 4, 5],
    'Amount': [5000, 15000, 3000, 25000, 1000]
})

# Perform a compliance check for suspicious transactions
suspicious_transactions = compliance_check(transaction_data)
print("Suspicious Transactions:")
print(suspicious_transactions)
