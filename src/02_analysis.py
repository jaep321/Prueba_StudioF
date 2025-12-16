import pandas as pd
import os
import io

def ejecutar_analisis():
    ruta_base = r"C:\Users\JORGE\Desktop\Prueba - Studio F\Prueba Tecnica Analista datos BI"
    archivos = {
        "clientes": "BD_Clientes.xlsx",
        "transaccional": "BD_Transaccional.xlsx"
    }
    
    salida = []
    
    for nombre, nombre_archivo in archivos.items():
        ruta = os.path.join(ruta_base, nombre_archivo)
        salida.append(f"# Analisis de {nombre_archivo}")
        try:
            df = pd.read_excel(ruta)
            salida.append(f"- Dimensiones: {df.shape}")
            salida.append(f"- Columnas: {', '.join(df.columns)}")
            
            # Nulos
            nulos = df.isnull().sum()
            nulos = nulos[nulos > 0]
            if not nulos.empty:
                salida.append("- Valores Faltantes:")
                for col, val in nulos.items():
                    salida.append(f"  - {col}: {val}")
            else:
                salida.append("- No hay valores faltantes.")
                
            # Muestra
            salida.append("\n- Muestra de Datos:")
            salida.append(df.head(3).to_markdown(index=False))
            
            # Estadísticas (numéricas)
            salida.append("\n- Estadisticas Numericas:")
            salida.append(df.describe().to_markdown())
            
            salida.append("\n" + "="*30 + "\n")
            
        except Exception as e:
            salida.append(f"Error cargando {nombre_archivo}: {str(e)}")

    with open(os.path.join(ruta_base, "eda_summary.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(salida))

if __name__ == "__main__":
    try:
        ejecutar_analisis()
        print("Analisis completo. Guardado en eda_summary.md")
    except Exception as e:
        print(f"Error Global: {e}")
