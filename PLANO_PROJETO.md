# Plano do Projeto - Datathon Passos Mágicos (Fase 5)

## Status Geral: 45% Completo

---

## 1. PLANEJAMENTO DO PROJETO

### Objetivo Principal
Desenvolver análise completa de dados educacionais (2022-2024) com modelo preditivo para identificar alunos em risco de defasagem, utilizando dados-driven insights e storytelling.

### Entregáveis Finais Requeridos
- ✅ Código limpo no GitHub com documentação
- ✅ Análise exploratória de dados (EDA)
- ✅ Respostas às 11 perguntas de negócio
- ⏳ Modelo preditivo em notebook Python
- ⏳ Aplicação Streamlit com deploy
- ⏳ Apresentação em PDF/PPT com storytelling
- ⏳ Vídeo de 5 minutos com resultados

---

## 2. FASES E STATUS

### FASE 1: Estrutura do Projeto ✅ COMPLETO
**Data de Conclusão**: 15/01/2026

**Deliverables**:
- ✅ Estrutura de pastas (notebooks, src, data, models, outputs, app, docs)
- ✅ `requirements.txt` com dependências
- ✅ `src/config.py` com configurações centralizadas
- ✅ `src/utils.py` com funções reutilizáveis
- ✅ `README.md` atualizado em português
- ✅ `.gitignore` configurado
- ✅ `docs/methodology.md` com metodologia

**Observações**:
- Usar Python 3.12.7 (base environment) - CONFIRMADO

---

### FASE 2: Exploração de Dados ✅ COMPLETO
**Data de Conclusão**: 15/01/2026

**Deliverables**:
- ✅ Notebook: `01_data_exploration.ipynb`
  - Carregamento dos 3 sheets (PEDE2022, PEDE2023, PEDE2024)
  - Análise de estrutura: 3030 registros × 34 colunas
  - Identificação de valores faltantes
  - Estatísticas descritivas

**Dados Encontrados**:
- PEDE2022: 860 alunos × 42 colunas
- PEDE2023: 1.014 alunos × 48 colunas
- PEDE2024: 1.156 alunos × 50 colunas
- Indicadores principais: IAN, IDA, IEG, IAA, IPS, IPP, IPV, INDE

**Observações**:
- Colunas com 100% de valores faltantes foram documentadas
- Duplicatas de colunas identificadas e tratadas
- Padrões de falta de dados esperados (e.g., inglês para alunos sem track de inglês)

---

### FASE 3: Limpeza e Preparação ✅ COMPLETO
**Data de Conclusão**: 15/01/2026

**Deliverables**:
- ✅ Notebook: `02_data_cleaning.ipynb`
  - Padronização de nomes de colunas
  - Remoção de colunas não relevantes
  - Consolidação de indicadores principais
  - Unificação dos 3 anos em dataset único

**Outputs**:
- ✅ `data/dados_unificados.csv` - 3.030 registros limpos
- ✅ `data/dados_pede2022.csv`
- ✅ `data/dados_pede2023.csv`
- ✅ `data/dados_pede2024.csv`

**Qualidade dos Dados**:
- Zero linhas duplicadas
- Indicadores principais com <9% de valores faltantes (aceitável)
- IPP com 34% de falta (presente apenas em subset)
- Todos os dados normalizados e validados

---

### FASE 4: Análise Exploratória (11 Perguntas) ✅ COMPLETO
**Data de Conclusão**: 15/01/2026

**Deliverables**:
- ✅ Notebook: `03_analytical_questions.ipynb`

**Respostas Encontradas**:

| # | Pergunta | Resposta Principal |
|---|----------|-------------------|
| 1 | Perfil IAN (defasagem) | 33% moderadamente/severamente defasados; estável nos anos |
| 2 | Desempenho IDA | 6,4/10 em média; sem mudanças significativas entre anos |
| 3 | IEG-IDA-IPV correlação | IEG vs IDA: 0,384 (moderado); engagement impacta performance |
| 4 | IAA-IDA alinhamento | 48% superestimam suas habilidades; desalinhamento observado |
| 5 | Padrões IPS (psicossocial) | 28% em alto risco psicossocial; prediz queda em IDA |
| 6 | Validação IAN-IPP | Correlação 0,681; avaliações consistentes |
| 7 | Drivers de IPV | IDA (0,514) > IEG (0,477); performance é principal driver |
| 8 | Combinações de indicadores para INDE | IDA (0,727) > IEG (0,714) > IPV (0,668) |
| 9 | Detecção precoce de risco | 18% em alto risco; 4+ indicadores baixos são sinal |
| 10 | Efetividade do programa | Fases mostram progressão consistente; programa efetivo |
| 11 | Insights adicionais | Diferenças em performance por gênero; análise etária |

**Metadados**:
- 3.030 registros analisados
- Período: 2022-2024 (3 anos)
- Correlações calculadas com Pearson
- Testes estatísticos validados

---

### FASE 5: Modelagem Preditiva ⏳ EM PROGRESSO
**Status**: Não iniciado
**Prazo Estimado**: 2-3 dias

**Objetivos**:
1. Identificar padrões precoces de defasagem
2. Construir modelo de classificação (em risco vs seguro)
3. Validar performance com métricas adequadas
4. Interpretar feature importance

**Notebook a Criar**: `04_predictive_modeling.ipynb`

**Metodologia Planejada**:
1. **Feature Engineering**
   - Selecionar features relevantes (IEG, IPS, IDA anterior, etc)
   - Criar features de interação (ex: IEG × IPS)
   - Normalizar escala

