import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

def create_visualizations():
    base_path = r"C:\Users\JORGE\Desktop\Prueba - Studio F\Prueba Tecnica Analista datos BI"
    csv_path = os.path.join(base_path, "output", "Clientes_Segmentados.csv")
    img_path = os.path.join(base_path, "images")
    
    print("Loading data...")
    try:
        df = pd.read_csv(csv_path)
    except FileNotFoundError:
        print("Segmented data not found in output/. Checking root...")
        csv_path = os.path.join(base_path, "Clientes_Segmentados.csv") # Fallback
        df = pd.read_csv(csv_path)

    # Set style
    sns.set(style="whitegrid")

    # 1. Cluster Distribution
    print("Plotting Cluster Distribution...")
    plt.figure(figsize=(10, 6))
    cluster_counts = df['Cluster'].value_counts().sort_index()
    colors = ['#2c3e50', '#e74c3c', '#3498db', '#f1c40f'] # Dark Blue, Red, Blue, Yellow
    
    ax = sns.barplot(x=cluster_counts.index, y=cluster_counts.values, palette=colors)
    plt.title('Distribución de Clientes por Segmento', fontsize=15)
    plt.xlabel('Cluster', fontsize=12)
    plt.ylabel('Cantidad de Clientes', fontsize=12)
    
    # Add labels
    for i, v in enumerate(cluster_counts.values):
        ax.text(i, v + 50, str(v), ha='center', fontweight='bold')
        
    plt.savefig(os.path.join(img_path, "cluster_distribution.png"), dpi=300, bbox_inches='tight')
    plt.close()

    # 2. Scatter Plot: Recency vs Monetary
    print("Plotting Recency vs Monetary...")
    plt.figure(figsize=(10, 6))
    
    # Filter out extreme outlier for visualization (The 400M guy) to keep scale readable
    df_viz = df[df['Monetary'] < df['Monetary'].quantile(0.999)]
    
    scatter = sns.scatterplot(
        data=df_viz, 
        x='Recency', 
        y='Monetary', 
        hue='Cluster', 
        palette=colors,
        alpha=0.6,
        s=50
    )
    plt.title('Segmentación: Recencia vs Valor Monetario', fontsize=15)
    plt.xlabel('Días desde última compra (Recencia)', fontsize=12)
    plt.ylabel('Monto Total Compras (Sin IVA)', fontsize=12)
    plt.legend(title='Cluster')
    
    plt.savefig(os.path.join(img_path, "scatter_rfm.png"), dpi=300, bbox_inches='tight')
    plt.close()

    # 3. Channel Preference
    print("Plotting Channel Preference...")
    # Melt for plotting
    channels = [col for col in df.columns if 'Share_Channel_' in col]
    short_channels = [c.replace('Share_Channel_', '') for c in channels]
    
    # Group by Cluster and Mean
    channel_means = df.groupby('Cluster')[channels].mean()
    channel_means.columns = short_channels
    
    channel_means.plot(kind='bar', stacked=True, figsize=(10, 6), colormap='viridis')
    plt.title('Preferencia de Canal por Cluster', fontsize=15)
    plt.xlabel('Cluster', fontsize=12)
    plt.ylabel('Proporción de Transacciones', fontsize=12)
    plt.legend(title='Canal', bbox_to_anchor=(1.05, 1), loc='upper left')
    
    plt.savefig(os.path.join(img_path, "channel_preference.png"), dpi=300, bbox_inches='tight')
    plt.close()
    
    print("Visualizations saved to images/")

if __name__ == "__main__":
    try:
        create_visualizations()
    except Exception as e:
        print(f"Error plotting: {e}")
