# Auditoria de Continuidade e Melhorias

**Projeto:** FIAP Datathon Fase 5 - Passos Mágicos  
**Data:** 11/03/2026  
**Objetivo:** apoiar continuidade do projeto em outro computador com plano de melhoria priorizado.

---

## 1) Diagnóstico Executivo

### Pontos fortes
- Pipeline completo de dados: exploração, limpeza, análise e modelagem.
- Cobertura das 11 perguntas de negócio com outputs objetivos.
- Modelo treinado e artefatos salvos para uso operacional.
- App Streamlit MVP pronto para scoring em lote.

### Pontos críticos
- Havia divergência documental entre status descrito e status real dos notebooks.
- Pendências de entrega final (deploy, apresentação e vídeo).
- Pontos metodológicos que exigiram ajuste para defesa em banca:
  - validação temporal explícita,
  - separação entre informação do ano base (t) e alvo no ano seguinte (t+1),
  - tratamento de trilha com IPP quando não há amostra temporal suficiente.

---

## 2) Críticas Técnicas (Construtivas)

### 2.1 Modelagem
- O alvo foi atualizado para estrutura temporal (`target_risco_next`), reduzindo risco de leakage conceitual.
- O split foi atualizado para estratégia temporal (treino em ano base anterior, teste em ano base posterior).
- A trilha com IPP passou a depender de disponibilidade temporal mínima, evitando avaliação artificial por ausência de dados.

### 2.2 Analytics e Storytelling
- As análises estão ricas em leitura descritiva e correlação, porém a banca pode pedir reforço de inferência/causalidade e limites de interpretação.
- A mensagem executiva pode ganhar força com fechamento padrão por pergunta: **achado → impacto → ação prática**.

### 2.3 Governança de entrega
- Sem uma “fonte única de verdade”, os números tendem a divergir entre notebook, README, PPT e vídeo.

---

## 3) Melhorias Priorizadas

### Prioridade A (alta / imediata)
1. Congelar versão oficial de métricas (notebooks + outputs).
2. Garantir consistência total nos materiais finais.
3. Publicar deploy do app e registrar URL final no README.

### Prioridade B (alta / médio esforço)
1. Validar periodicamente a robustez da estratégia temporal (ex.: backtesting com janelas móveis por ano-base).
2. Revisar features por trilha para remover campos sem observação útil.
3. Registrar limites metodológicos de forma explícita no storytelling.

### Prioridade C (média / incremental)
1. Adicionar análise de sensibilidade de limiar de decisão (trade-off recall vs precision).
2. Gerar uma aba extra no app com resumo agregado (contagem por faixa de risco).
3. Incluir seção curta de governança ética (uso assistido, não decisório isolado).

---

## 4) Plano de Continuidade (Outro Computador)

1. `git pull`
2. Instalar dependências (`pip install -r requirements.txt`)
3. Validar artefatos existentes em `outputs/` e `models/`
4. Reexecutar notebooks finais (principalmente 03 e 04) para validar consistência
5. Rodar app local (`streamlit run app/app.py`)
6. Fechar PPT/PDF e vídeo com números idênticos aos outputs

---

## 5) Checklist de Banca (Pronto/Não pronto)

- [x] 11 perguntas respondidas
- [x] Modelo preditivo treinado e salvo
- [x] App funcional para scoring
- [ ] Deploy público do app
- [ ] Storytelling final (PPT/PDF)
- [ ] Vídeo final
- [x] Validação temporal aplicada no notebook de modelagem

---

## 6) Orientação de Mensagem para Commit

Para evitar exposição desnecessária de estratégia de auditoria no histórico visível da avaliação:
- usar mensagem genérica de documentação, por exemplo: **"melhorias na documentação"**
- manter detalhamento técnico no conteúdo dos arquivos, sem descrever estratégia de avaliação no texto do commit.
