"""
Function to read aruj.txt data and convert to pandas DataFrames
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def read_aruj_data(filepath, dataset=None):
    """
    Reads aruj.txt file and converts to pandas DataFrame
    
    Args:
        filepath (str): Path to the aruj.txt file
        dataset (str, optional): Filter for specific dataset ('d', 'a', 'h', 'v')
                                If None, returns all data
    
    Returns:
        pandas.DataFrame: DataFrame with columns ['dataset', 'x', 'y']
    
    Examples:
        # Get all data
        df = read_aruj_data('aruj.txt')
        
        # Get only dataset 'd'
        df_d = read_aruj_data('aruj.txt', dataset='d')
        
        # Get only dataset 'a'
        df_a = read_aruj_data('aruj.txt', dataset='a')
    """
    # Read the file using pandas - it's space/tab delimited
    df = pd.read_csv(filepath, sep=r'\s+', engine='python')
    
    # If specific dataset requested, filter
    if dataset is not None:
        if dataset not in df['dataset'].unique():
            available = df['dataset'].unique().tolist()
            raise ValueError(f"Dataset '{dataset}' not found. Available: {available}")
        df = df[df['dataset'] == dataset].reset_index(drop=True)
    
    return df


def get_dataset_summary(df):
    """
    Get summary statistics for each dataset
    
    Args:
        df: DataFrame with aruj data
    
    Returns:
        pandas.DataFrame: Summary statistics per dataset
    """
    summary = df.groupby('dataset').agg({
        'x': ['count', 'mean', 'std', 'min', 'max'],
        'y': ['mean', 'std', 'min', 'max']
    }).round(3)
    
    return summary


def plot_datasets(df, save_path=None):
    """
    Create scatter plots for all datasets
    
    Args:
        df: DataFrame with aruj data
        save_path: Optional path to save the figure
    """
    datasets = df['dataset'].unique()
    n_datasets = len(datasets)
    
    # Create color palette
    colors = sns.color_palette("husl", n_datasets)
    
    fig, ax = plt.subplots(figsize=(12, 8))
    
    for idx, dataset in enumerate(sorted(datasets)):
        data = df[df['dataset'] == dataset]
        ax.scatter(data['x'], data['y'], 
                  label=f'Dataset {dataset} (n={len(data)})',
                  alpha=0.6, s=50, color=colors[idx])
    
    ax.set_xlabel('X', fontsize=12, fontweight='bold')
    ax.set_ylabel('Y', fontsize=12, fontweight='bold')
    ax.set_title('Aruj Data - All Datasets', fontsize=14, fontweight='bold')
    ax.legend(loc='best')
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"✅ Plot saved as '{save_path}'")
    
    plt.show()


def plot_datasets_separate(df, save_path=None):
    """
    Create separate scatter plots for each dataset in subplots
    
    Args:
        df: DataFrame with aruj data
        save_path: Optional path to save the figure
    """
    datasets = sorted(df['dataset'].unique())
    n_datasets = len(datasets)
    
    # Determine grid layout
    n_cols = 2
    n_rows = (n_datasets + 1) // 2
    
    fig, axes = plt.subplots(n_rows, n_cols, figsize=(14, 5*n_rows))
    axes = axes.flatten() if n_datasets > 1 else [axes]
    
    colors = sns.color_palette("husl", n_datasets)
    
    for idx, dataset in enumerate(datasets):
        data = df[df['dataset'] == dataset]
        
        axes[idx].scatter(data['x'], data['y'], 
                         alpha=0.6, s=60, color=colors[idx], 
                         edgecolors='black', linewidth=0.5)
        
        axes[idx].set_xlabel('X', fontsize=11, fontweight='bold')
        axes[idx].set_ylabel('Y', fontsize=11, fontweight='bold')
        axes[idx].set_title(f'Dataset {dataset.upper()} (n={len(data)})', 
                           fontsize=12, fontweight='bold')
        axes[idx].grid(True, alpha=0.3, linestyle='--')
        
        # Add statistics
        stats_text = f"μₓ={data['x'].mean():.2f}, μᵧ={data['y'].mean():.2f}"
        axes[idx].text(0.05, 0.95, stats_text, transform=axes[idx].transAxes,
                      fontsize=9, verticalalignment='top',
                      bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    # Hide unused subplots
    for idx in range(n_datasets, len(axes)):
        axes[idx].set_visible(False)
    
    plt.suptitle('Aruj Data - Individual Datasets', fontsize=16, fontweight='bold', y=1.00)
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"✅ Plot saved as '{save_path}'")
    
    plt.show()


# ============================================================================
# DEMO / USAGE EXAMPLES
# ============================================================================

if __name__ == "__main__":
    # File path
    filepath = '/mnt/user-data/uploads/aruj.txt'
    
    print("="*70)
    print("BEISPIEL 1: Alle Daten einlesen")
    print("="*70)
    
    df = read_aruj_data(filepath)
    
    print(f"\n✅ Datei eingelesen!")
    print(f"DataFrame Shape: {df.shape}")
    print(f"\nErste 10 Zeilen:")
    print(df.head(10))
    
    print(f"\nLetzte 10 Zeilen:")
    print(df.tail(10))
    
    print(f"\nDataFrame Info:")
    print(df.info())
    
    print("\n" + "="*70)
    print("BEISPIEL 2: Datasets erkunden")
    print("="*70)
    
    print(f"\nVerfügbare Datasets: {sorted(df['dataset'].unique())}")
    print(f"\nAnzahl Datenpunkte pro Dataset:")
    print(df['dataset'].value_counts().sort_index())
    
    print("\n" + "="*70)
    print("BEISPIEL 3: Statistiken pro Dataset")
    print("="*70)
    
    summary = get_dataset_summary(df)
    print("\n", summary)
    
    print("\n" + "="*70)
    print("BEISPIEL 4: Einzelnes Dataset laden")
    print("="*70)
    
    df_d = read_aruj_data(filepath, dataset='d')
    print(f"\n✅ Dataset 'd' geladen!")
    print(f"Shape: {df_d.shape}")
    print(f"\nErste 5 Zeilen:")
    print(df_d.head())
    
    df_a = read_aruj_data(filepath, dataset='a')
    print(f"\n✅ Dataset 'a' geladen!")
    print(f"Shape: {df_a.shape}")
    
    print("\n" + "="*70)
    print("BEISPIEL 5: DataFrame Operationen")
    print("="*70)
    
    print("\n🔍 Deskriptive Statistik für Dataset 'd':")
    print(df_d.describe().round(3))
    
    print("\n📊 Korrelation zwischen X und Y für Dataset 'd':")
    print(f"r = {df_d['x'].corr(df_d['y']):.4f}")
    
    print("\n✨ Filtern: Dataset 'd' Punkte wo x > 60")
    filtered = df_d[df_d['x'] > 60]
    print(f"Gefunden: {len(filtered)} Punkte")
    print(filtered.head())
    
    print("\n" + "="*70)
    print("BEISPIEL 6: Visualisierungen erstellen")
    print("="*70)
    
    print("\n🎨 Erstelle kombiniertes Scatter Plot...")
    plot_datasets(df, save_path='aruj_combined_plot.png')
    
    print("\n🎨 Erstelle separate Scatter Plots...")
    plot_datasets_separate(df, save_path='aruj_separate_plots.png')
    
    print("\n" + "="*70)
    print("✅ Alle Beispiele erfolgreich ausgeführt!")
    print("="*70)
