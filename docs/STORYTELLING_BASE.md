# Storytelling Base

## 1. Problema de Negocio

A Associacao Passos Magicos precisa decidir onde intervir primeiro, com recursos finitos, sem esperar a defasagem se consolidar.

O projeto responde duas frentes complementares:
- diagnostico: entender os fatores que explicam vulnerabilidade e progresso educacional;
- previsao: antecipar quem tem maior risco de defasagem no ciclo seguinte.

## 2. Escopo de Dados

- Periodo analisado: 2022, 2023 e 2024.
- Base consolidada: data/dados_unificados.csv.
- Unidade analitica: aluno por ano.
- Indicadores centrais: IAN, IDA, IEG, IAA, IPS, IPP, IPV e INDE.

Premissa tecnica importante:
- IPP e estruturalmente incompleto em 2022, por isso a trilha principal de modelagem nao depende de imputacao de IPP.

## 3. Estrutura da Solucao

1. exploracao e limpeza dos dados;
2. resposta individual das perguntas Q1 a Q11 (notebook analitico);
3. modelagem preditiva temporal consolidada (nb04);
4. operacionalizacao em app Streamlit.

## 4. Achados-Chave das Perguntas (Q1-Q11)

- Q1: a defasagem total caiu ao longo do periodo, com reducao mais forte da defasagem severa;
- Q2 e Q10: ha melhora agregada de desempenho, mas com oscilacoes e heterogeneidade por fase/etapa;
- Q3: engajamento (IEG) e alavanca transversal, associado a IDA e IPV, inclusive com evidencias de significancia estatistica em correlacoes nao parametricas;
- Q4: existe desalinhamento relevante entre autoavaliacao (IAA) e desempenho real (IDA);
- Q5 e Q6: IPS e IPP agregam leitura de risco complementar, nao redundante, com testes inferenciais de diferenca entre grupos;
- Q7 e Q8: drivers e combinacoes de indicadores explicam melhor o resultado do que variaveis isoladas; em Q7 os drivers foram organizados por dimensao (academica, engajamento e psicossocial) para orientar acao por equipe;
- Q9: baseline de ML no notebook analitico confirma viabilidade de triagem probabilistica;
- Q11: sintese integrada prioriza frentes de acao com horizonte operacional e adiciona o ICAP (Indice Composto de Alerta Precoce) para triagem unificada de risco.

Mensagem executiva:
- risco educacional e multidimensional; a melhor resposta e combinada (pedagogica, engajamento e psicossocial).

Mensagem de implementacao:
- operacionalmente, o pacote recomendado combina: ranking probabilistico (Q9), leitura por dimensao de driver (Q7) e score composto de alerta precoce ICAP (Q11).

## 5. Como o Modelo Principal Foi Construido (nb04)

Regra temporal (sem leakage de futuro):
- treino: ano base 2022 para prever 2023;
- teste: ano base 2023 para prever 2024.

Definicao de risco:
- target_risco_next = 1 quando ian_next_year <= 5.

Modelos comparados:
- regressao logistica;
- random forest;
- gradient boosting.

Criterio de selecao:
- prioridade 1: maior recall (cobertura de risco detectado);
- prioridade 2: maior roc_auc (desempate).

## 6. Resultado do Modelo Principal

Modelo vencedor:
- trilha_temporal_sem_ipp / random_forest.

Metricas em teste temporal:
- recall: 58,4%;
- precision: 64,3%;
- roc_auc: 0,743.

Leitura de negocio:
- de cada 100 alunos que efetivamente entram em risco, o modelo antecipa cerca de 58;
- de cada 100 alertas gerados, cerca de 64 sao risco real.

## 7. Trade-off Operacional (Threshold)

Exemplos observados na curva de threshold:
- corte 0,50:
  - 280 alertas;
  - 58,4% de cobertura;
  - 64,3% de acerto dos alertas.
- corte 0,40:
  - 463 alertas;
  - 77,9% de cobertura;
  - 51,8% de acerto dos alertas.
- corte 0,25:
  - 700 alertas;
  - 98,1% de cobertura;
  - 43,1% de acerto dos alertas.

Interpretacao:
- reduzir threshold aumenta cobertura e carga operacional;
- elevar threshold melhora acuracia dos alertas, mas deixa mais risco sem detectar.

## 8. Papel de Q9 vs nb04

- Q9 (notebook analitico): baseline explicavel para triagem e narrativa de negocio.
- nb04 (modelagem principal): comparacao formal de modelos, leaderboard, trade-off e artefatos para deploy.

Decisao de governanca:
- para numero oficial de modelo e thresholds, usar sempre os artefatos do nb04.

## 9. Aplicacao Pratica (App)

O app entrega:
- avaliacao individual de risco com recomendacoes objetivas;
- scoring em lote por CSV ou base oficial 2024;
- ajuste de ponto de corte conforme capacidade de atendimento.

## 10. Limites e Cuidados

1. serie historica curta para generalizacao de longo prazo;
2. ausencia estrutural de IPP em 2022 reduz comparabilidade longitudinal completa;
3. threshold deve ser governado por capacidade operacional da equipe;
4. modelo apoia decisao, mas nao substitui avaliacao pedagogica individual.

## 11. Roteiro Sugerido (PPT/Video)

1. problema e impacto social;
2. dados e metodologia;
3. achados das perguntas Q1-Q11;
4. modelo principal (nb04) e metricas;
5. trade-off operacional por threshold;
6. demonstracao do app;
7. plano de acao e governanca.
