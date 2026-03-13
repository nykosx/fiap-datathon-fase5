# Datathon Passos Magicos - Resumo de Execucao

Data de atualizacao: 13 de marco de 2026
Status geral: em fase final de entrega

## 1) Status do Projeto

### Concluido
- Exploracao de dados: notebooks/01_data_exploration.ipynb
- Limpeza e padronizacao: notebooks/02_data_cleaning.ipynb
- Analise diagnostica (Q1-Q11): notebooks/03_analytical_questions.ipynb
- Modelagem preditiva: notebooks/04_predictive_modeling.ipynb
- App de scoring (MVP): app/app.py
- Artefatos:
  - models/model_risco.joblib
  - outputs/model_risco_metadata.json
  - outputs/modelagem_leaderboard.csv

### Em aberto
- Deploy no Streamlit Community Cloud
- Apresentacao final (PPT/PDF)
- Video final (ate 5 minutos)

## 2) Base Analitica Oficial

- Dataset oficial unico: data/dados_unificados.csv
- Periodo: 2022, 2023 e 2024
- Observacao: IPP e estruturalmente ausente em 2022

## 3) Ajuste de Governanca de Dados

- Foi removida a ambiguidade entre arquivos unificados.
- A regra oficial agora e manter apenas data/dados_unificados.csv como base de consumo.
- Notebooks de consumo (03 e 04) mantem fallback para nomes legados apenas por compatibilidade de transicao.

## 4) Fonte de Verdade para Numeros

- notebooks/03_analytical_questions.ipynb
- notebooks/04_predictive_modeling.ipynb
- outputs/modelagem_leaderboard.csv
- outputs/model_risco_metadata.json

## 5) Proximos Passos Objetivos

1. Reexecutar notebooks 02, 03 e 04 para consolidar a base unica e outputs finais.
2. Publicar deploy do app e registrar URL no README.
3. Fechar consistencia final entre notebooks, slides e video.
