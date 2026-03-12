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


def build_recommendations(prob: float, inputs: dict) -> list:
    """Recomendacoes contextualizadas ao perfil do aluno."""
    recs = []

    if prob >= 0.7:
        recs.append(
            "**Atencao prioritaria:** Este aluno apresenta alta probabilidade de defasagem. "
            "Recomenda-se intervencao imediata pela equipe pedagogica."
        )
    elif prob >= 0.5:
        recs.append(
            "**Acompanhamento proximo:** Probabilidade elevada de defasagem. "
            "Inclua este aluno nos ciclos de monitoramento mensal."
        )

    ian = inputs.get("ian", 10)
    ida = inputs.get("ida", 10)
    ieg = inputs.get("ieg", 10)
    iaa = inputs.get("iaa", 10)
    ips = inputs.get("ips", 10)
    ipv = inputs.get("ipv", 10)

    if ian < 4:
        recs.append(
            "**IAN baixo (adequacao de nivel):** O aluno esta significativamente abaixo "
            "do esperado para sua fase. Considere reforco individualizado ou revisao de nivelamento."
        )
    elif ian < 6:
        recs.append(
            "**IAN moderado:** Ha lacunas de conteudo em relacao a fase. "
            "Recomenda-se atividades de recuperacao paralela."
        )

    if ida < 4:
        recs.append(
            "**IDA baixo (desenvolvimento academico):** Progressao academica abaixo do esperado. "
            "Revise frequencia, participacao em aulas e entrega de atividades."
        )

    if ieg < 4:
        recs.append(
            "**IEG baixo (engajamento):** Baixo engajamento com o programa. "
            "Estrategias de motivacao, mentoria e atividades extracurriculares podem ajudar."
        )

    if iaa < 4:
        recs.append(
            "**IAA baixo (autoavaliacao):** O aluno demonstra baixa percepcao de suas proprias "
            "capacidades. Sessoes de coaching e reforco de autoestima sao recomendadas."
        )

    if ips < 4:
        recs.append(
            "**IPS baixo (psicossocial):** Indicadores de vulnerabilidade psicossocial. "
            "Acionar assistente social ou psicologo da equipe Passos Magicos."
        )

    if ipv < 4:
        recs.append(
            "**IPV baixo (ponto de virada):** O aluno ainda nao atingiu seu ponto de virada. "
            "Intensifique o acompanhamento de metas de curto prazo e celebre pequenas conquistas."
        )

    math = inputs.get("math", 10)
    port = inputs.get("portuguese", 10)
    eng = inputs.get("english", 10)
    low_grades = [s for s, v in [("Matematica", math), ("Portugues", port), ("Ingles", eng)] if v < 4]
    if low_grades:
        recs.append(
            f"**Notas criticas em:** {', '.join(low_grades)}. "
            "Recomenda-se reforco especifico nessas disciplinas, preferencialmente em grupos reduzidos."
        )

    if inputs.get("indicated_for_intervention") == "Sim":
        recs.append(
            "**Aluno ja indicado para intervencao:** Verificar se o plano de acao esta ativo "
            "e documentar evolucao no proximo ciclo de avaliacao."
        )

    if inputs.get("achieved_turning_point") == "Nao":
        recs.append(
            "**Ponto de virada nao alcancado:** Definir um objetivo concreto e mensuravel "
            "junto ao aluno para o proximo trimestre."
        )

    if not recs:
        recs.append(
            "Perfil sem alertas criticos. Manter acompanhamento regular e incentivar "
            "a continuidade dos bons indicadores."
        )

    return recs


# ── carrega artefatos ─────────────────────────────────────────────────────────

if not MODEL_PATH.exists():
    st.error(f"Modelo nao encontrado em: {MODEL_PATH}")
    st.stop()

metadata, model = load_artifacts()

winner_track = metadata.get("winner_track", "trilha2_com_ipp") if metadata else "trilha2_com_ipp"
expected_features = []
if metadata:
    track_key = "track2" if winner_track == "trilha2_com_ipp" else "track1"
    expected_features = metadata.get(track_key, {}).get("features", [])

has_ipp = "ipp" in expected_features


# ── cabecalho ────────────────────────────────────────────────────────────────

st.title("Sistema de Risco Academico - Passos Magicos")
st.caption(
    "Identificacao precoce de alunos em risco de defasagem educacional. "
    "Modelo: regressao logistica | Recall: 0.901 | ROC-AUC: 0.931"
)
st.markdown("---")

