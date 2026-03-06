# AGENT HANDOFF — FIAP Datathon Fase 5 (Passos Mágicos)

## 1) Objetivo do projeto
Entregar uma solução completa do Datathon com:
- Análise diagnóstica (11 perguntas de negócio)
- Modelo preditivo de risco de defasagem
- Aplicação Streamlit com deploy
- Storytelling executivo (PPT/PDF) + vídeo final

---

## 2) Estado atual (fonte única para continuidade)
### Concluído
- Estrutura base do repositório pronta (`src`, `data`, `docs`, `notebooks`, `app`, `models`, `outputs`).
- Notebooks concluídos:
  - `notebooks/01_data_exploration.ipynb`
  - `notebooks/02_data_cleaning.ipynb`
  - `notebooks/03_analytical_questions.ipynb`
- Q8 atualizada conforme enunciado novo:
  - foco em combinações (`IDA + IEG + IPS + IPP`) que **elevam** INDE.
- Padronização de idioma avançada para PT-BR em notebooks e módulos principais (`src/config.py`, `src/utils.py`).
- Glossário consolidado no início do notebook `03_analytical_questions.ipynb`.

### Pendente crítico
- `notebooks/04_predictive_modeling.ipynb` (não existe ainda)
- `app/app.py` (não existe ainda)
- `models/model_risco.joblib` (não existe ainda)
- Deploy Streamlit Cloud
- Apresentação final + vídeo

---

## 3) Decisões importantes já tomadas (NÃO quebrar)
1. **Não imputar/extrapolar IPP para 2022 como análise principal**.
   - Justificativa: ausência estrutural (não é missing aleatório), risco alto de contaminação.
2. **Q6 e Q8 com nota metodológica explícita** sobre limitação do IPP em 2022.
3. **Termos técnicos podem permanecer em inglês** quando necessário (ex.: feature engineering).
4. **Comentários e explicações para leitura humana preferencialmente em PT-BR**.
5. **Manter siglas no código** (reprodutibilidade) e **explicá-las no texto** (legibilidade).

---

## 4) Contexto de dados (essencial)
- Base original: `BASE DE DADOS PEDE 2024 - DATATHON.xlsx`
- Sheets: `PEDE2022`, `PEDE2023`, `PEDE2024`
- Dataset unificado atual: `data/dados_unificados.csv` (3030 linhas x 34 colunas)
- IPP:
  - 2022: não existe
  - 2023/2024: existe com faltantes (~7–9%)

Observação: há colunas 100% vazias em alguns anos na base original (artefatos), já tratadas no pipeline de limpeza.

---

## 5) Checklist de consistência antes de qualquer nova mudança
1. Abrir e revisar:
   - `PLANO_PROJETO.md`
   - `AGENT_HANDOFF.md` (este arquivo)
   - `notebooks/03_analytical_questions.ipynb`
2. Validar que Q8 permanece no formato “elevam INDE” (uplift).
3. Confirmar que notas metodológicas de IPP em Q6/Q8 permanecem.
4. Evitar retrabalho de tradução já concluída.

---

## 6) Próxima etapa recomendada (ordem de execução)
### Etapa A — Modelagem preditiva (prioridade máxima)
Criar `notebooks/04_predictive_modeling.ipynb` com:
1. Definição de target de risco (regra clara e justificável)
2. Duas trilhas analíticas:
   - Trilha 1 (todos os anos): sem IPP
   - Trilha 2 (2023/2024): com IPP
3. Split treino/teste e baseline
4. Modelos candidatos (ex.: Logistic Regression, Random Forest, XGBoost/LightGBM)
5. Métricas: Recall, Precision, F1, ROC-AUC, matriz de confusão
6. Salvamento do melhor modelo em `models/model_risco.joblib`

### Etapa B — App Streamlit
Criar `app/app.py` com input de CSV + scoring + ranking de risco.

### Etapa C — Storytelling final
Consolidar resultados e alinhar números entre notebook, slides e vídeo.

---

## 7) Padrões de qualidade e estilo para próximos agentes
- Não alterar lógica já validada sem justificativa explícita.
- Não inventar imputação de campo estruturalmente ausente.
- Em resultados executivos:
  - primeiro uso: sigla + nome completo
  - depois: sigla
- Cada conclusão deve ter suporte em evidência numérica.
- Garantir reprodutibilidade: notebook deve rodar do início ao fim.

---

## 8) Procedimento rápido ao trocar de computador
1. `git pull`
2. Ler `AGENT_HANDOFF.md` + `PLANO_PROJETO.md`
3. Abrir `notebooks/03_analytical_questions.ipynb` e validar estado
4. Seguir diretamente para criação do `04_predictive_modeling.ipynb`

---

## 9) Observações finais
Este arquivo deve ser tratado como **contexto operacional oficial** para reduzir inconsistência entre sessões (casa/trabalho) e entre agentes no VS Code.
