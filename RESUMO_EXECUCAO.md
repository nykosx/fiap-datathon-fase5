# Datathon Passos Mágicos - Resumo de Execução

**Data de atualização:** 11 de março de 2026  
**Status geral:** Em fase final de entrega  
**Foco atual:** Consistência documental, deploy e materiais finais

---

## 1) Status Real do Projeto

### Concluído
- Exploração de dados: `notebooks/01_data_exploration.ipynb`
- Limpeza e unificação: `notebooks/02_data_cleaning.ipynb`
- Análise diagnóstica (Q1-Q11): `notebooks/03_analytical_questions.ipynb`
- Modelagem preditiva: `notebooks/04_predictive_modeling.ipynb`
- Artefatos gerados:
  - `models/model_risco.joblib`
  - `outputs/model_risco_metadata.json`
  - `outputs/modelagem_leaderboard.csv`
- Aplicação de scoring (MVP): `app/app.py`

### Em aberto
- Deploy no Streamlit Community Cloud
- Apresentação final (PPT/PDF)
- Vídeo final (até 5 minutos)

---

## 2) Dados e Base Analítica

- Dataset unificado: `data/dados_unificados.csv`
- Dimensão da base unificada: **3.030 linhas × 34 colunas**
- Período analisado: **2022, 2023 e 2024**
- Observação relevante: `IPP` é estruturalmente ausente em 2022

---

## 3) Principais Resultados (Notebook Analítico)

Resultados extraídos das saídas executadas em `notebooks/03_analytical_questions.ipynb`.

- **Q1 (IAN):** 54,2% moderadamente deficiente; 1,5% severamente deficiente
- **Q2 (IDA):** médias por ano = 6,09 (2022), 6,66 (2023), 6,35 (2024)
- **Q3 (IEG-IDA-IPV):** correlações fortes (~0,54 a 0,56)
- **Q4 (IAA vs IDA):** gap médio = +1,55; 65,3% superestimam autoavaliação
- **Q5 (IPS):** risco alto = 15,6%; correlação IPS-IDA = 0,022
- **Q6 (IAN-IPP):** correlação = 0,123 (fraca), com base majoritariamente 2023-2024
- **Q7 (drivers de IPV):** IEG (0,558) e IDA (0,557) como maiores correlações
- **Q8 (uplift de INDE):** melhor combinação = `IDA + IEG` (uplift 1,713)
- **Q9 (regra de risco no notebook):** risco alto = 0,3% (10 estudantes)
- **Q11:** matemática 6,17; português 6,43; inglês 6,29

---

## 4) Principais Resultados (Notebook Preditivo)

Resultados extraídos de `notebooks/04_predictive_modeling.ipynb` e `outputs/modelagem_leaderboard.csv`.

- Definição do alvo: `target_risco = 1` quando `inde_combined <= Q1`
- `Q1 inde_combined`: **6,7066**
- Taxa de risco do alvo: **20,99%**
- Trilhas de treino:
  - `trilha1_sem_ipp` (2022-2024)
  - `trilha2_com_ipp` (2023-2024)
- Modelo vencedor: **`trilha2_com_ipp / logistic`**

Métricas do vencedor:
- Recall: **0,9014**
- Precision: **0,5926**
- F1: **0,7151**
- ROC-AUC: **0,9312**
- PR-AUC: **0,7923**

---

## 5) Alertas Metodológicos Registrados

- Warning no treino da trilha com IPP para colunas sem valores observados em certos recortes (`SimpleImputer`), exigindo controle explícito de features por trilha.
- A seleção por recall está coerente com o objetivo pedagógico (reduzir falso negativo), mas aumenta falso positivo.
- Para fortalecer defesa em banca, recomenda-se validação temporal adicional (por ano/coorte).

---

## 6) Próximas Ações Objetivas

1. Publicar app no Streamlit Community Cloud e registrar URL no README.
2. Consolidar storytelling final com os números oficiais acima.
3. Produzir PPT/PDF e vídeo final com os mesmos valores dos notebooks/outputs.
4. Opcional recomendado: rodar versão temporal do modelo e incluir análise comparativa em anexo.

---

## 7) Fonte Única de Verdade

Para evitar divergência de métricas:
- `notebooks/03_analytical_questions.ipynb`
- `notebooks/04_predictive_modeling.ipynb`
- `outputs/modelagem_leaderboard.csv`
- `outputs/model_risco_metadata.json`
