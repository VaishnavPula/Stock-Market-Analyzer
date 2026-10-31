def insights(df):
    close=df['Close'].astype(float)
    if len(close)<20:return ['Not enough data for 20-session moving-average analysis.']
    trend='above' if close.iloc[-1]>close.tail(20).mean() else 'below'
    change=(close.iloc[-1]/close.iloc[-min(6,len(close))]-1)*100
    volatility=close.pct_change().tail(20).std()*100
    return [f'Latest close is {trend} its 20-session moving average.',f'Approximate recent 5-session return: {change:+.2f}%.',f'20-session daily return volatility: {volatility:.2f}%.','These are historical statistics, not investment advice.']
