# Plano do Projeto - Datathon Passos Mágicos (Fase 5)

## Objetivo
Conduzir a entrega completa do Datathon com análise diagnóstica, modelo preditivo de risco de defasagem, aplicação Streamlit e storytelling executivo.

## Entregáveis Obrigatórios
- Link do GitHub com códigos de limpeza e análise
- Apresentação de storytelling (PPT ou PDF)
- Notebook Python com modelo preditivo (feature engineering, treino/teste, modelagem e avaliação)
- Aplicação Streamlit com deploy no Community Cloud
- Vídeo de apresentação com até 5 minutos

---

## Status Consolidado

### Concluído
- Estrutura base do projeto (`src`, `data`, `docs`, `notebooks`)
- Exploração de dados (`01_data_exploration.ipynb`)
- Limpeza e unificação (`02_data_cleaning.ipynb`)
- Análise das 11 perguntas (`03_analytical_questions.ipynb`)
- Ajuste da Q8 para o novo enunciado: combinações (IDA + IEG + IPS + IPP) que elevam o INDE

### Em aberto
- Notebook de modelagem preditiva (`notebooks/04_predictive_modeling.ipynb`)
- Modelo treinado (`models/model_risco.joblib`)
- App Streamlit funcional (`app/app.py`)
- Deploy público no Streamlit Community Cloud
- Apresentação final (PPT/PDF)
- Vídeo final

---

## Plano de Execução (Sem Datas)

### Etapa 1 — Consolidação Analítica
1. Revisar consistência final dos notebooks 01, 02 e 03
2. Garantir que respostas das perguntas estejam coerentes com o enunciado atual
3. Confirmar nomenclatura, métricas e textos em português

### Etapa 2 — Modelagem Preditiva
1. Definir variável-alvo de risco com critério explícito
2. Preparar pipeline de dados (seleção de atributos, tratamento de faltantes, split treino/teste)
3. Treinar e comparar modelos (baseline e modelo final)
4. Avaliar com Recall, Precision, F1, ROC-AUC e matriz de confusão
5. Explicar resultados e salvar artefato do modelo

### Etapa 3 — Aplicação Streamlit
1. Implementar upload de CSV
2. Exibir previsão de risco e probabilidade por aluno
3. Mostrar lista de priorização para intervenção
4. Integrar com modelo salvo e validar fluxo ponta a ponta

### Etapa 4 — Storytelling Executivo
1. Montar narrativa com contexto, método, achados e recomendações
2. Incluir resultados da Q8 atualizada e do modelo preditivo
3. Produzir versão final em PPT/PDF

### Etapa 5 — Entrega Final
1. Publicar app no Streamlit Community Cloud
2. Gravar vídeo final (até 5 min)
3. Revisar checklist completo antes da submissão

---

## Critérios de Qualidade
- Reprodutibilidade: notebooks executam do início ao fim
- Consistência: números idênticos entre notebook, apresentação e vídeo
- Clareza: explicações objetivas, sem ambiguidade de métricas
- Ação: recomendações práticas para intervenção em alunos de risco

## Riscos e Mitigações
- Atraso na modelagem: garantir baseline funcional primeiro
- Falha no deploy: priorizar app MVP antes de recursos extras
- Divergência de números: congelar versão de dados e métricas oficiais antes da apresentação final

## Próxima Ação
Iniciar `notebooks/04_predictive_modeling.ipynb` com definição do target de risco e baseline de classificação.
