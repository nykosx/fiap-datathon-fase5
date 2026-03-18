# Metodologia do Projeto

## Visão Geral
Projeto de analytics e modelagem preditiva para avaliar o programa educacional da Associação Passos Mágicos.

## Abordagem de Análise de Dados

### Metodologia Orientada a Dados
Todas as conclusões e insights são derivados diretamente dos padrões observados. Não há suposições sem evidências estatísticas.

Regra de governança analítica:
- sempre separar evidência descritiva de inferência estatística;
- evitar linguagem causal quando os dados não sustentarem causalidade;
- para métricas oficiais de modelo e threshold, usar apenas artefatos do notebook 04 em outputs/.

### Fluxo de Análise

#### Fase 1: Exploração de Dados
**Propósito**: Entender estrutura, qualidade e completude dos dados.

**Ações**:
- Carregar os sheets Excel (2022-2024)
- Identificar estruturas de colunas e tipos
- Quantificar valores faltantes
- Calcular estatísticas descritivas
- Documentar características dos dados

**Por quê**: Criar linha de base antes de qualquer transformação.

---

#### Fase 2: Limpeza de Dados
**Propósito**: Preparar os dados para análises confiáveis.

**Ações**:
- Tratar valores faltantes (registrar método por coluna)
- Remover ou sinalizar duplicatas
- Padronizar nomes de colunas
- Ajustar tipos de dados quando necessário
- Criar dataset unificado multi-ano

**Por quê**: Garantir qualidade e evitar conclusões distorcidas.

---

#### Fase 3: Perguntas Analíticas (1-11)
**Propósito**: Responder questões de negócio com evidências de dados.

**Abordagem por pergunta**:
1. Definir métricas mensuráveis
2. Consultar os dados relevantes
3. Calcular estatísticas
4. Visualizar padrões
5. Documentar achados numéricos

**Por quê**: Gerar insights acionáveis sustentados por dados.

Nota para Q9:
- no notebook analítico, Q9 entrega um baseline de triagem de risco para decisão operacional rápida;
- a modelagem oficial para entrega final, comparação de modelos e artefatos de deploy está centralizada no notebook 04.

---

#### Fase 4: Modelagem Preditiva
**Propósito**: Identificar estudantes em risco de deficiência acadêmica.

**Passos**:
- Definição temporal de alvo:
	- construir `ian_next_year` por aluno (t+1),
	- definir `target_risco_next = 1` quando `ian_next_year <= 5` (criterio PEDE para defasagem),
	- manter a regra fixa para comparabilidade entre ciclos.
- Separação treino/teste temporal:
	- treino: base 2022 (prevendo 2023)
	- teste: base 2023 (prevendo 2024)
- Duas trilhas de modelagem no desenho temporal:
	- Trilha 1: sem IPP (maior cobertura)
	- Trilha 2: com IPP (maior riqueza psicopedagógica, quando houver amostra suficiente)
- Comparação de modelos (Regressão Logística, Random Forest, Gradient Boosting)
- Métricas de avaliação (Precisão, Recall, F1, ROC-AUC, PR-AUC, calibração)
- Critério de escolha: maior `recall`, com `roc_auc` como desempate
- Plots de avaliação: matriz de confusão, ROC, Precision-Recall, calibração e análise de threshold

**Por quê**: Permitir intervenções proativas para alunos em risco.

---

#### Fase 5: Deploy
**Propósito**: Tornar o modelo utilizável na prática.

**Entregas**:
- Aplicação web em Streamlit
- Deploy em nuvem: https://fiap-tech-challenge-fase5-prediction.streamlit.app/
- Interface simples e objetiva

**Por quê**: Converter a análise em ferramenta operacional.

---

## Esquema de Cores

**Primária**: #2c3e50 (azul-cinza escuro)
- Tom profissional
- Alto contraste
- Adequado para apresentações formais

**Cores de Destaque**:
- #3498db (Azul): Informação neutra
- #27ae60 (Verde): Indicadores positivos
- #e74c3c (Vermelho): Risco/alerta
- #95a5a6 (Cinza): Neutro

**Fundo**: Cinza claro/branco para legibilidade em tela e impressão.

---

## Padrões de Visualização

### Gráficos por objetivo
- **Distribuição**: Histogramas, KDE
- **Comparação**: Barras simples/agrupadas
- **Tendências**: Linhas, áreas
- **Relações**: Dispersão, heatmap de correlação
- **Composição**: Barras empilhadas (uso moderado)

### Diretrizes
- Eixos com unidade clara
- Títulos concisos descrevendo o insight
- Legenda quando houver múltiplas séries
- Grade leve para leitura de valores
- Anotações para pontos-chave

