# 🎉 Festejos Juninos PE — Dashboard de Inteligência de Negócios

> Projeto da Disciplina de Banco de Dados e Inteligência de Negócios  
> Especialização em Tomada de Decisão Baseada em Evidências — UFRPE  
> **Equipe:** Vanthuir Maia, Fabiana, Renata, Wander e Milena | **Polo:** Garanhuns

---

## 📌 Sobre o Projeto

Dashboard interativo desenvolvido com **Python + Streamlit + Plotly** para análise do investimento público em festejos juninos no estado de Pernambuco, cruzando três fontes de dados reais:

| Fonte                                                                     | Descrição                                                         | Formato |
| ------------------------------------------------------------------------- | ----------------------------------------------------------------- | ------- |
| [MPPE — Festejos Juninos](https://portal.mppe.mp.br/web/festejos-juninos) | Contratações artísticas por município (2021–2026)                 | `.xlsx` |
| [BDE-PE — IDH Municipal](https://www.bde.pe.gov.br)                       | Índice de Desenvolvimento Humano dos 185 municípios (2010)        | `.xls`  |
| [SEFAZ-PE — Transferências](https://www.sefaz.pe.gov.br)                  | Repasses estaduais por município — ICMS, IPVA, IPI (jan–jun/2025) | `.json` |

O objetivo é fornecer **subsídios para tomada de decisão no setor público**, identificando padrões de alocação de recursos em relação ao desenvolvimento humano dos municípios pernambucanos.

---

## 📊 Capturas do Dashboard

### Aba 1 — Visão Geral

**Top municípios por investimento × IDHM**
![Top municípios](prints/print1_top_municipios.png)

**Evolução do investimento por ano**
![Evolução anual](prints/print2_evolucao_ano.png)

**IDH vs Investimento em Festejos**
![Scatter IDH](prints/print3_scatter_idh.png)

**Transferências do Estado vs Gasto em Festejos**
![Transferências](prints/print4_transferencias.png)

---

### Aba 2 — Análise para Tomada de Decisão

**Score de atenção: IDH baixo + alto gasto**
![Score atenção](prints/print6_score_atencao.png)

**Proporção gasto em festejos / transferência recebida (%)**
![Proporção](prints/print7_proporcao_transferencia.png)

**Total investido por mesorregião**
![Mesorregião barras](prints/print9_meso_barras.png)

**IDH Médio vs % do orçamento em festejos por mesorregião**
![Mesorregião scatter](prints/print10_meso_scatter.png)

---

## 🗂️ Estrutura do Projeto

```
ProjetoDisciplina/
├── etl.py                          # Pipeline ETL: carrega, limpa, integra e exporta o parquet
├── .gitignore
├── README.md
├── data/
│   ├── DadosAbertosFestejosJuninos.xlsx
│   ├── idh.xls
│   └── transferenciasMunicipais.json
├── parquet/
│   ├── app.py                      # Dashboard Streamlit
│   ├── requirements.txt
│   └── data/
│       └── df_master.parquet       # Dataset consolidado gerado pelo ETL
└── prints/                         # Capturas do dashboard
```

---

## ⚙️ Como Executar

### Pré-requisitos

- Python 3.10+
- Git

### Instalação

```bash
# Clone o repositório
git clone https://github.com/VanthuirMaia/ProjetoDisciplinaBDIN_TDBE_UFRPE.git
cd ProjetoDisciplinaBDIN_TDBE_UFRPE

# Crie e ative o ambiente virtual
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # Linux/Mac

# Instale as dependências
pip install -r parquet/requirements.txt
```

### Executar

```bash
# Passo 1: gerar o dataset consolidado
python etl.py

# Passo 2: subir o dashboard
cd parquet
streamlit run app.py
```

O dashboard estará disponível em `http://localhost:8501`.

---

## 🔎 O que o Dashboard Responde

| Análise                                            | Decisão Apoiada                                        |
| -------------------------------------------------- | ------------------------------------------------------ |
| Top municípios por investimento (colorido por IDH) | Identificar concentração de recursos                   |
| IDH vs gasto com tendência OLS                     | Verificar se municípios mais ricos gastam mais         |
| Evolução anual (2021–2026)                         | Planejar orçamento e detectar retomada pós-pandemia    |
| Transferência estadual vs festejos                 | Avaliar proporcionalidade do gasto cultural            |
| Score de atenção (IDH baixo + alto gasto)          | Priorizar fiscalização e auditoria                     |
| Proporção festejos/transferência (%)               | Detectar comprometimento excessivo do orçamento        |
| Quadrantes de risco                                | Classificar municípios por nível de atenção necessária |
| Comparativo por mesorregião                        | Visão regional para políticas públicas estaduais       |
| Correlação animada por ano                         | Acompanhar evolução temporal do padrão de gasto        |

---

## ⚠️ Limitações dos Dados

- **IDH de 2010**: dado do último Censo disponível, pode não refletir a realidade atual dos municípios
- **Transferências apenas jan–jun/2025**: impossibilita comparação temporal completa com os festejos
- **Base de festejos declaratória**: municípios informam voluntariamente — valores no arquivo podem divergir do painel online no momento da consulta (ex: Garanhuns consta com R$ 18.000 no arquivo vs R$ 3,6M exibidos no portal)
- **Ausência de dados populacionais**: impossibilitou análise per capita

---

## 🤖 Uso de Inteligência Artificial

O assistente **Claude (Anthropic)** foi utilizado como suporte técnico para estruturação e depuração do código Python. Todo o conteúdo analítico — escolha das fontes, definição das perguntas de negócio, interpretação dos resultados e elaboração das conclusões — foi produzido pela equipe.

---

## 📄 Licença

Projeto acadêmico — uso educacional. Dados públicos conforme licenças das fontes originais (MPPE, BDE-PE, SEFAZ-PE).
