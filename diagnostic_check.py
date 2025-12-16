import pandas as pd
import os

base_path = r"C:\Users\JORGE\Desktop\Prueba - Studio F\Prueba Tecnica Analista datos BI"
csv_seg = os.path.join(base_path, "output", "Clientes_Segmentados.csv")

if os.path.exists(csv_seg):
    df = pd.read_csv(csv_seg)
    print("--- INFO ---")
    print(df.info())
    print("\n--- HEAD ---")
    print(df.head())
    print("\n--- RECENCY STATS ---")
    print(df['Recency'].describe())
    print("\n--- COLUMNS ---")
    print(df.columns.tolist())
else:
    print("File not found")
