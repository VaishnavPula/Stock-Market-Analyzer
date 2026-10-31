import numpy as np
from .preprocessing import row_from_closes
def forecast(model,closes,days):
    if days not in (1,5,7): raise ValueError('Choose 1, 5 or 7 sessions.')
    values=list(map(float,closes)); out=[]
    for _ in range(days):
        value=float(model.predict(np.asarray([row_from_closes(values)]))[0]);out.append(round(value,2));values.append(value)
    return out
