import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

def crear_visualizaciones():
    ruta_base = r"C:\Users\JORGE\Desktop\Prueba - Studio F\Prueba Tecnica Analista datos BI"
    ruta_csv = os.path.join(ruta_base, "output", "Clientes_Segmentados.csv")
    ruta_img = os.path.join(ruta_base, "images")
    
    print("Cargando datos...")
    try:
        df = pd.read_csv(ruta_csv)
    except FileNotFoundError:
        print("Datos segmentados no encontrados en output/. Buscando en raiz...")
        ruta_csv = os.path.join(ruta_base, "Clientes_Segmentados.csv") # Fallback
        df = pd.read_csv(ruta_csv)

    # Configurar estilo
    sns.set(style="whitegrid")

    # 1. Distribucion de Clusters
    print("Graficando Distribucion de Clusters...")
    plt.figure(figsize=(10, 6))
    conteo_clusters = df['Cluster'].value_counts().sort_index()
    colores = ['#2c3e50', '#e74c3c', '#3498db', '#f1c40f'] # Azul Oscuro, Rojo, Azul, Amarillo
    
    ax = sns.barplot(x=conteo_clusters.index, y=conteo_clusters.values, palette=colores)
    plt.title('Distribución de Clientes por Segmento', fontsize=15)
    plt.xlabel('Cluster', fontsize=12)
    plt.ylabel('Cantidad de Clientes', fontsize=12)
    
    # Agregar etiquetas
    for i, v in enumerate(conteo_clusters.values):
        ax.text(i, v + 50, str(v), ha='center', fontweight='bold')
        
    plt.savefig(os.path.join(ruta_img, "cluster_distribution.png"), dpi=300, bbox_inches='tight')
    plt.close()

    # 2. Grafico de Dispersion: Recencia vs Valor Monetario
    print("Graficando Recencia vs Valor Monetario...")
    plt.figure(figsize=(10, 6))
    
    # Filtrar outlier extremo para visualizacion (El cliente de 400M) para mantener escala legible
    df_viz = df[df['Monetary'] < df['Monetary'].quantile(0.999)]
    
    scatter = sns.scatterplot(
        data=df_viz, 
        x='Recency', 
        y='Monetary', 
        hue='Cluster', 
        palette=colores,
        alpha=0.6,
        s=50
    )
    plt.title('Segmentación: Recencia vs Valor Monetario', fontsize=15)
    plt.xlabel('Días desde última compra (Recencia)', fontsize=12)
    plt.ylabel('Monto Total Compras (Sin IVA)', fontsize=12)
    plt.legend(title='Cluster')
    
    plt.savefig(os.path.join(ruta_img, "scatter_rfm.png"), dpi=300, bbox_inches='tight')
    plt.close()

    # 3. Preferencia de Canal
    print("Graficando Preferencia de Canal...")
    # Melt para graficar
    canales = [col for col in df.columns if 'Share_Channel_' in col]
    canales_cortos = [c.replace('Share_Channel_', '') for c in canales]
    
    # Agrupar por Cluster y Media
    medias_canal = df.groupby('Cluster')[canales].mean()
    medias_canal.columns = canales_cortos
    
    medias_canal.plot(kind='bar', stacked=True, figsize=(10, 6), colormap='viridis')
    plt.title('Preferencia de Canal por Cluster', fontsize=15)
    plt.xlabel('Cluster', fontsize=12)
    plt.ylabel('Proporción de Transacciones', fontsize=12)
    plt.legend(title='Canal', bbox_to_anchor=(1.05, 1), loc='upper left')
    
    plt.savefig(os.path.join(ruta_img, "channel_preference.png"), dpi=300, bbox_inches='tight')
    plt.close()
    
    print("Visualizaciones guardadas en images/")

if __name__ == "__main__":
    try:
        crear_visualizaciones()
    except Exception as e:
        print(f"Error graficando: {e}")
