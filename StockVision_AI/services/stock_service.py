import re
import pandas as pd
import yfinance as yf
COMPANIES = {'apple':'AAPL','microsoft':'MSFT','google':'GOOGL','alphabet':'GOOGL','amazon':'AMZN','tesla':'TSLA','reliance':'RELIANCE.NS','tcs':'TCS.NS','infosys':'INFY.NS','hdfc bank':'HDFCBANK.NS'}
def symbol_for(value):
    value = str(value or '').strip()
    if not value: raise ValueError('Enter a company or ticker symbol.')
    result = COMPANIES.get(value.lower(), value.upper())
    if not re.fullmatch(r'[A-Z0-9.\-^=]{1,25}', result): raise ValueError('Invalid stock symbol.')
    return result
def get_history(symbol, period='1y', start=None, end=None):
    if period not in ('1mo','3mo','6mo','1y','3y','5y'): raise ValueError('Unsupported date range.')
    if start or end:
        if not (start and end): raise ValueError('Provide both start and end dates.')
        a,b = pd.Timestamp(start),pd.Timestamp(end)
        if a >= b or b > pd.Timestamp.now() + pd.Timedelta(days=1): raise ValueError('Invalid date range.')
        df = yf.Ticker(symbol).history(start=start,end=end,auto_adjust=True)
    else: df = yf.Ticker(symbol).history(period=period,auto_adjust=True)
    if df.empty: raise ValueError('No market data available for this symbol or date range.')
    df = df[['Open','High','Low','Close','Volume']].dropna(subset=['Close']).sort_index()
    if df.empty: raise ValueError('No valid price data returned.')
    return df

def serialize(df):
    return [{'date':str(i.date()),'open':round(float(r.Open),2),'high':round(float(r.High),2),'low':round(float(r.Low),2),'close':round(float(r.Close),2),'volume':int(r.Volume)} for i,r in df.iterrows()]
