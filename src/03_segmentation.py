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
    
    # Convertir fecha con tolerancia a distintos formatos
    df_trans['FechaCalendario'] = pd.to_datetime(df_trans['FechaCalendario'], errors='coerce')
    # Si todo quedo en NaT, intentar conversión desde serial de Excel
    if df_trans['FechaCalendario'].isna().all():
        df_trans['FechaCalendario'] = pd.to_datetime(
            df_trans['FechaCalendario'],
            errors='coerce',
            origin='1899-12-30',
            unit='D'
        )
    
    # Filter valid dates (e.g., from 2021 onwards)
    df_trans = df_trans[df_trans['FechaCalendario'] > '2020-01-01']
    
    if df_trans.empty:
        raise ValueError("No se pudieron interpretar fechas validas en FechaCalendario.")
        
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
    
    # Preferencias de Producto (Linea, Familia, Marca)
    # Agrupar Linea a top N para evitar dimensionalidad excesiva
    top_lineas = (
        df_trans.groupby('Linea')['VentaSinIVA']
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .index
    )
    df_trans['Linea_Grupo'] = df_trans['Linea'].where(df_trans['Linea'].isin(top_lineas), 'Otras')

    # Calcular % de gasto por Linea (Top 10 + Otras)
    linea_pivot = df_trans.pivot_table(index='FkCliente', columns='Linea_Grupo', values='VentaSinIVA', aggfunc='sum', fill_value=0)
    linea_pivot = linea_pivot.div(linea_pivot.sum(axis=1), axis=0) # Convertir a porcentaje
    linea_pivot.columns = ['Share_Linea_' + str(c) for c in linea_pivot.columns]

    # Calcular % de gasto por Familia
    familia_pivot = df_trans.pivot_table(index='FkCliente', columns='Familia', values='VentaSinIVA', aggfunc='sum', fill_value=0)
    familia_pivot = familia_pivot.div(familia_pivot.sum(axis=1), axis=0)
    familia_pivot.columns = ['Share_Familia_' + str(c) for c in familia_pivot.columns]

    # Calcular % de gasto por Marca
    marca_pivot = df_trans.pivot_table(index='FkCliente', columns='DescripcionMarca', values='VentaSinIVA', aggfunc='sum', fill_value=0)
    marca_pivot = marca_pivot.div(marca_pivot.sum(axis=1), axis=0)
    marca_pivot.columns = ['Share_Marca_' + str(c) for c in marca_pivot.columns]
    
    # Preferencias de Canal (Pivot TipoEstablecimiento)
    channel_pivot = df_trans.pivot_table(index='FkCliente', columns='TipoEstablecimiento', values='NumDocumento', aggfunc='nunique', fill_value=0)
    channel_pivot = channel_pivot.div(channel_pivot.sum(axis=1), axis=0)
    channel_pivot.columns = ['Share_Channel_' + str(c) for c in channel_pivot.columns]
    
    # Unir Caracteristicas
    features = pd.concat([user_trans, linea_pivot, familia_pivot, marca_pivot, channel_pivot], axis=1)
    
    # Limpieza final
    features = features.fillna(0)
    features = features.replace([np.inf, -np.inf], 0)
    features = features.clip(lower=0)
    
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
    # Fix: Ensure FkCliente is preserved and no extra index is created
    final_df = features.reset_index().merge(df_clients, on='FkCliente', how='left')
    
    # Filter out insanity (if any remain)
    final_df = final_df[final_df['Recency'] < 5000] 
    
    csv_final = os.path.join(ruta_base, "output", "Clientes_Segmentados.csv")
    final_df.to_csv(csv_final, index=False)
    print(f"Datos segmentados guardados en {csv_final}")

if __name__ == "__main__":
    try:
        realizar_segmentacion()
    except Exception as e:
        print(f"Error: {e}")
