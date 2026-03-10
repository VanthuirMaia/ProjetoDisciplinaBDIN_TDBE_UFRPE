"""
Dashboard BI - Festejos Juninos x IDH x Transferências Municipais (PE)
Streamlit + Plotly com filtros dinâmicos em tempo real
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from pathlib import Path

# ─── Mapeamento de Mesorregiões ────────────────────────────────────────────────
MESORREGIOES = {
    "ABREU E LIMA": "Metropolitana", "ARACOIABA": "Metropolitana",
    "CABO DE SANTO AGOSTINHO": "Metropolitana", "CAMARAGIBE": "Metropolitana",
    "IGARASSU": "Metropolitana", "ILHA DE ITAMARACA": "Metropolitana",
    "IPOJUCA": "Metropolitana", "ITAPISSUMA": "Metropolitana",
    "JABOATAO DOS GUARARAPES": "Metropolitana", "MORENO": "Metropolitana",
    "OLINDA": "Metropolitana", "PAULISTA": "Metropolitana",
    "RECIFE": "Metropolitana", "SAO LOURENCO DA MATA": "Metropolitana",
    "FERNANDO DE NORONHA": "Metropolitana",
    "AGUA PRETA": "Zona da Mata", "ALIANCA": "Zona da Mata",
    "AMARAJI": "Zona da Mata", "BARREIROS": "Zona da Mata",
    "BELEM DE MARIA": "Zona da Mata", "BOM JARDIM": "Zona da Mata",
    "BUENOS AIRES": "Zona da Mata", "CAMOCIM DE SAO FELIX": "Zona da Mata",
    "CAMUTANGA": "Zona da Mata", "CARPINA": "Zona da Mata",
    "CATENDE": "Zona da Mata", "CHA DE ALEGRIA": "Zona da Mata",
    "CHA GRANDE": "Zona da Mata", "CONDADO": "Zona da Mata",
    "CORTES": "Zona da Mata", "ESCADA": "Zona da Mata",
    "FEIRA NOVA": "Zona da Mata", "FERREIROS": "Zona da Mata",
    "GAMELEIRA": "Zona da Mata", "GLORIA DO GOITA": "Zona da Mata",
    "GOIANA": "Zona da Mata", "ITAMBE": "Zona da Mata",
    "ITAQUITINGA": "Zona da Mata", "JAQUEIRA": "Zona da Mata",
    "JOAO ALFREDO": "Zona da Mata", "JOAQUIM NABUCO": "Zona da Mata",
    "LAGOA DE ITAENGA": "Zona da Mata", "LAGOA DO CARRO": "Zona da Mata",
    "LIMOEIRO": "Zona da Mata", "MACAPARANA": "Zona da Mata",
    "MACHADOS": "Zona da Mata", "MARAIAL": "Zona da Mata",
    "NAZARE DA MATA": "Zona da Mata", "OROBO": "Zona da Mata",
    "PALMARES": "Zona da Mata", "PANELAS": "Zona da Mata",
    "PASSIRA": "Zona da Mata", "PAUDALHO": "Zona da Mata",
    "POCAO": "Zona da Mata", "POMBOS": "Zona da Mata",
    "RIBEIRAO": "Zona da Mata", "RIO FORMOSO": "Zona da Mata",
    "SAIRE": "Zona da Mata", "SAO BENEDITO DO SUL": "Zona da Mata",
    "SAO JOSE DA COROA GRANDE": "Zona da Mata", "SAO VICENTE FERRER": "Zona da Mata",
    "SIRINHAEM": "Zona da Mata", "TAMANDARE": "Zona da Mata",
    "TIMBAUBA": "Zona da Mata", "TRACUNHAEM": "Zona da Mata",
    "VICENCIA": "Zona da Mata", "VITORIA DE SANTO ANTAO": "Zona da Mata",
    "XEXEU": "Zona da Mata",
    "AGRESTINA": "Agreste", "ALAGOINHA": "Agreste", "ALTINHO": "Agreste",
    "ANGELIM": "Agreste", "BARRA DE GUABIRABA": "Agreste",
    "BELO JARDIM": "Agreste", "BEZERROS": "Agreste", "BONITO": "Agreste",
    "BREJO DA MADRE DE DEUS": "Agreste", "BREJAO": "Agreste",
    "BOM CONSELHO": "Agreste", "CACHOEIRINHA": "Agreste",
    "CAETES": "Agreste", "CALCADO": "Agreste", "CANHOTINHO": "Agreste",
    "CAPOEIRAS": "Agreste", "CARUARU": "Agreste", "CASINHAS": "Agreste",
    "CORRENTES": "Agreste", "CUMARU": "Agreste", "CUPIRA": "Agreste",
    "FREI MIGUELINHO": "Agreste", "GARANHUNS": "Agreste", "GRAVATA": "Agreste",
    "IATI": "Agreste", "IBIRAJUBA": "Agreste", "JATAUBA": "Agreste",
    "JUCATI": "Agreste", "JUPI": "Agreste", "JUREMA": "Agreste",
    "LAGOA DO OURO": "Agreste", "LAGOA DOS GATOS": "Agreste",
    "LAJEDO": "Agreste", "PALMEIRINA": "Agreste", "PARANATAMA": "Agreste",
    "PEDRA": "Agreste", "PESQUEIRA": "Agreste", "PRIMAVERA": "Agreste",
    "QUIPAPA": "Agreste", "RIACHO DAS ALMAS": "Agreste",
    "SALGADINHO": "Agreste", "SALOA": "Agreste", "SANHARO": "Agreste",
    "SANTA CRUZ": "Agreste", "SANTA CRUZ DO CAPIBARIBE": "Agreste",
    "SANTA MARIA DO CAMBUCA": "Agreste", "SAO BENTO DO UNA": "Agreste",
    "SAO CAITANO": "Agreste", "SAO JOAO": "Agreste",
    "SAO JOAQUIM DO MONTE": "Agreste", "SURUBIM": "Agreste",
    "TACAIMBO": "Agreste", "TAQUARITINGA DO NORTE": "Agreste",
    "TORITAMA": "Agreste", "TUPANATINGA": "Agreste",
    "VENTUROSA": "Agreste", "VERTENTE DO LERIO": "Agreste",
    "VERTENTES": "Agreste",
    "AFOGADOS DA INGAZEIRA": "Sertão", "AGUAS BELAS": "Sertão",
    "ARCOVERDE": "Sertão", "BETANIA": "Sertão", "BREJINHO": "Sertão",
    "BUIQUE": "Sertão", "CALUMBI": "Sertão", "CARNAIBA": "Sertão",
    "CARNAUBEIRA DA PENHA": "Sertão", "CUSTODIA": "Sertão",
    "EXU": "Sertão", "FLORES": "Sertão", "FLORESTA": "Sertão",
    "IBIMIRIM": "Sertão", "IGUARACY": "Sertão", "INGAZEIRA": "Sertão",
    "INAJA": "Sertão", "IPUBI": "Sertão", "ITACURUBA": "Sertão",
    "ITAIBA": "Sertão", "ITAPETIM": "Sertão", "MIRANDIBA": "Sertão",
    "PARNAMIRIM": "Sertão", "QUIXABA": "Sertão", "SALGUEIRO": "Sertão",
    "SANTA CRUZ DA BAIXA VERDE": "Sertão", "SANTA FILOMENA": "Sertão",
    "SANTA TEREZINHA": "Sertão", "SAO JOSE DO BELMONTE": "Sertão",
    "SAO JOSE DO EGITO": "Sertão", "SERRA TALHADA": "Sertão",
    "SERRITA": "Sertão", "SERTANIA": "Sertão", "SOLIDAO": "Sertão",
    "TABIRA": "Sertão", "TACARATU": "Sertão", "TRIUNFO": "Sertão",
    "TUPARETAMA": "Sertão",
    "AFRANIO": "São Francisco", "ARARIPINA": "São Francisco",
    "BELEM DO SAO FRANCISCO": "São Francisco", "BODOCO": "São Francisco",
    "CABROBO": "São Francisco", "DORMENTES": "São Francisco",
    "GRANITO": "São Francisco", "LAGOA GRANDE": "São Francisco",
    "MOREILANDIA": "São Francisco", "OROCO": "São Francisco",
    "OURICURI": "São Francisco", "PETROLANDIA": "São Francisco",
    "PETROLINA": "São Francisco", "TERRA NOVA": "São Francisco",
    "TRINDADE": "São Francisco", "VERDEJANTE": "São Francisco",
    "CEDRO": "São Francisco", "JATOBA": "São Francisco",
}

# ─── Config da página ──────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Festejos Juninos PE - BI Dashboard",
    page_icon="🎉",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Carrega dados ─────────────────────────────────────────────────────────────
@st.cache_data
def carregar_dados() -> pd.DataFrame:
    caminho = Path(__file__).parent / "parquet" / "data" / "df_master.parquet"
    df = pd.read_parquet(caminho)
    df["classe_idh"] = pd.cut(
        df["idhm"],
        bins=[0, 0.499, 0.599, 0.699, 0.799, 1.0],
        labels=["Muito Baixo", "Baixo", "Médio", "Alto", "Muito Alto"],
    )
    df["mesorregiao"] = df["municipio_key"].map(MESORREGIOES).fillna("Não classificado")
    return df


df_raw = carregar_dados()

# ─── Sidebar: Filtros ──────────────────────────────────────────────────────────
st.sidebar.title("🎛️ Filtros")

anos_disponiveis = sorted(df_raw["ano"].unique())
anos_sel = st.sidebar.multiselect("Ano dos Festejos", options=anos_disponiveis, default=anos_disponiveis)

fonte_opcoes = sorted(df_raw["fonte_recurso"].dropna().unique())
fonte_sel = st.sidebar.multiselect("Fonte do Recurso", options=fonte_opcoes, default=fonte_opcoes)

faixa_idh = st.sidebar.select_slider(
    "Faixa de IDHM",
    options=["Muito Baixo", "Baixo", "Médio", "Alto", "Muito Alto"],
    value=("Muito Baixo", "Muito Alto"),
)
ordem_idh = ["Muito Baixo", "Baixo", "Médio", "Alto", "Muito Alto"]
idx_min = ordem_idh.index(faixa_idh[0])
idx_max = ordem_idh.index(faixa_idh[1])
classes_sel = ordem_idh[idx_min : idx_max + 1]

top_n = st.sidebar.slider("Top N municípios nos rankings", min_value=5, max_value=30, value=15)

# ─── Aplica filtros ────────────────────────────────────────────────────────────
df = df_raw[
    (df_raw["ano"].isin(anos_sel)) &
    (df_raw["fonte_recurso"].isin(fonte_sel)) &
    (df_raw["classe_idh"].isin(classes_sel))
].copy()

# ─── Helper: agrega por município ─────────────────────────────────────────────
def agg_por_municipio(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby("municipio_key", as_index=False)
        .agg(
            municipio=("municipio", "first"),
            total_festejos=("total_festejos", "sum"),
            num_contratacoes=("num_contratacoes", "sum"),
            idhm=("idhm", "first"),
            classe_idh=("classe_idh", "first"),
            mesorregiao=("mesorregiao", "first"),
            total_transferencia=("total_transferencia", "first"),
        )
    )

# ─── Abas ─────────────────────────────────────────────────────────────────────
aba_geral, aba_analise = st.tabs(["📊 Visão Geral", "🔎 Análise para Decisão"])

# ══════════════════════════════════════════════════════════════════════════════
# ABA 1 — VISÃO GERAL
# ══════════════════════════════════════════════════════════════════════════════
with aba_geral:
    st.title("🎉 Festejos Juninos de Pernambuco — Painel de Análise")
    st.caption("Fontes: Dados Abertos PE (Festejos Juninos) | BDE-PE (IDH Municipal) | SEFAZ-PE (Transferências Municipais)")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("💰 Total Investido em Festejos", f"R$ {df['total_festejos'].sum():,.0f}".replace(",", "."))
    col2.metric("🏙️ Municípios com Festejos", df["municipio_key"].nunique())
    col3.metric("🎭 Contratações Artísticas", int(df["num_contratacoes"].sum()))
    col4.metric("📊 IDHM Médio", f"{df['idhm'].mean():.3f}" if df["idhm"].notna().any() else "—")

    st.divider()

    col_a, col_b = st.columns([1.2, 1])

    with col_a:
        st.subheader("🏆 Top Municípios por Investimento em Festejos")
        df_mun = agg_por_municipio(df).sort_values("total_festejos", ascending=False).head(top_n)
        fig_bar = px.bar(
            df_mun.sort_values("total_festejos"),
            x="total_festejos", y="municipio", orientation="h",
            color="idhm", color_continuous_scale="RdYlGn",
            labels={"total_festejos": "Investimento (R$)", "municipio": "Município", "idhm": "IDHM"},
            hover_data={"num_contratacoes": True, "idhm": ":.3f"},
            text_auto=".2s",
        )
        fig_bar.update_layout(height=480, coloraxis_colorbar=dict(title="IDHM"), margin=dict(l=0, r=0))
        st.plotly_chart(fig_bar, use_container_width=True)

    with col_b:
        st.subheader("🔍 IDH vs Investimento em Festejos")
        st.caption("Cada ponto = município. Tamanho = nº de contratações")
        df_scatter = agg_por_municipio(df).dropna(subset=["idhm"])
        fig_scatter = px.scatter(
            df_scatter, x="idhm", y="total_festejos",
            size="num_contratacoes", color="classe_idh",
            hover_name="municipio",
            category_orders={"classe_idh": ordem_idh},
            color_discrete_sequence=px.colors.qualitative.Set2,
            labels={"idhm": "IDHM (2010)", "total_festejos": "Investimento (R$)",
                    "classe_idh": "Classe IDH", "num_contratacoes": "Contratações"},
            trendline="ols",
        )
        fig_scatter.update_layout(height=480, margin=dict(l=0, r=0))
        st.plotly_chart(fig_scatter, use_container_width=True)

    st.divider()
    col_c, col_d = st.columns(2)

    with col_c:
        st.subheader("📅 Evolução do Investimento por Ano")
        df_ano = df.groupby("ano", as_index=False).agg(
            total_festejos=("total_festejos", "sum"),
            municipios=("municipio_key", "nunique"),
        )
        fig_line = px.bar(df_ano, x="ano", y="total_festejos", text_auto=".2s",
                          color="total_festejos", color_continuous_scale="Blues",
                          labels={"ano": "Ano", "total_festejos": "Total Investido (R$)"})
        fig_line.add_scatter(x=df_ano["ano"], y=df_ano["municipios"], name="Municípios",
                             yaxis="y2", mode="lines+markers",
                             marker=dict(color="orange", size=8), line=dict(color="orange"))
        fig_line.update_layout(height=380,
                               yaxis2=dict(overlaying="y", side="right", title="Municípios"),
                               coloraxis_showscale=False, showlegend=True, margin=dict(l=0, r=0))
        st.plotly_chart(fig_line, use_container_width=True)

    with col_d:
        st.subheader("💸 Transferências do Estado vs Gasto com Festejos")
        df_tc = (agg_por_municipio(df).dropna(subset=["total_transferencia"])
                 .sort_values("total_transferencia", ascending=False).head(top_n))
        fig_comp = go.Figure()
        fig_comp.add_trace(go.Bar(name="Transferência (R$)", x=df_tc["municipio"],
                                  y=df_tc["total_transferencia"], marker_color="#4C8BE0"))
        fig_comp.add_trace(go.Bar(name="Festejos (R$)", x=df_tc["municipio"],
                                  y=df_tc["total_festejos"], marker_color="#E05C4C"))
        fig_comp.update_layout(barmode="group", height=380, xaxis_tickangle=-40,
                               legend=dict(orientation="h", yanchor="bottom", y=1.02),
                               margin=dict(l=0, r=0))
        st.plotly_chart(fig_comp, use_container_width=True)

    st.divider()
    col_e, col_f = st.columns([1, 1.5])

    with col_e:
        st.subheader("📊 Distribuição do IDHM")
        df_hist = agg_por_municipio(df).dropna(subset=["idhm"])
        fig_hist = px.histogram(df_hist, x="idhm", color="classe_idh", nbins=20,
                                category_orders={"classe_idh": ordem_idh},
                                color_discrete_sequence=px.colors.qualitative.Set2,
                                labels={"idhm": "IDHM", "count": "Municípios"})
        fig_hist.update_layout(height=350, margin=dict(l=0, r=0), bargap=0.05)
        st.plotly_chart(fig_hist, use_container_width=True)

    with col_f:
        st.subheader("📋 Detalhamento por Município")
        df_tab = agg_por_municipio(df).sort_values("total_festejos", ascending=False).copy()
        df_tab["total_festejos_fmt"] = df_tab["total_festejos"].map("R$ {:,.0f}".format)
        df_tab["total_transferencia_fmt"] = df_tab["total_transferencia"].map(
            lambda x: f"R$ {x:,.0f}" if pd.notna(x) else "—")
        df_tab["idhm_fmt"] = df_tab["idhm"].map(lambda x: f"{x:.3f}" if pd.notna(x) else "—")
        st.dataframe(
            df_tab[["municipio","idhm_fmt","classe_idh","total_festejos_fmt","num_contratacoes","total_transferencia_fmt"]].rename(columns={
                "municipio": "Município", "idhm_fmt": "IDHM", "classe_idh": "Classe IDH",
                "total_festejos_fmt": "Total Festejos", "num_contratacoes": "Contratações",
                "total_transferencia_fmt": "Transferência Estado",
            }),
            use_container_width=True, height=330, hide_index=True,
        )

    st.caption("Projeto TDBE — UFRPE | Dados: Dados Abertos PE · BDE-PE · SEFAZ-PE")


# ══════════════════════════════════════════════════════════════════════════════
# ABA 2 — ANÁLISE PARA DECISÃO
# ══════════════════════════════════════════════════════════════════════════════
with aba_analise:
    st.title("🔎 Análise para Tomada de Decisão")
    st.caption("Identifica padrões de alocação de recursos em relação ao desenvolvimento humano dos municípios")

    df_mun_full = agg_por_municipio(df).dropna(subset=["idhm", "total_transferencia"])

    # ── Índice de Prioridade: IDH baixo + gasto alto ───────────────────────────
    # Normaliza entre 0 e 1 para calcular score
    min_idh, max_idh = df_mun_full["idhm"].min(), df_mun_full["idhm"].max()
    min_fest, max_fest = df_mun_full["total_festejos"].min(), df_mun_full["total_festejos"].max()

    df_mun_full["idh_norm"] = (df_mun_full["idhm"] - min_idh) / (max_idh - min_idh)
    df_mun_full["fest_norm"] = (df_mun_full["total_festejos"] - min_fest) / (max_fest - min_fest)

    # Score de atenção: baixo IDH + alto gasto em festejos
    df_mun_full["score_atencao"] = (1 - df_mun_full["idh_norm"]) * 0.6 + df_mun_full["fest_norm"] * 0.4

    # Proporção gasto festejos / transferência recebida
    df_mun_full["proporcao_festejos"] = df_mun_full["total_festejos"] / df_mun_full["total_transferencia"] * 100

    st.divider()

    # ── 1. Ranking: IDH Baixo + Alto Investimento ──────────────────────────────
    st.subheader("⚠️ Municípios com Baixo IDH e Alto Gasto em Festejos")
    st.caption("Atenção prioritária: municípios que gastam mais em festejos do que sua condição de desenvolvimento justificaria")

    df_atencao = df_mun_full.sort_values("score_atencao", ascending=False).head(top_n).copy()

    col1, col2 = st.columns(2)

    with col1:
        fig_atencao = px.scatter(
            df_atencao,
            x="idhm",
            y="total_festejos",
            size="proporcao_festejos",
            color="score_atencao",
            color_continuous_scale="Reds",
            hover_name="municipio",
            hover_data={"proporcao_festejos": ":.1f", "idhm": ":.3f", "score_atencao": ":.2f"},
            labels={
                "idhm": "IDHM",
                "total_festejos": "Gasto em Festejos (R$)",
                "score_atencao": "Score de Atenção",
                "proporcao_festejos": "% da Transferência",
            },
            text="municipio",
        )
        fig_atencao.update_traces(textposition="top center", textfont_size=9)
        fig_atencao.update_layout(height=420, margin=dict(l=0, r=0),
                                  coloraxis_colorbar=dict(title="Score"))
        st.plotly_chart(fig_atencao, use_container_width=True)

    with col2:
        df_tab_atencao = df_atencao[["municipio","idhm","classe_idh","total_festejos","proporcao_festejos","score_atencao"]].copy()
        df_tab_atencao["idhm"] = df_tab_atencao["idhm"].map("{:.3f}".format)
        df_tab_atencao["total_festejos"] = df_tab_atencao["total_festejos"].map("R$ {:,.0f}".format)
        df_tab_atencao["proporcao_festejos"] = df_tab_atencao["proporcao_festejos"].map("{:.1f}%".format)
        df_tab_atencao["score_atencao"] = df_tab_atencao["score_atencao"].map("{:.2f}".format)
        st.dataframe(
            df_tab_atencao.rename(columns={
                "municipio": "Município", "idhm": "IDHM", "classe_idh": "Classe IDH",
                "total_festejos": "Gasto Festejos", "proporcao_festejos": "% da Transferência",
                "score_atencao": "Score Atenção ↓",
            }),
            use_container_width=True, height=420, hide_index=True,
        )

    st.divider()

    # ── 2. Proporção Festejos / Transferência ─────────────────────────────────
    st.subheader("💸 Proporção do Gasto em Festejos sobre a Transferência Recebida")
    st.caption("Quanto do repasse estadual cada município comprometeu com festejos juninos")

    col3, col4 = st.columns([1.3, 1])

    with col3:
        df_prop = df_mun_full.sort_values("proporcao_festejos", ascending=False).head(top_n)
        cores = df_prop["idhm"].tolist()

        fig_prop = px.bar(
            df_prop.sort_values("proporcao_festejos"),
            x="proporcao_festejos",
            y="municipio",
            orientation="h",
            color="idhm",
            color_continuous_scale="RdYlGn",
            text=df_prop.sort_values("proporcao_festejos")["proporcao_festejos"].map("{:.1f}%".format),
            labels={"proporcao_festejos": "% da Transferência Estadual", "municipio": "Município", "idhm": "IDHM"},
            hover_data={"total_festejos": True, "total_transferencia": True},
        )
        fig_prop.update_traces(textposition="outside")
        fig_prop.update_layout(height=460, margin=dict(l=0, r=50),
                               coloraxis_colorbar=dict(title="IDHM"))
        st.plotly_chart(fig_prop, use_container_width=True)

    with col4:
        # Quadrante: proporção alta + IDH baixo = risco fiscal/social
        df_mun_full["quadrante"] = df_mun_full.apply(
            lambda r: "⚠️ Risco: IDH baixo + alta proporção"
                if r["idhm"] < 0.6 and r["proporcao_festejos"] > df_mun_full["proporcao_festejos"].median()
                else ("📌 Atenção: IDH alto + alta proporção"
                    if r["idhm"] >= 0.6 and r["proporcao_festejos"] > df_mun_full["proporcao_festejos"].median()
                    else ("✅ Equilibrado: IDH baixo + baixa proporção"
                        if r["idhm"] < 0.6
                        else "🟢 Saudável: IDH alto + baixa proporção")),
            axis=1,
        )
        contagem = df_mun_full["quadrante"].value_counts().reset_index()
        contagem.columns = ["Situação", "Municípios"]
        fig_pizza = px.pie(contagem, names="Situação", values="Municípios",
                           color_discrete_sequence=["#E05C4C","#F0A500","#4C8BE0","#3DB77D"],
                           hole=0.4)
        fig_pizza.update_layout(height=460, margin=dict(l=0, r=0),
                                legend=dict(orientation="v", x=0))
        st.plotly_chart(fig_pizza, use_container_width=True)

    st.divider()

    # ── 3. Comparativo por Mesorregião ────────────────────────────────────────
    st.subheader("🗺️ Comparativo por Mesorregião de PE")

    df_meso = (
        df_mun_full.groupby("mesorregiao", as_index=False)
        .agg(
            total_festejos=("total_festejos", "sum"),
            total_transferencia=("total_transferencia", "sum"),
            idhm_medio=("idhm", "mean"),
            municipios=("municipio_key", "nunique"),
        )
    )
    df_meso["proporcao"] = df_meso["total_festejos"] / df_meso["total_transferencia"] * 100
    df_meso["festejos_per_capita_mun"] = df_meso["total_festejos"] / df_meso["municipios"]

    col5, col6 = st.columns(2)

    with col5:
        fig_meso_bar = px.bar(
            df_meso.sort_values("total_festejos", ascending=False),
            x="mesorregiao", y="total_festejos",
            color="idhm_medio", color_continuous_scale="RdYlGn",
            text_auto=".2s",
            labels={"mesorregiao": "Mesorregião", "total_festejos": "Total Festejos (R$)",
                    "idhm_medio": "IDHM Médio"},
            title="Total Investido por Mesorregião"
        )
        fig_meso_bar.update_layout(height=380, margin=dict(l=0, r=0),
                                   coloraxis_colorbar=dict(title="IDHM"))
        st.plotly_chart(fig_meso_bar, use_container_width=True)

    with col6:
        fig_meso_scatter = px.scatter(
            df_meso,
            x="idhm_medio", y="proporcao",
            size="municipios", color="mesorregiao",
            text="mesorregiao",
            labels={"idhm_medio": "IDHM Médio", "proporcao": "% Festejos / Transferência",
                    "municipios": "Nº Municípios"},
            title="IDH Médio vs % do Orçamento em Festejos"
        )
        fig_meso_scatter.update_traces(textposition="top center")
        fig_meso_scatter.update_layout(height=380, margin=dict(l=0, r=0), showlegend=False)
        st.plotly_chart(fig_meso_scatter, use_container_width=True)

    # Tabela resumo mesorregiões
    df_meso_tab = df_meso.copy()
    df_meso_tab["total_festejos"] = df_meso_tab["total_festejos"].map("R$ {:,.0f}".format)
    df_meso_tab["total_transferencia"] = df_meso_tab["total_transferencia"].map("R$ {:,.0f}".format)
    df_meso_tab["idhm_medio"] = df_meso_tab["idhm_medio"].map("{:.3f}".format)
    df_meso_tab["proporcao"] = df_meso_tab["proporcao"].map("{:.1f}%".format)
    df_meso_tab["festejos_per_capita_mun"] = df_meso_tab["festejos_per_capita_mun"].map("R$ {:,.0f}".format)
    st.dataframe(
        df_meso_tab.rename(columns={
            "mesorregiao": "Mesorregião", "total_festejos": "Total Festejos",
            "total_transferencia": "Total Transferências", "idhm_medio": "IDHM Médio",
            "municipios": "Municípios", "proporcao": "% Festejos/Transferência",
            "festejos_per_capita_mun": "Festejos por Município",
        }),
        use_container_width=True, hide_index=True,
    )

    st.divider()

    # ── 4. Evolução correlação IDH × Festejos por ano ─────────────────────────
    st.subheader("📈 Correlação entre IDH e Gasto em Festejos por Ano")
    st.caption("Como a relação IDH × investimento evoluiu ao longo dos anos filtrados")

    df_corr_ano = (
        df_raw[df_raw["ano"].isin(anos_sel)]
        .groupby(["municipio_key", "ano"], as_index=False)
        .agg(
            municipio=("municipio", "first"),
            total_festejos=("total_festejos", "sum"),
            idhm=("idhm", "first"),
            mesorregiao=("mesorregiao", "first"),
        )
        .dropna(subset=["idhm"])
    )

    fig_corr = px.scatter(
        df_corr_ano,
        x="idhm", y="total_festejos",
        animation_frame="ano",
        color="mesorregiao",
        hover_name="municipio",
        size="total_festejos",
        size_max=50,
        labels={"idhm": "IDHM", "total_festejos": "Gasto em Festejos (R$)", "mesorregiao": "Mesorregião"},
        range_x=[df_corr_ano["idhm"].min() - 0.02, df_corr_ano["idhm"].max() + 0.02],
        range_y=[0, df_corr_ano["total_festejos"].max() * 1.1],
    )
    fig_corr.update_layout(height=500, margin=dict(l=0, r=0))
    st.plotly_chart(fig_corr, use_container_width=True)

    st.caption("Projeto TDBE — UFRPE | Dados: Dados Abertos PE · BDE-PE · SEFAZ-PE")