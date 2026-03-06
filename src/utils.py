"""
Funções utilitárias para processamento e visualização de dados.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from typing import List, Dict, Tuple, Optional
from .config import COLORS, PLOT_CONFIG

def setup_plot_style():
    """Configura matplotlib e seaborn com o estilo visual do projeto."""
    plt.rcParams.update(PLOT_CONFIG)
    sns.set_palette([COLORS['primary'], COLORS['accent'], COLORS['secondary'], 
                     COLORS['success'], COLORS['warning'], COLORS['neutral']])

def load_data(file_path: str) -> Dict[str, pd.DataFrame]:
    """
    Carrega dados do Excel com múltiplos sheets (um por ano).
    
    Parâmetros:
    -----------
    file_path : str
        Caminho para o arquivo Excel
        
    Retorna:
    --------
    dict : Dicionário com ano como chave e DataFrame como valor
    """
    excel_file = pd.ExcelFile(file_path)
    data = {}
    
    for sheet in excel_file.sheet_names:
        df = pd.read_excel(excel_file, sheet_name=sheet)
        data[sheet] = df
        
    return data

def get_missing_summary(df: pd.DataFrame) -> pd.DataFrame:
    """
    Gera um resumo de valores faltantes.
    
    Parâmetros:
    -----------
    df : DataFrame
        Dados de entrada
        
    Retorna:
    --------
    DataFrame : Resumo com contagem e percentual de valores faltantes
    """
    missing = pd.DataFrame({
        'Missing_Count': df.isnull().sum(),
        'Missing_Pct': (df.isnull().sum() / len(df) * 100).round(2)
    })
    
    return missing[missing['Missing_Count'] > 0].sort_values('Missing_Count', ascending=False)

def plot_missing_heatmap(df: pd.DataFrame, title: str = "Missing Values Heatmap"):
    """
    Visualiza o padrão de valores faltantes no DataFrame.
    
    Parâmetros:
    -----------
    df : DataFrame
        Dados de entrada
    title : str
        Título do gráfico
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
    Gera estatísticas descritivas para colunas numéricas.
    
    Parâmetros:
    -----------
    df : DataFrame
        Dados de entrada
        
    Retorna:
    --------
    DataFrame : Resumo estatístico básico
    """
    stats = df.describe().T
    stats['dtype'] = df.dtypes
    stats['missing'] = df.isnull().sum()
    stats['missing_pct'] = (df.isnull().sum() / len(df) * 100).round(2)
    
    return stats

def safe_numeric_convert(series: pd.Series) -> pd.Series:
    """
    Converte uma série para numérico com segurança, tratando erros.
    
    Parâmetros:
    -----------
    series : Series
        Série de entrada
        
    Retorna:
    --------
    Series : Série convertida para numérico
    """
    return pd.to_numeric(series, errors='coerce')
