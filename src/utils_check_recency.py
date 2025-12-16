import pandas as pd
import sys
import os

try:
    ruta_base = r"C:\Users\JORGE\Desktop\Prueba - Studio F\Prueba Tecnica Analista datos BI"
    # Intentar leer desde input/ o raiz
    path = os.path.join(ruta_base, "input", "BD_Transaccional.xlsx")
    if not os.path.exists(path):
        path = os.path.join(ruta_base, "BD_Transaccional.xlsx")
        
    df = pd.read_excel(path)
    df['FechaCalendario'] = pd.to_datetime(df['FechaCalendario'])
    ref = df['FechaCalendario'].max()
    recency = df.groupby('FkCliente')['FechaCalendario'].max().apply(lambda x: (ref - x).days)
    print("Estadísticas de Recencia:")
    print(recency.describe(percentiles=[0.5, 0.75, 0.9, 0.95]))
except Exception as e:
    print(e)
