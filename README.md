# Passos Magicos - Datathon Fase 5

Analise diagnostica e preditiva do desenvolvimento educacional de criancas e jovens da Associacao Passos Magicos.

## Status Atual (mar/2026)

### Entregas concluidas
- Analise diagnostica das 11 perguntas em notebooks/03_analytical_questions.ipynb.
- Modelagem preditiva em notebooks/04_predictive_modeling.ipynb.
- Metodologia preditiva temporal aplicada (ano base t para risco no ano t+1).
- Artefatos gerados:
  - models/model_risco.joblib
  - outputs/model_risco_metadata.json
  - outputs/modelagem_leaderboard.csv
  - outputs/predicoes_modelo_vencedor.csv
- Base oficial padronizada gerada em data/dados_unificados.csv.
- Aplicacao Streamlit MVP pronta para scoring em lote em app/app.py.

### Pendencias para submissao
- Deploy no Streamlit Community Cloud.
- Apresentacao final (PPT/PDF).
- Video final (ate 5 minutos).

## Estrutura do Projeto

- app/: aplicacao Streamlit
- data/: dados processados e dados brutos em data/raw/
- docs/: documentacao e auditoria
- models/: artefatos do modelo
- notebooks/: pipeline analitico e preditivo
- outputs/: metadados e leaderboard
- src/: utilitarios e configuracao

## Fontes de Dados

Dados brutos (entrada do pipeline):
- data/raw/BASE DE DADOS PEDE 2024 - DATATHON.xlsx

Documentos de referencia da pos-graduacao:
- docs/fonte_datathon/Dicionario Dados Datathon.pdf
- docs/fonte_datathon/POSTECH - DTAT - Datathon - Fase 5.pdf

## Base Oficial

Para analise e modelagem, use apenas:
- data/dados_unificados.csv

Observacao:
- O campo IPP e estruturalmente ausente em 2022.

## Como Executar

1. Instalar dependencias

```bash
pip install -r requirements.txt
```

2. Executar notebooks na ordem:
- notebooks/01_data_exploration.ipynb
- notebooks/02_data_cleaning.ipynb
- notebooks/03_analytical_questions.ipynb
- notebooks/04_predictive_modeling.ipynb

3. Executar app

```bash
streamlit run app/app.py
```

## Licenca

Projeto academico para avaliacao na POSTECH FIAP.
