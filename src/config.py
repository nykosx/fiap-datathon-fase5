"""
Arquivo de configuração do projeto Datathon Passos Mágicos.
Configurações centralizadas de caminhos, cores e parâmetros.
"""

from pathlib import Path

# Caminhos do projeto
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
MODELS_DIR = PROJECT_ROOT / "models"
OUTPUTS_DIR = PROJECT_ROOT / "outputs"

# Arquivo de dados
DATA_FILE = PROJECT_ROOT / "BASE DE DADOS PEDE 2024 - DATATHON.xlsx"

# Esquema de cores - tema profissional
COLORS = {
    'primary': '#2c3e50',      # Dark blue-gray (main color)
    'secondary': '#34495e',    # Lighter dark gray
    'accent': '#3498db',       # Blue accent
    'warning': '#e74c3c',      # Red for alerts
    'success': '#27ae60',      # Green for positive
    'neutral': '#95a5a6',      # Gray for neutral
    'background': '#ecf0f1',   # Light gray background
    'text': '#2c3e50'          # Dark text
}

# Configuração de estilo dos gráficos
PLOT_CONFIG = {
    'figure.facecolor': 'white',
    'axes.facecolor': '#f8f9fa',
    'axes.edgecolor': COLORS['primary'],
    'axes.labelcolor': COLORS['text'],
    'text.color': COLORS['text'],
    'xtick.color': COLORS['text'],
    'ytick.color': COLORS['text'],
    'grid.color': '#d5d8dc',
    'grid.alpha': 0.3,
    'font.size': 10,
    'axes.titlesize': 12,
    'axes.labelsize': 10,
    'figure.titlesize': 14
}

# Parâmetros de modelagem
RANDOM_STATE = 42
TEST_SIZE = 0.2
CV_FOLDS = 5

# Colunas de indicadores
INDICATORS = {
    'IAN': 'Adequação do nível',
    'IDA': 'Desempenho acadêmico',
    'IEG': 'Engajamento',
    'IAA': 'Autoavaliação',
    'IPS': 'Aspectos psicossociais',
    'IPP': 'Aspectos psicopedagógicos',
    'IPV': 'Ponto de virada',
    'INDE': 'Índice de desempenho global'
}