---

## Rigor Estatístico

### Testes Aplicados
- Correlação (Pearson/Spearman)
- Testes de normalidade quando aplicável
- Testes de hipótese para comparações
- Intervalos de confiança para estimativas

### Limiares
- Nível de significância: α = 0.05
- Força de correlação: |r| > 0.3 (fraca), > 0.5 (moderada), > 0.7 (forte)
- Alerta para falta de dados: > 10% faltante

---

## Padrões de Qualidade de Código

### Práticas em Python
- Type hints em funções
- Docstrings completas
- Código modular (funções compartilhadas em src/ reaproveitadas no app)
- Controle de versão com commits descritivos
- Arquivo de dependências para reprodutibilidade

### Documentação
- Células markdown explicam a metodologia
- Comentários apenas para lógicas não triviais
- Interpretação dos resultados após cada análise

---

## Perguntas a Responder

1. **Evolução do IAN**: Tendência do perfil de deficiência
2. **Desempenho IDA**: Trajetória de performance acadêmica
3. **Correlação IEG-IDA-IPV**: Impacto do engajamento
4. **Alinhamento IAA-IDA**: Autopercepção vs. realidade
5. **Padrões IPS**: Sinais de risco psicossocial
6. **Validação IAN-IPP**: Consistência da avaliação de deficiência
7. **Drivers de IPV**: Preditores do ponto de virada
8. **Multidimensionalidade dos Indicadores**: Combinações (IDA + IEG + IPS + IPP) que elevam mais o INDE
9. **Predição de Risco**: Alerta antecipado
10. **Efetividade do Programa**: Melhoria entre fases
11. **Insights Adicionais**: Padrões descobertos nos dados

---

## Achados da Exploração de Dados

### Visão Geral do Dataset
- **PEDE2022**: 860 alunos × 42 colunas
- **PEDE2023**: 1.014 alunos × 48 colunas
- **PEDE2024**: 1.156 alunos × 50 colunas
- **Valores faltantes**: ~45 mil células nos 3 anos

### Principais Observações

**Inconsistências de Colunas**:
- Nomes diferentes entre anos ("Inglês" vs "Ing", "Portug" vs "Por")
- Novas colunas surgem a cada ano (42 → 48 → 50)
- Algumas colunas com 100% de ausência (artefatos de exportação)

**Padrões de Ausência**:
- Esperado: notas de Inglês/Ing (67% faltante em 2022, 59% em 2024)
- Esperado: colunas históricas "Pedra 20/21" (62-83% faltante para coortes antigas)
- Não esperado: colunas 100% faltantes em 2023/2024 (Avaliador5/6, Rec, contagem de avaliadores)
- Indicadores centrais (IDA, IEG, IPS, IAA, IPV, IAN): <9% faltantes (analisáveis)

**Qualidade dos Dados**:
- Nenhuma linha duplicada detectada
- Faltantes mínimos em colunas acadêmicas (Matem/Mat: 0,23-9,17%)
- RA atua como identificador único

### Indicadores-Chave

**Indicadores de Performance** (0-10):
- **IAN**: Adequação acadêmica (média ~6,4)
- **IDA**: Desempenho acadêmico (média ~6,1)
- **IEG**: Engajamento (média ~7,9)
- **IAA**: Autoavaliação (média ~8,3)
- **IPS**: Aspectos psicossociais (média ~6,9)
- **IPP**: Avaliação psicopedagógica
- **IPV**: Ponto de virada (média ~7,3)
- **INDE**: Índice de desempenho global (média ~7,0)

**Notas Acadêmicas** (0-10):
- Matem/Mat: média ~5,8
- Portugu/Por: média ~6,3
- Inglês/Ing: média ~5,9 (matrícula seletiva)

### Estratégia de Limpeza

1. **Padronizar Nomes de Colunas**: Mapear variações para nomes padronizados
2. **Remover 100% Faltantes**: Eliminar artefatos (Avaliador5/6, colunas Rec vazias)
3. **Tratar Ausências Esperadas**: Documentar causas (trilha de idioma, coorte)
4. **Criar Dataset Unificado**: Mesclar anos com identificador de ano
5. **Foco em Indicadores Centrais**: IAN, IDA, IEG, IAA, IPS, IPP, IPV, INDE
6. **Preservar Dados Brutos**: Manter arquivos Excel originais para auditoria

---

## Escopo deste Documento

Este arquivo descreve apenas a metodologia e as decisoes tecnicas do projeto.

Para status, continuidade e entregas, consulte:
- docs/PROJECT_GUIDE.md

Para narrativa executiva de apresentacao e video, consulte:
- docs/STORYTELLING_BASE.md