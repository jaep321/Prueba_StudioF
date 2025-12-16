import pandas as pd
import os

base_path = r"C:\Users\JORGE\Desktop\Prueba - Studio F\Prueba Tecnica Analista datos BI"
# Intentar leer desde input/ o raiz
path = os.path.join(base_path, "input", "BD_Transaccional.xlsx")
if not os.path.exists(path):
    path = os.path.join(base_path, "BD_Transaccional.xlsx")

df = pd.read_excel(path)

print("Valores Unicos TipoEstablecimiento:", df['TipoEstablecimiento'].unique())
print("Valores Unicos Linea:", df['Linea'].unique())
print("Valores Unicos Familia:", df['Familia'].unique())
print("Valores Unicos DescripcionMarca:", df['DescripcionMarca'].unique())
