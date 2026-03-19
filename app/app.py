import json
import sys
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.config import METADATA_PATH, MODEL_PATH, OFFICIAL_DATA_PATH
from src.utils import canonicalize_phase, parse_risk_threshold_from_target, prepare_scoring_frame

CAPACITY_PATH = PROJECT_ROOT / "outputs" / "modelagem_tradeoff_capacidade.csv"

st.set_page_config(
    page_title="Risco de Defasagem - Passos Magicos",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed",
)

@st.cache_resource
def load_artifacts():
    metadata = None
    if METADATA_PATH.exists():
        with open(METADATA_PATH, "r", encoding="utf-8") as fp:
            metadata = json.load(fp)
    model = joblib.load(MODEL_PATH)
    return metadata, model


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


def build_driver_summary(inputs: dict) -> list[str]:
    """Gera explicacao local simples baseada em indicadores informados."""
    drivers = []
    indicator_labels = {
        "ian": "IAN",
        "ida": "IDA",
        "ieg": "IEG",
        "iaa": "IAA",
        "ips": "IPS",
        "ipv": "IPV",
    }

    gaps = []
    for key, label in indicator_labels.items():
        val = float(inputs.get(key, 10.0) or 10.0)
        gaps.append((label, val, 10.0 - val))

    for label, val, gap in sorted(gaps, key=lambda x: x[2], reverse=True)[:3]:
        if val < 6.0:
            drivers.append(f"{label} baixo ({val:.1f}) sugere maior vulnerabilidade no proximo ciclo.")

    if not drivers:
        drivers.append("Indicadores principais estao em faixa estavel; risco depende mais da combinacao global dos sinais.")
    return drivers


def batch_action_from_prob(prob: float) -> str:
    if prob >= 0.75:
        return "Intervencao imediata (72h)"
    if prob >= 0.55:
        return "Plano pedagogico em ate 2 semanas"
    if prob >= 0.35:
        return "Monitoramento quinzenal"
    return "Acompanhamento regular"


def validate_batch_input(input_df: pd.DataFrame, expected_features: list[str]) -> tuple[pd.DataFrame, dict]:
    report = {
        "missing_columns": [],
        "null_rates": {},
        "unknown_categories": {},
        "warnings": [],
    }

    missing_columns = [c for c in expected_features if c not in input_df.columns]
    report["missing_columns"] = missing_columns

    numeric_candidates = [c for c in ["age", "ian", "ida", "ieg", "iaa", "ips", "ipv", "ipp"] if c in input_df.columns]
    categorical_expected = {
        "gender": {"Feminino", "Masculino"},
        "school_institution": {"Escola Pública", "Escola Publica", "Rede Decisão", "Rede Decisao", "Escola Privada", "Outros"},
        "fase_padronizada": {"Alfa", "Fase 1", "Fase 2", "Fase 3", "Fase 4", "Fase 5", "Fase 6", "Fase 7", "Fase 8"},
    }

    for col in input_df.columns:
        report["null_rates"][col] = float(input_df[col].isna().mean())

    for col in numeric_candidates:
        converted = pd.to_numeric(input_df[col], errors="coerce")
        if converted.isna().mean() > input_df[col].isna().mean():
            report["warnings"].append(f"Coluna {col}: valores nao numericos foram detectados e serao imputados no pipeline.")

    for col, allowed in categorical_expected.items():
        if col in input_df.columns:
            observed = set(input_df[col].dropna().astype(str).str.strip().unique().tolist())
            unknown = sorted([v for v in observed if v not in allowed])
            if unknown:
                report["unknown_categories"][col] = unknown[:20]

    if missing_columns:
        report["warnings"].append("Ha colunas ausentes em relacao ao esperado pelo modelo.")

    high_null = [c for c, r in report["null_rates"].items() if r >= 0.5]
    if high_null:
        report["warnings"].append("Algumas colunas possuem >= 50% de nulos e podem reduzir confiabilidade do score.")

    return input_df, report


def load_capacity_presets() -> pd.DataFrame | None:
    if not CAPACITY_PATH.exists():
        return None
    try:
        df = pd.read_csv(CAPACITY_PATH)
    except Exception:
        return None
    required = {"capacidade_max_alertas", "ponto_de_corte_sugerido", "cobertura_risco_detectado", "taxa_de_acerto_dos_alertas"}
    if not required.issubset(df.columns):
        return None
    return df


