from ml.train_model import train
from ml.predict import forecast
def predict_prices(df,days):
    model,closes,metrics,error=train(df)
    prices=forecast(model,closes,days)
    return {'predictions':prices,'metrics':metrics,'latest':round(float(closes[-1]),2),'change_pct':round((prices[-1]/closes[-1]-1)*100,2),'uncertainty_note':f'One-step held-out absolute error 90th percentile: {error:.2f} price units. Not a calibrated multi-day interval.'}
