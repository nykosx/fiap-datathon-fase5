import json
from pathlib import Path

import joblib
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(
    page_title="Risco de Defasagem — Passos Mágicos",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed",
)

PROJECT_ROOT = Path(__file__).resolve().parent.parent
MODEL_PATH = PROJECT_ROOT / "models" / "model_risco.joblib"
METADATA_PATH = PROJECT_ROOT / "outputs" / "model_risco_metadata.json"


# ── helpers ──────────────────────────────────────────────────────────────────

@st.cache_resource
def load_artifacts():
    meta = None
    if METADATA_PATH.exists():
        with open(METADATA_PATH, "r", encoding="utf-8") as fp:
            meta = json.load(fp)
    mdl = joblib.load(MODEL_PATH)
    return meta, mdl


def ensure_cols(df: pd.DataFrame, cols: list) -> pd.DataFrame:
    out = df.copy()
    for c in cols:
        if c not in out.columns:
            out[c] = pd.NA
    return out


def risk_color(prob: float) -> str:
    if prob >= 0.7:
        return "#c0392b"
    if prob >= 0.5:
        return "#e67e22"
    if prob >= 0.3:
        return "#f1c40f"
    return "#27ae60"


def risk_label(prob: float) -> str:
    if prob >= 0.7:
        return "Risco Critico"
    if prob >= 0.5:
        return "Risco Alto"
    if prob >= 0.3:
        return "Risco Moderado"
    return "Baixo Risco"


def build_recommendations(prob: float, inputs: dict, q1_threshold: float = 6.63) -> list:
    """Recomendacoes contextualizadas ao perfil e nivel de risco do aluno."""
    recs = []

    ian  = inputs.get("ian",  10)
    ida  = inputs.get("ida",  10)
    ieg  = inputs.get("ieg",  10)
    iaa  = inputs.get("iaa",  10)
    ips  = inputs.get("ips",  10)
    ipv  = inputs.get("ipv",  10)
    inde = inputs.get("inde_combined")
    math_ = inputs.get("math",       10)
    port  = inputs.get("portuguese", 10)
    eng   = inputs.get("english",    10)
    turn  = inputs.get("achieved_turning_point",    "Nao")
    interv = inputs.get("indicated_for_intervention", "Nao")

    # ── Nível de risco global ────────────────────────────────────────────────
    if prob >= 0.7:
        recs.append(
            "🔴 **Atencao prioritaria:** Alta probabilidade de defasagem no proximo ciclo. "
            "Intervencao imediata pela equipe pedagogica é recomendada."
        )
    elif prob >= 0.5:
        recs.append(
            "🟠 **Acompanhamento proximo:** Probabilidade elevada de defasagem. "
            "Incluir nos ciclos de monitoramento mensal e revisar plano pedagogico."
        )
    elif prob >= 0.3:
        recs.append(
            "🟡 **Zona de atencao:** Risco moderado. "
            "Monitorar evolucao nos proximos bimestres e identificar tendencias negativas."
        )
    else:
        recs.append(
            "🟢 **Perfil estavel:** Baixo risco de defasagem. "
            "Manter incentivos, acompanhamento regular e reforcar pontos fortes do aluno."
        )

    # ── Contexto INDE vs. limiar de risco ────────────────────────────────────
    if inde is not None:
        if inde <= q1_threshold:
            recs.append(
                f"**INDE atual ({inde:.2f}) abaixo do limiar de risco ({q1_threshold:.2f}):** "
                "O indice composto ja sinaliza defasagem. Avaliar sub-indicadores para identificar pontos criticos."
            )
        elif inde <= q1_threshold + 0.5:
            recs.append(
                f"**INDE atual ({inde:.2f}) proximo do limiar de risco ({q1_threshold:.2f}):** "
                "Margem estreita — pequena queda pode levar a defasagem no proximo ano."
            )

    # ── Indicadores Passos Magicos ────────────────────────────────────────────
    if ian < 4:
        recs.append(
            "**IAN critico (adequacao de nivel):** Aluno significativamente abaixo da fase esperada. "
            "Considere reforco individualizado ou revisao de nivelamento."
        )
    elif ian < 6:
        recs.append(
            "**IAN em desenvolvimento:** Ha lacunas de conteudo em relacao a fase. "
            "Atividades de recuperacao paralela sao recomendadas."
        )

    if ida < 4:
        recs.append(
            "**IDA critico (desenvolvimento academico):** Progressao academica muito abaixo do esperado. "
            "Revisar frequencia, participacao em aulas e entrega de atividades."
        )
    elif ida < 6:
        recs.append(
            "**IDA em desenvolvimento:** Progresso aquem do potencial. "
            "Identificar barreiras especificas de aprendizagem e oferecer suporte direcionado."
        )

    if ieg < 4:
        recs.append(
            "**IEG critico (engajamento):** Baixo engajamento com o programa. "
            "Estrategias de motivacao, mentoria e atividades extracurriculares sao indicadas."
        )
    elif ieg < 6:
        recs.append(
            "**IEG moderado:** Engajamento parcial. "
            "Verificar fatores externos que possam estar afetando a participacao."
        )

    if iaa < 4:
        recs.append(
            "**IAA critico (autoavaliacao):** Aluno demonstra baixa percepcao de suas capacidades. "
            "Sessoes de coaching e tecnicas de reforco de autoestima sao recomendadas."
        )
    elif iaa < 6:
        recs.append(
            "**IAA moderado:** Aluno tende a subestimar seu desenvolvimento. "
            "Feedback positivo estruturado e reconhecimento de conquistas podem ajudar."
        )

    if ips < 4:
        recs.append(
            "**IPS critico (psicossocial):** Vulnerabilidade psicossocial elevada. "
            "Acionar assistente social ou psicologo da equipe Passos Magicos."
        )
    elif ips < 6:
        recs.append(
            "**IPS moderado:** Alguma pressao psicossocial identificada. "
            "Verificar contexto familiar, de saude e rede de apoio do aluno."
        )

    if ipv < 4:
        recs.append(
            "**IPV critico (ponto de virada):** Aluno ainda distante do ponto de virada. "
            "Definir metas de curto prazo concretas e celebrar pequenas conquistas."
        )
    elif ipv < 6:
        recs.append(
            "**IPV em construcao:** Aluno em caminho para o ponto de virada. "
            "Reforcar perspectiva de futuro e projetos de vida."
        )

    # ── Notas escolares ───────────────────────────────────────────────────────
    low_grades = [s for s, v in [("Matematica", math_), ("Portugues", port), ("Ingles", eng)] if v < 4]
    mid_grades = [s for s, v in [("Matematica", math_), ("Portugues", port), ("Ingles", eng)] if 4 <= v < 6]
    if low_grades:
        recs.append(
            f"**Notas criticas em:** {', '.join(low_grades)}. "
            "Reforco especifico nestas disciplinas, preferencialmente em grupos reduzidos."
        )
    elif mid_grades:
        recs.append(
            f"**Notas em desenvolvimento em:** {', '.join(mid_grades)}. "
            "Acompanhar evolucao e oferecer suporte direcionado."
        )

    # ── Flags contextuais ─────────────────────────────────────────────────────
    if interv == "Sim":
        recs.append(
            "**Ja indicado para intervencao:** Verificar se o plano de acao esta ativo "
            "e documentar evolucao no proximo ciclo de avaliacao."
        )

    if turn == "Nao":
        recs.append(
            "**Ponto de virada nao alcancado:** Definir um objetivo concreto e mensuravel "
            "junto ao aluno para o proximo trimestre."
        )

    return recs


