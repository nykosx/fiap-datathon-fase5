# Passos Magicos - Datathon Fase 5

Analise diagnostica e preditiva do desenvolvimento educacional de criancas e jovens da Associacao Passos Magicos.

## Visao Geral

O projeto entrega:
- analise diagnostica das 11 perguntas de negocio;
- modelo preditivo temporal de risco de defasagem no ano seguinte;
- aplicacao Streamlit para avaliacao individual e scoring em lote;
- base documental consolidada para execucao, metodologia e storytelling.

## Documentos Oficiais

Use estes arquivos como referencia principal:
- docs/PROJECT_GUIDE.md: status, continuidade, entregaveis e fonte de verdade operacional;
- docs/methodology.md: desenho metodologico e criterios tecnicos;
- docs/STORYTELLING_BASE.md: narrativa completa para PPT/PDF e video.

## Estrutura do Projeto

- app/: aplicacao Streamlit
- data/: dados processados e dados brutos em data/raw/
- docs/: documentacao consolidada
- models/: artefatos do modelo
- notebooks/: pipeline analitico e preditivo
- outputs/: metricas, previsoes e tabelas de apoio
- src/: utilitarios e configuracao

## Base Oficial

Para analise e modelagem, use apenas:
- data/dados_unificados.csv

Observacao:
- O campo IPP e estruturalmente ausente em 2022.

## Artefatos Oficiais

Arquivos oficiais para leitura de resultados e materiais finais:
- outputs/modelagem_leaderboard.csv
- outputs/model_risco_metadata.json
- outputs/predicoes_modelo_vencedor.csv
- outputs/modelagem_tradeoff_thresholds.csv
- outputs/modelagem_tradeoff_capacidade.csv

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
