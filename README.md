# Passos Mágicos - Datathon Fase 5

Análise preditiva e diagnóstica do desenvolvimento educacional de crianças e jovens da Associação Passos Mágicos.

## Status Atual

- Analise diagnostica concluida em `notebooks/03_analytical_questions.ipynb` (Q1-Q11).
- Modelagem preditiva concluida em `notebooks/04_predictive_modeling.ipynb`.
- Modelo salvo em `models/model_risco.joblib`.
- Metadados e leaderboard salvos em `outputs/model_risco_metadata.json` e `outputs/modelagem_leaderboard.csv`.
- App Streamlit criado em `app/app.py` para scoring em lote via CSV.

## Estrutura do Projeto

```
fiap-datathon-fase5/
├── data/                           # Dados processados
├── notebooks/                      # Notebooks de análise
│   ├── 01_data_exploration.ipynb
│   ├── 02_data_cleaning.ipynb
│   ├── 03_analytical_questions.ipynb
│   └── 04_predictive_modeling.ipynb
├── src/                           # Módulos de código
│   ├── config.py                  # Configurações e constantes
│   └── utils.py                   # Funções utilitárias
├── models/                        # Artefatos de modelos treinados
├── outputs/                       # Gráficos e relatórios gerados
├── app/                           # Aplicação Streamlit
├── docs/                          # Documentação
└── requirements.txt               # Dependências Python
```

## Objetivos

1. Análise diagnóstica dos indicadores educacionais (IAN, IDA, IEG, IAA, IPS, IPP, IPV, INDE)
2. Identificação de padrões de risco e defasagem
3. Modelo preditivo para detecção precoce de alunos em risco
4. Aplicação web para uso prático do modelo

## Instalação

```bash
pip install -r requirements.txt
```

## Metodologia

### Fase 1: Exploração de Dados
- Carregamento e validação dos dados (2022-2024)
- Análise de qualidade e completude
- Estatísticas descritivas por ano e fase

### Fase 2: Limpeza e Preparação
- Tratamento de valores ausentes
- Normalização de indicadores
- Feature engineering

### Fase 3: Análise Analítica
- Resposta às 11 questões de negócio
- Análise de correlações e tendências
- Visualizações de apoio posicionadas abaixo de cada questão principal

### Fase 4: Modelagem Preditiva
- Definição de alvo: risco quando `inde_combined <= Q1`
- Duas trilhas de treino:
	- Trilha 1: 2022-2024 sem IPP
	- Trilha 2: 2023-2024 com IPP
- Modelos comparados: Logistic Regression, Random Forest, Gradient Boosting
- Critério de seleção: maior `recall`, com `roc_auc` como desempate

### Fase 5: Deployment
- Aplicação Streamlit
- Deploy no Community Cloud (pendente)

## Principais Resultados de Modelagem

- Vencedor: `trilha2_com_ipp / logistic`
- Recall de validacao: `0.901`
- ROC-AUC de validacao: `0.931`

Os detalhes completos estao em `outputs/modelagem_leaderboard.csv`.

## Como Executar

### 1. Ambiente

```bash
pip install -r requirements.txt
```

### 2. Rodar notebooks

Execute na ordem:

1. `notebooks/01_data_exploration.ipynb`
2. `notebooks/02_data_cleaning.ipynb`
3. `notebooks/03_analytical_questions.ipynb`
4. `notebooks/04_predictive_modeling.ipynb`

### 3. Rodar app de scoring

```bash
streamlit run app/app.py
```

## Indicadores Avaliados

- **IAN**: Adequação do nível escolar
- **IDA**: Desempenho acadêmico
- **IEG**: Engajamento nas atividades
- **IAA**: Autoavaliação do aluno
- **IPS**: Aspectos psicossociais
- **IPP**: Aspectos psicopedagógicos
- **IPV**: Ponto de virada comportamental
- **INDE**: Índice de desempenho global

## Autores

Pós-Graduação em Data Analytics - FIAP

## Licença

Este projeto é parte de um trabalho acadêmico para a POSTECH FIAP.
