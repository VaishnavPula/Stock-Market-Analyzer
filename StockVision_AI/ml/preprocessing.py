import numpy as np
import pandas as pd
FEATURES = ['lag1','lag2','lag3','lag5','ma5','ma10','ma20','volatility']
def row_from_closes(closes):
    a = np.asarray(closes,dtype=float)
    if len(a)<21: raise ValueError('At least 21 historical closing prices are needed.')
    returns = np.diff(a[-21:])/a[-21:-1]
    return [a[-1],a[-2],a[-3],a[-5],a[-5:].mean(),a[-10:].mean(),a[-20:].mean(),float(np.std(returns))]
def prepare(df):
    close = df['Close'].astype(float).to_numpy()
    if len(close)<80: raise ValueError('At least 80 trading sessions are required for model training.')
    X,y=[],[]
    for i in range(21,len(close)):
        X.append(row_from_closes(close[:i]));y.append(close[i])
    return np.asarray(X),np.asarray(y),close
