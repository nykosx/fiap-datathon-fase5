"""
Utility functions for data processing and visualization.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from typing import List, Dict, Tuple, Optional
from .config import COLORS, PLOT_CONFIG

def setup_plot_style():
    """Configure matplotlib and seaborn with project style."""
    plt.rcParams.update(PLOT_CONFIG)
    sns.set_palette([COLORS['primary'], COLORS['accent'], COLORS['secondary'], 
                     COLORS['success'], COLORS['warning'], COLORS['neutral']])

def load_data(file_path: str) -> Dict[str, pd.DataFrame]:
    """
    Load Excel data with multiple sheets (one per year).
    
    Parameters:
    -----------
    file_path : str
        Path to the Excel file
        
    Returns:
    --------
    dict : Dictionary with year as key and DataFrame as value
    """
    excel_file = pd.ExcelFile(file_path)
    data = {}
    
    for sheet in excel_file.sheet_names:
        df = pd.read_excel(excel_file, sheet_name=sheet)
        data[sheet] = df
        
    return data

def get_missing_summary(df: pd.DataFrame) -> pd.DataFrame:
    """
    Generate summary of missing values.
    
    Parameters:
    -----------
    df : DataFrame
        Input data
        
    Returns:
    --------
    DataFrame : Summary with count and percentage of missing values
    """
    missing = pd.DataFrame({
        'Missing_Count': df.isnull().sum(),
        'Missing_Pct': (df.isnull().sum() / len(df) * 100).round(2)
    })
    
    return missing[missing['Missing_Count'] > 0].sort_values('Missing_Count', ascending=False)

def plot_missing_heatmap(df: pd.DataFrame, title: str = "Missing Values Heatmap"):
    """
    Visualize missing values pattern in DataFrame.
    
    Parameters:
    -----------
    df : DataFrame
        Input data
    title : str
        Plot title
    """
    fig, ax = plt.subplots(figsize=(12, 6))
    
    missing_data = df.isnull()
    sns.heatmap(missing_data, 
                yticklabels=False, 
                cbar=True,
                cmap=['white', COLORS['warning']],
                ax=ax)
    
    ax.set_title(title, fontsize=14, fontweight='bold', color=COLORS['text'])
    plt.tight_layout()
    return fig

def get_basic_stats(df: pd.DataFrame) -> pd.DataFrame:
    """
    Generate descriptive statistics for numeric columns.
    
    Parameters:
    -----------
    df : DataFrame
        Input data
        
    Returns:
    --------
    DataFrame : Basic statistical summary
    """
    stats = df.describe().T
    stats['dtype'] = df.dtypes
    stats['missing'] = df.isnull().sum()
    stats['missing_pct'] = (df.isnull().sum() / len(df) * 100).round(2)
    
    return stats

def safe_numeric_convert(series: pd.Series) -> pd.Series:
    """
    Safely convert a series to numeric, handling errors.
    
    Parameters:
    -----------
    series : Series
        Input series
        
    Returns:
    --------
    Series : Converted numeric series
    """
    return pd.to_numeric(series, errors='coerce')
