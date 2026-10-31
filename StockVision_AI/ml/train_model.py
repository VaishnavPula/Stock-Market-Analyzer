import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from .preprocessing import prepare
def train(df):
    X,y,close = prepare(df)
    split=int(len(X)*.8)
    if split<30 or len(X)-split<10: raise ValueError('Insufficient samples for evaluation.')
    model=RandomForestRegressor(n_estimators=90,max_depth=12,min_samples_leaf=2,random_state=42,n_jobs=-1)
    model.fit(X[:split],y[:split]); predicted=model.predict(X[split:])
    metrics={'mae':round(float(mean_absolute_error(y[split:],predicted)),3),'rmse':round(float(np.sqrt(mean_squared_error(y[split:],predicted))),3),'r2':round(float(r2_score(y[split:],predicted)),4)}
    errors=np.abs(y[split:]-predicted)
    # Refit on all available data after measuring held-out error.
    model.fit(X,y)
    return model,close,metrics,float(np.quantile(errors,.9))
