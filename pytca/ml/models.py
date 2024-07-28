from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

def train_forecast_model(data, target_column):
    X = data.drop(columns=[target_column])
    y = data[target_column]
    
    pipeline = Pipeline([
        ('scaler', StandardScaler()),
        ('model', RandomForestRegressor())
    ])
    
    model = pipeline.fit(X, y)
    return model
