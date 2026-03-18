# Handoff para Proximo Agent

## Objetivo deste handoff
Garantir continuidade rapida para fechamento final (banca + app + materiais), sem retrabalho metodologico.

## Contexto consolidado
- A base oficial segue em `data/dados_unificados.csv`.
- O notebook analitico `notebooks/03_analytical_questions.ipynb` foi reforcado em profundidade (Q7 por dimensao, testes inferenciais Spearman com p-valor em Q3/Q4/Q5, e ICAP no Q11).
- O notebook preditivo `notebooks/04_predictive_modeling.ipynb` esta alinhado ao fluxo temporal e usa utilitarios compartilhados de `src/notebook_utils.py`.
- O app `app/app.py` foi modularizado para usar `src/config.py` e `src/utils.py`.
- Documentacao principal atualizada em `README.md`, `docs/PROJECT_GUIDE.md`, `docs/methodology.md` e `docs/STORYTELLING_BASE.md`.

## Checkpoint critico pedido pelo usuario
- Revisao feita sobre risco de texto antigo no app dizendo que target era INDE:
  - **Status atual**: nao foi identificado trecho no app definindo INDE como target.
  - O app exibe definicao baseada em metadata: `target_risco_next = 1 quando ian_next_year <= 5`.
  - Se surgir comentario antigo no Streamlit Cloud, provavel causa e deploy desatualizado (nao o codigo local atual).

## Avaliacao: a nota de banca elevou?
Avaliacao qualitativa: **sim, houve elevacao provavel de nota (moderada para alta)**.

Motivos:
- Maior aderencia a pergunta da banca com aprofundamento analitico (Q7-Q11).
- Melhor defesa tecnica por separar descritivo vs inferencial e incluir p-valores em correlacoes chave.
- Sintese executiva mais forte (ICAP + pacote operacional Q7/Q9/Q11).
- Documentacao mais governada, com fonte oficial de metricas clara (nb04/outputs).

O que ainda impede nota maxima:
- Falta fechamento final de PPT/PDF e video com consistencia numerica total.
- Falta validacao final de reproducibilidade (rodar notebooks-chave e registrar evidencias).
- Falta checklist final de deploy e smoke test completo do app em cloud.

## Pendencias (prioridade)
### Critico
1. Fechar materiais finais (PPT/PDF e video) usando somente numeros oficiais de `outputs/` e narrativa de `docs/STORYTELLING_BASE.md`.
2. Fazer smoke test do app publicado com 1 caso individual e 1 CSV em lote, registrando evidencias.
3. Confirmar que o Streamlit Cloud esta rodando exatamente este commit (evitar discrepancia de texto antigo).

### Recomendado
1. Executar novamente celulas finais de `notebooks/03_analytical_questions.ipynb` e `notebooks/04_predictive_modeling.ipynb` para garantir outputs consistentes com os arquivos atuais.
2. Validar que os artefatos esperados existem e estao sincronizados:
   - `models/model_risco.joblib`
   - `outputs/model_risco_metadata.json`
   - `outputs/modelagem_leaderboard.csv`
   - `outputs/predicoes_modelo_vencedor.csv`
   - `outputs/modelagem_tradeoff_thresholds.csv`
   - `outputs/modelagem_tradeoff_capacidade.csv`
3. Revisar linguagem final para banca: evitar causalidade indevida e reforcar trade-off de threshold por capacidade operacional.

### Possiveis melhorias
1. Adicionar mini secao de "monitoramento mensal" no app (drift de score, taxa de alertas, cobertura observada).
2. Incluir explicacao de thresholds sugeridos por capacidade diretamente na UI do app em lote.
3. Adicionar teste automatizado simples de validacao de schema para input CSV do app.
4. Criar anexo tecnico curto para banca com limitacoes (serie curta, IPP incompleto 2022, dependencia de governanca de threshold).

## Riscos de regressao
- Alterar definicao de target fora de `ian_next_year <= 5` quebra comparabilidade de metricas historicas.
- Reintroduzir INDE como feature do modelo invalida governanca por leakage conceitual.
- Regerar notebooks sem controle pode sobrescrever outputs binarios e confundir versao oficial.

## Plano de execucao sugerido para o proximo agent
1. Validar cloud deploy atual vs codigo local (foco no texto de target no app).
2. Rodar smoke test funcional do app e registrar resultado em markdown curto.
3. Fechar versao final de roteiro de apresentacao (5-7 slides + fala de 60-90s para Q11/ICAP).
4. Fazer revisao final de consistencia numerica entre storytelling e outputs.

## Definicoes que devem permanecer estaveis
- Split temporal: treino base 2022 -> alvo 2023; teste base 2023 -> alvo 2024.
- Target: `target_risco_next = 1 quando ian_next_year <= 5`.
- Criterio de selecao do modelo: recall primeiro, roc_auc como desempate.
- Q9 no nb03 e baseline narrativo; metricas oficiais de modelagem vem do nb04/outputs.
