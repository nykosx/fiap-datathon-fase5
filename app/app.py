import json
import re
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(
    page_title="Risco de Defasagem - Passos Magicos",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed",
)

PROJECT_ROOT = Path(__file__).resolve().parent.parent
MODEL_PATH = PROJECT_ROOT / "models" / "model_risco.joblib"
METADATA_PATH = PROJECT_ROOT / "outputs" / "model_risco_metadata.json"
OFFICIAL_DATA_PATH = PROJECT_ROOT / "data" / "dados_unificados.csv"


@st.cache_resource
def load_artifacts():
    metadata = None
    if METADATA_PATH.exists():
        with open(METADATA_PATH, "r", encoding="utf-8") as fp:
            metadata = json.load(fp)
    model = joblib.load(MODEL_PATH)
    return metadata, model


def parse_risk_threshold_from_target(target_definition: str, default: float = 5.0) -> float:
    if not target_definition:
        return default
    match = re.search(r"<=\s*([0-9]+(?:\.[0-9]+)?)", target_definition)
    if not match:
        return default
    try:
        return float(match.group(1))
    except ValueError:
        return default


def ensure_cols(df: pd.DataFrame, cols: list[str]) -> pd.DataFrame:
    out = df.copy()
    for col in cols:
        if col not in out.columns:
            out[col] = np.nan
    return out


_PHASE_MAP = {
    "alfa": "ALFA",
    "0": "ALFA",
    "1": "FASE 1",
    "fase1": "FASE 1",
    "fase 1": "FASE 1",
    "2": "FASE 2",
    "fase2": "FASE 2",
    "fase 2": "FASE 2",
    "3": "FASE 3",
    "fase3": "FASE 3",
    "fase 3": "FASE 3",
    "4": "FASE 4",
    "fase4": "FASE 4",
    "fase 4": "FASE 4",
    "5": "FASE 5",
    "fase5": "FASE 5",
    "fase 5": "FASE 5",
    "6": "FASE 6",
    "fase6": "FASE 6",
    "fase 6": "FASE 6",
    "7": "FASE 7",
    "fase7": "FASE 7",
    "fase 7": "FASE 7",
    "8": "FASE 8",
    "fase8": "FASE 8",
    "fase 8": "FASE 8",
}


def canonicalize_phase(value):
    if value is None or (isinstance(value, float) and np.isnan(value)):
        return np.nan
    token = str(value).strip().lower()
    if token in _PHASE_MAP:
        return _PHASE_MAP[token]

    m = re.match(r"^(\d+)", token)
    if m:
        n = int(m.group(1))
        if n == 0:
            return "ALFA"
        if 1 <= n <= 8:
            return f"FASE {n}"
    return np.nan


def prepare_scoring_frame(df: pd.DataFrame, expected_features: list[str]) -> pd.DataFrame:
    working = df.copy()

    if "fase_padronizada" in expected_features and "fase_padronizada" not in working.columns:
        if "phase" in working.columns:
            working["fase_padronizada"] = working["phase"].apply(canonicalize_phase)

    scored = ensure_cols(working, expected_features)[expected_features].copy()
    scored = scored.replace({pd.NA: np.nan})

    categorical_features = {
        "year",
        "fase_padronizada",
        "gender",
        "school_institution",
        "achieved_turning_point",
        "indicated_for_intervention",
    }

    for col in scored.columns:
        if col in categorical_features:
            scored[col] = scored[col].replace(["", " ", "nan", "None", "NA", "N/A"], np.nan)
        else:
            scored[col] = pd.to_numeric(scored[col], errors="coerce")

    return scored


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