def resolve_expected_features(metadata: dict | None) -> tuple[str, list[str]]:
    winner_track = metadata.get("winner_track", "trilha_temporal_sem_ipp") if metadata else "trilha_temporal_sem_ipp"
    expected_features = (metadata.get("track1") or {}).get("features", []) if metadata else []
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
        col_a, col_b = st.columns(2)

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
    }

    st.markdown("**Fatores que mais pesaram no score (explicacao local simplificada)**")
    for driver in build_driver_summary(form_inputs):
        st.markdown(f"- {driver}")

    st.markdown("**Acoes sugeridas**")
    for rec in build_recommendations(prob, form_inputs, ian_threshold=ian_threshold):
        st.markdown(f"- {rec}")


def render_batch_tab(model, metadata: dict | None, expected_features: list[str]):
    st.subheader("Predicao em massa (CSV)")
    st.markdown("Envie um CSV para gerar probabilidades de risco e ranking de priorizacao em lote.")

    # Template simples para a equipe preencher com as colunas minimas esperadas.
    template_defaults = {
        "year": "PEDE2024",
        "fase_padronizada": "Fase 4",
        "age": 13,
        "ida": 6.0,
        "ieg": 6.0,
        "iaa": 6.0,
        "ips": 6.0,
        "ipv": 6.0,
        "gender": "Feminino",
        "school_institution": "Escola Pública",
        "phase": "Fase 4",
        "ipp": 6.0,
    }
    template_row = {col: template_defaults.get(col, "") for col in expected_features}
    template_df = pd.DataFrame([template_row])
    st.download_button(
        label="Baixar CSV modelo",
        data=template_df.to_csv(index=False).encode("utf-8"),
        file_name="modelo_entrada_scoring.csv",
        mime="text/csv",
        help="Use este arquivo como guia de preenchimento para o scoring em lote.",
    )

    with st.expander("Colunas esperadas no CSV", expanded=False):
        st.code(", ".join(expected_features), language="text")

    capacity_df = load_capacity_presets()
    mode = st.radio(
        "Modo de definicao do ponto de corte",
        options=["Manual", "Por capacidade operacional"],
        horizontal=True,
    )

    if mode == "Manual" or capacity_df is None:
        score_threshold = st.slider(
            "Ponto de corte de alerta",
            min_value=0.10,
            max_value=0.90,
            value=0.50,
            step=0.05,
            help="Valores menores aumentam cobertura, mas tambem aumentam alertas falsos.",
        )
        if mode == "Por capacidade operacional" and capacity_df is None:
            st.warning("Tabela de capacidade nao encontrada. Usando modo manual.")
    else:
        options = capacity_df["capacidade_max_alertas"].astype(int).tolist()
        selected_cap = st.selectbox("Capacidade maxima de alertas", options=options, index=min(1, len(options) - 1))
        selected = capacity_df[capacity_df["capacidade_max_alertas"].astype(int) == int(selected_cap)].iloc[0]
        score_threshold = float(selected["ponto_de_corte_sugerido"])
        st.info(
            f"Corte sugerido: {score_threshold:.2f} | "
            f"Cobertura: {float(selected['cobertura_risco_detectado']):.1%} | "
            f"Acerto dos alertas: {float(selected['taxa_de_acerto_dos_alertas']):.1%}"
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

    _, quality_report = validate_batch_input(input_df, expected_features)
    with st.expander("Relatorio de qualidade da entrada", expanded=True):
        if quality_report["missing_columns"]:
            st.error(f"Colunas ausentes: {', '.join(quality_report['missing_columns'])}")
        else:
            st.success("Colunas esperadas presentes.")

        high_null_cols = [f"{c} ({r:.0%})" for c, r in quality_report["null_rates"].items() if r >= 0.5]
        if high_null_cols:
            st.warning("Colunas com alta taxa de nulos: " + ", ".join(high_null_cols))

        if quality_report["unknown_categories"]:
            for col, vals in quality_report["unknown_categories"].items():
                st.warning(f"Categorias nao mapeadas em {col}: {', '.join(vals)}")

        for w in quality_report["warnings"]:
            st.caption(f"- {w}")

    scored = prepare_scoring_frame(input_df, expected_features)
    probs = model.predict_proba(scored)[:, 1]
    preds = (probs >= score_threshold).astype(int)

    result = input_df.copy()
    result["prob_risco"] = probs
    result["classe_risco"] = preds
    result["prioridade"] = pd.qcut(result["prob_risco"], q=4, labels=["baixa", "media", "alta", "critica"], duplicates="drop")
    result["acao_sugerida"] = result["prob_risco"].apply(batch_action_from_prob)
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
