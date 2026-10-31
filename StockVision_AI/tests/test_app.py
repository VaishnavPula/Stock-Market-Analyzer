import numpy as np
import pandas as pd
from ml.preprocessing import prepare
from ml.train_model import train
from ml.predict import forecast
from services.stock_service import symbol_for

def test_symbol():
    assert symbol_for('Apple')=='AAPL'
    assert symbol_for('reliance')=='RELIANCE.NS'
def test_model_pipeline():
    rng=np.random.default_rng(42)
    prices=100+np.cumsum(rng.normal(0,1,150))
    df=pd.DataFrame({'Close':prices})
    X,y,close=prepare(df)
    assert len(X)==129
    model,closes,metrics,error=train(df)
    assert len(forecast(model,closes,5))==5
    assert metrics['mae']>=0 and error>=0
