"""
ETL - Projeto BI: Festejos Juninos x IDH x Transferências Municipais (PE)
Carrega os 3 arquivos da pasta data/, normaliza, faz merge e salva df_master.parquet
"""

import pandas as pd
import json
import unicodedata
import re
from pathlib import Path

DATA_DIR = Path(__file__).parent / "data"
OUTPUT = Path(__file__).parent / "parquet" / "data" / "df_master.parquet"

# ─── Correções manuais de grafia ───────────────────────────────────────────────
CORRECOES = {
    "BELEM DE SAO FRANCISCO": "BELEM DO SAO FRANCISCO",
    "LAGOA DO ITAENGA":        "LAGOA DE ITAENGA",
    "SAO CAETANO":             "SAO CAITANO",
}


def normalizar_municipio(nome: str) -> str:
    """Remove acentos, padroniza maiúsculas e espaços."""
    if not isinstance(nome, str):
        return ""
    nome = nome.strip().upper()
    nome = unicodedata.normalize("NFKD", nome)
    nome = "".join(c for c in nome if not unicodedata.combining(c))
    nome = re.sub(r"\s+", " ", nome)
    return CORRECOES.get(nome, nome)


# ─── Carrega Festejos Juninos ──────────────────────────────────────────────────
def carregar_festejos() -> pd.DataFrame:
    df = pd.read_excel(DATA_DIR / "DadosAbertosFestejosJuninos.xlsx")
    df = df.rename(columns={
        "Município/Distrito Estadual":          "municipio",
        "Número Empenho":                       "num_empenho",
        "Atração Artística":                    "atracao",
        "Valor Total das Contratações Artísticas": "valor_contratacao",
        "Ano":                                  "ano",
        "Data":                                 "data",
        "Fonte do Recurso":                     "fonte_recurso",
    })

    # Remove anos inválidos
    df = df[pd.to_numeric(df["ano"], errors="coerce").notna()].copy()
    df["ano"] = df["ano"].astype(int)

    # Remove linhas sem município ou valor
    df = df.dropna(subset=["municipio", "valor_contratacao"])
    df["municipio_key"] = df["municipio"].apply(normalizar_municipio)

    return df


# ─── Carrega IDH ──────────────────────────────────────────────────────────────
def carregar_idh() -> pd.DataFrame:
    # Arquivo é HTML disfarçado de .xls
    df = pd.read_html(DATA_DIR / "idh.xls")[1]
    df.columns = ["municipio", "idhm", "idhm_l", "idhm_e", "idhm_r"]
    df = df.iloc[2:].reset_index(drop=True)

    # IDH vem como string "0679" → float 0.679
    for col in ["idhm", "idhm_l", "idhm_e", "idhm_r"]:
        df[col] = pd.to_numeric(df[col], errors="coerce") / 1000

    df["municipio_key"] = df["municipio"].apply(normalizar_municipio)
    return df


# ─── Carrega Transferências Municipais ────────────────────────────────────────
def carregar_transferencias() -> pd.DataFrame:
    with open(DATA_DIR / "transferenciasMunicipais.json", encoding="utf-8") as f:
        data = json.load(f)

    df = pd.DataFrame(data["campos"])
    df = df.rename(columns={"MUNICÍPIO": "municipio", "TOTAL": "total_transferencia"})
    df["municipio_key"] = df["municipio"].apply(normalizar_municipio)

    # Agrega por município (soma todos os meses disponíveis)
    df_agg = df.groupby("municipio_key", as_index=False).agg(
        total_transferencia=("total_transferencia", "sum"),
        total_icms=("ICMS", "sum"),
        total_ipva=("IPVA", "sum"),
        total_ipi=("IPI", "sum"),
        meses_disponiveis=("mes", "nunique"),
    )
    return df_agg


# ─── Merge e salva ────────────────────────────────────────────────────────────
def build_master():
    print("Carregando dados...")
    df_fest  = carregar_festejos()
    df_idh   = carregar_idh()
    df_transf = carregar_transferencias()

    # Agrega festejos por município e ano
    df_fest_agg = df_fest.groupby(["municipio_key", "municipio", "ano", "fonte_recurso"], as_index=False).agg(
        total_festejos=("valor_contratacao", "sum"),
        num_contratacoes=("valor_contratacao", "count"),
    )

    # Merge: festejos + IDH
    df = df_fest_agg.merge(
        df_idh[["municipio_key", "idhm", "idhm_l", "idhm_e", "idhm_r"]],
        on="municipio_key",
        how="left",
    )

    # Merge: + transferências
    df = df.merge(df_transf, on="municipio_key", how="left")

    # Salva
    df.to_parquet(OUTPUT, index=False)
    print(f"Master salvo em {OUTPUT}")
    print(f"Shape: {df.shape}")
    print(df.head(3))
    return df


if __name__ == "__main__":
    build_master()