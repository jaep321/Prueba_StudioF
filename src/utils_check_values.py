import pandas as pd
import os

base_path = r"C:\Users\JORGE\Desktop\Prueba - Studio F\Prueba Tecnica Analista datos BI"
df = pd.read_excel(os.path.join(base_path, "BD_Transaccional.xlsx"))

print("Unique TipoEstablecimiento:", df['TipoEstablecimiento'].unique())
print("Unique Linea:", df['Linea'].unique())
print("Unique Familia:", df['Familia'].unique())
print("Unique DescripcionMarca:", df['DescripcionMarca'].unique())
