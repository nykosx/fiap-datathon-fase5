# Plano do Projeto - Datathon Passos Mágicos (Fase 5)

## Objetivo
Concluir a entrega final do Datathon com consistência documental, storytelling executivo e publicação da solução preditiva.

## Entregáveis Obrigatórios
- Link do GitHub com códigos de limpeza e análise
- Apresentação de storytelling (PPT ou PDF)
- Notebook Python com modelo preditivo (feature engineering, treino/teste, modelagem e avaliação)
- Aplicação Streamlit com deploy no Community Cloud
- Vídeo de apresentação com até 5 minutos

---

## Status Consolidado (mar/2026)

### Concluído
- Estrutura completa do projeto (`src`, `data`, `docs`, `notebooks`, `app`, `models`, `outputs`)
- Exploração e limpeza de dados (`01_data_exploration.ipynb`, `02_data_cleaning.ipynb`)
- Respostas às 11 perguntas (`03_analytical_questions.ipynb`)
- Modelagem preditiva executada (`04_predictive_modeling.ipynb`)
- Modelo e arquivos de saída gerados:
	- `models/model_risco.joblib`
	- `outputs/model_risco_metadata.json`
	- `outputs/modelagem_leaderboard.csv`
- App Streamlit MVP funcional (`app/app.py`)

### Em aberto
- Deploy público no Streamlit Community Cloud
- Apresentação final (PPT/PDF)
- Vídeo final

---

## Plano de Fechamento (Prioridade Atual)

### Etapa 1 — Consistência de Entrega (prioridade máxima)
1. Congelar números oficiais (notebooks + outputs)
2. Garantir que README, slides e vídeo usem exatamente os mesmos valores
3. Revisar linguagem final em PT-BR e mensagens executivas

### Etapa 2 — Robustez Analítica para Banca
1. Registrar limitação de IPP ausente em 2022 (Q6, Q8 e modelagem)
2. Documentar trade-offs da seleção por recall
3. Consolidar no storytelling a validação temporal já aplicada (treino 2022->2023 e teste 2023->2024)

### Etapa 3 — Operacionalização
1. Validar o app com CSV completo e CSV com colunas faltantes
2. Publicar no Streamlit Community Cloud
3. Inserir URL final no README

### Etapa 4 — Storytelling Executivo
1. Estruturar narrativa: contexto → achados → risco → ação recomendada
2. Destacar Q8 (uplift) e modelo vencedor com implicações práticas
3. Produzir versão final em PPT/PDF

### Etapa 5 — Submissão
1. Gravar vídeo final (até 5 min)
2. Rodar checklist final de aderência aos requisitos

---

## Critérios de Qualidade
- Reprodutibilidade: notebooks executam do início ao fim
- Consistência: números idênticos entre notebook, apresentação e vídeo
- Clareza: explicações objetivas, com limitação metodológica explícita
- Ação: recomendações práticas para priorização de intervenção

## Riscos e Mitigações
- Divergência de números entre artefatos
	- Mitigação: versão oficial congelada com fonte única em notebooks/outputs
- Falha no deploy
	- Mitigação: validar app localmente antes do publish
- Interpretação de “predição” pela banca
	- Mitigação: explicitar que o alvo é temporal (t+1) e que o split de avaliação também é temporal

## Próxima Ação
Fechar apresentação final com base nos números oficiais já publicados em `outputs/modelagem_leaderboard.csv` e `outputs/model_risco_metadata.json`.
