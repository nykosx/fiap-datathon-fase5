"""
Funções utilitárias para processamento, scoring e visualização de dados.
"""

import re
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from typing import List, Dict, Tuple, Optional
from .config import COLORS, PLOT_CONFIG


def parse_risk_threshold_from_target(target_definition: str, default: float = 5.0) -> float:
    """Extrai o limiar numérico da definição textual do alvo de risco."""
    if not target_definition:
        return default
    match = re.search(r"<=\s*([0-9]+(?:\.[0-9]+)?)", target_definition)
    if not match:
        return default
    try:
        return float(match.group(1))
    except ValueError:
        return default


def ensure_cols(df: pd.DataFrame, cols: list[str]) -> pd.DataFrame:
    """Garante a existência das colunas esperadas em um DataFrame."""
    out = df.copy()
    for col in cols:
        if col not in out.columns:
            out[col] = np.nan
    return out


_PHASE_MAP = {
    "alfa": "ALFA",
    "0": "ALFA",
    "1": "FASE 1",
    "fase1": "FASE 1",
    "fase 1": "FASE 1",
    "2": "FASE 2",
    "fase2": "FASE 2",
    "fase 2": "FASE 2",
    "3": "FASE 3",
    "fase3": "FASE 3",
    "fase 3": "FASE 3",
    "4": "FASE 4",
    "fase4": "FASE 4",
    "fase 4": "FASE 4",
    "5": "FASE 5",
    "fase5": "FASE 5",
    "fase 5": "FASE 5",
    "6": "FASE 6",
    "fase6": "FASE 6",
    "fase 6": "FASE 6",
    "7": "FASE 7",
    "fase7": "FASE 7",
    "fase 7": "FASE 7",
    "8": "FASE 8",
    "fase8": "FASE 8",
    "fase 8": "FASE 8",
}


def canonicalize_phase(value):
    """Padroniza representações de fase para o formato canônico do projeto."""
    if value is None or (isinstance(value, float) and np.isnan(value)):
        return np.nan
    token = str(value).strip().lower()
    if token in _PHASE_MAP:
        return _PHASE_MAP[token]

    match = re.match(r"^(\d+)", token)
    if match:
        phase_number = int(match.group(1))
        if phase_number == 0:
            return "ALFA"
        if 1 <= phase_number <= 8:
            return f"FASE {phase_number}"
    return np.nan


def prepare_scoring_frame(df: pd.DataFrame, expected_features: list[str]) -> pd.DataFrame:
    """Alinha e limpa o DataFrame de entrada para scoring com o modelo oficial."""
    working = df.copy()

    if "fase_padronizada" in expected_features and "fase_padronizada" not in working.columns:
        if "phase" in working.columns:
            working["fase_padronizada"] = working["phase"].apply(canonicalize_phase)

    scored = ensure_cols(working, expected_features)[expected_features].copy()
    scored = scored.replace({pd.NA: np.nan})

    categorical_features = {
        "year",
        "fase_padronizada",
        "gender",
        "school_institution",
        "achieved_turning_point",
        "indicated_for_intervention",
    }

    for col in scored.columns:
        if col in categorical_features:
            scored[col] = scored[col].replace(["", " ", "nan", "None", "NA", "N/A"], np.nan)
        else:
            scored[col] = pd.to_numeric(scored[col], errors="coerce")

    return scored

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
