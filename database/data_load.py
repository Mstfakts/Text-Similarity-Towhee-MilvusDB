import pandas as pd

def read_from_csv(path, index_col=0):
    df = pd.read_csv(path, index_col=[index_col])
    return df