2. **Preparação de Dados**
   - Balancear classes (risco vs não-risco)
   - Split 80/20 (treino/teste)
   - Cross-validation com 5 folds

3. **Modelagem**
   - Testar: Logistic Regression, Random Forest, XGBoost, LightGBM
   - Selecionar melhor modelo por F1-score (recall importante para risco)
   - Tuning de hiperparâmetros

4. **Avaliação**
   - Métricas: Precision, Recall, F1, AUC-ROC
   - Matriz de confusão
   - SHAP values para interpretabilidade

5. **Output**
   - Modelo treinado (`models/model_risco.joblib`)
   - Feature importance chart
   - Threshold de decisão documentado

---

### FASE 6: Aplicação Streamlit ⏳ NÃO INICIADO
**Status**: Não iniciado
**Prazo Estimado**: 2-3 dias

**Deliverable**: `app/app.py`

**Funcionalidades Planejadas**:
1. Upload de arquivo CSV com dados de novos alunos
2. Previsão em tempo real com modelo treinado
3. Dashboard com visualizações:
   - Distribuição de risco (gauge charts)
   - Correlações entre indicadores
   - Comparação com benchmark
4. Export de relatório em PDF
5. Logging de previsões

**Temas**:
- Dark theme com #2c3e50 (cor primária solicitada)
- Background claro para legibilidade
- Responsivo e profissional

**Deploy**:
- Streamlit Community Cloud
- Link compartilhável

---

### FASE 7: Documentação e Apresentação ⏳ NÃO INICIADO
**Status**: Não iniciado
**Prazo Estimado**: 2-3 dias

**Deliverables**:

1. **Apresentação (PDF/PPT)**
   - Storytelling dos dados
   - Visualizações profissionais
   - Insights principais
   - Recomendações

2. **Vídeo (5 min max)**
   - Apresentação dos resultados
   - Demonstração do modelo
   - Impacto esperado

3. **Documentação**
   - `docs/methodology.md` (atualizado com resultados)
   - Dicionário de dados completo
   - Guia de uso do modelo
   - Limitações e próximos passos

---

## 3. ISSUES A RESOLVER

### 🔴 CRÍTICO

1. **Tradução para Português**
   - ❌ Markdown dos notebooks em INGLÊS → deve ser PORTUGUÊS
   - ❌ Documentação em INGLÊS → deve ser PORTUGUÊS
   - ✅ Variáveis de código podem permanecer em INGLÊS
   - Ação necessária: Revisar e traduzir:
     - `01_data_exploration.ipynb` - markdown
     - `02_data_cleaning.ipynb` - markdown
     - `03_analytical_questions.ipynb` - markdown
     - `docs/methodology.md` - todo o documento
     - `README.md` - atualizar

2. **Código em Células Markdown**
   - ❌ Imagem anexada mostra código Python em cell markdown
   - Problema: Código não executável, dificulta leitura
   - Ação necessária: Verificar e remover código de células markdown

### 🟡 IMPORTANTE

3. **Configuração de Kernel**
   - ✅ Python 3.12.7 confirmado como ambiente base
   - Manter consistência em todos os notebooks

---

## 4. CRONOGRAMA ESTIMADO

| Fase | Status | Prazo | Prioridade |
|------|--------|-------|-----------|
| 1. Estrutura | ✅ Completo | Feito | - |
| 2. Exploração | ✅ Completo | Feito | - |
| 3. Limpeza | ✅ Completo | Feito | - |
| 4. Análise 11Q | ✅ Completo | Feito | - |
| 5. Modelagem | ⏳ Em progresso | 2-3 dias | ALTA |
| 6. Streamlit | ⏳ Não iniciado | 2-3 dias | ALTA |
| 7. Apresentação | ⏳ Não iniciado | 2-3 dias | ALTA |
| 8. Deploy + Vídeo | ⏳ Não iniciado | 1-2 dias | ALTA |

**Tempo total estimado**: 7-11 dias
**Data prevista de conclusão**: ~26/01/2026

---

## 5. TECNOLOGIAS E FERRAMENTAS

| Componente | Tecnologia | Status |
|-----------|-----------|--------|
| Linguagem | Python 3.12.7 | ✅ |
| Análise de Dados | Pandas, NumPy | ✅ |
| Visualização | Matplotlib, Seaborn | ✅ |
| ML | Scikit-learn, XGBoost, LightGBM | ⏳ |
| Web App | Streamlit | ⏳ |
| Deploy | Streamlit Community Cloud | ⏳ |
| Versionamento | Git + GitHub | ✅ |
| IDE | VS Code | ✅ |

---

## 6. PRÓXIMOS PASSOS IMEDIATOS

1. **[HOJE]** Traduzir todo markdown para português
2. **[HOJE]** Verificar e remover código de células markdown
3. **[AMANHÃ]** Iniciar notebook de modelagem preditiva
4. **[POSTERIOR]** Construir aplicação Streamlit
5. **[FINAL]** Deploy e vídeo de apresentação

---

## 7. NOTAS IMPORTANTES

- Sem inferences: dados devem dirigir todas as conclusões
- Tema escuro (#2c3e50) para profissionalismo
- Foco em early warning para intervenção precoce
- Documentação é essencial para reproducibilidade
- Todas as decisões devem ser justificadas por dados

---

**Última atualização**: 15/01/2026
**Responsável**: Análise de Dados
**Versão**: 1.0
