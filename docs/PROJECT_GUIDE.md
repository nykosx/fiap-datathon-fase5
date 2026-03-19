# Guia do Projeto

## Objetivo

Entregar uma solucao completa do Datathon com:
- pipeline de dados reprodutivel;
- analise diagnostica das 11 perguntas de negocio;
- modelo preditivo de risco de defasagem no ano seguinte;
- aplicacao Streamlit para apoio operacional;
- materiais finais de storytelling para PPT/PDF e video.

## Estado Atual

### Concluido
- Exploracao e consolidacao dos dados em notebooks/01_data_exploration.ipynb e notebooks/02_data_cleaning.ipynb.
- Analise diagnostica em notebooks/03_analytical_questions.ipynb.
- Modelagem preditiva temporal em notebooks/04_predictive_modeling.ipynb.
- App Streamlit funcional em app/app.py.
- Artefatos gerados:
  - models/model_risco.joblib
  - outputs/model_risco_metadata.json
  - outputs/modelagem_leaderboard.csv
  - outputs/predicoes_modelo_vencedor.csv
  - outputs/modelagem_tradeoff_thresholds.csv
  - outputs/modelagem_tradeoff_capacidade.csv

### Em aberto
- Apresentacao final (PPT/PDF).
- Video final (ate 5 minutos).

Guias de apoio para acelerar essa etapa:
- docs/APRESENTACAO_GUIA.md
- docs/VIDEO_GUIA.md

## Fonte de Verdade

### Base oficial
- data/dados_unificados.csv

### Numeros oficiais para materiais finais
- notebooks/03_analytical_questions.ipynb
- notebooks/04_predictive_modeling.ipynb
- outputs/modelagem_leaderboard.csv
- outputs/model_risco_metadata.json
- outputs/predicoes_modelo_vencedor.csv
- outputs/modelagem_tradeoff_thresholds.csv
- outputs/modelagem_tradeoff_capacidade.csv

Observacao de governanca:
- o Q9 no notebook analitico funciona como baseline de triagem e leitura executiva;
- os numeros oficiais de modelagem para banca e app devem vir do nb04 e dos arquivos em outputs/.
- Q5 e Q7 medem associacao contemporanea, nao temporal; a critica de "antecedem" e "ao longo do tempo" esta documentada nas celulas de cada questao.
- Q8 cobre apenas os anos com IPP disponivel (IPP ausente em 2022); ver nota na celula de Q8.
- Q9 usa alvo de estado atual (ian < 10); previsao do ciclo seguinte esta no nb04. Ver nota na celula de Q9.

## Decisoes Metodologicas que Devem Ser Preservadas

1. A avaliacao do modelo e temporal:
   - treino: ano base 2022 para prever 2023;
   - teste: ano base 2023 para prever 2024.
2. O alvo e target_risco_next, definido por `ian_next_year <= 5` no ano seguinte.
3. O criterio de selecao do modelo prioriza cobertura de risco detectado (recall), com roc_auc como desempate.
4. Trilha unica de modelagem sem IPP. O IPP foi introduzido no PEDE2023 e e estruturalmente ausente na base de treino (2022) — nao e um dado faltante aleatorio, e uma coluna que ainda nao existia. Imputar IPP em 2022 constituiria leakage conceitual. Analise adicional (Q6) mostra correlacao do IPP com risco de apenas -0,12, indicando que o indicador mede engajamento com o programa, nao defasagem academica diretamente. Esse achado deve constar na apresentacao.

## Continuacao Recomendada

1. Validar o app localmente com CSV de exemplo e base oficial 2024.
2. Fechar PPT/PDF com numeros identicos aos outputs.
3. Gravar o video final seguindo o roteiro-base em docs/STORYTELLING_BASE.md.
4. Registrar a URL oficial do app no README e no roteiro final.

## Checklist Final

- [x] Pipeline de dados consolidado
- [x] 11 perguntas respondidas
- [x] Modelo treinado e salvo
- [x] App funcional
- [x] Tabelas de trade-off geradas
- [x] Deploy publicado
- [ ] PPT/PDF final
- [ ] Video final

## Deploy Publicado

- URL oficial: https://fiap-tech-challenge-fase5-prediction.streamlit.app/
