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
- Arquivos-fonte reorganizados para pastas estáveis:
  - base bruta em `data/raw/BASE DE DADOS PEDE 2024 - DATATHON.xlsx`
  - documentos do enunciado em `docs/fonte_datathon/`
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
  - `outputs/predicoes_modelo_vencedor.csv`
  - `outputs/dummy_app_scoring_input.csv`
  - `outputs/feature_ablation_report.csv`
  - `outputs/feature_selection_recommendation.json`
- App Streamlit criado: `app/app.py`.
  - Upload CSV, scoring, classe de risco e priorização.
  - Compatível com trilha temporal atual e metadata atualizado.
  - Template CSV para lote disponível no app.
  - Faixas de recomendação e threshold de scoring em lote ajustados.

### Pendente crítico
- Deploy Streamlit Cloud
- Apresentação final (PPT/PDF)
- Vídeo final

### Pendente técnico residual
- Smoke test final em ambiente limpo após `git pull` no novo computador
- Conferência final de consistência entre notebooks, outputs, slides e roteiro de vídeo

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
5. **Modelo vencedor atual**: `trilha_temporal_sem_ipp / logistic`.
6. **App deve permanecer coerente com a metodologia temporal**.
  - Entradas do scoring representam o ano-base `t`.
  - O risco previsto representa probabilidade de risco no ano seguinte `t+1`.

---

## 4) Contexto de dados (essencial)
- Base original: `data/raw/BASE DE DADOS PEDE 2024 - DATATHON.xlsx`
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
2. Testar aba individual e aba em lote.
3. Validar com `outputs/dummy_app_scoring_input.csv`.
4. Confirmar consistência das probabilidades e ranking de priorização.

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
2. Instalar dependências com `pip install -r requirements.txt`
3. Ler `AGENT_HANDOFF.md` + `PLANO_PROJETO.md` + `README.md`
4. Validar presença dos arquivos-fonte em `data/raw/` e `docs/fonte_datathon/`
5. Validar artefatos em `models/` e `outputs/`
6. Testar o app localmente com `streamlit run app/app.py`
7. Se houver qualquer divergência de artefato, reexecutar os notebooks na ordem 01 → 04
8. Revisar `docs/AUDITORIA_CONTINUIDADE.md` para priorização de próximos passos

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
- **Pendências técnicas ainda abertas**:
  - smoke test final do app em ambiente limpo com CSV dummy e CSV real de scoring,
  - revisão final dos artefatos gerados antes de publicar/deployar,
  - registrar URL do deploy no `README.md` após publicação.

### Orientação para retomada
1. Executar smoke test final do app (aba individual e lote com CSV template + dummy).
2. Validar que notebooks e outputs continuam coerentes no novo ambiente.
3. Seguir para deploy + materiais finais.