# ── carrega artefatos ─────────────────────────────────────────────────────────

if not MODEL_PATH.exists():
    st.error(f"Modelo nao encontrado em: {MODEL_PATH}")
    st.stop()

metadata, model = load_artifacts()

winner_track = metadata.get("winner_track", "trilha_core_com_ipp") if metadata else "trilha_core_com_ipp"
expected_features = []
if metadata:
    if winner_track in {"trilha2_com_ipp", "trilha_core_com_ipp", "trilha_temporal_com_ipp"}:
        track_key = "track2"
    else:  # trilha1_sem_ipp, trilha_core_sem_ipp, trilha_temporal_sem_ipp, fallback
        track_key = "track1"
    expected_features = (metadata.get(track_key) or {}).get("features", [])

has_ipp = "ipp" in expected_features


# ── cabecalho ────────────────────────────────────────────────────────────────

st.title("Sistema de Risco Academico - Passos Magicos")
m = metadata.get("winner_metrics", {}) if metadata else {}
st.caption(
    "Identificacao precoce de alunos em risco de defasagem educacional. "
    f"Modelo: {metadata.get('winner_model', 'logistic') if metadata else 'logistic'} | "
    f"Recall: {m.get('recall', 0):.3f} | ROC-AUC: {m.get('roc_auc', 0):.3f}"
)
st.markdown("---")

tab_individual, tab_massa = st.tabs(["Aluno Individual", "Predicao em Massa (CSV)"])


# ══════════════════════════════════════════════════════════════════════════════
# ABA 1 — ALUNO INDIVIDUAL
# ══════════════════════════════════════════════════════════════════════════════

