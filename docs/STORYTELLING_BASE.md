# Storytelling Base

## 1. Problema de Negocio

A Associacao Passos Magicos acompanha criancas e jovens em trajetorias educacionais distintas e precisa priorizar intervencoes com antecedencia. O desafio do projeto foi responder duas frentes:
- diagnosticar, com dados, os principais sinais de vulnerabilidade e progresso dos alunos;
- prever com antecedencia quais estudantes tem maior risco de defasagem no ciclo seguinte.

## 2. Base de Dados e Escopo

- Periodo analisado: 2022, 2023 e 2024.
- Base oficial consolidada: data/dados_unificados.csv.
- Unidade de analise: aluno por ano.
- Indicadores centrais utilizados: IAN, IDA, IEG, IAA, IPS, IPV, INDE e notas escolares.

Observacao metodologica importante:
- IPP e estruturalmente ausente em 2022, por isso nao foi tratado como coluna imputada na analise principal.

## 3. Abordagem Analitica

O projeto seguiu quatro etapas:
1. exploracao dos dados;
2. limpeza e padronizacao multi-ano;
3. resposta das 11 perguntas de negocio;
4. modelagem preditiva temporal e disponibilizacao em app.

## 4. Principais Achados Diagnosticos

Os notebooks analiticos mostram que:
- os indicadores educacionais e psicossociais ajudam a diferenciar perfis de maior e menor vulnerabilidade;
- o INDE resume bem o desempenho global, mas nao substitui a leitura dos subindicadores;
- combinacoes de desempenho academico, engajamento e fatores psicossociais sao mais informativas do que leituras isoladas.

Mensagem executiva:
- o risco nao e unidimensional; ele emerge da combinacao entre desempenho, engajamento e contexto.

## 5. Como o Modelo Foi Construido

O modelo foi desenhado para prever risco no ano seguinte, e nao apenas classificar o presente.

Regra temporal:
- treino: ano base 2022, alvo em 2023;
- teste: ano base 2023, alvo em 2024.

Definicao de risco:
- um aluno entra em risco quando o INDE do ano seguinte fica no quartil inferior do conjunto de treino.

Modelos comparados:
- Regressao Logistica
- Random Forest
- Gradient Boosting

Critero de escolha:
- primeiro, maximizar cobertura de risco detectado;
- depois, usar roc_auc como desempate.

## 6. Resultado do Modelo

Modelo vencedor:
- trilha_temporal_sem_ipp / logistic

Metricas do modelo vencedor no teste temporal:
- cobertura de risco detectado: 52,9%
- taxa de acerto dos alertas: 54,3%
- roc_auc: 0,808

Interpretacao:
- de cada 100 alunos que realmente entram em risco, o modelo sinaliza cerca de 53;
- de cada 100 alertas emitidos, cerca de 54 sao casos reais de risco.

Mensagem executiva:
- o modelo ainda nao captura todos os casos, mas ja oferece sinal preditivo util para priorizacao.

## 7. Trade-off Operacional

O modelo permite ajustar o ponto de corte de alerta conforme a capacidade da equipe.

Exemplos observados:
- corte 0.50:
  - 151 alertas
  - 52,9% de cobertura
  - 54,3% de acerto dos alertas
- corte 0.40:
  - 197 alertas
  - 61,9% de cobertura
  - 48,7% de acerto dos alertas
- corte 0.25:
  - 287 alertas
  - 78,1% de cobertura
  - 42,2% de acerto dos alertas

Leitura de negocio:
- reduzir o ponto de corte aumenta a cobertura de alunos em risco;
- em contrapartida, aumenta o numero de falsos alertas e a demanda operacional.

## 8. Aplicacao Pratica

O app Streamlit foi preparado para dois usos:
- avaliacao individual de um aluno;
- scoring em lote via CSV ou base oficial 2024.

Com isso, a equipe pode:
- priorizar casos para acompanhamento;
- gerar ranking de risco da carteira atual;
- adaptar o volume de alertas a capacidade real de atendimento.

## 9. Limites do Projeto

1. O modelo prioriza cobertura de risco, entao aceita mais falsos alertas do que uma estrategia puramente conservadora.
2. A base historica ainda e curta para validacoes temporais mais robustas.
3. A ausencia estrutural de IPP em 2022 limita comparacoes longitudinais dessa variavel.
4. A previsao para base 2024 e prospectiva; a confirmacao do acerto depende da observacao do ano seguinte.

## 10. Recomendacao Final

Uso sugerido para a Associacao:
- adotar o modelo como ferramenta de apoio, e nao como criterio isolado de decisao;
- definir o ponto de corte conforme a capacidade da equipe pedagogica;
- iniciar com uma politica explicita de priorizacao e revisar trimestralmente os resultados.

## 11. Estrutura Sugerida para PPT e Video

1. Contexto do problema
2. Base de dados e metodologia
3. Principais achados diagnosticos
4. Como o modelo foi construido
5. Resultado do modelo vencedor
6. Trade-off operacional por capacidade
7. Demontracao do app
8. Recomendacao final e proximos passos
