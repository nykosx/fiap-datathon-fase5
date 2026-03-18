"""Utilitarios compartilhados para notebooks analiticos e de modelagem."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Callable

import numpy as np
import pandas as pd


def resolve_project_root(start: Path | None = None) -> Path:
    """Resolve a raiz do projeto a partir do diretorio atual do notebook."""
    current = (start or Path.cwd()).resolve()
    candidates = [current, *current.parents]
    for path in candidates:
        if (path / "data" / "dados_unificados.csv").exists() and (path / "src").exists():
            return path
    # fallback para execucao padrao em notebooks/
    return current.parent if current.name == "notebooks" else current


def load_official_dataset(project_root: Path | None = None) -> tuple[pd.DataFrame, Path, Path]:
    """Carrega o dataset oficial consolidado e retorna dataframe + caminhos."""
    root = project_root or resolve_project_root()
    data_path = root / "data" / "dados_unificados.csv"
    if not data_path.exists():
        raise FileNotFoundError(f"Arquivo oficial nao encontrado: {data_path}")
    df = pd.read_csv(data_path)
    return df, data_path, root


def add_common_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Adiciona colunas comuns usadas em analise: ano, inde_unificado e genero_padronizado."""
    out = df.copy()

    if "year" in out.columns:
        out["ano"] = pd.to_numeric(out["year"].astype(str).str.extract(r"(\d{4})")[0], errors="coerce")
    else:
        out["ano"] = np.nan

    inde_map = {2022: "inde_2022", 2023: "inde_2023", 2024: "inde_2024"}
    out["inde_unificado"] = np.nan
    for ano_ref, col in inde_map.items():
        if col in out.columns:
            out.loc[out["ano"] == ano_ref, "inde_unificado"] = pd.to_numeric(
                out.loc[out["ano"] == ano_ref, col], errors="coerce"
            )

    if "gender" in out.columns:
        out["genero_padronizado"] = (
            out["gender"]
            .astype(str)
            .str.strip()
            .str.upper()
            .replace({"M": "MASCULINO", "F": "FEMININO", "NAN": np.nan})
        )
    else:
        out["genero_padronizado"] = np.nan

    return out


_PHASE_NUM = re.compile(r"^\s*([0-9]{1,2})\s*$")
_PHASE_CODE = re.compile(r"^\s*([0-9]{1,2})([A-Z])\s*$", re.IGNORECASE)
_PHASE_TEXT = re.compile(r"^\s*FASE\s*([0-9]{1,2})\s*$", re.IGNORECASE)
_CLASS_ALFA = re.compile(r"^\s*ALFA\s+([A-Z])\b", re.IGNORECASE)


def _parse_phase_class(phase_val, class_val) -> tuple[str | float, str | float]:
    phase_token = "" if pd.isna(phase_val) else str(phase_val).strip().upper()
    class_token = "" if pd.isna(class_val) else str(class_val).strip().upper()

    phase_norm, class_norm = np.nan, np.nan

    if phase_token == "ALFA" or phase_token.startswith("ALFA "):
        phase_norm = "ALFA"
    else:
        match = _PHASE_TEXT.match(phase_token)
        if match:
            phase_norm = f"FASE {int(match.group(1))}"
        else:
            match = _PHASE_CODE.match(phase_token)
            if match:
                phase_norm = f"FASE {int(match.group(1))}"
                class_norm = match.group(2)
            else:
                match = _PHASE_NUM.match(phase_token)
                if match:
                    phase_norm = f"FASE {int(match.group(1))}"

    if pd.isna(class_norm):
        if len(class_token) == 1 and class_token.isalpha():
            class_norm = class_token
        else:
            match = _PHASE_CODE.match(class_token)
            if match:
                class_norm = match.group(2)
            else:
                match = _CLASS_ALFA.match(class_token)
                if match:
                    class_norm = match.group(1)
                    if pd.isna(phase_norm):
                        phase_norm = "ALFA"

    return phase_norm, class_norm


def add_phase_normalization(df: pd.DataFrame) -> pd.DataFrame:
    """Normaliza fase e turma para colunas canônicas."""
    out = df.copy()
    phase_col = "phase" if "phase" in out.columns else None
    class_col = "class" if "class" in out.columns else None

    if phase_col is None and class_col is None:
        out["fase_padronizada"] = np.nan
        out["turma_padronizada"] = np.nan
        out["fase_ref"] = np.nan
        out["turma_ref"] = np.nan
        return out

    norm = out.apply(
        lambda row: _parse_phase_class(
            row.get(phase_col, np.nan) if phase_col else np.nan,
            row.get(class_col, np.nan) if class_col else np.nan,
        ),
        axis=1,
        result_type="expand",
    )
    norm.columns = ["fase_padronizada", "turma_padronizada"]
    out["fase_padronizada"] = norm["fase_padronizada"]
    out["turma_padronizada"] = norm["turma_padronizada"]
    out["fase_ref"] = out["fase_padronizada"].fillna(out.get("phase"))
    out["turma_ref"] = out["turma_padronizada"].fillna(out.get("class"))
    return out


def prepare_analytical_dataset(df: pd.DataFrame) -> pd.DataFrame:
    """Pipeline comum para preparar base analitica no notebook 03."""
    out = add_common_columns(df)
    out = add_phase_normalization(out)
    return out


def make_figure_saver(project_root: Path) -> tuple[Path, Callable]:
    """Cria pasta de figuras e retorna helper salvar_figura(fig, nome_arquivo)."""
    fig_dir = project_root / "outputs" / "figuras"
    fig_dir.mkdir(parents=True, exist_ok=True)

    def salvar_figura(fig, nome_arquivo: str):
        caminho = fig_dir / nome_arquivo
        fig.savefig(caminho, dpi=150, bbox_inches="tight")
        print(f"Figura salva: {caminho.name}")

    return fig_dir, salvar_figura


def build_temporal_risk_base(df: pd.DataFrame, target_threshold: float = 5.0) -> pd.DataFrame:
    """Constroi base temporal com alvo de risco no ano seguinte para modelagem."""
    required = {"year", "student_id", "ian"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Colunas obrigatorias ausentes: {sorted(missing)}")

    out = df.copy()
    out["year_num"] = pd.to_numeric(out["year"].astype(str).str.extract(r"(\d{4})")[0], errors="coerce")
    out["ian"] = pd.to_numeric(out["ian"], errors="coerce")
    out = out.sort_values(["student_id", "year_num"]).copy()

    out["ian_next_year"] = out.groupby("student_id")["ian"].shift(-1)
    out["next_year_num"] = out.groupby("student_id")["year_num"].shift(-1)

    consecutive_mask = out["next_year_num"] == (out["year_num"] + 1)
    out.loc[~consecutive_mask, "ian_next_year"] = np.nan

    model_df = out.dropna(subset=["ian_next_year", "year_num"]).copy()
    model_df["base_year"] = model_df["year_num"].astype(int)
    model_df["prediction_year"] = model_df["base_year"] + 1
    model_df["target_risco_next"] = (model_df["ian_next_year"] <= target_threshold).astype(int)
    return model_df
