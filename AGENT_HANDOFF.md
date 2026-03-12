# AGENT HANDOFF — FIAP Datathon Fase 5 (Passos Mágicos)

## 1) Objetivo do projeto
Entregar uma solução completa do Datathon com:
- Análise diagnóstica (11 perguntas de negócio)
- Modelo preditivo de risco de defasagem
- Aplicação Streamlit para scoring em lote
- Storytelling executivo (PPT/PDF) + vídeo final

---

## 2) Estado atual (fonte única para continuidade)

### Concluído
- Estrutura do repositório pronta (`src`, `data`, `docs`, `notebooks`, `app`, `models`, `outputs`).
- Notebook analítico concluído e atualizado: `notebooks/03_analytical_questions.ipynb`.
  - Q8 alinhada ao enunciado novo: combinações que **elevam** INDE (uplift).
  - Q1-Q11 com texto de pergunta em markdown.
  - Visualizações individuais inseridas abaixo das questões principais (Q1, Q2, Q3, Q5, Q6, Q8, Q9).
- Notebook de modelagem criado e executado: `notebooks/04_predictive_modeling.ipynb`.
  - Duas trilhas: sem IPP (2022-2024) e com IPP (2023-2024).
  - Comparação de modelos: Logistic Regression, Random Forest, Gradient Boosting.
  - Critério de seleção: `recall` (principal) + `roc_auc` (desempate).
- Artefatos gerados:
  - `models/model_risco.joblib`
  - `outputs/model_risco_metadata.json`
  - `outputs/modelagem_leaderboard.csv`
- App Streamlit criado: `app/app.py`.
  - Upload CSV, scoring, classe de risco e priorização.

### Pendente crítico
- Deploy Streamlit Cloud
- Apresentação final (PPT/PDF)
- Vídeo final

### Atualização de governança documental (mar/2026)
- Documentação principal sincronizada com estado real do projeto:
  - `README.md`
  - `PLANO_PROJETO.md`
  - `RESUMO_EXECUCAO.md`
- Documento de continuidade e melhorias criado em:
  - `docs/AUDITORIA_CONTINUIDADE.md`

Observação: os números oficiais para slides e vídeo devem ser tomados diretamente de `notebooks/03_analytical_questions.ipynb`, `notebooks/04_predictive_modeling.ipynb` e outputs em `outputs/`.

---

## 3) Decisões importantes já tomadas (NÃO quebrar)
1. **Não imputar/extrapolar IPP para 2022 como análise principal**.
   - Justificativa: ausência estrutural (não é missing aleatório), risco de enviesar inferência.
2. **Q6 e Q8 com nota metodológica explícita** sobre limitação do IPP em 2022.
3. **Q8 no formato uplift de INDE** para combinações (`IDA + IEG + IPS + IPP`).
4. **Comentários e explicações em PT-BR**; manter nomes de variáveis/siglas para reprodutibilidade.
5. **Modelo vencedor atual**: `trilha2_com_ipp / logistic`.

---

## 4) Contexto de dados (essencial)
- Base original: `BASE DE DADOS PEDE 2024 - DATATHON.xlsx`
- Sheets: `PEDE2022`, `PEDE2023`, `PEDE2024`
- Dataset unificado atual: `data/dados_unificados.csv` (3030 linhas)
- IPP:
  - 2022: não existe
  - 2023/2024: existe com faltantes

Observação: há colunas 100% vazias em alguns anos na base original (artefatos), já tratadas no pipeline de limpeza.

---

## 5) Checklist de consistência antes de qualquer nova mudança
1. Revisar:
   - `PLANO_PROJETO.md`
   - `AGENT_HANDOFF.md` (este arquivo)
   - `README.md`
2. Validar que Q8 permanece em “elevam INDE” (uplift).
3. Confirmar presença das notas metodológicas de IPP em Q6/Q8 e na modelagem.
4. Não remover as visualizações individuais por questão já inseridas no notebook analítico.

---

## 6) Próxima etapa recomendada (ordem de execução)

### Etapa A — Validação funcional do app
1. Rodar `streamlit run app/app.py`.
2. Testar com CSVs de entrada com e sem todas as colunas esperadas.
3. Validar consistência das probabilidades e ranking de priorização.

### Etapa B — Storytelling final
1. Consolidar resultados dos notebooks em narrativa executiva.
2. Garantir consistência dos números entre notebook, slides e roteiro de vídeo.

### Etapa C — Deploy
1. Publicar app no Streamlit Community Cloud.
2. Documentar URL final no README.

### Etapa D — Fechamento de submissão
1. Preparar PPT/PDF com números estritamente iguais aos notebooks/outputs.
2. Gravar vídeo final (<= 5 min) sem divergência de métricas.
3. Rodar checklist final em `docs/AUDITORIA_CONTINUIDADE.md`.

---

## 7) Padrões de qualidade e estilo para próximos agentes
- Não alterar lógica validada sem justificativa explícita.
- Não criar imputação de campo estruturalmente ausente (caso IPP 2022).
- Cada conclusão deve ter suporte em evidência numérica.
- Garantir reprodutibilidade: notebook deve rodar do início ao fim.

---

## 8) Procedimento rápido ao trocar de computador
1. `git pull`
2. Ler `AGENT_HANDOFF.md` + `PLANO_PROJETO.md` + `README.md`
3. Validar estado de `notebooks/03_analytical_questions.ipynb` e `notebooks/04_predictive_modeling.ipynb`
4. Testar app localmente (`streamlit run app/app.py`)
5. Revisar `docs/AUDITORIA_CONTINUIDADE.md` para priorização de próximos passos

---

## 9) Observações finais
Este arquivo deve ser tratado como contexto operacional oficial para reduzir inconsistência entre sessões e entre agentes no VS Code.

---

## 10) Atualização rápida de continuidade (mar/2026)

### Revisão de limpeza e tratamento de dados
- Foi realizada revisão geral de consistência entre notebooks, app e artefatos de modelagem.
- O `app/app.py` foi ajustado para compatibilidade entre nomes legados e atuais de trilhas no metadata do modelo.
- A documentação executiva e de metodologia foi revisada para alinhamento de nomenclatura.

### Status dos pendentes
- **Pendências de entrega final ainda abertas**: deploy Streamlit Cloud, apresentação (PPT/PDF) e vídeo final.
- **Pendência técnica de notebook**: validar e finalizar limpeza de encoding em `notebooks/03_analytical_questions.ipynb` antes da versão final de submissão.

### Orientação para retomada
1. Priorizar correção/validação final do notebook analítico (`03_analytical_questions.ipynb`).
2. Reexecutar notebook e confirmar textos/saídas sem artefatos.
3. Seguir para deploy + materiais finais.
