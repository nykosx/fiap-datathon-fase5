# Passos Mágicos - Datathon Fase 5

Análise diagnóstica e preditiva do desenvolvimento educacional de crianças e jovens da Associação Passos Mágicos.

## Status Atual (mar/2026)

### Entregas concluídas
- Análise diagnóstica das 11 perguntas em `notebooks/03_analytical_questions.ipynb`.
- Modelagem preditiva em `notebooks/04_predictive_modeling.ipynb`.
- Artefatos gerados:
	- `models/model_risco.joblib`
	- `outputs/model_risco_metadata.json`
	- `outputs/modelagem_leaderboard.csv`
- Base canônica gerada em `data/dados_unificados_canonico.csv`.
- Aplicação Streamlit MVP pronta para scoring em lote em `app/app.py`.

### Pendências para submissão
- Deploy no Streamlit Community Cloud.
- Apresentação final (PPT/PDF).
- Vídeo final (até 5 minutos).

## Estrutura do Projeto

```
fiap-datathon-fase5/
├── app/                            # Aplicação Streamlit
├── data/                           # Dados processados
├── docs/                           # Documentação e auditoria
├── models/                         # Artefatos do modelo
├── notebooks/                      # Pipeline analítico e preditivo
│   ├── 01_data_exploration.ipynb
│   ├── 02_data_cleaning.ipynb
│   ├── 03_analytical_questions.ipynb
│   └── 04_predictive_modeling.ipynb
├── outputs/                        # Metadados e leaderboard
├── src/                            # Utilitários e configuração
└── requirements.txt
```

## Principais Resultados (versão oficial)

### Destaques da análise diagnóstica
- Q1 (IAN): 54,2% moderadamente deficiente e 1,5% severamente deficiente.
- Q3 (IEG-IDA-IPV): correlações fortes (~0,54 a 0,56).
- Q4 (IAA x IDA): gap médio de +1,55 com 65,3% de superestimação.
- Q8 (uplift de INDE): melhor combinação `IDA + IEG` (uplift 1,713).
- Q9 (regra atual de risco): 0,3% em risco alto pelos critérios definidos no notebook.

### Destaques da modelagem
- Alvo: `target_risco = 1` quando `inde_combined <= Q1`.
- Duas trilhas:
	- `trilha_core_sem_ipp` (2022-2024)
	- `trilha_core_com_ipp` (2023-2024)
- Modelo vencedor: `trilha_core_com_ipp / logistic`.
- Métricas do vencedor:
	- Recall: `0.887`
	- Precision: `0.589`
	- ROC-AUC: `0.935`
	- PR-AUC: `0.813`

## Como Executar

### 1) Instalar dependências

```bash
pip install -r requirements.txt
```

### 2) Executar notebooks

Ordem recomendada:
1. `notebooks/01_data_exploration.ipynb`
2. `notebooks/02_data_cleaning.ipynb`
3. `notebooks/03_analytical_questions.ipynb`
4. `notebooks/04_predictive_modeling.ipynb`

### 3) Executar app de scoring

```bash
streamlit run app/app.py
```

## Notas Metodológicas Importantes

- O campo `IPP` é estruturalmente ausente em 2022.
- Q6 e Q8 reportam explicitamente essa limitação.
- A seleção do modelo prioriza `recall` para reduzir falsos negativos pedagógicos.

## Próximos Passos Recomendados

- Fechar consistência final de números entre notebook, slides e vídeo.
- Publicar deploy do app e incluir URL neste README.
- Executar versão temporal de validação para fortalecer robustez preditiva.

## Autores

Pós-Graduação em Data Analytics - FIAP.

## Licença

Projeto acadêmico para avaliação na POSTECH FIAP.
