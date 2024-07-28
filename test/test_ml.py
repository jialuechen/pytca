import pytest
from pytca.ml.models import train_forecast_model
import pandas as pd

def test_train_forecast_model():
    data = pd.DataFrame({
        'feature1': [1, 2, 3, 4, 5],
        'feature2': [2, 3, 4, 5, 6],
        'target': [1.1, 1.2, 1.3, 1.4, 1.5]
    })
    model = train_forecast_model(data, 'target')
    assert model, "Model should be trained"
