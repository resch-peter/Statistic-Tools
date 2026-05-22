"""
Script to read and visualize Frank's Numbers data sets
Creates scatter plots for all 5 data sets
"""

import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

def read_data_from_file(filepath):
    """
    Reads the data file and extracts all data sets
    
    Args:
        filepath: Path to the data file
    
    Returns:
        Dictionary with data set numbers as keys and (x, y) tuples as values
    """
    datasets = {}
    current_dataset = None
    x_data = []
    y_data = []
    
    with open(filepath, 'r') as f:
        for line in f:
            line = line.strip()
            
            # Skip empty lines
            if not line:
                continue
            
            # Check if this is a dataset header
            if line.startswith('Data set'):
                # Save previous dataset if exists
                if current_dataset is not None and x_data:
                    datasets[current_dataset] = (np.array(x_data), np.array(y_data))
                
                # Extract dataset number
                current_dataset = int(line.split()[-1])
                x_data = []
                y_data = []
            
            # Skip title line
            elif line.startswith('Multiple'):
                continue
            
            # Parse data line
            else:
                try:
                    parts = line.split()
                    if len(parts) == 2:
                        x_data.append(float(parts[0]))
                        y_data.append(float(parts[1]))
                except ValueError:
                    # Skip lines that can't be parsed
                    continue
        
        # Don't forget the last dataset
        if current_dataset is not None and x_data:
            datasets[current_dataset] = (np.array(x_data), np.array(y_data))
    
    return datasets


def calculate_statistics(x, y):
    """Calculate basic statistics for a dataset"""
    return {
        'mean_x': np.mean(x),
        'mean_y': np.mean(y),
        'std_x': np.std(x, ddof=1),
        'std_y': np.std(y, ddof=1),
        'correlation': np.corrcoef(x, y)[0, 1],
        'n_points': len(x)
    }


def plot_single_dataset(ax, x, y, dataset_num, stats):
    """Plot a single dataset on given axes"""
    # Scatter plot
    ax.scatter(x, y, alpha=0.7, s=100, edgecolors='black', linewidth=1.5)
    
    # Linear regression line
    coeffs = np.polyfit(x, y, 1)
    poly = np.poly1d(coeffs)
    x_line = np.linspace(x.min(), x.max(), 100)
    ax.plot(x_line, poly(x_line), 'r--', alpha=0.8, linewidth=2, label=f'y = {coeffs[0]:.2f}x + {coeffs[1]:.2f}')
    
    # Formatting
    ax.set_xlabel('X', fontsize=11, fontweight='bold')
    ax.set_ylabel('Y', fontsize=11, fontweight='bold')
    ax.set_title(f'Data Set {dataset_num}', fontsize=13, fontweight='bold', pad=10)
    ax.grid(True, alpha=0.3, linestyle='--')
    ax.legend(fontsize=9)
    
    # Add statistics as text
    stats_text = f"n={stats['n_points']}\n"
    stats_text += f"r={stats['correlation']:.3f}\n"
    stats_text += f"μₓ={stats['mean_x']:.2f}, μᵧ={stats['mean_y']:.2f}"
    
    ax.text(0.05, 0.95, stats_text, transform=ax.transAxes,
            fontsize=9, verticalalignment='top',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))


def create_visualization(datasets, output_file='scatter_plots.png'):
    """
    Create scatter plots for all datasets
    
    Args:
        datasets: Dictionary of datasets
        output_file: Name of output file
    """
    # Create figure with subplots
    n_datasets = len(datasets)
    
    if n_datasets <= 4:
        fig, axes = plt.subplots(2, 2, figsize=(14, 12))
        axes = axes.flatten()
    else:
        fig, axes = plt.subplots(2, 3, figsize=(18, 12))
        axes = axes.flatten()
    
    fig.suptitle('Frank\'s Numbers - Scatter Plot Analysis', 
                 fontsize=16, fontweight='bold', y=0.995)
    
    # Plot each dataset
    for idx, (dataset_num, (x, y)) in enumerate(sorted(datasets.items())):
        if idx < len(axes):
            stats = calculate_statistics(x, y)
            plot_single_dataset(axes[idx], x, y, dataset_num, stats)
            
            # Print statistics to console
            print(f"\n{'='*50}")
            print(f"Data Set {dataset_num} Statistics:")
            print(f"{'='*50}")
            print(f"Number of points: {stats['n_points']}")
            print(f"Mean X: {stats['mean_x']:.4f}")
            print(f"Mean Y: {stats['mean_y']:.4f}")
            print(f"Std Dev X: {stats['std_x']:.4f}")
            print(f"Std Dev Y: {stats['std_y']:.4f}")
            print(f"Correlation: {stats['correlation']:.4f}")
    
    # Hide unused subplots
    for idx in range(n_datasets, len(axes)):
        axes[idx].set_visible(False)
    
    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"\n✅ Visualization saved as '{output_file}'")
    plt.show()


def main():
    """Main function"""
    # Path to data file
    data_file = 'FranksNumbers.txt'
    
    print("📊 Reading Frank's Numbers data...")
    print(f"From file: {data_file}\n")
    
    # Read data
    datasets = read_data_from_file(data_file)
    
    print(f"✅ Successfully loaded {len(datasets)} data sets!")
    
    # Create visualization
    print("\n🎨 Creating scatter plots...")
    create_visualization(datasets, output_file='franks_scatter_plots.png')
    
    print("\n" + "="*50)
    print("✨ Analysis complete!")
    print("="*50)


if __name__ == "__main__":
    main()