with tab_individual:
    st.subheader("Avaliacao de um aluno")

    q1_thr = metadata.get("q1_train_inde_next_year", 6.63) if metadata else 6.63
    st.info(
        f"ℹ️ O modelo prevê o risco de **defasagem no próximo ano** com base nos indicadores atuais. "
        f"Definição de risco: INDE no próximo ciclo ≤ **{q1_thr:.2f}** (1º quartil do conjunto de treino). "
        f"Modelo: **{metadata.get('winner_model', 'logistic') if metadata else 'logistic'}** — "
        f"Recall: **{m.get('recall', 0):.1%}** | ROC-AUC: **{m.get('roc_auc', 0):.3f}**"
    )

    with st.form("form_aluno"):
        col_a, col_b, col_c = st.columns(3)

        with col_a:
            st.markdown("**Dados Cadastrais**")
            year = st.selectbox("Ano de referencia", ["PEDE2022", "PEDE2023", "PEDE2024"]) if "year" in expected_features else "PEDE2024"
            phase_options = [
                "ALFA",
                "FASE 1", "FASE 2", "FASE 3", "FASE 4", "FASE 5", "FASE 6", "FASE 7", "FASE 8",
                "1", "2", "3", "4", "5", "6", "7", "8",
            ]
            phase = (
                st.selectbox("Fase atual", phase_options)
                if "phase" in expected_features
                else "4"
            )
            admission_year = (
                st.number_input("Ano de ingresso", min_value=2010, max_value=2024, value=2020, step=1)
                if "admission_year" in expected_features
                else None
            )
            age = (
                st.number_input("Idade atual", min_value=6, max_value=25, value=13, step=1)
                if "age" in expected_features
                else None
            )
            age_2022 = (
                st.number_input("Idade em 2022", min_value=6, max_value=25, value=11, step=1)
                if "age_2022" in expected_features
                else None
            )
            gender = st.selectbox("Genero", ["Feminino", "Masculino"]) if "gender" in expected_features else "Feminino"
            school_institution = (
                st.selectbox("Instituicao escolar", ["Escola Publica", "Rede Decisao", "Escola Privada", "Outros"])
                if "school_institution" in expected_features
                else "Escola Publica"
            )
            st.markdown("**Contexto Pedagogico**")
            # Sempre visíveis — usados nas recomendações (não entram no modelo)
            achieved_turning_point = st.selectbox(
                "Atingiu ponto de virada?", ["Nao", "Sim"],
                help="Indica se o aluno ja demonstrou uma mudanca significativa de perspectiva."
            )
            indicated_for_intervention = st.selectbox(
                "Ja indicado para intervencao?", ["Nao", "Sim"],
                help="Indica se o aluno ja faz parte de algum plano de intervencao ativo."
            )
            deficiency = st.selectbox("Possui deficiencia?", ["Nao", "Sim"]) if "deficiency" in expected_features else "Nao"

        with col_b:
            st.markdown("**Indicadores Passos Magicos**")
            ian = st.slider(
                "IAN - Adequacao de Nivel", 0.0, 10.0, 5.0, 0.1,
                help="Mede o alinhamento entre o desempenho do aluno e a fase esperada para sua idade."
            )
            ida = st.slider(
                "IDA - Desenvolvimento Academico", 0.0, 10.0, 5.0, 0.1,
                help="Mede o progresso academico ao longo do periodo avaliado."
            )
            ieg = st.slider(
                "IEG - Engajamento", 0.0, 10.0, 5.0, 0.1,
                help="Grau de participacao e engajamento do aluno no programa."
            )
            iaa = st.slider(
                "IAA - Autoavaliacao", 0.0, 10.0, 5.0, 0.1,
                help="Percepcao do aluno sobre seu proprio desempenho e evolucao."
            )
            ips = st.slider(
                "IPS - Psicossocial", 0.0, 10.0, 5.0, 0.1,
                help="Indicador de bem-estar psicossocial e condicao socioeconomica. Valores baixos indicam maior vulnerabilidade."
            )
            ipv = st.slider(
                "IPV - Ponto de Virada", 0.0, 10.0, 5.0, 0.1,
                help="Indica se o aluno esta se aproximando ou ja atingiu seu ponto de virada."
            )
            if has_ipp:
                ipp = st.slider(
                    "IPP - Ponto de Partida", 0.0, 10.0, 5.0, 0.1,
                    help="Situacao inicial do aluno ao ingressar no programa."
                )
            else:
                ipp = None

        with col_c:
            st.markdown("**Desempenho Escolar**")
            math = st.slider("Matematica", 0.0, 10.0, 5.0, 0.1)
            portuguese = st.slider("Portugues", 0.0, 10.0, 5.0, 0.1)
            english = st.slider("Ingles", 0.0, 10.0, 5.0, 0.1)
            if "inde_combined" in expected_features:
                inde_combined = st.slider(
                    "INDE - Indice de Desenv. Educacional", 0.0, 10.0, 7.0, 0.01,
                    help=(
                        f"Indice geral de desenvolvimento educacional do ultimo ciclo disponivel. "
                        f"Limiar de risco de referencia: {q1_thr:.2f}"
                    ),
                )
            else:
                inde_combined = None

        submitted = st.form_submit_button("Calcular Risco", use_container_width=True)

    if submitted:
        # mapeia valores do formulario para os esperados pelo modelo
        school_map = {
            "Escola Publica": "Escola Pública",
            "Rede Decisao": "Rede Decisão",
            "Escola Privada": "Escola Privada",
            "Outros": "Outros",
        }
        tp_map = {"Nao": "Não", "Sim": "Sim"}

        input_dict = {
            "ian": ian,
            "ida": ida,
            "ieg": ieg,
            "iaa": iaa,
            "ips": ips,
            "ipv": ipv,
            "math": math,
            "portuguese": portuguese,
            "english": english,
        }

        if "year" in expected_features:
            input_dict["year"] = year
        if "phase" in expected_features:
            input_dict["phase"] = phase
        if "admission_year" in expected_features and admission_year is not None:
            input_dict["admission_year"] = admission_year
        if "age" in expected_features and age is not None:
            input_dict["age"] = age
        if "age_2022" in expected_features and age_2022 is not None:
            input_dict["age_2022"] = age_2022
        if "deficiency" in expected_features:
            input_dict["deficiency"] = 1.0 if deficiency == "Sim" else 0.0
        if "gender" in expected_features:
            input_dict["gender"] = gender
        if "school_institution" in expected_features:
            input_dict["school_institution"] = school_map.get(school_institution, school_institution)
        if "achieved_turning_point" in expected_features:
            input_dict["achieved_turning_point"] = tp_map.get(achieved_turning_point, achieved_turning_point)
        if "indicated_for_intervention" in expected_features:
            input_dict["indicated_for_intervention"] = tp_map.get(indicated_for_intervention, indicated_for_intervention)

        if "inde_combined" in expected_features and inde_combined is not None:
            input_dict["inde_combined"] = inde_combined
        if has_ipp and ipp is not None:
            input_dict["ipp"] = ipp

        input_df = pd.DataFrame([input_dict])
        scored = ensure_cols(input_df, expected_features)[expected_features]
        prob = float(model.predict_proba(scored)[0, 1])

        st.markdown("---")
        col_res1, col_res2 = st.columns([1, 2])

        with col_res1:
            st.subheader("Resultado")
            color = risk_color(prob)
            label = risk_label(prob)
            st.markdown(
                f"<div style='background:{color};padding:24px;border-radius:12px;text-align:center;'>"
                f"<p style='color:white;font-size:1.3rem;margin:0;font-weight:bold;'>{label}</p>"
                f"<p style='color:white;font-size:2.4rem;margin:4px 0;font-weight:bold;'>{prob:.1%}</p>"
                f"<p style='color:rgba(255,255,255,0.85);margin:0;font-size:0.9rem;'>probabilidade de risco no proximo ciclo</p>"
                f"</div>",
                unsafe_allow_html=True,
            )
            st.markdown(" ")
            if "phase" in expected_features:
                st.metric("Fase", phase)
            if "year" in expected_features:
                st.metric("Ano de referencia", year)
            if inde_combined is not None:
                delta_inde = inde_combined - q1_thr
                st.metric(
                    "INDE atual vs. limiar de risco",
                    f"{inde_combined:.2f}",
                    delta=f"{delta_inde:+.2f} vs. {q1_thr:.2f}",
                    delta_color="normal",
                )

        with col_res2:
            st.subheader("Perfil de indicadores")
            indicators = {
                "IAN": ian, "IDA": ida, "IEG": ieg,
                "IAA": iaa, "IPS": ips, "IPV": ipv,
            }
            if has_ipp and ipp is not None:
                indicators["IPP"] = ipp

            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=list(indicators.keys()),
                y=list(indicators.values()),
                marker_color=[
                    "#c0392b" if v < 4 else "#e67e22" if v < 6 else "#27ae60"
                    for v in indicators.values()
                ],
                text=[f"{v:.1f}" for v in indicators.values()],
                textposition="outside",
            ))
            fig.update_layout(
                yaxis=dict(range=[0, 11], title="Valor"),
                xaxis_title="Indicador",
                height=300,
                margin=dict(t=20, b=20),
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
            )
            fig.add_hline(
                y=4, line_dash="dash", line_color="red", opacity=0.4,
                annotation_text="limite critico (4.0)"
            )
            st.plotly_chart(fig, use_container_width=True)

        st.markdown("---")
        st.subheader("Recomendacoes de intervencao")
        form_inputs = {
            "ian": ian, "ida": ida, "ieg": ieg, "iaa": iaa, "ips": ips, "ipv": ipv,
            "math": math, "portuguese": portuguese, "english": english,
            "inde_combined": inde_combined,
            "indicated_for_intervention": indicated_for_intervention,
            "achieved_turning_point": achieved_turning_point,
        }
        for rec in build_recommendations(prob, form_inputs, q1_threshold=q1_thr):
            st.markdown(f"- {rec}")

        st.markdown("---")
        st.info(
            "Este sistema e uma ferramenta de apoio a equipe pedagogica e nao substitui "
            "a avaliacao individualizada pelos profissionais da Passos Magicos."
        )


