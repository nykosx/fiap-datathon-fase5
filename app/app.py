import json
from pathlib import Path

import joblib
import pandas as pd
import streamlit as st


st.set_page_config(page_title="Risco de Defasagem", layout="wide")

PROJECT_ROOT = Path(__file__).resolve().parent.parent
MODEL_PATH = PROJECT_ROOT / "models" / "model_risco.joblib"
METADATA_PATH = PROJECT_ROOT / "outputs" / "model_risco_metadata.json"


def load_metadata(path: Path):
    if not path.exists():
        return None
    with open(path, "r", encoding="utf-8") as fp:
        return json.load(fp)


def ensure_required_columns(df: pd.DataFrame, expected_cols):
    fixed = df.copy()
    for col in expected_cols:
        if col not in fixed.columns:
            fixed[col] = pd.NA
    return fixed


st.title("Classificacao de risco academico")
st.caption("Upload de CSV para gerar probabilidade de risco e ranking de priorizacao.")

if not MODEL_PATH.exists():
    st.error(f"Modelo nao encontrado em: {MODEL_PATH}")
    st.stop()

metadata = load_metadata(METADATA_PATH)
model = joblib.load(MODEL_PATH)

winner_track = metadata.get("winner_track") if metadata else "desconhecido"
expected_features = []
if metadata:
    if winner_track == "trilha2_com_ipp" and metadata.get("track2"):
        expected_features = metadata["track2"].get("features", [])
    else:
        expected_features = metadata["track1"].get("features", [])

with st.expander("Informacoes do modelo", expanded=True):
    st.write(f"Track vencedor: **{winner_track}**")
    if metadata and "winner_metrics" in metadata:
        m = metadata["winner_metrics"]
        st.write(
            f"Recall: **{m.get('recall', 0):.3f}** | "
            f"Precision: **{m.get('precision', 0):.3f}** | "
            f"ROC AUC: **{m.get('roc_auc', 0):.3f}**"
        )
    if expected_features:
        st.write("Features esperadas:")
        st.code(", ".join(expected_features), language="text")

uploaded = st.file_uploader("Envie um CSV com dados de alunos", type=["csv"])

if uploaded is not None:
    input_df = pd.read_csv(uploaded)
    st.subheader("Amostra de entrada")
    st.dataframe(input_df.head(10), use_container_width=True)

    if expected_features:
        scored_base = ensure_required_columns(input_df, expected_features)[expected_features].copy()
    else:
        scored_base = input_df.copy()

    probs = model.predict_proba(scored_base)[:, 1]
    preds = (probs >= 0.5).astype(int)

    result = input_df.copy()
    result["prob_risco"] = probs
    result["classe_risco"] = preds
    result["prioridade"] = pd.qcut(
        result["prob_risco"],
        q=4,
        labels=["baixa", "media", "alta", "critica"],
        duplicates="drop"
    )
    result = result.sort_values("prob_risco", ascending=False).reset_index(drop=True)

    st.subheader("Resultado de scoring")
    st.dataframe(result.head(50), use_container_width=True)

    csv_out = result.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Baixar resultado (CSV)",
        data=csv_out,
        file_name="scoring_risco.csv",
        mime="text/csv"
    )