tab_individual, tab_massa = st.tabs(["Aluno Individual", "Predicao em Massa (CSV)"])


# ══════════════════════════════════════════════════════════════════════════════
# ABA 1 — ALUNO INDIVIDUAL
# ══════════════════════════════════════════════════════════════════════════════

with tab_individual:
    st.subheader("Avaliacao de um aluno")
    st.markdown(
        "Preencha os indicadores do aluno para obter a probabilidade de risco de defasagem "
        "e recomendacoes de intervencao personalizadas."
    )

    with st.form("form_aluno"):
        col_a, col_b, col_c = st.columns(3)

        with col_a:
            st.markdown("**Dados Cadastrais**")
            year = st.selectbox(
                "Ano de referencia",
                ["PEDE2022", "PEDE2023", "PEDE2024"],
                help="Captura efeito de coorte/tempo. Ex.: perfis 2022 e 2024 podem ter distribuicoes diferentes.",
            )
            phase = st.slider("Fase atual", min_value=1, max_value=8, value=4)
            admission_year = st.number_input(
                "Ano de ingresso", min_value=2010, max_value=2024, value=2020, step=1
            )
            age = st.number_input("Idade atual", min_value=6, max_value=25, value=13, step=1)
            ref_year_num = int(year.replace("PEDE", ""))
            age_2022 = max(0, int(age - (ref_year_num - 2022)))
            st.caption(f"Idade em 2022 (calculada automaticamente): **{age_2022}**")
            gender = st.selectbox("Genero", ["Menina", "Menino"])
            school_institution = st.selectbox(
                "Instituicao escolar", ["Escola Publica", "Rede Decisao"]
            )

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
                help="Indicador de bem-estar psicossocial e condicao socioeconomica."
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
            st.markdown("**Notas e Situacao**")
            math = st.slider("Matematica", 0.0, 10.0, 5.0, 0.1)
            portuguese = st.slider("Portugues", 0.0, 10.0, 5.0, 0.1)
            english = st.slider("Ingles", 0.0, 10.0, 5.0, 0.1)
            deficiency = st.selectbox("Possui deficiencia?", ["Nao", "Sim"])
            achieved_turning_point = st.selectbox("Atingiu ponto de virada?", ["Nao", "Sim"])
            indicated_for_intervention = st.selectbox(
                "Indicado para intervencao?", ["Nao", "Sim"]
            )

        submitted = st.form_submit_button("Calcular Risco", use_container_width=True)

    if submitted:
        # mapeia valores do formulario para os esperados pelo modelo
        school_map = {"Escola Publica": "Escola Pública", "Rede Decisao": "Rede Decisão"}
        tp_map = {"Nao": "Não", "Sim": "Sim"}

        input_dict = {
            "year": year,
            "phase": phase,
            "admission_year": admission_year,
            "age": age,
            "age_2022": age_2022,
            "ian": ian,
            "ida": ida,
            "ieg": ieg,
            "iaa": iaa,
            "ips": ips,
            "ipv": ipv,
            "math": math,
            "portuguese": portuguese,
            "english": english,
            "deficiency": 1.0 if deficiency == "Sim" else 0.0,
            "gender": "Menina" if gender == "Menina" else "Menino",
            "school_institution": school_map.get(school_institution, school_institution),
            "achieved_turning_point": tp_map.get(achieved_turning_point, achieved_turning_point),
            "indicated_for_intervention": tp_map.get(indicated_for_intervention, indicated_for_intervention),
        }
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
                f"<p style='color:rgba(255,255,255,0.85);margin:0;font-size:0.9rem;'>probabilidade de risco</p>"
                f"</div>",
                unsafe_allow_html=True,
            )
            st.markdown(" ")
            st.metric("Fase", phase)
            st.metric("Ano de referencia", year)

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
            "indicated_for_intervention": indicated_for_intervention,
            "achieved_turning_point": achieved_turning_point,
        }
        for rec in build_recommendations(prob, form_inputs):
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

    uploaded = st.file_uploader("Envie um CSV com dados de alunos", type=["csv"])

    if uploaded is not None:
        input_df = pd.read_csv(uploaded)
        st.subheader("Amostra de entrada")
        st.dataframe(input_df.head(10), use_container_width=True)

        scored_base = ensure_cols(input_df, expected_features)[expected_features].copy()
        probs = model.predict_proba(scored_base)[:, 1]
        preds = (probs >= 0.5).astype(int)

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