def build_recommendations(prob: float, inputs: dict, ian_threshold: float = 5.0) -> list[str]:
    recs = []

    ian = float(inputs.get("ian", 10.0) or 10.0)
    ida = float(inputs.get("ida", 10.0) or 10.0)
    ieg = float(inputs.get("ieg", 10.0) or 10.0)
    iaa = float(inputs.get("iaa", 10.0) or 10.0)
    ips = float(inputs.get("ips", 10.0) or 10.0)
    ipv = float(inputs.get("ipv", 10.0) or 10.0)

    if prob >= 0.7:
        recs.append("🔴 **Atencao prioritaria:** Alta probabilidade de defasagem no proximo ciclo. Acionar intervencao imediata.")
    elif prob >= 0.5:
        recs.append("🟠 **Acompanhamento proximo:** Probabilidade elevada de defasagem. Inserir no monitoramento mensal.")
    elif prob >= 0.3:
        recs.append("🟡 **Zona de atencao:** Risco moderado. Monitorar tendencia e reforcar suporte pedagogico.")
    else:
        recs.append("🟢 **Perfil estavel:** Baixo risco estimado no proximo ciclo. Manter acompanhamento regular.")

    if ian <= ian_threshold:
        recs.append(
            f"**IAN atual ({ian:.2f}) no limite de risco ({ian_threshold:.2f}) ou abaixo:** priorizar plano de recuperacao academica e nivelamento."
        )
    elif ian <= ian_threshold + 1.0:
        recs.append(
            f"**IAN atual ({ian:.2f}) proximo do limite de risco ({ian_threshold:.2f}):** pequena piora pode levar a defasagem no ciclo seguinte."
        )

    if ida < 6:
        recs.append("**IDA em desenvolvimento:** revisar lacunas de conteudo e frequencia de atividades.")
    if ieg < 6:
        recs.append("**IEG abaixo do ideal:** reforcar engajamento com mentoria e combinados de participacao.")
    if iaa < 6:
        recs.append("**IAA abaixo do ideal:** aplicar feedback estruturado para fortalecer autopercepcao.")
    if ips < 6:
        recs.append("**IPS abaixo do ideal:** investigar contexto psicossocial e rede de apoio.")
    if ipv < 6:
        recs.append("**IPV abaixo do ideal:** definir metas de curto prazo e acompanhar marcos de progresso.")

    return recs


def resolve_expected_features(metadata: dict | None) -> tuple[str, list[str]]:
    winner_track = metadata.get("winner_track", "trilha_temporal_sem_ipp") if metadata else "trilha_temporal_sem_ipp"
    expected_features = []
    if metadata:
        if winner_track in {"trilha2_com_ipp", "trilha_core_com_ipp", "trilha_temporal_com_ipp"}:
            track_key = "track2"
        else:
            track_key = "track1"
        expected_features = (metadata.get(track_key) or {}).get("features", [])
    return winner_track, expected_features


def render_header(metadata: dict | None):
    st.title("Sistema de Risco Academico - Passos Magicos")

    metrics = metadata.get("winner_metrics", {}) if metadata else {}
    target_definition = metadata.get("target_definition", "target_risco_next = 1 quando ian_next_year <= 5") if metadata else "target_risco_next = 1 quando ian_next_year <= 5"

    st.caption(
        "Identificacao precoce de alunos em risco de defasagem no ciclo seguinte. "
        f"Modelo: {metadata.get('winner_model', 'random_forest') if metadata else 'random_forest'} | "
        f"Recall: {metrics.get('recall', 0):.1%} | ROC-AUC: {metrics.get('roc_auc', 0):.3f}"
    )

    st.info(
        "Definicao atual de risco no projeto: "
        f"**{target_definition}**"
    )


