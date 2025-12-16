import pandas as pd
import os

def cargar_y_describir_datos():
    ruta_base = r"C:\Users\JORGE\Desktop\Prueba - Studio F\Prueba Tecnica Analista datos BI"
    archivos = {
        "clientes": "BD_Clientes.xlsx",
        "transaccional": "BD_Transaccional.xlsx"
    }
    
    datos = {}
    for nombre, nombre_archivo in archivos.items():
        ruta = os.path.join(ruta_base, nombre_archivo)
        try:
            print(f"\n{'='*20} Cargando {nombre} ({nombre_archivo}) {'='*20}")
            df = pd.read_excel(ruta)
            datos[nombre] = df
            
            print(f"Dimensiones (Filas, Columnas): {df.shape}")
            print("\nColumnas:")
            print(df.columns.tolist())
            
            print("\nValores Faltantes:")
            print(df.isnull().sum()[df.isnull().sum() > 0])
            
            print("\nTipos de Datos:")
            print(df.dtypes)
            
            print("\nPrimeras 3 filas:")
            print(df.head(3).to_string())
            
            # Verificaciones específicas para Transaccional
            if nombre == "transaccional":
                if 'FechaCalendario' in df.columns:
                    print(f"\nRango de Fechas: {df['FechaCalendario'].min()} a {df['FechaCalendario'].max()}")
                
        except Exception as e:
            print(f"Error cargando {nombre}: {e}")

if __name__ == "__main__":
    cargar_y_describir_datos()
