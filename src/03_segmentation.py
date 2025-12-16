import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import os
import matplotlib.pyplot as plt

def perform_segmentation():
    base_path = r"C:\Users\JORGE\Desktop\Prueba - Studio F\Prueba Tecnica Analista datos BI"
    
    # Load Data
    print("Loading data...")
    df_trans = pd.read_excel(os.path.join(base_path, "BD_Transaccional.xlsx"))
    df_clients = pd.read_excel(os.path.join(base_path, "BD_Clientes.xlsx"))
    
    # 1. Feature Engineering on Transactions
    # Convert date
    df_trans['FechaCalendario'] = pd.to_datetime(df_trans['FechaCalendario'])
    ref_date = df_trans['FechaCalendario'].max()
    
    # Handle returns (Negative Sales)
    # We will assume Recency/Frequency should consider any interaction, but Monetary is net.
    # Actually, for "Churn", returns are interactions too.
    # But for "Value", we sum net.
    
    # Group by Client
    print("Aggregating transactional data...")
    user_trans = df_trans.groupby('FkCliente').agg({
        'FechaCalendario': lambda x: (ref_date - x.max()).days, # Recency
        'NumDocumento': 'nunique', # Frequency
        'VentaSinIVA': 'sum', # Monetary
        'Cantidad': 'sum'
    }).rename(columns={
        'FechaCalendario': 'Recency',
        'NumDocumento': 'Frequency',
        'VentaSinIVA': 'Monetary',
        'Cantidad': 'Total_Items'
    })
    
    # Product Preferences (Pivot Linea)
    # Calculate % of spend per Linea
    linea_pivot = df_trans.pivot_table(index='FkCliente', columns='Linea', values='VentaSinIVA', aggfunc='sum', fill_value=0)
    linea_pivot = linea_pivot.div(linea_pivot.sum(axis=1), axis=0) # Convert to percentage
    linea_pivot.columns = ['Share_Linea_' + str(c) for c in linea_pivot.columns]
    
    # Channel Preferences (Pivot TipoEstablecimiento)
    channel_pivot = df_trans.pivot_table(index='FkCliente', columns='TipoEstablecimiento', values='NumDocumento', aggfunc='nunique', fill_value=0)
    channel_pivot = channel_pivot.div(channel_pivot.sum(axis=1), axis=0)
    channel_pivot.columns = ['Share_Channel_' + str(c) for c in channel_pivot.columns]
    
    # Merge Features
    features = pd.concat([user_trans, linea_pivot, channel_pivot], axis=1)
    
    # Clean cleanup
    features = features.fillna(0)
    features = features.replace([np.inf, -np.inf], 0)
    
    # Merge with Demographics (just for profiling, maybe use Age for clustering?)
    # Calculate Age
    # df_clients['Fecha_Nacimiento'] = pd.to_datetime(df_clients['Fecha_Nacimiento'], errors='coerce')
    # df_clients['Age'] = (ref_date - df_clients['Fecha_Nacimiento']).dt.days / 365.25
    # For now, let's stick to behavioral segmentation (RFM + Preferences) for robust clusters
    
    # 2. Scaling
    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(features)
    
    # 3. K-Means
    # Using K=4 (typical: Loyal, Potential, At Risk, Lost)
    print("Running K-Means...")
    kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
    features['Cluster'] = kmeans.fit_predict(scaled_features)
    
    # 4. Profile Clusters
    profile = features.groupby('Cluster').mean()
    count = features.groupby('Cluster').size().rename('Count')
    profile = pd.concat([count, profile], axis=1)
    
    # Save Results
    output_file = os.path.join(base_path, "segmentation_profile.md")
    with open(output_file, 'w') as f:
        f.write("# Segmentation Results (K=4)\n\n")
        f.write(profile.to_markdown())
        f.write("\n\n## Cluster Interpretation Candidates:\n")
        f.write("- **Recency**: Lower is better (more recent).\n")
        f.write("- **Frequency/Monetary**: Higher is better.\n")
        
    # Save tagged data for Power BI
    final_df = features.merge(df_clients, on='FkCliente', how='left')
    final_csv = os.path.join(base_path, "Clientes_Segmentados.csv")
    final_df.to_csv(final_csv, index=False)
    print(f"Saved segmented data to {final_csv}")

if __name__ == "__main__":
    try:
        perform_segmentation()
    except Exception as e:
        print(f"Error: {e}")