def render_individual_tab(model, metadata: dict | None, expected_features: list[str], has_ipp: bool, ian_threshold: float):
    st.subheader("Avaliacao de um aluno")

    metrics = metadata.get("winner_metrics", {}) if metadata else {}

    with st.expander("Como interpretar o score", expanded=False):
        st.markdown(
            "- **Recall**: de cada 100 alunos que realmente entram em risco, quantos o modelo sinaliza.\n"
            "- **Precisao**: de cada 100 alertas, quantos sao casos reais de risco.\n"
            "- **Ponto de corte de alerta**: limite para classificar como risco no uso operacional."
        )

    with st.form("form_aluno"):
        col_a, col_b, col_c = st.columns(3)

        with col_a:
            st.markdown("**Dados cadastrais**")
            year = st.selectbox("Ano de referencia", ["PEDE2022", "PEDE2023", "PEDE2024"]) if "year" in expected_features else "PEDE2024"
            phase_options = ["Alfa", "Fase 1", "Fase 2", "Fase 3", "Fase 4", "Fase 5", "Fase 6", "Fase 7", "Fase 8"]
            show_phase = "fase_padronizada" in expected_features or "phase" in expected_features
            phase_str = st.selectbox("Fase atual", phase_options) if show_phase else "Fase 4"

            age = st.number_input("Idade atual", min_value=6, max_value=25, value=13, step=1) if "age" in expected_features else None
            gender = st.selectbox("Genero", ["Feminino", "Masculino"]) if "gender" in expected_features else "Feminino"
            school_institution = (
                st.selectbox("Instituicao escolar", ["Escola Publica", "Rede Decisao", "Escola Privada", "Outros"])
                if "school_institution" in expected_features
                else "Escola Publica"
            )

        with col_b:
            st.markdown("**Indicadores Passos Magicos**")
            ian = st.slider("IAN", 0.0, 10.0, 5.0, 0.1)
            ida = st.slider("IDA", 0.0, 10.0, 5.0, 0.1)
            ieg = st.slider("IEG", 0.0, 10.0, 5.0, 0.1)
            iaa = st.slider("IAA", 0.0, 10.0, 5.0, 0.1)
            ips = st.slider("IPS", 0.0, 10.0, 5.0, 0.1)
            ipv = st.slider("IPV", 0.0, 10.0, 5.0, 0.1)
            ipp = st.slider("IPP", 0.0, 10.0, 5.0, 0.1) if has_ipp else None

        with col_c:
            st.markdown("**Desempenho escolar**")
            math = st.slider("Matematica", 0.0, 10.0, 5.0, 0.1)
            portuguese = st.slider("Portugues", 0.0, 10.0, 5.0, 0.1)
            english = st.slider("Ingles", 0.0, 10.0, 5.0, 0.1)
            achieved_turning_point = st.selectbox("Atingiu ponto de virada?", ["Nao", "Sim"])
            indicated_for_intervention = st.selectbox("Ja indicado para intervencao?", ["Nao", "Sim"])

        submitted = st.form_submit_button("Calcular risco", use_container_width=True)

    if not submitted:
        return

    school_map = {
        "Escola Publica": "Escola Pública",
        "Rede Decisao": "Rede Decisão",
        "Escola Privada": "Escola Privada",
        "Outros": "Outros",
    }
    sim_nao_map = {"Nao": "Não", "Sim": "Sim"}

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
    if "fase_padronizada" in expected_features:
        input_dict["fase_padronizada"] = canonicalize_phase(phase_str)
    elif "phase" in expected_features:
        input_dict["phase"] = phase_str
    if "age" in expected_features and age is not None:
        input_dict["age"] = age
    if "gender" in expected_features:
        input_dict["gender"] = gender
    if "school_institution" in expected_features:
        input_dict["school_institution"] = school_map.get(school_institution, school_institution)
    if "achieved_turning_point" in expected_features:
        input_dict["achieved_turning_point"] = sim_nao_map.get(achieved_turning_point, achieved_turning_point)
    if "indicated_for_intervention" in expected_features:
        input_dict["indicated_for_intervention"] = sim_nao_map.get(indicated_for_intervention, indicated_for_intervention)
    if has_ipp and ipp is not None:
        input_dict["ipp"] = ipp

    scored = prepare_scoring_frame(pd.DataFrame([input_dict]), expected_features)
    prob = float(model.predict_proba(scored)[0, 1])

    st.markdown("---")
    col_res1, col_res2 = st.columns([1, 2])

    with col_res1:
        color = risk_color(prob)
        label = risk_label(prob)
        st.markdown(
            f"<div style='background:{color};padding:20px;border-radius:12px;text-align:center;'>"
            f"<p style='color:white;font-size:1.2rem;margin:0;font-weight:bold;'>{label}</p>"
            f"<p style='color:white;font-size:2.2rem;margin:4px 0;font-weight:bold;'>{prob:.1%}</p>"
            f"<p style='color:rgba(255,255,255,0.90);margin:0;font-size:0.9rem;'>probabilidade de risco no proximo ciclo</p>"
            f"</div>",
            unsafe_allow_html=True,
        )
        st.metric("Limiar de risco usado no alvo (IAN)", f"<= {ian_threshold:.2f}")
        st.metric("Recall do modelo", f"{metrics.get('recall', 0):.1%}")
        st.metric("Precisao dos alertas", f"{metrics.get('precision', 0):.1%}")

    with col_res2:
        indicators = {
            "IAN": ian,
            "IDA": ida,
            "IEG": ieg,
            "IAA": iaa,
            "IPS": ips,
            "IPV": ipv,
        }
        if has_ipp and ipp is not None:
            indicators["IPP"] = ipp

        fig = go.Figure()
        fig.add_trace(
            go.Bar(
                x=list(indicators.keys()),
                y=list(indicators.values()),
                marker_color=["#c0392b" if v < 4 else "#e67e22" if v < 6 else "#27ae60" for v in indicators.values()],
                text=[f"{v:.1f}" for v in indicators.values()],
                textposition="outside",
            )
        )
        fig.update_layout(
            yaxis=dict(range=[0, 11], title="Valor"),
            xaxis_title="Indicador",
            height=300,
            margin=dict(t=10, b=10),
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
        )
        fig.add_hline(y=ian_threshold, line_dash="dash", line_color="red", opacity=0.4, annotation_text=f"limiar IAN ({ian_threshold:.2f})")
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    st.subheader("Recomendacoes de intervencao")
    form_inputs = {
        "ian": ian,
        "ida": ida,
        "ieg": ieg,
        "iaa": iaa,
        "ips": ips,
        "ipv": ipv,
        "math": math,
        "portuguese": portuguese,
        "english": english,
        "achieved_turning_point": achieved_turning_point,
        "indicated_for_intervention": indicated_for_intervention,
    }

    for rec in build_recommendations(prob, form_inputs, ian_threshold=ian_threshold):
        st.markdown(f"- {rec}")


