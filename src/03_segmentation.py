import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import os
import matplotlib.pyplot as plt

def realizar_segmentacion():
    ruta_base = r"C:\Users\JORGE\Desktop\Prueba - Studio F\Prueba Tecnica Analista datos BI"
    
    # Cargar Datos
    print("Cargando datos...")
    try:
        df_trans = pd.read_excel(os.path.join(ruta_base, "input", "BD_Transaccional.xlsx"))
        df_clients = pd.read_excel(os.path.join(ruta_base, "input", "BD_Clientes.xlsx"))
    except FileNotFoundError:
        # Fallback si input no existe (estructura vieja)
        df_trans = pd.read_excel(os.path.join(ruta_base, "BD_Transaccional.xlsx"))
        df_clients = pd.read_excel(os.path.join(ruta_base, "BD_Clientes.xlsx"))
    
    # 1. Ingenieria de Caracteristicas en Transacciones
    # Convertir fecha
    df_trans['FechaCalendario'] = pd.to_datetime(df_trans['FechaCalendario'], errors='coerce')
    # Filter valid dates (e.g., from 2021 onwards) to avoid Year 0001 outliers
    df_trans = df_trans[df_trans['FechaCalendario'] > '2020-01-01']
    
    fecha_ref = df_trans['FechaCalendario'].max()
    
    # Agrupar por Cliente
    print("Agregando datos transaccionales...")
    user_trans = df_trans.groupby('FkCliente').agg({
        'FechaCalendario': lambda x: (fecha_ref - x.max()).days, # Recencia
        'NumDocumento': 'nunique', # Frecuencia
        'VentaSinIVA': 'sum', # Monto (Monetary)
        'Cantidad': 'sum'
    }).rename(columns={
        'FechaCalendario': 'Recency',
        'NumDocumento': 'Frequency',
        'VentaSinIVA': 'Monetary',
        'Cantidad': 'Total_Items'
    })
    
    # Preferencias de Producto (Pivot Linea)
    # Calcular % de gasto por Linea
    linea_pivot = df_trans.pivot_table(index='FkCliente', columns='Linea', values='VentaSinIVA', aggfunc='sum', fill_value=0)
    linea_pivot = linea_pivot.div(linea_pivot.sum(axis=1), axis=0) # Convertir a porcentaje
    linea_pivot.columns = ['Share_Linea_' + str(c) for c in linea_pivot.columns]
    
    # Preferencias de Canal (Pivot TipoEstablecimiento)
    channel_pivot = df_trans.pivot_table(index='FkCliente', columns='TipoEstablecimiento', values='NumDocumento', aggfunc='nunique', fill_value=0)
    channel_pivot = channel_pivot.div(channel_pivot.sum(axis=1), axis=0)
    channel_pivot.columns = ['Share_Channel_' + str(c) for c in channel_pivot.columns]
    
    # Unir Caracteristicas
    features = pd.concat([user_trans, linea_pivot, channel_pivot], axis=1)
    
    # Limpieza final
    features = features.fillna(0)
    features = features.replace([np.inf, -np.inf], 0)
    
    # 2. Escalado
    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(features)
    
    # 3. K-Means
    # Usando K=4 (tipico: Leales, Potenciales, En Riesgo, Perdidos)
    print("Ejecutando K-Means...")
    kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
    features['Cluster'] = kmeans.fit_predict(scaled_features)
    
    # 4. Perfilamiento de Clusters
    perfil = features.groupby('Cluster').mean()
    conteo = features.groupby('Cluster').size().rename('Count')
    perfil = pd.concat([conteo, perfil], axis=1)
    
    # Guardar Resultados
    archivo_salida = os.path.join(ruta_base, "output", "Reporte_Tecnico.md") # Nota: esto sobreescribiria el reporte manual, mejor no.
    # No guardamos reporte automatico aqui porque ya tenemos Entrega_Prueba.md. 
    # Solo imprimimos perfil.
    print("\nPerfil de Clusters:")
    print(perfil.to_string())
        
    # --- NUEVO: Exportar Series de Tiempo para Dashboard (Página 1) ---
    print("Generando datos temporales...")
    # Agrupar por Mes
    df_trans['Mes'] = df_trans['FechaCalendario'].dt.to_period('M').astype(str)
    ventas_mensuales = df_trans.groupby('Mes')['VentaSinIVA'].sum().reset_index()
    ventas_mensuales.columns = ['Mes', 'Ventas']
    
    csv_mensual = os.path.join(ruta_base, "output", "Ventas_Mensuales.csv")
    ventas_mensuales.to_csv(csv_mensual, index=False)
    
    # Agrupar por Zona/Ciudad (para Mapa)
    ventas_zona = df_trans.groupby('Ciudad')['VentaSinIVA'].sum().reset_index()
    csv_zona = os.path.join(ruta_base, "output", "Ventas_Zona.csv")
    ventas_zona.to_csv(csv_zona, index=False)
    
    # Agrupar por Linea/Categoria (para Tab 1 - Nuevo)
    ventas_linea = df_trans.groupby('Linea')['VentaSinIVA'].sum().reset_index().sort_values('VentaSinIVA', ascending=False)
    csv_linea = os.path.join(ruta_base, "output", "Ventas_Linea.csv")
    ventas_linea.to_csv(csv_linea, index=False)
    
    # --- Guardar datos etiquetados para Power BI ---
    # Fix: Reset index to ensure FkCliente is a column for merge
    final_df = features.reset_index().merge(df_clients, on='FkCliente', how='left')
    csv_final = os.path.join(ruta_base, "output", "Clientes_Segmentados.csv")
    final_df.to_csv(csv_final, index=False)
    print(f"Datos segmentados guardados en {csv_final}")

if __name__ == "__main__":
    try:
        realizar_segmentacion()
    except Exception as e:
        print(f"Error: {e}")
