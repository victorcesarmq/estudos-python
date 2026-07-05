import pandas as pd

#-------------------------------------------------------------
'''
Tratamento de Erros e verificacoes em DataFrames
'''
def empty(df: pd.DataFrame):
    return df.empty

def lenz(df):
    return len(df) == 0

def lenzi(df):
    return len(df.index) == 0
#-------------------------------------------------------------