# ══════════════════════════════════════════════════════════════════════════════
# ABA 2 — PREDICAO EM MASSA
# ══════════════════════════════════════════════════════════════════════════════

with tab_massa:
    st.subheader("Scoring em lote via CSV")
    st.markdown(
        "Envie um arquivo CSV com multiplos alunos para gerar probabilidades de risco "
        "e ranking de priorizacao em uma unica operacao."
    )

    with st.expander("Colunas esperadas no CSV", expanded=False):
        st.code(", ".join(expected_features), language="text")
        m_info = metadata.get("winner_metrics", {}) if metadata else {}
        st.write(
            f"**Modelo:** {metadata.get('winner_model', '-')} | "
            f"**Track:** {winner_track} | "
            f"**Recall:** {m_info.get('recall', 0):.3f} | "
            f"**ROC-AUC:** {m_info.get('roc_auc', 0):.3f}"
        )
        if expected_features:
            template_csv = pd.DataFrame(columns=expected_features).to_csv(index=False).encode("utf-8")
            st.download_button(
                label="Download template CSV (colunas vazias)",
                data=template_csv,
                file_name="template_scoring.csv",
                mime="text/csv",
            )

    score_threshold = st.slider(
        "Limiar de classificacao de risco",
        min_value=0.10, max_value=0.90, value=0.50, step=0.05,
        help=(
            "Probabilidade acima da qual o aluno é classificado como 'em risco'. "
            "Reduza para aumentar a sensibilidade (mais alunos identificados, mais falsos positivos). "
            "O valor padrão 0.50 é o ponto de equilíbrio do modelo."
        ),
    )

    uploaded = st.file_uploader("Envie um CSV com dados de alunos", type=["csv"])

    if uploaded is not None:
        input_df = pd.read_csv(uploaded)
        st.subheader("Amostra de entrada")
        st.dataframe(input_df.head(10), use_container_width=True)

        scored_base = ensure_cols(input_df, expected_features)[expected_features].copy()
        probs = model.predict_proba(scored_base)[:, 1]
        preds = (probs >= score_threshold).astype(int)

        result = input_df.copy()
        result["prob_risco"] = probs
        result["classe_risco"] = preds
        result["prioridade"] = pd.qcut(
            result["prob_risco"],
            q=4,
            labels=["baixa", "media", "alta", "critica"],
            duplicates="drop",
        )
        result = result.sort_values("prob_risco", ascending=False).reset_index(drop=True)

        col_m1, col_m2, col_m3, col_m4 = st.columns(4)
        col_m1.metric("Total de alunos", len(result))
        col_m2.metric("Em risco (>=50%)", int((probs >= 0.5).sum()))
        col_m3.metric("Prioridade critica", int((result["prioridade"] == "critica").sum()))
        col_m4.metric("Prob. media", f"{probs.mean():.1%}")

        st.subheader("Resultado de scoring")
        st.dataframe(result.head(100), use_container_width=True)

        csv_out = result.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="Baixar resultado (CSV)",
            data=csv_out,
            file_name="scoring_risco.csv",
            mime="text/csv",
        )


# ── rodape ───────────────────────────────────────────────────────────────────

st.markdown("---")
st.markdown(
    "<div style='text-align:center;color:#888;font-size:0.85rem'>"
    "Tech Challenge Fase 5 - POSTECH Data Analytics - "
    "Associacao Passos Magicos - Sistema de Risco Academico"
    "</div>",
    unsafe_allow_html=True,
)