def render_batch_tab(model, metadata: dict | None, expected_features: list[str]):
    st.subheader("Predicao em massa (CSV)")
    st.markdown("Envie um CSV para gerar probabilidades de risco e ranking de priorizacao em lote.")

    with st.expander("Colunas esperadas no CSV", expanded=False):
        st.code(", ".join(expected_features), language="text")

    score_threshold = st.slider(
        "Ponto de corte de alerta",
        min_value=0.10,
        max_value=0.90,
        value=0.50,
        step=0.05,
        help="Valores menores aumentam cobertura, mas tambem aumentam alertas falsos.",
    )

    uploaded = st.file_uploader("Envie um CSV com dados de alunos", type=["csv"])
    use_official_2024 = st.checkbox(
        "Usar base oficial 2024 (dados_unificados.csv) quando nao houver upload",
        value=False,
    )

    input_df = None
    source_label = None

    if uploaded is not None:
        input_df = pd.read_csv(uploaded)
        source_label = "CSV enviado"
    elif use_official_2024:
        if not OFFICIAL_DATA_PATH.exists():
            st.error(f"Base oficial nao encontrada em: {OFFICIAL_DATA_PATH}")
            return

        base_df = pd.read_csv(OFFICIAL_DATA_PATH)
        if "year" in base_df.columns:
            input_df = base_df[base_df["year"].astype(str).str.contains("2024", na=False)].copy()
        else:
            input_df = base_df.copy()
        source_label = "Base oficial 2024"

    if input_df is None:
        return

    if input_df.empty:
        st.warning("Nenhuma linha disponivel para scoring.")
        return

    st.caption(f"Fonte utilizada: {source_label}")
    st.dataframe(input_df.head(10), use_container_width=True)

    scored = prepare_scoring_frame(input_df, expected_features)
    probs = model.predict_proba(scored)[:, 1]
    preds = (probs >= score_threshold).astype(int)

    result = input_df.copy()
    result["prob_risco"] = probs
    result["classe_risco"] = preds
    result["prioridade"] = pd.qcut(result["prob_risco"], q=4, labels=["baixa", "media", "alta", "critica"], duplicates="drop")
    result = result.sort_values("prob_risco", ascending=False).reset_index(drop=True)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total de alunos", len(result))
    c2.metric(f"Em risco (>= {score_threshold:.2f})", int((probs >= score_threshold).sum()))
    c3.metric("Prioridade critica", int((result["prioridade"] == "critica").sum()))
    c4.metric("Probabilidade media", f"{probs.mean():.1%}")

    st.subheader("Resultado de scoring")
    st.dataframe(result.head(100), use_container_width=True)

    csv_out = result.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Baixar resultado (CSV)",
        data=csv_out,
        file_name="scoring_risco.csv",
        mime="text/csv",
    )


if not MODEL_PATH.exists():
    st.error(f"Modelo nao encontrado em: {MODEL_PATH}")
    st.stop()

metadata, model = load_artifacts()
winner_track, expected_features = resolve_expected_features(metadata)
has_ipp = "ipp" in expected_features
ian_threshold = parse_risk_threshold_from_target((metadata or {}).get("target_definition", ""), default=5.0)

render_header(metadata)
st.markdown("---")

tab_individual, tab_batch = st.tabs(["Aluno individual", "Predicao em massa"])

with tab_individual:
    render_individual_tab(model, metadata, expected_features, has_ipp, ian_threshold)

with tab_batch:
    render_batch_tab(model, metadata, expected_features)

st.markdown("---")
st.markdown(
    "<div style='text-align:center;color:#888;font-size:0.85rem'>"
    "Tech Challenge Fase 5 - POSTECH Data Analytics - Sistema de Risco Academico"
    "</div>",
    unsafe_allow_html=True,
)
