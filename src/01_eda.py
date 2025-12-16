import pandas as pd
import os

def load_and_describe_data():
    base_path = r"C:\Users\JORGE\Desktop\Prueba - Studio F\Prueba Tecnica Analista datos BI"
    files = {
        "clientes": "BD_Clientes.xlsx",
        "transaccional": "BD_Transaccional.xlsx"
    }
    
    data = {}
    for name, filename in files.items():
        path = os.path.join(base_path, filename)
        try:
            print(f"\n{'='*20} Loading {name} ({filename}) {'='*20}")
            df = pd.read_excel(path)
            data[name] = df
            
            print(f"Shape: {df.shape}")
            print("\nColumns:")
            print(df.columns.tolist())
            
            print("\nMissing Values:")
            print(df.isnull().sum()[df.isnull().sum() > 0])
            
            print("\nData Types:")
            print(df.dtypes)
            
            print("\nFirst 3 rows:")
            print(df.head(3).to_string())
            
            # Specific checks for Transaccional
            if name == "transaccional":
                if 'FechaCalendario' in df.columns:
                    print(f"\nDate Range: {df['FechaCalendario'].min()} to {df['FechaCalendario'].max()}")
                
        except Exception as e:
            print(f"Error loading {name}: {e}")

if __name__ == "__main__":
    load_and_describe_data()
