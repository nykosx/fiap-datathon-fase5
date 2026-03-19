# Guia Curto da Apresentacao (PPT/PDF)

## Objetivo
Este guia foi desenhado para facilitar a montagem rapida da apresentacao pela equipe, sem excesso de texto para decorar.

## Regra de ouro
- 10 slides, 8 a 12 minutos.
- 1 mensagem principal por slide.
- 1 grafico por slide (sem poluicao visual).
- Fechar cada slide com 3 linhas: achado, impacto, acao.

## Estrutura recomendada (10 slides)

1. Capa e problema
- Mensagem: como priorizar intervencoes com recursos limitados.
- Frase pronta: "Queremos reduzir alunos em risco de defasagem antes da queda se consolidar."

2. Dados e recorte
- Fonte: data/dados_unificados.csv.
- Periodo: 2022-2024.
- Unidade: aluno/ano.

3. Q1 - Defasagem ao longo do tempo
- Grafico: outputs/figuras/q1_evolucao_taxas_defasagem.png
- Achado: defasagem total e severa mudam ao longo dos anos.
- Impacto: risco nao e uniforme no tempo.
- Acao: monitoramento anual por coorte e por fase.

4. Q2 - Tendencia de desempenho (IDA)
- Grafico: outputs/figuras/q2_ida_tendencia_observado_ajustado.png
- Achado: IDA observado pode divergir do ajustado por composicao de fase.
- Impacto: media agregada sozinha pode enganar a gestao.
- Acao: metas separadas para ganho intrafase e mix de fases.

5. Q3 - Engajamento como alavanca
- Grafico: outputs/figuras/q3_curva_quintis_ieg.png
- Achado: quintis mais altos de IEG tendem a melhores IDA/IPV.
- Impacto: engajamento e indicador lider operacional.
- Acao: plano focado nos quintis baixos de IEG.

6. Q4 e Q5 - Calibracao e psicossocial
- Grafico: outputs/figuras/q4_curva_calibracao_decil.png
- Grafico alternativo (se precisar trocar): outputs/figuras/q5_risco_ida_por_quartil_ips.png
- Achado: ha descalibracao IAA-IDA e gradiente de risco por IPS.
- Impacto: risco nao e apenas academico.
- Acao: triagem combinada pedagogica e psicossocial.
- Obs. tecnica: Q5 mede associacao contemporanea (mesmo periodo); nao e analise temporal causal.

7. Q9 baseline + modelo principal (nb04)
- Grafico Q9: outputs/figuras/q9_roc_modelo_risco_defasagem.png
- Complemento oficial: outputs/modelagem_leaderboard.csv
- Mensagem: Q9 (baseline de triagem) + nb04 (previsao temporal do ciclo seguinte) sao complementares, nao redundantes.
- Diferenca-chave: Q9 classifica estado atual com dados historicos; nb04 prediz o proximo ciclo com shift de um ano.

8. Trade-off operacional (decisao real)
- Tabela: outputs/modelagem_tradeoff_thresholds.csv
- Tabela: outputs/modelagem_tradeoff_capacidade.csv
- Mensagem: corte menor aumenta cobertura e carga operacional; corte maior reduz ruido e perde casos.

9. Demo do app para equipe educacional
- App: avaliacao individual + lote + modo por capacidade + relatorio de qualidade da entrada.
- Mensagem: resultado vira acao operacional, nao so score tecnico.

10. Plano de implementacao em 30-60-90 dias
- 30 dias: triagem mensal por risco e capacidade.
- 60 dias: ajustes por fase/quintil de engajamento.
- 90 dias: revisao de impacto com indicadores de resultado.

## Storytelling pronto (resumo de 1 minuto)
"Partimos de uma pergunta de negocio simples: como priorizar alunos com maior risco de defasagem antes da piora? Com base em dados de 2022 a 2024, vimos que o risco e multidimensional: desempenho, engajamento e contexto psicossocial andam juntos. Construimos uma esteira analitica para explicar os fatores e uma modelagem temporal para prever risco no ciclo seguinte. O resultado nao e so acuracia: e capacidade de decisao. Com o trade-off por threshold e o app, a equipe consegue ajustar cobertura de alerta ao tamanho operacional e agir com prioridade clara."

## Checklist rapido antes da entrega
- Confirmar numeros oficiais nos arquivos de outputs.
- Validar se os graficos usados batem com os achados narrados.
- Evitar termos causais fortes quando a analise e associativa.
- Encerrar com plano de acao e governanca (nao so metricas).
