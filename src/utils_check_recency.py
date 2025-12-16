import pandas as pd
import sys

try:
    df = pd.read_excel(r'C:\Users\JORGE\Desktop\Prueba - Studio F\Prueba Tecnica Analista datos BI\BD_Transaccional.xlsx')
    df['FechaCalendario'] = pd.to_datetime(df['FechaCalendario'])
    ref = df['FechaCalendario'].max()
    recency = df.groupby('FkCliente')['FechaCalendario'].max().apply(lambda x: (ref - x).days)
    print(recency.describe(percentiles=[0.5, 0.75, 0.9, 0.95]))
except Exception as e:
    print(e)
