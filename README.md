# Passos Mágicos - Datathon Fase 5

Análise preditiva e diagnóstica do desenvolvimento educacional de crianças e jovens da Associação Passos Mágicos.

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
- Visualizações profissionais

### Fase 4: Modelagem Preditiva
- Seleção de features relevantes
- Treinamento de modelos de classificação
- Avaliação de performance
- Interpretabilidade (SHAP values)

### Fase 5: Deployment
- Aplicação Streamlit
- Deploy no Community Cloud

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
