"""
Function to read Frank's Numbers data and convert to pandas DataFrames
"""

import pandas as pd
import re


def read_franks_data_to_dataframe(filepath, dataset_number=None):
    """
    Reads Frank's Numbers file and converts to pandas DataFrame(s)
    
    Args:
        filepath (str): Path to the data file
        dataset_number (int, optional): Specific dataset to read (1-5). 

        
                                       If None, returns all datasets.
    
    Returns:
        If dataset_number is specified:
            pandas.DataFrame: Single DataFrame with columns ['X', 'Y']
        
        If dataset_number is None:
            dict: Dictionary with dataset numbers as keys and DataFrames as values
            
    Examples:
        # Get all datasets
        all_data = read_franks_data_to_dataframe('FranksNumbers.txt')
        df1 = all_data[1]  # Access dataset 1
        
        # Get only dataset 3
        df3 = read_franks_data_to_dataframe('FranksNumbers.txt', dataset_number=3)
    """
    datasets = {}
    current_dataset = None
    data_rows = []
    
    with open(filepath, 'r') as f:
        for line in f:
            line = line.strip()
            
            # Skip empty lines
            if not line:
                continue
            
            # Check if this is a dataset header
            if line.startswith('Data set'):
                # Save previous dataset if exists
                if current_dataset is not None and data_rows:
                    df = pd.DataFrame(data_rows, columns=['X', 'Y'])
                    datasets[current_dataset] = df
                
                # Extract dataset number
                current_dataset = int(line.split()[-1])
                data_rows = []
            
            # Skip title line
            elif line.startswith('Multiple'):
                continue
            
            # Parse data line
            else:
                try:
                    parts = line.split()
                    if len(parts) == 2:
                        x_val = float(parts[0])
                        y_val = float(parts[1])
                        data_rows.append({'X': x_val, 'Y': y_val})
                except ValueError:
                    # Skip lines that can't be parsed
                    continue
        
        # Don't forget the last dataset
        if current_dataset is not None and data_rows:
            df = pd.DataFrame(data_rows, columns=['X', 'Y'])
            datasets[current_dataset] = df
    
    # Return based on what was requested
    if dataset_number is not None:
        if dataset_number in datasets:
            return datasets[dataset_number]
        else:
            raise ValueError(f"Dataset {dataset_number} not found. Available datasets: {list(datasets.keys())}")
    else:
        return datasets


def read_franks_data_combined(filepath):
    """
    Reads Frank's Numbers file and combines all datasets into one DataFrame
    with a 'Dataset' column to identify the source
    
    Args:
        filepath (str): Path to the data file
    
    Returns:
        pandas.DataFrame: Combined DataFrame with columns ['Dataset', 'X', 'Y']
    
    Example:
        df_combined = read_franks_data_combined('FranksNumbers.txt')
        # Filter to specific dataset
        df1_only = df_combined[df_combined['Dataset'] == 1]
    """
    all_datasets = read_franks_data_to_dataframe(filepath)
    
    # Add dataset identifier to each dataframe
    combined_data = []
    for dataset_num, df in all_datasets.items():
        df_copy = df.copy()
        df_copy.insert(0, 'Dataset', dataset_num)
        combined_data.append(df_copy)
    
    # Combine all datasets
    df_combined = pd.concat(combined_data, ignore_index=True)
    
    return df_combined


# ============================================================================
# DEMO / USAGE EXAMPLES
# ============================================================================

if __name__ == "__main__":
    # File path
    filepath = 'FranksNumbers.txt'

    
    print("="*70)
    print("BEISPIEL 1: Alle Datensätze einlesen")
    print("="*70)
    
    # Get all datasets as dictionary
    all_data = read_franks_data_to_dataframe(filepath)
    
    print(f"\n✅ {len(all_data)} Datensätze eingelesen!\n")
    
    for dataset_num, df in all_data.items():
        print(f"📊 Dataset {dataset_num}:")
        print(f"   Shape: {df.shape} (Zeilen, Spalten)")
        print(f"   Vorschau:")
        print(df.head(3).to_string(index=False))
        print()
    
    print("\n" + "="*70)
    print("BEISPIEL 2: Nur Dataset 3 einlesen")
    print("="*70)
    
    df3 = read_franks_data_to_dataframe(filepath, dataset_number=3)
    print(f"\n✅ Dataset 3 geladen!")
    print(f"Shape: {df3.shape}\n")
    print(df3)
    
    print("\n" + "="*70)
    print("BEISPIEL 3: Alle Datensätze kombiniert")
    print("="*70)
    
    df_combined = read_franks_data_combined(filepath)
    print(f"\n✅ Kombinierter DataFrame erstellt!")
    print(f"Shape: {df_combined.shape}\n")
    print("Erste 10 Zeilen:")
    print(df_combined.head(10))
    
    print("\n📈 Statistiken pro Dataset:")
    print(df_combined.groupby('Dataset')[['X', 'Y']].describe().round(3))
    
    print("\n" + "="*70)
    print("BEISPIEL 4: DataFrame-Operationen")
    print("="*70)
    
    # Get dataset 1
    df1 = all_data[1]
    
    print("\n🔍 Dataset 1 - Deskriptive Statistik:")
    print(df1.describe().round(3))
    
    print("\n📊 Korrelation zwischen X und Y:")
    print(f"r = {df1['X'].corr(df1['Y']):.4f}")
    
    print("\n✨ Filtern: Alle Punkte wo X > 10")
    filtered = df1[df1['X'] > 10]
    print(filtered)
    
    print("\n" + "="*70)
    print("✅ Alle Beispiele erfolgreich ausgeführt!")
    print("="*70)
