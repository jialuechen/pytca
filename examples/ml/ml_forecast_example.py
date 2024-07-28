from pytca.ml.models import train_forecast_model
import pandas as pd

# Example data
data = pd.DataFrame({
    'feature1': [1, 2, 3, 4, 5],
    'feature2': [2, 3, 4, 5, 6],
    'target': [1.1, 1.2, 1.3, 1.4, 1.5]
})

model = train_forecast_model(data, 'target')
print("Model trained successfully.")
