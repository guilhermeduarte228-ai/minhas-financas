import os
import re
import streamlit as st
import pandas as pd
import sqlite3
import calendar
import hashlib
from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta
import io
import urllib.parse

st.set_page_config(page_title="FINANCAS.OS // Terminal", page_icon="◈", layout="wide", initial_sidebar_state="auto")

# ================= DESIGN SYSTEM FINTECH / LINEAR / BLOOMBERG DARK =================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700;800&display=swap');

    :root {
        --bg-base: #060911;
        --bg-surface: #0b101b;
        --bg-elevated: #101726;
        --border-subtle: rgba(148, 163, 184, 0.12);
        --border-glow: rgba(56, 189, 248, 0.35);
        --accent-cyan: #38bdf8;
        --accent-emerald: #10b981;
        --accent-violet: #818cf8;
        --accent-rose: #f43f5e;
        --text-primary: #f8fafc;
        --text-secondary: #94a3b8;
        --text-muted: #64748b;
    }

    html, body, .stApp {
        background-color: var(--bg-base) !important;
        background-image:
            radial-gradient(circle at 15% 0%, rgba(56, 189, 248, 0.06) 0%, transparent 40%),
            radial-gradient(circle at 85% 10%, rgba(129, 140, 248, 0.05) 0%, transparent 40%);
        color: var(--text-primary);
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    .block-container {
        max-width: 1320px !important;
        padding-top: 1.1rem !important;
        padding-bottom: 3rem !important;
        padding-left: 1.4rem !important;
        padding-right: 1.4rem !important;
    }

    @media (max-width: 768px) {
        .block-container {
            padding-top: 0.6rem !important;
            padding-left: 0.7rem !important;
            padding-right: 0.7rem !important;
        }
    }

    #MainMenu, footer { visibility: hidden; }
    header[data-testid="stHeader"] { background: transparent !important; }

    /* Sidebar Minimalista Estilo Linear */
    section[data-testid="stSidebar"] {
        background-color: #080c15 !important;
        border-right: 1px solid var(--border-subtle) !important;
    }
    section[data-testid="stSidebar"] .stRadio > div {
        gap: 3px;
    }
    section[data-testid="stSidebar"] label {
        background: transparent !important;
        border: 1px solid transparent !important;
        border-radius: 8px !important;
        padding: 8px 10px !important;
        width: 100%;
        color: #94a3b8 !important;
        font-weight: 500 !important;
        font-size: 0.80rem !important;
        letter-spacing: -0.01em;
        transition: all 0.15s ease;
    }
    section[data-testid="stSidebar"] label:hover {
        background: rgba(255, 255, 255, 0.04) !important;
        color: #f8fafc !important;
    }
    section[data-testid="stSidebar"] label:has(input:checked) {
        background: rgba(56, 189, 248, 0.09) !important;
        border: 1px solid rgba(56, 189, 248, 0.25) !important;
        color: #38bdf8 !important;
        font-weight: 600 !important;
    }
    section[data-testid="stSidebar"] [data-baseweb="radio"] > div:first-child {
        display: none !important;
    }

    /* Top Command Bar */
    .cmd-bar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        background: rgba(11, 16, 27, 0.85);
        backdrop-filter: blur(12px);
        border: 1px solid var(--border-subtle);
        border-radius: 12px;
        padding: 10px 16px;
        margin-bottom: 14px;
        flex-wrap: wrap;
        gap: 8px;
    }
    .cmd-left {
        display: flex;
        align-items: center;
        gap: 12px;
    }
    .cmd-badge-sys {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.68rem;
        font-weight: 700;
        letter-spacing: 0.08em;
        color: #38bdf8;
        background: rgba(56, 189, 248, 0.1);
        border: 1px solid rgba(56, 189, 248, 0.25);
        padding: 3px 8px;
        border-radius: 6px;
    }
    .cmd-breadcrumb {
        font-size: 0.85rem;
        font-weight: 600;
        color: #f8fafc;
    }
    .cmd-meta {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.70rem;
        color: #64748b;
    }
    .cmd-right {
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .tele-chip {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.66rem;
        font-weight: 600;
        color: #94a3b8;
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid var(--border-subtle);
        padding: 4px 10px;
        border-radius: 6px;
        display: inline-flex;
        align-items: center;
        gap: 6px;
    }
    .pulse-dot {
        width: 6px;
        height: 6px;
        border-radius: 50%;
        background: #10b981;
        box-shadow: 0 0 8px #10b981;
    }

    /* Grade de 4 KPIs (4 colunas no PC -> 2x2 no Celular) */
    .kpi-grid-4 {
        display: grid;
        grid-template-columns: repeat(4, minmax(0, 1fr));
        gap: 10px;
        margin-bottom: 14px;
    }
    @media (max-width: 900px) {
        .kpi-grid-4 {
            grid-template-columns: repeat(2, minmax(0, 1fr));
            gap: 8px;
        }
    }
    .kpi-card {
        background: linear-gradient(180deg, rgba(16, 23, 38, 0.9) 0%, rgba(11, 16, 27, 0.95) 100%);
        border: 1px solid var(--border-subtle);
        border-radius: 12px;
        padding: 14px 15px;
        position: relative;
        transition: border-color 0.2s ease;
    }
    .kpi-card:hover {
        border-color: rgba(148, 163, 184, 0.28);
    }
    .kpi-top-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .kpi-lbl {
        font-size: 0.66rem;
        font-weight: 600;
        color: #94a3b8;
        text-transform: uppercase;
        letter-spacing: 0.06em;
    }
    .kpi-tag {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.60rem;
        font-weight: 700;
        padding: 2px 6px;
        border-radius: 4px;
    }
    .tag-emerald { background: rgba(16, 185, 129, 0.12); color: #34d399; border: 1px solid rgba(16, 185, 129, 0.25); }
    .tag-cyan { background: rgba(56, 189, 248, 0.12); color: #38bdf8; border: 1px solid rgba(56, 189, 248, 0.25); }
    .tag-violet { background: rgba(129, 140, 248, 0.12); color: #a5b4fc; border: 1px solid rgba(129, 140, 248, 0.25); }
    .tag-rose { background: rgba(244, 63, 94, 0.12); color: #fb7185; border: 1px solid rgba(244, 63, 94, 0.25); }

    .kpi-val {
        font-family: 'JetBrains Mono', monospace;
        font-size: 1.42rem;
        font-weight: 700;
        color: #f8fafc;
        margin: 8px 0 6px 0;
        letter-spacing: -0.03em;
    }
    @media (max-width: 768px) {
        .kpi-val { font-size: 1.12rem; }
        .kpi-card { padding: 11px 12px; }
    }
    .kpi-foot {
        font-size: 0.68rem;
        color: #64748b;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    /* Progress Bar Ultra-fina */
    .thin-bar-bg {
        width: 100%;
        height: 4px;
        background: rgba(255, 255, 255, 0.06);
        border-radius: 99px;
        overflow: hidden;
        margin: 6px 0;
    }
    .thin-bar-fill {
        height: 100%;
        background: linear-gradient(90deg, #38bdf8, #818cf8);
        border-radius: 99px;
    }

    /* Surface Panels */
    .tech-panel {
        background: var(--bg-surface);
        border: 1px solid var(--border-subtle);
        border-radius: 14px;
        padding: 16px;
        margin-bottom: 12px;
    }
    .panel-hdr {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding-bottom: 10px;
        margin-bottom: 12px;
        border-bottom: 1px solid var(--border-subtle);
    }
    .panel-hdr-title {
        font-size: 0.80rem;
        font-weight: 700;
        color: #f8fafc;
        letter-spacing: -0.01em;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .panel-hdr-sub {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.65rem;
        color: #64748b;
    }

    /* Botões Minimalistas */
    .stButton > button {
        background: #111827 !important;
        color: #e2e8f0 !important;
        border: 1px solid rgba(148, 163, 184, 0.16) !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        font-size: 0.75rem !important;
        padding: 0.42rem 0.75rem !important;
        transition: all 0.15s ease !important;
    }
    .stButton > button:hover {
        background: #182236 !important;
        border-color: #38bdf8 !important;
        color: #ffffff !important;
    }
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, rgba(56, 189, 248, 0.22) 0%, rgba(16, 185, 129, 0.22) 100%) !important;
        border: 1px solid #38bdf8 !important;
        color: #38bdf8 !important;
        box-shadow: 0 0 12px rgba(56, 189, 248, 0.18) !important;
    }
    .btn-clear button {
        background: rgba(244, 63, 94, 0.08) !important;
        color: #fb7185 !important;
        border: 1px solid rgba(244, 63, 94, 0.25) !important;
    }
    .btn-clear button:hover {
        background: rgba(244, 63, 94, 0.16) !important;
        border-color: #f43f5e !important;
    }
    .btn-action-icon button {
        background: rgba(56, 189, 248, 0.08) !important;
        color: #38bdf8 !important;
        border: 1px solid rgba(56, 189, 248, 0.25) !important;
    }

    /* Grade do Calendário de Alocações 100% Responsiva (7 colunas fixas PC e Celular) */
    [data-testid="stHorizontalBlock"]:has(> [data-testid="stColumn"]:nth-child(7)),
    [data-testid="stHorizontalBlock"]:has(> [data-testid="column"]:nth-child(7)) {
        display: grid !important;
        grid-template-columns: repeat(7, minmax(0, 1fr)) !important;
        gap: 4px !important;
        width: 100% !important;
        margin-bottom: 4px !important;
    }
    [data-testid="stHorizontalBlock"]:has(> [data-testid="stColumn"]:nth-child(7)) > [data-testid="stColumn"],
    [data-testid="stHorizontalBlock"]:has(> [data-testid="column"]:nth-child(7)) > [data-testid="column"] {
        width: 100% !important;
        min-width: 0 !important;
        max-width: 100% !important;
        flex: 1 1 0% !important;
        padding: 0 !important;
    }
    [data-testid="stHorizontalBlock"]:has(> [data-testid="stColumn"]:nth-child(7)) button,
    [data-testid="stHorizontalBlock"]:has(> [data-testid="column"]:nth-child(7)) button {
        width: 100% !important;
        min-width: 0 !important;
        padding: 4px 1px !important;
        min-height: 36px !important;
        height: 36px !important;
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 0.70rem !important;
        font-weight: 700 !important;
        border-radius: 7px !important;
        line-height: 1 !important;
    }

    /* Data Rows / Ledger Style */
    .ledger-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 9px 12px;
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid var(--border-subtle);
        border-radius: 9px;
        margin-bottom: 6px;
        transition: background 0.15s ease;
    }
    .ledger-row:hover {
        background: rgba(255, 255, 255, 0.04);
    }

    /* Cards de Bancos */
    .bank-card {
        background: var(--bg-surface);
        border: 1px solid var(--border-subtle);
        border-radius: 12px;
        padding: 14px;
        margin-bottom: 10px;
    }
    .bank-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 8px;
        margin-top: 10px;
    }
    .bank-stat {
        background: #080c14;
        border: 1px solid var(--border-subtle);
        border-radius: 8px;
        padding: 8px 10px;
    }
    .bank-stat-lbl {
        font-size: 0.58rem;
        color: #64748b;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .bank-stat-val {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.90rem;
        font-weight: 700;
        color: #f8fafc;
        margin-top: 2px;
    }

    /* Tabela do Calendário Visual do Ciclo */
    .cal-table {
        width: 100%;
        border-collapse: separate;
        border-spacing: 4px;
        margin-top: 8px;
    }
    .cal-th {
        text-align: center;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.62rem;
        font-weight: 700;
        color: #64748b;
        padding: 4px 0;
    }
    .cal-cell {
        background: #080c14;
        border: 1px solid rgba(148, 163, 184, 0.12);
        border-radius: 8px;
        height: 48px;
        vertical-align: top;
        padding: 4px;
        text-align: right;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.64rem;
        font-weight: 600;
    }
    .cal-cell.payday { border-color: #eab308 !important; box-shadow: inset 0 0 6px rgba(234, 179, 8, 0.25); }
    .cal-cell.today { border-color: #38bdf8 !important; box-shadow: 0 0 6px rgba(56, 189, 248, 0.35); }
    .cal-cell.has-entrada { background: rgba(16, 185, 129, 0.14) !important; border-color: rgba(16, 185, 129, 0.55) !important; }
    .cal-cell.has-saida { background: rgba(244, 63, 94, 0.14) !important; border-color: rgba(244, 63, 94, 0.55) !important; }
    .cal-cell.has-reemb-livre { background: rgba(234, 179, 8, 0.14) !important; border-color: rgba(234, 179, 8, 0.65) !important; }
    .cal-cell.has-ambos { background: rgba(245, 158, 11, 0.14) !important; border-color: rgba(245, 158, 11, 0.55) !important; }
    .cal-badge {
        font-size: 0.54rem;
        font-weight: 700;
        font-family: 'JetBrains Mono', monospace;
        display: block;
        text-align: left;
        margin-top: 2px;
        line-height: 1.1;
    }
    .badge-in { color: #34d399; }
    .badge-out { color: #fb7185; }
    .badge-reemb-livre { color: #fbbf24; }

    /* Inputs compactos */
    div[data-testid="stNumberInput"] input,
    div[data-testid="stTextInput"] input {
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 0.80rem !important;
        background-color: #080c14 !important;
        border-radius: 8px !important;
    }

    /* Abas limpas */
    .stTabs [data-baseweb="tab-list"] {
        gap: 4px;
        background-color: #0b101b;
        padding: 4px;
        border-radius: 10px;
        border: 1px solid var(--border-subtle);
    }
    .stTabs [data-baseweb="tab"] {
        height: 32px;
        border-radius: 7px;
        color: #94a3b8;
        font-size: 0.74rem;
        font-weight: 600;
        border: none !important;
        background: transparent;
        padding: 0 12px;
    }
    .stTabs [aria-selected="true"] {
        background-color: rgba(56, 189, 248, 0.12) !important;
        color: #38bdf8 !important;
    }
    .stTabs [data-baseweb="tab-highlight"] { display: none; }
</style>
""", unsafe_allow_html=True)

# ----------------- BASE DE DADOS -----------------
def init_db():
    conn = sqlite3.connect("financas.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS transacoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data TEXT,
            descricao TEXT,
            valor REAL,
            categoria TEXT,
            tipo TEXT,
            banco TEXT DEFAULT 'Nubank',
            meio TEXT DEFAULT 'Cartão de Crédito'
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS lancamentos_previstos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data_prevista TEXT,
            descricao TEXT,
            valor REAL,
            categoria TEXT,
            tipo TEXT,
            banco TEXT DEFAULT 'Nubank',
            fixo INTEGER DEFAULT 0
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS compras_parceladas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            banco TEXT,
            descricao TEXT,
            valor_parcela REAL,
            parcela_atual INTEGER,
            total_parcelas INTEGER,
            mes_ano_fim TEXT,
            categoria TEXT
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS reembolsos_destinados (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data TEXT,
            valor_total REAL,
            detalhes TEXT
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS reembolsos_destinados_itens (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            reembolso_id INTEGER,
            data TEXT,
            banco TEXT,
            acao TEXT,
            valor REAL,
            motivo TEXT,
            estornado INTEGER DEFAULT 0
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS contas_bancarias (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            banco TEXT UNIQUE,
            cor_identificador TEXT,
            tem_cartao INTEGER DEFAULT 1,
            limite_cartao REAL DEFAULT 0,
            limite_liberado REAL DEFAULT 0,
            fatura_atual REAL DEFAULT 0,
            saldo_conta REAL DEFAULT 0,
            limite_cheque_especial REAL DEFAULT 0,
            cheque_especial_usado REAL DEFAULT 0,
            dia_vencimento INTEGER DEFAULT 10,
            dia_fechamento INTEGER DEFAULT 3
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS app_config (
            chave TEXT PRIMARY KEY,
            valor TEXT
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS alocacoes_previstas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data_alocacao TEXT UNIQUE,
            cliente TEXT DEFAULT 'Cliente Alocação',
            valor_diaria REAL DEFAULT 128.78,
            valor_gasolina REAL DEFAULT 30.00,
            valor_pedagio REAL DEFAULT 25.60
        )
    """)
    
    # Migrações seguras
    c.execute("PRAGMA table_info(contas_bancarias)")
    cols = [col[1] for col in c.fetchall()]
    if "tem_cartao" not in cols:
        c.execute("ALTER TABLE contas_bancarias ADD COLUMN tem_cartao INTEGER DEFAULT 1")
    if "limite_liberado" not in cols:
        c.execute("ALTER TABLE contas_bancarias ADD COLUMN limite_liberado REAL DEFAULT 0")
    c.execute("PRAGMA table_info(transacoes)")
    t_cols = [col[1] for col in c.fetchall()]
    if "fitid" not in t_cols:
        c.execute("ALTER TABLE transacoes ADD COLUMN fitid TEXT DEFAULT ''")
    c.execute("PRAGMA table_info(reembolsos_destinados_itens)")
    r_cols = [col[1] for col in c.fetchall()]
    if "status" not in r_cols:
        c.execute("ALTER TABLE reembolsos_destinados_itens ADD COLUMN status TEXT DEFAULT 'Efetivado'")

    c.execute("UPDATE contas_bancarias SET banco = 'Itaú', cor_identificador = '#ec7000' WHERE banco = 'Inter'")
    c.execute("UPDATE transacoes SET banco = 'Itaú' WHERE banco = 'Inter'")
    c.execute("UPDATE contas_bancarias SET cor_identificador = '#ffe600' WHERE banco = 'Mercado Pago'")
    
    c.execute("SELECT COUNT(*) FROM contas_bancarias")
    if c.fetchone()[0] == 0:
        bancos_dados = [
            ("Nubank", "#a855f7", 1, 5000.00, 3046.00, 1954.00, 0.00, 0.00, 0.00, 10, 3),
            ("Caixa Econômica", "#38bdf8", 0, 0.00, 0.00, 0.00, 2000.00, 0.00, 0.00, 15, 8),
            ("Mercado Pago", "#ffe600", 0, 0.00, 0.00, 0.00, 1500.00, 0.00, 0.00, 5, 28),
            ("Bradesco", "#f43f5e", 1, 4000.00, 2200.00, 0.00, 0.00, 1800.00, 0.00, 20, 13),
            ("Itaú", "#ec7000", 1, 6000.00, 5000.00, 0.00, 0.00, 1000.00, 0.00, 25, 18)
        ]
        c.executemany("""
            INSERT INTO contas_bancarias 
            (banco, cor_identificador, tem_cartao, limite_cartao, limite_liberado, fatura_atual, saldo_conta, limite_cheque_especial, cheque_especial_usado, dia_vencimento, dia_fechamento)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, bancos_dados)
    
    conn.commit()
    conn.close()

init_db()

def processar_reembolsos_na_data():
    hoje_str = date.today().strftime("%Y-%m-%d")
    conn = sqlite3.connect("financas.db")
    c = conn.cursor()
    c.execute("""
        SELECT id, banco, acao, valor, motivo, data
        FROM reembolsos_destinados_itens
        WHERE estornado = 0 AND status = 'Previsto' AND data <= ?
    """, (hoje_str,))
    vencidos = c.fetchall()
    for row in vencidos:
        id_item, banco, acao, val, motivo, dt_item = row
        val = float(val)
        dt_fmt = datetime.strptime(dt_item, "%Y-%m-%d").strftime("%d/%m/%Y") if len(dt_item) == 10 else dt_item
        if acao == "Abater Cheque Especial":
            c.execute("UPDATE contas_bancarias SET cheque_especial_usado = MAX(0.0, cheque_especial_usado - ?) WHERE banco = ?", (val, banco))
            c.execute("""
                INSERT INTO transacoes (data, descricao, valor, categoria, tipo, banco, meio)
                VALUES (?, ?, ?, 'Reembolso KM', 'Entrada', ?, 'Abate Cheque Especial')
            """, (dt_fmt, f"Reembolso: {motivo}", val, banco))
        elif acao == "Pagar/Abater Fatura de Cartão":
            c.execute("UPDATE contas_bancarias SET fatura_atual = MAX(0.0, fatura_atual - ?) WHERE banco = ?", (val, banco))
            c.execute("""
                INSERT INTO transacoes (data, descricao, valor, categoria, tipo, banco, meio)
                VALUES (?, ?, ?, 'Reembolso KM', 'Entrada', ?, 'Pagamento de Fatura')
            """, (dt_fmt, f"Reembolso: {motivo}", val, banco))
        elif acao == "Creditar em Conta Corrente":
            c.execute("UPDATE contas_bancarias SET saldo_conta = saldo_conta + ? WHERE banco = ?", (val, banco))
            c.execute("""
                INSERT INTO transacoes (data, descricao, valor, categoria, tipo, banco, meio)
                VALUES (?, ?, ?, 'Reembolso KM', 'Entrada', ?, 'Conta Corrente / Pix')
            """, (dt_fmt, f"Reembolso: {motivo}", val, banco))
        c.execute("UPDATE reembolsos_destinados_itens SET status = 'Efetivado' WHERE id = ?", (id_item,))
    conn.commit()
    conn.close()

processar_reembolsos_na_data()

def get_contas():
    conn = sqlite3.connect("financas.db")
    df = pd.read_sql_query("SELECT * FROM contas_bancarias", conn)
    conn.close()
    return df

def get_transacoes():
    conn = sqlite3.connect("financas.db")
    df = pd.read_sql_query("SELECT * FROM transacoes ORDER BY id DESC", conn)
    conn.close()
    return df

def get_previstos():
    conn = sqlite3.connect("financas.db")
    df = pd.read_sql_query("SELECT * FROM lancamentos_previstos ORDER BY data_prevista ASC", conn)
    conn.close()
    return df

def get_parcelas():
    conn = sqlite3.connect("financas.db")
    df = pd.read_sql_query("SELECT * FROM compras_parceladas ORDER BY id DESC", conn)
    conn.close()
    return df

def get_historico_reembolsos():
    conn = sqlite3.connect("financas.db")
    df = pd.read_sql_query("SELECT * FROM reembolsos_destinados ORDER BY id DESC", conn)
    conn.close()
    return df

def get_alocacoes():
    conn = sqlite3.connect("financas.db")
    df = pd.read_sql_query("SELECT * FROM alocacoes_previstas ORDER BY data_alocacao ASC", conn)
    conn.close()
    return df

def toggle_alocacao_dia(data_str, cliente="Alocação Cliente", valor_diaria=128.78, valor_gasolina=30.00, valor_pedagio=25.60):
    conn = sqlite3.connect("financas.db")
    c = conn.cursor()
    c.execute("SELECT id FROM alocacoes_previstas WHERE data_alocacao = ?", (data_str,))
    row = c.fetchone()
    if row:
        c.execute("DELETE FROM alocacoes_previstas WHERE id = ?", (row[0],))
    else:
        c.execute("""
            INSERT INTO alocacoes_previstas (data_alocacao, cliente, valor_diaria, valor_gasolina, valor_pedagio)
            VALUES (?, ?, ?, ?, ?)
        """, (data_str, cliente, float(valor_diaria), float(valor_gasolina), float(valor_pedagio)))
    conn.commit()
    conn.close()

def definir_dias_uteis_alocacao(lista_datas_str, cliente="Alocação Cliente", valor_diaria=128.78, valor_gasolina=30.00, valor_pedagio=25.60):
    conn = sqlite3.connect("financas.db")
    c = conn.cursor()
    for d_str in lista_datas_str:
        c.execute("SELECT id FROM alocacoes_previstas WHERE data_alocacao = ?", (d_str,))
        if not c.fetchone():
            c.execute("""
                INSERT INTO alocacoes_previstas (data_alocacao, cliente, valor_diaria, valor_gasolina, valor_pedagio)
                VALUES (?, ?, ?, ?, ?)
            """, (d_str, cliente, float(valor_diaria), float(valor_gasolina), float(valor_pedagio)))
    conn.commit()
    conn.close()

def limpar_alocacoes_periodo(dt_ini_str, dt_fim_str):
    conn = sqlite3.connect("financas.db")
    c = conn.cursor()
    c.execute("DELETE FROM alocacoes_previstas WHERE data_alocacao >= ? AND data_alocacao <= ?", (dt_ini_str, dt_fim_str))
    conn.commit()
    conn.close()

def get_reembolsos_itens():
    conn = sqlite3.connect("financas.db")
    df = pd.read_sql_query("SELECT * FROM reembolsos_destinados_itens WHERE estornado = 0 ORDER BY id DESC", conn)
    conn.close()
    return df

def adicionar_previsto(data_str, desc, valor, cat, tipo, banco, meses_repetir=1, fixo=0):
    conn = sqlite3.connect("financas.db")
    c = conn.cursor()
    data_base = datetime.strptime(data_str, "%Y-%m-%d").date()
    
    for i in range(meses_repetir):
        data_mes = data_base + relativedelta(months=i)
        data_final_str = data_mes.strftime("%Y-%m-%d")
        c.execute("""
            INSERT INTO lancamentos_previstos (data_prevista, descricao, valor, categoria, tipo, banco, fixo)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (data_final_str, desc, valor, cat, tipo, banco, fixo))
        
    conn.commit()
    conn.close()

def atualizar_previsto(id_prev, data_str, desc, valor, cat, tipo, banco, fixo):
    id_prev = int(id_prev)
    conn = sqlite3.connect("financas.db")
    c = conn.cursor()
    c.execute("""
        UPDATE lancamentos_previstos
        SET data_prevista = ?, descricao = ?, valor = ?, categoria = ?, tipo = ?, banco = ?, fixo = ?
        WHERE id = ?
    """, (data_str, desc, valor, cat, tipo, banco, fixo, id_prev))
    conn.commit()
    conn.close()

def efetivar_previsto(id_prev):
    id_prev = int(id_prev)
    conn = sqlite3.connect("financas.db")
    c = conn.cursor()
    c.execute("SELECT data_prevista, descricao, valor, categoria, tipo, banco FROM lancamentos_previstos WHERE id = ?", (id_prev,))
    row = c.fetchone()
    if row:
        data_p, desc, valor, cat, tipo, banco = row
        dt_fmt = datetime.now().strftime("%d/%m %H:%M")
        c.execute("""
            INSERT INTO transacoes (data, descricao, valor, categoria, banco, meio, tipo)
            VALUES (?, ?, ?, ?, ?, 'Conta Corrente / Pix', ?)
        """, (dt_fmt, f"{desc} (Efetivado)", valor, cat, banco, tipo))
        if tipo == "Entrada":
            c.execute("UPDATE contas_bancarias SET saldo_conta = saldo_conta + ? WHERE banco = ?", (valor, banco))
        else:
            c.execute("UPDATE contas_bancarias SET saldo_conta = saldo_conta - ? WHERE banco = ?", (valor, banco))
        c.execute("DELETE FROM lancamentos_previstos WHERE id = ?", (id_prev,))
    conn.commit()
    conn.close()

def get_intervalo_ciclo(ano, mes, modo="Ciclo Completo (04 a 03)"):
    dt_ini = date(ano, mes, 4)
    dt_15 = date(ano, mes, 15)
    dt_16 = date(ano, mes, 16)
    dt_fim = date(ano, mes, 3) + relativedelta(months=1)  # Dia 03 do mês seguinte (salário do mês)
    if "1ª Parte" in modo:
        return dt_ini, dt_15, dt_fim
    elif "2ª Parte" in modo:
        return dt_16, dt_fim, dt_fim
    else:
        return dt_ini, dt_fim, dt_fim

def remover_previsto(id_prev):
    id_prev = int(id_prev)
    conn = sqlite3.connect("financas.db")
    c = conn.cursor()
    c.execute("DELETE FROM lancamentos_previstos WHERE id = ?", (id_prev,))
    conn.commit()
    conn.close()

def adicionar_parcela(banco, desc, valor_parcela, parcela_atual, total_parcelas, cat):
    conn = sqlite3.connect("financas.db")
    c = conn.cursor()
    meses_restantes = max(0, total_parcelas - parcela_atual)
    dt_fim = date.today() + relativedelta(months=meses_restantes)
    meses_nomes_pt = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]
    mes_ano_fim = f"{meses_nomes_pt[dt_fim.month - 1]}/{dt_fim.year}"
    
    c.execute("""
        INSERT INTO compras_parceladas (banco, descricao, valor_parcela, parcela_atual, total_parcelas, mes_ano_fim, categoria)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (banco, desc, valor_parcela, parcela_atual, total_parcelas, mes_ano_fim, cat))
    conn.commit()
    conn.close()

def avancar_parcela(id_parc):
    id_parc = int(id_parc)
    conn = sqlite3.connect("financas.db")
    c = conn.cursor()
    c.execute("SELECT parcela_atual, total_parcelas FROM compras_parceladas WHERE id = ?", (id_parc,))
    row = c.fetchone()
    if row:
        p_atual, p_total = row
        if p_atual < p_total:
            nova_atual = p_atual + 1
            meses_restantes = max(0, p_total - nova_atual)
            dt_fim = date.today() + relativedelta(months=meses_restantes)
            meses_nomes_pt = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]
            mes_ano_fim = f"{meses_nomes_pt[dt_fim.month - 1]}/{dt_fim.year}"
            c.execute("UPDATE compras_parceladas SET parcela_atual = ?, mes_ano_fim = ? WHERE id = ?", (nova_atual, mes_ano_fim, id_parc))
    conn.commit()
    conn.close()

def remover_parcela(id_parc):
    id_parc = int(id_parc)
    conn = sqlite3.connect("financas.db")
    c = conn.cursor()
    c.execute("DELETE FROM compras_parceladas WHERE id = ?", (id_parc,))
    conn.commit()
    conn.close()

def limpar_todas_previsoes():
    conn = sqlite3.connect("financas.db")
    c = conn.cursor()
    c.execute("DELETE FROM lancamentos_previstos")
    conn.commit()
    conn.close()

def limpar_extrato_completo():
    conn = sqlite3.connect("financas.db")
    c = conn.cursor()
    c.execute("DELETE FROM transacoes")
    conn.commit()
    conn.close()

def zerar_saldos_e_faturas():
    conn = sqlite3.connect("financas.db")
    c = conn.cursor()
    c.execute("UPDATE contas_bancarias SET fatura_atual = 0.0, saldo_conta = 0.0, cheque_especial_usado = 0.0")
    conn.commit()
    conn.close()

def atualizar_banco_completo(banco, tem_cartao, fatura, lim_cartao, lim_liberado, saldo, lim_cheque, cheque_usado, dia_venc, dia_fech):
    conn = sqlite3.connect("financas.db")
    c = conn.cursor()
    c.execute("""
        UPDATE contas_bancarias 
        SET tem_cartao = ?, fatura_atual = ?, limite_cartao = ?, limite_liberado = ?, saldo_conta = ?, limite_cheque_especial = ?, cheque_especial_usado = ?, dia_vencimento = ?, dia_fechamento = ?
        WHERE banco = ?
    """, (tem_cartao, fatura, lim_cartao, lim_liberado, saldo, lim_cheque, cheque_usado, dia_venc, dia_fech, banco))
    conn.commit()
    conn.close()

def atualizar_vencimentos(banco, dia_venc, dia_fech):
    conn = sqlite3.connect("financas.db")
    c = conn.cursor()
    c.execute("""
        UPDATE contas_bancarias 
        SET dia_vencimento = ?, dia_fechamento = ?
        WHERE banco = ?
    """, (dia_venc, dia_fech, banco))
    conn.commit()
    conn.close()

def atualizar_transacao_extrato(id_tx, nova_data, nova_desc, novo_valor, nova_cat, novo_banco, novo_meio, novo_tipo):
    id_tx = int(id_tx)
    conn = sqlite3.connect("financas.db")
    c = conn.cursor()
    c.execute("SELECT valor, tipo, banco, meio FROM transacoes WHERE id = ?", (id_tx,))
    old = c.fetchone()
    if old:
        old_val, old_tipo, old_banco, old_meio = old
        # Reverte efeito antigo
        if old_tipo == "Saída":
            if old_meio == "Cartão de Crédito":
                c.execute("UPDATE contas_bancarias SET fatura_atual = MAX(0.0, fatura_atual - ?) WHERE banco = ?", (old_val, old_banco))
            else:
                c.execute("UPDATE contas_bancarias SET saldo_conta = saldo_conta + ? WHERE banco = ?", (old_val, old_banco))
        elif old_tipo == "Entrada":
            c.execute("UPDATE contas_bancarias SET saldo_conta = saldo_conta - ? WHERE banco = ?", (old_val, old_banco))

        # Atualiza registro
        c.execute("""
            UPDATE transacoes
            SET data = ?, descricao = ?, valor = ?, categoria = ?, banco = ?, meio = ?, tipo = ?
            WHERE id = ?
        """, (nova_data, nova_desc, novo_valor, nova_cat, novo_banco, novo_meio, novo_tipo, id_tx))

        # Aplica novo efeito
        if novo_tipo == "Saída":
            if novo_meio == "Cartão de Crédito":
                c.execute("UPDATE contas_bancarias SET fatura_atual = fatura_atual + ? WHERE banco = ?", (novo_valor, novo_banco))
            else:
                c.execute("UPDATE contas_bancarias SET saldo_conta = saldo_conta - ? WHERE banco = ?", (novo_valor, novo_banco))
        elif novo_tipo == "Entrada":
            c.execute("UPDATE contas_bancarias SET saldo_conta = saldo_conta + ? WHERE banco = ?", (novo_valor, novo_banco))
    conn.commit()
    conn.close()

def remover_transacao_extrato(id_tx):
    id_tx = int(id_tx)
    conn = sqlite3.connect("financas.db")
    c = conn.cursor()
    c.execute("SELECT valor, tipo, banco, meio FROM transacoes WHERE id = ?", (id_tx,))
    old = c.fetchone()
    if old:
        old_val, old_tipo, old_banco, old_meio = old
        if old_tipo == "Saída":
            if old_meio == "Cartão de Crédito":
                c.execute("UPDATE contas_bancarias SET fatura_atual = MAX(0.0, fatura_atual - ?) WHERE banco = ?", (old_val, old_banco))
            else:
                c.execute("UPDATE contas_bancarias SET saldo_conta = saldo_conta + ? WHERE banco = ?", (old_val, old_banco))
        elif old_tipo == "Entrada":
            c.execute("UPDATE contas_bancarias SET saldo_conta = saldo_conta - ? WHERE banco = ?", (old_val, old_banco))
        c.execute("DELETE FROM transacoes WHERE id = ?", (id_tx,))
    conn.commit()
    conn.close()

def adicionar_transacao(data, desc, valor, cat, banco, meio, tipo):
    conn = sqlite3.connect("financas.db")
    c = conn.cursor()
    c.execute("INSERT INTO transacoes (data, descricao, valor, categoria, banco, meio, tipo) VALUES (?, ?, ?, ?, ?, ?, ?)", (data, desc, valor, cat, banco, meio, tipo))
    if tipo == "Saída":
        if meio == "Cartão de Crédito":
            c.execute("UPDATE contas_bancarias SET fatura_atual = fatura_atual + ? WHERE banco = ?", (valor, banco))
        else:
            c.execute("UPDATE contas_bancarias SET saldo_conta = saldo_conta - ? WHERE banco = ?", (valor, banco))
    elif tipo == "Entrada":
        c.execute("UPDATE contas_bancarias SET saldo_conta = saldo_conta + ? WHERE banco = ?", (valor, banco))
    conn.commit()
    conn.close()

def aplicar_destinacao_reembolso(data_str, valor_total, lista_destinos, efetivar_agora=True):
    conn = sqlite3.connect("financas.db")
    c = conn.cursor()
    logs = []
    status_str = "Efetivado" if efetivar_agora else "Previsto"
    
    c.execute("INSERT INTO reembolsos_destinados (data, valor_total, detalhes) VALUES (?, ?, ?)", (data_str, valor_total, ""))
    reemb_id = c.lastrowid
    
    for item in lista_destinos:
        banco = item["banco"]
        acao = item["acao"]
        val = float(item["valor"])
        motivo = item["motivo"]
        
        if val <= 0:
            continue
            
        logs.append(f"{banco}: R$ {val:,.2f} ({motivo} -> {acao}) [{status_str}]")
        
        c.execute("""
            INSERT INTO reembolsos_destinados_itens (reembolso_id, data, banco, acao, valor, motivo, estornado, status)
            VALUES (?, ?, ?, ?, ?, ?, 0, ?)
        """, (reemb_id, data_str, banco, acao, val, motivo, status_str))
        
        if efetivar_agora:
            if acao == "Abater Cheque Especial":
                c.execute("UPDATE contas_bancarias SET cheque_especial_usado = MAX(0.0, cheque_especial_usado - ?) WHERE banco = ?", (val, banco))
                c.execute("""
                    INSERT INTO transacoes (data, descricao, valor, categoria, tipo, banco, meio)
                    VALUES (?, ?, ?, 'Reembolso KM', 'Entrada', ?, 'Abate Cheque Especial')
                """, (datetime.now().strftime("%d/%m %H:%M"), f"Reembolso: {motivo}", val, banco))
                
            elif acao == "Pagar/Abater Fatura de Cartão":
                c.execute("UPDATE contas_bancarias SET fatura_atual = MAX(0.0, fatura_atual - ?) WHERE banco = ?", (val, banco))
                c.execute("""
                    INSERT INTO transacoes (data, descricao, valor, categoria, tipo, banco, meio)
                    VALUES (?, ?, ?, 'Reembolso KM', 'Entrada', ?, 'Pagamento de Fatura')
                """, (datetime.now().strftime("%d/%m %H:%M"), f"Reembolso: {motivo}", val, banco))
                
            elif acao == "Creditar em Conta Corrente":
                c.execute("UPDATE contas_bancarias SET saldo_conta = saldo_conta + ? WHERE banco = ?", (val, banco))
                c.execute("""
                    INSERT INTO transacoes (data, descricao, valor, categoria, tipo, banco, meio)
                    VALUES (?, ?, ?, 'Reembolso KM', 'Entrada', ?, 'Conta Corrente / Pix')
                """, (datetime.now().strftime("%d/%m %H:%M"), f"Reembolso: {motivo}", val, banco))

    detalhe_geral = " | ".join(logs)
    c.execute("UPDATE reembolsos_destinados SET detalhes = ? WHERE id = ?", (detalhe_geral, reemb_id))
    
    conn.commit()
    conn.close()

def efetivar_reembolso_item(id_item):
    id_item = int(id_item)
    conn = sqlite3.connect("financas.db")
    c = conn.cursor()
    c.execute("SELECT banco, acao, valor, motivo, estornado, status FROM reembolsos_destinados_itens WHERE id = ?", (id_item,))
    row = c.fetchone()
    if row and row[4] == 0 and row[5] == "Previsto":
        banco, acao, val, motivo, _, _ = row
        val = float(val)
        if acao == "Abater Cheque Especial":
            c.execute("UPDATE contas_bancarias SET cheque_especial_usado = MAX(0.0, cheque_especial_usado - ?) WHERE banco = ?", (val, banco))
            c.execute("""
                INSERT INTO transacoes (data, descricao, valor, categoria, tipo, banco, meio)
                VALUES (?, ?, ?, 'Reembolso KM', 'Entrada', ?, 'Abate Cheque Especial')
            """, (datetime.now().strftime("%d/%m %H:%M"), f"Reembolso: {motivo}", val, banco))
        elif acao == "Pagar/Abater Fatura de Cartão":
            c.execute("UPDATE contas_bancarias SET fatura_atual = MAX(0.0, fatura_atual - ?) WHERE banco = ?", (val, banco))
            c.execute("""
                INSERT INTO transacoes (data, descricao, valor, categoria, tipo, banco, meio)
                VALUES (?, ?, ?, 'Reembolso KM', 'Entrada', ?, 'Pagamento de Fatura')
            """, (datetime.now().strftime("%d/%m %H:%M"), f"Reembolso: {motivo}", val, banco))
        elif acao == "Creditar em Conta Corrente":
            c.execute("UPDATE contas_bancarias SET saldo_conta = saldo_conta + ? WHERE banco = ?", (val, banco))
            c.execute("""
                INSERT INTO transacoes (data, descricao, valor, categoria, tipo, banco, meio)
                VALUES (?, ?, ?, 'Reembolso KM', 'Entrada', ?, 'Conta Corrente / Pix')
            """, (datetime.now().strftime("%d/%m %H:%M"), f"Reembolso: {motivo}", val, banco))
        c.execute("UPDATE reembolsos_destinados_itens SET status = 'Efetivado' WHERE id = ?", (id_item,))
    conn.commit()
    conn.close()

def atualizar_item_destino(id_item, nova_data, novo_banco, nova_acao, novo_valor, novo_motivo):
    id_item = int(id_item)
    novo_valor = float(novo_valor)
    conn = sqlite3.connect("financas.db")
    c = conn.cursor()
    c.execute("""
        SELECT banco, acao, valor, motivo, estornado, reembolso_id, status
        FROM reembolsos_destinados_itens
        WHERE id = ?
    """, (id_item,))
    row = c.fetchone()
    if row and row[4] == 0:
        old_banco, old_acao, old_val, old_motivo, _, reemb_id, st_atual = row
        old_val = float(old_val)
        hoje_str = date.today().strftime("%Y-%m-%d")

        # Se já estava efetivado, reverte o efeito antigo nos saldos/faturas/cheque
        if st_atual == "Efetivado":
            if old_acao == "Abater Cheque Especial":
                c.execute("UPDATE contas_bancarias SET cheque_especial_usado = cheque_especial_usado + ? WHERE banco = ?", (old_val, old_banco))
            elif old_acao == "Pagar/Abater Fatura de Cartão":
                c.execute("UPDATE contas_bancarias SET fatura_atual = fatura_atual + ? WHERE banco = ?", (old_val, old_banco))
            elif old_acao == "Creditar em Conta Corrente":
                c.execute("UPDATE contas_bancarias SET saldo_conta = saldo_conta - ? WHERE banco = ?", (old_val, old_banco))

        # Define novo status de acordo com a nova data (se data > hoje, vira Previsto; se <= hoje, vira Efetivado)
        novo_status = "Efetivado" if nova_data <= hoje_str else "Previsto"

        c.execute("""
            UPDATE reembolsos_destinados_itens
            SET data = ?, banco = ?, acao = ?, valor = ?, motivo = ?, status = ?
            WHERE id = ?
        """, (nova_data, novo_banco, nova_acao, novo_valor, novo_motivo, novo_status, id_item))

        # Se o novo status for Efetivado, aplica o novo efeito nos saldos/faturas/cheque
        if novo_status == "Efetivado":
            if nova_acao == "Abater Cheque Especial":
                c.execute("UPDATE contas_bancarias SET cheque_especial_usado = MAX(0.0, cheque_especial_usado - ?) WHERE banco = ?", (novo_valor, novo_banco))
            elif nova_acao == "Pagar/Abater Fatura de Cartão":
                c.execute("UPDATE contas_bancarias SET fatura_atual = MAX(0.0, fatura_atual - ?) WHERE banco = ?", (novo_valor, novo_banco))
            elif nova_acao == "Creditar em Conta Corrente":
                c.execute("UPDATE contas_bancarias SET saldo_conta = saldo_conta + ? WHERE banco = ?", (novo_valor, novo_banco))

        # Recalcula valor_total do lote pai
        c.execute("""
            SELECT COALESCE(SUM(valor), 0.0)
            FROM reembolsos_destinados_itens
            WHERE reembolso_id = ? AND estornado = 0
        """, (reemb_id,))
        novo_tot_lote = c.fetchone()[0]
        c.execute("UPDATE reembolsos_destinados SET valor_total = ? WHERE id = ?", (novo_tot_lote, reemb_id))

    conn.commit()
    conn.close()

def estornar_item_destino(id_item):
    id_item = int(id_item)
    conn = sqlite3.connect("financas.db")
    c = conn.cursor()
    c.execute("SELECT banco, acao, valor, motivo, estornado, reembolso_id, status FROM reembolsos_destinados_itens WHERE id = ?", (id_item,))
    row = c.fetchone()
    if row and row[4] == 0:
        banco, acao, val, motivo, _, reemb_id, st_atual = row
        val = float(val)
        
        if st_atual == "Efetivado":
            if acao == "Abater Cheque Especial":
                c.execute("UPDATE contas_bancarias SET cheque_especial_usado = cheque_especial_usado + ? WHERE banco = ?", (val, banco))
                c.execute("""
                    INSERT INTO transacoes (data, descricao, valor, categoria, tipo, banco, meio)
                    VALUES (?, ?, ?, 'Estorno Reembolso', 'Saída', ?, 'Estorno Abate Cheque')
                """, (datetime.now().strftime("%d/%m %H:%M"), f"Estorno: {motivo}", val, banco))
                
            elif acao == "Pagar/Abater Fatura de Cartão":
                c.execute("UPDATE contas_bancarias SET fatura_atual = fatura_atual + ? WHERE banco = ?", (val, banco))
                c.execute("""
                    INSERT INTO transacoes (data, descricao, valor, categoria, tipo, banco, meio)
                    VALUES (?, ?, ?, 'Estorno Reembolso', 'Saída', ?, 'Estorno Pagamento Fatura')
                """, (datetime.now().strftime("%d/%m %H:%M"), f"Estorno: {motivo}", val, banco))
                
            elif acao == "Creditar em Conta Corrente":
                c.execute("UPDATE contas_bancarias SET saldo_conta = saldo_conta - ? WHERE banco = ?", (val, banco))
                c.execute("""
                    INSERT INTO transacoes (data, descricao, valor, categoria, tipo, banco, meio)
                    VALUES (?, ?, ?, 'Estorno Reembolso', 'Saída', ?, 'Estorno Crédito Conta')
                """, (datetime.now().strftime("%d/%m %H:%M"), f"Estorno: {motivo}", val, banco))

        c.execute("UPDATE reembolsos_destinados_itens SET estornado = 1 WHERE id = ?", (id_item,))
        c.execute("UPDATE reembolsos_destinados SET valor_total = MAX(0.0, valor_total - ?) WHERE id = ?", (val, reemb_id))
        
    conn.commit()
    conn.close()

def gerar_relatorio_pdf(dados_bancos, entradas_m, saidas_m, saldo_proj, total_parc_m, total_rest_parc, diagnosticos_texto):
    tot_saldo = dados_bancos["saldo_conta"].sum()
    tot_fat = dados_bancos[dados_bancos["tem_cartao"] == 1]["fatura_atual"].sum()
    tot_chq = dados_bancos["cheque_especial_usado"].sum()
    
    content_lines = []
    # Cabeçalho
    content_lines.append("BT /F1 16 Tf 50 750 Td (RELATORIO FINANCEIRO CONSOLIDADO & SAUDE) Tj ET")
    data_str = datetime.now().strftime("%d/%m/%Y as %H:%M")
    content_lines.append(f"BT /F1 9 Tf 50 732 Td (Gerado em {data_str} - Balanco Geral do Mes Vigente) Tj ET")
    
    # Linha divisória
    content_lines.append("0.1 0.5 0.8 rg 50 722 512 2 re f")
    
    # Resumo
    y = 700
    content_lines.append(f"BT /F1 12 Tf 50 {y} Td (RESUMO FINANCEIRO CONSOLIDADO:) Tj ET")
    y -= 18
    
    kpis = [
        ("Saldo Total em Conta Corrente", f"R$ {tot_saldo:,.2f}"),
        ("Faturas Totais de Cartao", f"R$ {tot_fat:,.2f}"),
        ("Limite Cheque Especial em Uso", f"R$ {tot_chq:,.2f}"),
        ("Entradas Previstas no Mes", f"+ R$ {entradas_m:,.2f}"),
        ("Saidas Previstas no Mes", f"- R$ {saidas_m:,.2f}"),
        ("Saldo Projetado Final", f"R$ {saldo_proj:,.2f}"),
        ("Parcelas Comprometidas no Mes", f"R$ {total_parc_m:,.2f}"),
        ("Saldo Devedor Restante em Parcelas", f"R$ {total_rest_parc:,.2f}")
    ]
    
    for k, v in kpis:
        safe_k = k.replace("(", "").replace(")", "")
        content_lines.append(f"BT /F1 9 Tf 50 {y} Td ({safe_k}:) Tj ET")
        content_lines.append(f"BT /F1 10 Tf 280 {y} Td ({v}) Tj ET")
        y -= 15
        
    y -= 12
    content_lines.append(f"BT /F1 12 Tf 50 {y} Td (DIRETRIZES PARA OTIMIZACAO DA SUA SAUDE FINANCEIRA:) Tj ET")
    y -= 18
    
    for diag in diagnosticos_texto:
        tit = diag.get("titulo", "").replace("(", "").replace(")", "")
        content_lines.append(f"BT /F1 10 Tf 50 {y} Td ([!] {tit}) Tj ET")
        y -= 14
        
        desc = diag.get("desc", "").replace("(", "").replace(")", "")
        words = desc.split(" ")
        cur_l = "    "
        for w in words:
            if len(cur_l) + len(w) + 1 > 85:
                content_lines.append(f"BT /F1 8 Tf 50 {y} Td ({cur_l}) Tj ET")
                y -= 12
                cur_l = "    " + w
            else:
                cur_l += " " + w
        if cur_l.strip():
            content_lines.append(f"BT /F1 8 Tf 50 {y} Td ({cur_l}) Tj ET")
            y -= 16

    stream_data = "\n".join(content_lines).encode("latin-1", "replace")
    
    objects = [
        b"<< /Type /Catalog /Pages 2 0 R >>",
        b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Contents 4 0 R /Resources << /Font << /F1 5 0 R >> >> >>",
        b"<< /Length " + str(len(stream_data)).encode() + b" >>\nstream\n" + stream_data + b"\nendstream",
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica /Encoding /WinAnsiEncoding >>"
    ]
    
    pdf = bytearray()
    pdf.extend(b"%PDF-1.4\n")
    offsets = []
    for i, obj in enumerate(objects, 1):
        offsets.append(len(pdf))
        pdf.extend(f"{i} 0 obj\n".encode())
        pdf.extend(obj)
        pdf.extend(b"\nendobj\n")
        
    startxref = len(pdf)
    pdf.extend(b"xref\n0 " + str(len(objects) + 1).encode() + b"\n")
    pdf.extend(b"0000000000 65535 f \n")
    for off in offsets:
        pdf.extend(f"{off:010d} 00000 n \n".encode())
    pdf.extend(b"trailer\n<< /Size " + str(len(objects) + 1).encode() + b" /Root 1 0 R >>\n")
    pdf.extend(b"startxref\n" + str(startxref).encode() + b"\n%%EOF")
    return bytes(pdf)

def parse_ofx_content(text):
    transactions = []
    bal_match = re.search(r"<LEDGERBAL>[\s\S]*?<BALAMT>([\-\d\.,]+)", text, re.IGNORECASE)
    ledger_bal = None
    if bal_match:
        try:
            ledger_bal = float(bal_match.group(1).replace(",", "."))
        except:
            pass

    trns = re.findall(r"<STMTTRN>([\s\S]*?)</STMTTRN>", text, re.IGNORECASE)
    if not trns:
        trns = re.findall(r"<STMTTRN>([\s\S]*?)(?=<STMTTRN>|</BANKTRANLIST>|</CCDATA>|</STMTRS>|\Z)", text, re.IGNORECASE)

    for block in trns:
        amt_match = re.search(r"<TRNAMT>([\-\d\.,]+)", block, re.IGNORECASE)
        date_match = re.search(r"<DTPOSTED>(\d{8})", block, re.IGNORECASE)
        memo_match = re.search(r"<MEMO>([^\r\n<]+)", block, re.IGNORECASE)
        name_match = re.search(r"<NAME>([^\r\n<]+)", block, re.IGNORECASE)
        type_match = re.search(r"<TRNTYPE>([^\r\n<]+)", block, re.IGNORECASE)
        fitid_match = re.search(r"<FITID>([^\r\n<]+)", block, re.IGNORECASE)
        
        if amt_match:
            try:
                amt = float(amt_match.group(1).replace(",", "."))
            except:
                continue
                
            raw_date = date_match.group(1) if date_match else ""
            if len(raw_date) == 8:
                formatted_date = f"{raw_date[6:8]}/{raw_date[4:6]}/{raw_date[0:4]}"
            else:
                formatted_date = datetime.now().strftime("%d/%m/%Y")
                
            desc = ""
            if memo_match:
                desc = memo_match.group(1).strip()
            elif name_match:
                desc = name_match.group(1).strip()
            else:
                desc = "Transação OFX"
                
            tipo_trn = type_match.group(1).strip().upper() if type_match else ""
            
            raw_fitid = fitid_match.group(1).strip() if fitid_match else ""
            if not raw_fitid:
                raw_fitid = hashlib.md5(f"{formatted_date}_{amt}_{desc}".encode("utf-8")).hexdigest()[:16]
            transactions.append({
                "data": formatted_date,
                "descricao": desc,
                "valor": amt,
                "tipo_ofx": tipo_trn,
                "fitid": raw_fitid
            })
            
    return transactions, ledger_bal

def get_status_saldo(saldo):
    if saldo < 0:
        return "🚨 No vermelho (Socorro!)", "msg-danger"
    elif saldo == 0.0:
        return "🙏 Preciso de um milagre", "msg-danger"
    elif 0 < saldo <= 20.0:
        return "🍞 Dá só pro pão na chapa", "msg-warning"
    elif 20.0 < saldo <= 100.0:
        return "⚠️ Cuidado com o Pix", "msg-warning"
    elif 100.0 < saldo <= 1000.0:
        return "🧘 Sobrevivendo com dignidade", "msg-neutral"
    else:
        return "🚀 Modo patrão ativado", "msg-success"


def pagar_fatura_cartao(banco_cartao, banco_pagador, valor_pagar):
    valor_pagar = float(valor_pagar)
    if valor_pagar <= 0:
        return
    conn = sqlite3.connect("financas.db")
    c = conn.cursor()
    dt_fmt = datetime.now().strftime("%d/%m %H:%M")
    c.execute("UPDATE contas_bancarias SET saldo_conta = saldo_conta - ? WHERE banco = ?", (valor_pagar, banco_pagador))
    c.execute("UPDATE contas_bancarias SET fatura_atual = MAX(0.0, fatura_atual - ?) WHERE banco = ?", (valor_pagar, banco_cartao))
    c.execute("""
        INSERT INTO transacoes (data, descricao, valor, categoria, tipo, banco, meio)
        VALUES (?, ?, ?, 'Fatura', 'Saída', ?, 'Conta Corrente / Pix')
    """, (dt_fmt, f"Pagamento Fatura {banco_cartao}", valor_pagar, banco_pagador))
    conn.commit()
    conn.close()

df_bancos = get_contas()
df_tx = get_transacoes()
df_prev = get_previstos()
df_parc = get_parcelas()
df_reemb_hist = get_historico_reembolsos()
df_reemb_itens = get_reembolsos_itens()
df_aloc = get_alocacoes()

total_faturas = df_bancos[df_bancos["tem_cartao"] == 1]["fatura_atual"].sum()
total_saldos = df_bancos["saldo_conta"].sum()
total_cheque = df_bancos["cheque_especial_usado"].sum()

msg_total, classe_total = get_status_saldo(total_saldos)

if "bloco_ativo" not in st.session_state:
    st.session_state.bloco_ativo = "previstos"

if "mostrar_form_prev" not in st.session_state:
    st.session_state.mostrar_form_prev = False

if "mostrar_form_parc" not in st.session_state:
    st.session_state.mostrar_form_parc = False

if "mostrar_calc_km" not in st.session_state:
    st.session_state.mostrar_calc_km = False
if "inp_diaria_aloc" not in st.session_state:
    st.session_state.inp_diaria_aloc = 128.78
if "inp_gas_aloc" not in st.session_state:
    st.session_state.inp_gas_aloc = 30.00
if "inp_ped_aloc" not in st.session_state:
    st.session_state.inp_ped_aloc = 25.60
if "mostrar_form_rateio" not in st.session_state:
    st.session_state.mostrar_form_rateio = False
if "recolher_lanc_ciclo" not in st.session_state:
    st.session_state.recolher_lanc_ciclo = True
if "recolher_dest_reemb" not in st.session_state:
    st.session_state.recolher_dest_reemb = True
if "recolher_parc_lista" not in st.session_state:
    st.session_state.recolher_parc_lista = True
if "recolher_extrato_lista" not in st.session_state:
    st.session_state.recolher_extrato_lista = True

if "editando_id" not in st.session_state:
    st.session_state.editando_id = None
if "editando_tx_id" not in st.session_state:
    st.session_state.editando_tx_id = None
if "editando_reemb_id" not in st.session_state:
    st.session_state.editando_reemb_id = None

if "copiando_prev" not in st.session_state:
    st.session_state.copiando_prev = None

hoje = date.today()
dt_ciclo_default = hoje if hoje.day >= 4 else (hoje - relativedelta(months=1))
if "cal_mes" not in st.session_state:
    st.session_state.cal_mes = dt_ciclo_default.month
if "cal_ano" not in st.session_state:
    st.session_state.cal_ano = dt_ciclo_default.year
if "modo_ciclo" not in st.session_state or st.session_state.modo_ciclo not in ["Ciclo Completo (04 a 03)", "1ª Parte (Dia 04 a 15)", "2ª Parte (Dia 16 a 03)"]:
    st.session_state.modo_ciclo = "Ciclo Completo (04 a 03)"


# Garante valores padrão corretos para os parâmetros da alocação
if st.session_state.get("inp_diaria_aloc", 0.0) == 0.0:
    st.session_state.inp_diaria_aloc = 128.78
if st.session_state.get("inp_gas_aloc", 0.0) == 0.0:
    st.session_state.inp_gas_aloc = 30.00
if st.session_state.get("inp_ped_aloc", 0.0) == 0.0:
    st.session_state.inp_ped_aloc = 25.60

# ================= NAVEGAÇÃO LATERAL MINIMALISTA =================
if "menu_nav" not in st.session_state:
    st.session_state.menu_nav = "Overview"

with st.sidebar:
    st.markdown("""
    <div style="display:flex;align-items:center;gap:10px;padding:6px 4px 14px 4px;border-bottom:1px solid rgba(148,163,184,0.12);margin-bottom:12px;">
        <div style="width:28px;height:28px;border-radius:7px;background:linear-gradient(135deg,#38bdf8,#818cf8);display:flex;align-items:center;justify-content:center;font-family:'JetBrains Mono';font-weight:800;color:#060911;font-size:0.85rem;">◈</div>
        <div>
            <div style="font-family:'JetBrains Mono',monospace;font-size:0.88rem;font-weight:800;color:#f8fafc;letter-spacing:-0.02em;">FINANCAS.OS</div>
            <div style="font-size:0.64rem;color:#64748b;">Terminal Financeiro</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    opcoes_menu = [
        "Overview",
        "Bancos & Contas",
        "Calendário de Alocação",
        "Reembolsos & Rateio",
        "Ciclo & Previsões",
        "Cartões & Parcelas",
        "Extrato & OFX",
        "Diagnóstico & PDF",
        "Configurações"
    ]
    if st.session_state.menu_nav not in opcoes_menu:
        st.session_state.menu_nav = "Overview"

    escolha_menu = st.radio("Navegação", opcoes_menu, index=opcoes_menu.index(st.session_state.menu_nav), label_visibility="collapsed")
    if escolha_menu != st.session_state.menu_nav:
        st.session_state.mostrar_form_prev = False
        st.session_state.mostrar_calc_km = False
        st.session_state.mostrar_form_rateio = False
        st.session_state.recolher_lanc_ciclo = True
        st.session_state.recolher_dest_reemb = True
        st.session_state.recolher_parc_lista = True
        st.session_state.recolher_extrato_lista = True
        st.session_state.menu_nav = escolha_menu
        st.rerun()

# ================= CÁLCULOS GLOBAIS =================
dt_hero_ini, dt_hero_fim, dt_sal_03 = get_intervalo_ciclo(st.session_state.cal_ano, st.session_state.cal_mes, "Ciclo Completo (04 a 03)")
meses_nomes_glob = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]
nome_mes_glob = meses_nomes_glob[st.session_state.cal_mes - 1]

entradas_futuras_brutas = 0.0
saidas_comprometidas_ciclo = 0.0
if not df_prev.empty:
    for _, r_p in df_prev.iterrows():
        try:
            d_p = datetime.strptime(r_p["data_prevista"], "%Y-%m-%d").date()
            if dt_hero_ini <= d_p <= dt_hero_fim:
                if r_p["tipo"] == "Entrada":
                    entradas_futuras_brutas += float(r_p["valor"])
                else:
                    saidas_comprometidas_ciclo += float(r_p["valor"])
        except:
            pass

reembolsos_livres_futuros = 0.0
if not df_reemb_itens.empty:
    for _, r_ri in df_reemb_itens.iterrows():
        if r_ri.get("status", "Efetivado") == "Previsto":
            try:
                d_r = datetime.strptime(r_ri["data"], "%Y-%m-%d").date()
                in_w = (dt_hero_ini <= d_r <= dt_hero_fim)
            except:
                in_w = True
            if in_w and r_ri["acao"] == "Creditar em Conta Corrente":
                reembolsos_livres_futuros += float(r_ri["valor"])

renda_futura_livre = (entradas_futuras_brutas - saidas_comprometidas_ciclo) + reembolsos_livres_futuros
projecao_com_futuro = total_saldos + renda_futura_livre

if "aloc_cal_mes" not in st.session_state:
    st.session_state.aloc_cal_mes = st.session_state.cal_mes
if "aloc_cal_ano" not in st.session_state:
    st.session_state.aloc_cal_ano = st.session_state.cal_ano

dt_aloc_g_ini = date(st.session_state.aloc_cal_ano, st.session_state.aloc_cal_mes, 1).strftime("%Y-%m-%d")
dt_aloc_g_fim = date(st.session_state.aloc_cal_ano, st.session_state.aloc_cal_mes, calendar.monthrange(st.session_state.aloc_cal_ano, st.session_state.aloc_cal_mes)[1]).strftime("%Y-%m-%d")
df_aloc_glob = pd.DataFrame()
if not df_aloc.empty:
    df_aloc_glob = df_aloc[(df_aloc["data_alocacao"] >= dt_aloc_g_ini) & (df_aloc["data_alocacao"] <= dt_aloc_g_fim)]

qtd_dias_aloc_glob = len(df_aloc_glob)
tot_diarias_glob = float(df_aloc_glob["valor_diaria"].sum()) if qtd_dias_aloc_glob > 0 else 0.0
tot_gas_glob = float(df_aloc_glob["valor_gasolina"].sum()) if qtd_dias_aloc_glob > 0 else 0.0
tot_ped_glob = float(df_aloc_glob["valor_pedagio"].sum()) if qtd_dias_aloc_glob > 0 else 0.0
tot_lucro_glob = tot_diarias_glob - tot_gas_glob
tot_reemb_aloc_glob = tot_diarias_glob + tot_ped_glob

total_dias_ciclo = max(1, (dt_hero_fim - dt_hero_ini).days)
dias_passados_ciclo = min(total_dias_ciclo, max(0, (hoje - dt_hero_ini).days))
pct_ciclo = int((dias_passados_ciclo / total_dias_ciclo) * 100)

# ================= TOP COMMAND BAR =================
st.markdown(f"""
<div class="cmd-bar">
    <div class="cmd-left">
        <span class="cmd-badge-sys">SYS // LIVE</span>
        <div>
            <div class="cmd-breadcrumb">{st.session_state.menu_nav}</div>
            <div class="cmd-meta">CICLO {nome_mes_glob.upper()}/{st.session_state.cal_ano} • {dt_hero_ini.strftime('%d/%m')} → {dt_hero_fim.strftime('%d/%m')}</div>
        </div>
    </div>
    <div class="cmd-right">
        <span class="tele-chip"><span class="pulse-dot"></span> DB SYNC</span>
        <span class="tele-chip">PAYDAYS: 03 & 16</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ================= 4 KPI CARDS COM SPARKLINES SVG =================
sinal_rf = "+" if renda_futura_livre >= 0 else "-"
cor_rf = "#34d399" if renda_futura_livre >= 0 else "#fb7185"

spark_green = '<svg width="54" height="20" viewBox="0 0 54 20" fill="none"><path d="M1 16 L12 13 L22 15 L34 7 L44 9 L53 2" stroke="#10b981" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>'
spark_cyan = '<svg width="54" height="20" viewBox="0 0 54 20" fill="none"><path d="M1 14 L14 14 L24 10 L36 11 L45 5 L53 3" stroke="#38bdf8" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>'
spark_violet = '<svg width="54" height="20" viewBox="0 0 54 20" fill="none"><path d="M1 18 L11 11 L21 12 L32 6 L43 8 L53 2" stroke="#818cf8" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>'

st.markdown(f"""
<div class="kpi-grid-4">
    <div class="kpi-card">
        <div class="kpi-top-row">
            <span class="kpi-lbl">Liquidez em Conta</span>
            <span class="kpi-tag tag-emerald">REAL</span>
        </div>
        <div class="kpi-val">R$ {total_saldos:,.2f}</div>
        <div class="kpi-foot"><span>Saldo consolidado</span>{spark_green}</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-top-row">
            <span class="kpi-lbl">Renda Futura Livre</span>
            <span class="kpi-tag tag-cyan">CICLO {pct_ciclo}%</span>
        </div>
        <div class="kpi-val" style="color:{cor_rf};">{sinal_rf} R$ {abs(renda_futura_livre):,.2f}</div>
        <div class="thin-bar-bg"><div class="thin-bar-fill" style="width:{pct_ciclo}%;"></div></div>
        <div class="kpi-foot"><span>Projeção: R$ {projecao_com_futuro:,.2f}</span>{spark_cyan}</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-top-row">
            <span class="kpi-lbl">Alocações ({qtd_dias_aloc_glob}d)</span>
            <span class="kpi-tag tag-violet">KM + DIÁRIA</span>
        </div>
        <div class="kpi-val" style="color:#a5b4fc;">R$ {tot_reemb_aloc_glob:,.2f}</div>
        <div class="kpi-foot"><span>Lucro: R$ {tot_lucro_glob:,.2f}</span>{spark_violet}</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-top-row">
            <span class="kpi-lbl">Passivo Cartões</span>
            <span class="kpi-tag tag-rose">FATURAS</span>
        </div>
        <div class="kpi-val" style="color:#fb7185;">R$ {total_faturas:,.2f}</div>
        <div class="kpi-foot"><span>Cheque Esp.: R$ {total_cheque:,.2f}</span></div>
    </div>
</div>
""", unsafe_allow_html=True)

# ================= GRÁFICO SVG TECNOLÓGICO =================
def render_tech_chart_svg():
    st.markdown('<div class="tech-panel">', unsafe_allow_html=True)
    st.markdown("""
    <div class="panel-hdr">
        <span class="panel-hdr-title">◈ Exposição por Instituição Bancária</span>
        <span class="panel-hdr-sub">SALDO VS. FATURA</span>
    </div>
    """, unsafe_allow_html=True)

    max_val = max(
        100.0,
        float(df_bancos["saldo_conta"].max()) if not df_bancos.empty else 0.0,
        float(df_bancos["fatura_atual"].max()) if not df_bancos.empty else 0.0,
        float(df_bancos["cheque_especial_usado"].max()) if not df_bancos.empty else 0.0
    )

    rows_svg = []
    for _, b in df_bancos.iterrows():
        nome_b = str(b["banco"])
        cor_b = str(b["cor_identificador"])
        saldo_v = float(b["saldo_conta"])
        fat_v = float(b["fatura_atual"])
        chq_v = float(b["cheque_especial_usado"])

        w_saldo = min(100.0, (saldo_v / max_val) * 100.0)
        w_fat = min(100.0, (fat_v / max_val) * 100.0)
        w_chq = min(100.0, (chq_v / max_val) * 100.0)

        rows_svg.append(
            f'<div style="margin-bottom:10px;">'
            f'<div style="display:flex;justify-content:space-between;align-items:center;font-size:0.72rem;margin-bottom:4px;">'
            f'<span style="font-weight:600;color:#e2e8f0;display:flex;align-items:center;gap:6px;"><span style="width:7px;height:7px;border-radius:2px;background:{cor_b};display:inline-block;"></span>{nome_b}</span>'
            f'<span style="font-family:JetBrains Mono,monospace;font-size:0.66rem;color:#94a3b8;">'
            f'<span style="color:#34d399;">+R$ {saldo_v:,.0f}</span> · <span style="color:#fb7185;">-R$ {(fat_v+chq_v):,.0f}</span>'
            f'</span>'
            f'</div>'
            f'<div style="display:grid;grid-template-columns:1fr 1fr;gap:4px;background:#080c14;padding:4px;border-radius:6px;border:1px solid rgba(148,163,184,0.08);">'
            f'<div style="height:5px;background:rgba(16,185,129,0.12);border-radius:3px;overflow:hidden;"><div style="width:{w_saldo:.1f}%;height:100%;background:linear-gradient(90deg,#059669,#34d399);"></div></div>'
            f'<div style="height:5px;background:rgba(244,63,94,0.12);border-radius:3px;overflow:hidden;"><div style="width:{max(w_fat, w_chq):.1f}%;height:100%;background:linear-gradient(90deg,#e11d48,#fb7185);"></div></div>'
            f'</div>'
            f'</div>'
        )

    st.markdown("".join(rows_svg), unsafe_allow_html=True)
    st.markdown("""
    <div style="display:flex;gap:14px;font-family:'JetBrains Mono',monospace;font-size:0.62rem;color:#64748b;margin-top:4px;">
        <span><span style="color:#34d399;">■</span> LIQUIDEZ EM CONTA</span>
        <span><span style="color:#fb7185;">■</span> FATURA / CHEQUE ESP.</span>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ================= HELPER CALENDÁRIO DE ALOCAÇÃO + CALCULADORA VINCULADA =================
def render_calendario_alocacoes_e_calc():
    meses_aloc_nomes = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]
    nome_m_aloc = meses_aloc_nomes[st.session_state.aloc_cal_mes - 1]

    st.markdown('<div class="tech-panel">', unsafe_allow_html=True)
    ca_nav1, ca_nav2, ca_nav3 = st.columns([3.8, 1.1, 1.1])
    with ca_nav1:
        st.markdown(f'<div class="panel-hdr-title" style="padding-top:4px;">◈ Matriz de Alocação • {nome_m_aloc}/{st.session_state.aloc_cal_ano}</div>', unsafe_allow_html=True)
    with ca_nav2:
        if st.button("◀", key="aloc_m_ant", help="Mês anterior"):
            if st.session_state.aloc_cal_mes == 1:
                st.session_state.aloc_cal_mes = 12
                st.session_state.aloc_cal_ano -= 1
            else:
                st.session_state.aloc_cal_mes -= 1
            st.rerun()
    with ca_nav3:
        if st.button("▶", key="aloc_m_prox", help="Próximo mês"):
            if st.session_state.aloc_cal_mes == 12:
                st.session_state.aloc_cal_mes = 1
                st.session_state.aloc_cal_ano += 1
            else:
                st.session_state.aloc_cal_mes += 1
            st.rerun()

    cp_a1, cp_a2, cp_a3 = st.columns(3)
    with cp_a1:
        val_diaria_aloc = st.number_input("Diária (R$)", min_value=0.0, value=float(st.session_state.inp_diaria_aloc), step=1.0, key="inp_diaria_aloc")
    with cp_a2:
        val_gas_aloc = st.number_input("Gasolina/dia", min_value=0.0, value=float(st.session_state.inp_gas_aloc), step=1.0, key="inp_gas_aloc")
    with cp_a3:
        val_ped_aloc = st.number_input("Pedágio/dia", min_value=0.0, value=float(st.session_state.inp_ped_aloc), step=1.0, key="inp_ped_aloc")

    datas_marcadas_set = set(df_aloc["data_alocacao"].tolist()) if not df_aloc.empty else set()
    cal_matrix = calendar.monthcalendar(st.session_state.aloc_cal_ano, st.session_state.aloc_cal_mes)
    dias_hdr = ["SEG", "TER", "QUA", "QUI", "SEX", "SÁB", "DOM"]
    hdr_html = '<div style="display:grid;grid-template-columns:repeat(7,1fr);gap:4px;margin:8px 0 4px 0;">'
    for dh in dias_hdr:
        hdr_html += f'<div style="text-align:center;font-family:JetBrains Mono,monospace;font-size:0.60rem;font-weight:700;color:#64748b;">{dh}</div>'
    hdr_html += '</div>'
    st.markdown(hdr_html, unsafe_allow_html=True)

    for sem_idx, semana in enumerate(cal_matrix):
        cols_w = st.columns(7)
        for d_idx, dia_num in enumerate(semana):
            if dia_num == 0:
                cols_w[d_idx].markdown("<div style='height:36px;background:rgba(255,255,255,0.015);border:1px dashed rgba(148,163,184,0.08);border-radius:7px;'></div>", unsafe_allow_html=True)
            else:
                dt_cell = date(st.session_state.aloc_cal_ano, st.session_state.aloc_cal_mes, dia_num)
                dt_cell_str = dt_cell.strftime("%Y-%m-%d")
                is_marked = (dt_cell_str in datas_marcadas_set)
                lbl_btn = f"● {dia_num:02d}" if is_marked else f"{dia_num:02d}"
                if cols_w[d_idx].button(
                    lbl_btn,
                    key=f"cal_aloc_btn_{dt_cell_str}",
                    type="primary" if is_marked else "secondary",
                    help=f"{'Remover' if is_marked else 'Alocar'} dia {dt_cell.strftime('%d/%m/%Y')}"
                ):
                    toggle_alocacao_dia(dt_cell_str, "Alocação Cliente", val_diaria_aloc, val_gas_aloc, val_ped_aloc)
                    st.rerun()

    dt_m_ini = date(st.session_state.aloc_cal_ano, st.session_state.aloc_cal_mes, 1)
    last_day_m = calendar.monthrange(st.session_state.aloc_cal_ano, st.session_state.aloc_cal_mes)[1]
    dt_m_fim = date(st.session_state.aloc_cal_ano, st.session_state.aloc_cal_mes, last_day_m)

    ca_act1, ca_act2 = st.columns(2)
    with ca_act1:
        if st.button("Preencher Dias Úteis (Seg–Sex)", key="btn_marcar_uteis_aloc"):
            uteis = []
            cur_d = dt_m_ini
            while cur_d <= dt_m_fim:
                if cur_d.weekday() < 5:
                    uteis.append(cur_d.strftime("%Y-%m-%d"))
                cur_d += timedelta(days=1)
            definir_dias_uteis_alocacao(uteis, "Alocação Cliente", val_diaria_aloc, val_gas_aloc, val_ped_aloc)
            st.rerun()
    with ca_act2:
        st.markdown('<div class="btn-clear">', unsafe_allow_html=True)
        if st.button("Limpar Mês", key="btn_limpar_mes_aloc"):
            limpar_alocacoes_periodo(dt_m_ini.strftime("%Y-%m-%d"), dt_m_fim.strftime("%Y-%m-%d"))
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    df_aloc_mes = pd.DataFrame()
    if not df_aloc.empty:
        df_aloc_mes = df_aloc[(df_aloc["data_alocacao"] >= dt_m_ini.strftime("%Y-%m-%d")) & (df_aloc["data_alocacao"] <= dt_m_fim.strftime("%Y-%m-%d"))]

    qtd_dias_aloc = len(df_aloc_mes)
    tot_diarias_bruto = float(df_aloc_mes["valor_diaria"].sum()) if qtd_dias_aloc > 0 else 0.0
    tot_gas_mes = float(df_aloc_mes["valor_gasolina"].sum()) if qtd_dias_aloc > 0 else 0.0
    tot_ped_mes = float(df_aloc_mes["valor_pedagio"].sum()) if qtd_dias_aloc > 0 else 0.0
    tot_lucro_liq_aloc = tot_diarias_bruto - tot_gas_mes
    tot_reembolso_esperado = tot_diarias_bruto + tot_ped_mes

    st.markdown(f"""
    <div style="background:#080c14;border:1px solid rgba(148,163,184,0.12);border-radius:10px;padding:10px 12px;margin-top:8px;">
        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px;">
            <span style="font-family:'JetBrains Mono',monospace;font-size:0.66rem;font-weight:700;color:#38bdf8;">TELEMETRIA {nome_m_aloc.upper()}</span>
            <span style="font-family:'JetBrains Mono',monospace;font-size:0.66rem;color:#94a3b8;">{qtd_dias_aloc} DIAS ALOCADOS</span>
        </div>
        <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:6px;font-size:0.66rem;">
            <div style="background:#0e1422;padding:6px 8px;border-radius:6px;border:1px solid rgba(148,163,184,0.08);">
                <span style="color:#64748b;font-size:0.58rem;">COMBUSTÍVEL</span><br>
                <strong style="color:#fb7185;font-family:'JetBrains Mono';font-size:0.78rem;">R$ {tot_gas_mes:,.2f}</strong>
            </div>
            <div style="background:#0e1422;padding:6px 8px;border-radius:6px;border:1px solid rgba(148,163,184,0.08);">
                <span style="color:#64748b;font-size:0.58rem;">PEDÁGIOS</span><br>
                <strong style="color:#fbbf24;font-family:'JetBrains Mono';font-size:0.78rem;">R$ {tot_ped_mes:,.2f}</strong>
            </div>
            <div style="background:#0e1422;padding:6px 8px;border-radius:6px;border:1px solid rgba(148,163,184,0.08);">
                <span style="color:#64748b;font-size:0.58rem;">LUCRO LÍQ.</span><br>
                <strong style="color:#34d399;font-family:'JetBrains Mono';font-size:0.78rem;">R$ {tot_lucro_liq_aloc:,.2f}</strong>
            </div>
            <div style="background:#0e1422;padding:6px 8px;border-radius:6px;border:1px solid rgba(148,163,184,0.08);">
                <span style="color:#64748b;font-size:0.58rem;">REEMBOLSO</span><br>
                <strong style="color:#38bdf8;font-family:'JetBrains Mono';font-size:0.78rem;">R$ {tot_reembolso_esperado:,.2f}</strong>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if qtd_dias_aloc > 0:
        if st.button(f"Exportar para Rateio de Reembolso → R$ {tot_reembolso_esperado:,.2f}", key="btn_enviar_aloc_rateio"):
            st.session_state["reemb_total_val"] = round(tot_reembolso_esperado, 2)
            st.session_state["qtd_destinos"] = 3
            st.session_state["v_A"] = round(tot_ped_mes, 2)
            st.session_state["v_B"] = round(tot_gas_mes, 2)
            st.session_state["v_C"] = round(max(0.0, tot_reembolso_esperado - tot_ped_mes - tot_gas_mes), 2)
            st.session_state.mostrar_form_rateio = True
            st.session_state.menu_nav = "Reembolsos & Rateio"
            st.rerun()

    # Calculadora Rápida vinculada
    ref_diaria_cal = float(st.session_state.get("inp_diaria_aloc", 128.78))
    ref_gas_cal = float(st.session_state.get("inp_gas_aloc", 30.00))
    ref_ped_cal = float(st.session_state.get("inp_ped_aloc", 25.60))
    dias_default_calc = qtd_dias_aloc if qtd_dias_aloc > 0 else 5

    btn_calc_lbl = (
        "Ocultar Simulador"
        if st.session_state.mostrar_calc_km
        else f"Simulador Rápido (Ref: R$ {ref_diaria_cal:,.2f} + R$ {ref_ped_cal:,.2f})"
    )
    if st.button(btn_calc_lbl, key="toggle_calc_km"):
        st.session_state.mostrar_calc_km = not st.session_state.mostrar_calc_km
        st.rerun()

    if st.session_state.mostrar_calc_km:
        st.markdown('<div style="background:#080c14;border:1px solid rgba(148,163,184,0.12);border-radius:10px;padding:10px;margin-top:6px;">', unsafe_allow_html=True)
        c_c1, c_c2 = st.columns(2)
        with c_c1:
            dias_est = st.number_input("Dias", min_value=1, value=dias_default_calc, step=1, key="calc_dias_est")
            diaria_bruta_unit = st.number_input("Diária (R$)", min_value=0.0, value=ref_diaria_cal, step=1.0, key=f"calc_diaria_{ref_diaria_cal:.2f}")
            gasolina_unit = st.number_input("Gasolina/dia", min_value=0.0, value=ref_gas_cal, step=1.0, key=f"calc_gas_{ref_gas_cal:.2f}")
            pedagio_dia = st.number_input("Pedágio/dia", min_value=0.0, value=ref_ped_cal, step=1.0, key=f"calc_ped_{ref_ped_cal:.2f}")
        with c_c2:
            lucro_unit = diaria_bruta_unit - gasolina_unit
            gasolina_est = dias_est * gasolina_unit
            diarias_lucro = dias_est * lucro_unit
            pedagio_total_est = dias_est * pedagio_dia
            total_est = (dias_est * diaria_bruta_unit) + pedagio_total_est
            st.caption(f"Combustível: **R$ {gasolina_est:,.2f}**")
            st.caption(f"Lucro Líquido: **R$ {diarias_lucro:,.2f}**")
            st.caption(f"Pedágios: **R$ {pedagio_total_est:,.2f}**")
            st.markdown(f"**Reembolso Total:** <span style='color:#38bdf8;font-family:JetBrains Mono;font-weight:700;'>R$ {total_est:,.2f}</span>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ================= HELPER DO AI ADVISOR COMPLETO =================
def render_advisor_box():
    st.markdown('<div class="tech-panel">', unsafe_allow_html=True)
    st.markdown("""
    <div class="panel-hdr">
        <span class="panel-hdr-title">◈ AI Financial Engine</span>
        <span class="panel-hdr-sub">PROJEÇÃO & DIAGNÓSTICO</span>
    </div>
    """, unsafe_allow_html=True)

    total_parcelas_mes = float(df_parc["valor_parcela"].sum()) if not df_parc.empty else 0.0
    total_divida_parcelas = sum(max(0, int(r["total_parcelas"]) - int(r["parcela_atual"])) * float(r["valor_parcela"]) for _, r in df_parc.iterrows()) if not df_parc.empty else 0.0

    projecoes_6m = []
    for offset_m in range(6):
        dt_ref_m = date(st.session_state.cal_ano, st.session_state.cal_mes, 1) + relativedelta(months=offset_m)
        label_m = f"{meses_nomes_glob[dt_ref_m.month - 1][:3].upper()}/{str(dt_ref_m.year)[2:]}"
        parc_ativas_m = 0.0
        if not df_parc.empty:
            for _, rp in df_parc.iterrows():
                if (int(rp["parcela_atual"]) + offset_m) <= int(rp["total_parcelas"]):
                    parc_ativas_m += float(rp["valor_parcela"])
        alivio = max(0.0, total_parcelas_mes - parc_ativas_m)
        sobra_m = renda_futura_livre + alivio
        projecoes_6m.append({"mes": label_m, "parcelas": parc_ativas_m, "sobra": sobra_m})

    cols_6m_html = "".join(
        f'<div style="background:#080c14;border:1px solid rgba(148,163,184,0.1);border-radius:7px;padding:6px 3px;text-align:center;">'
        f'<div style="font-family:JetBrains Mono,monospace;font-size:0.58rem;color:#64748b;font-weight:700;">{p6["mes"]}</div>'
        f'<div style="font-family:JetBrains Mono,monospace;font-size:0.70rem;font-weight:700;color:{"#34d399" if p6["sobra"] >= 0 else "#fb7185"};margin-top:2px;">{"+" if p6["sobra"] >= 0 else ""}{p6["sobra"]:,.0f}</div>'
        f'<div style="font-family:JetBrains Mono,monospace;font-size:0.50rem;color:#475569;margin-top:1px;">P:{p6["parcelas"]:,.0f}</div>'
        f'</div>'
        for p6 in projecoes_6m
    )
    st.markdown(
        f'<div style="background:#0a0f1a;border:1px solid rgba(56,189,248,0.18);border-radius:9px;padding:10px;margin-bottom:10px;">'
        f'<div style="font-family:JetBrains Mono,monospace;font-size:0.62rem;font-weight:700;color:#38bdf8;margin-bottom:6px;">HORIZONTE DE LIQUIDEZ (6M)</div>'
        f'<div style="display:grid;grid-template-columns:repeat(6,1fr);gap:4px;">{cols_6m_html}</div>'
        f'</div>',
        unsafe_allow_html=True
    )

    contas_com_saldo = df_bancos[df_bancos["saldo_conta"] > 0].sort_values(by="saldo_conta", ascending=False)
    melhor_conta = contas_com_saldo.iloc[0] if not contas_com_saldo.empty else None
    cartoes_disp = df_bancos[df_bancos["tem_cartao"] == 1].copy()
    melhor_cartao = None
    if not cartoes_disp.empty:
        cartoes_disp["lim_real"] = cartoes_disp.apply(lambda r: float(r["limite_liberado"]) if float(r["limite_liberado"]) > 0 else max(0.0, float(r["limite_cartao"]) - float(r["fatura_atual"])), axis=1)
        validos = cartoes_disp[cartoes_disp["lim_real"] >= 50.0].sort_values(by="lim_real", ascending=False)
        if not validos.empty:
            melhor_cartao = validos.iloc[0]

    with st.expander("Alocação de Capital: Gasolina & Pedágio", expanded=False):
        if qtd_dias_aloc_glob == 0:
            st.caption("Marque os dias na Matriz de Alocação para gerar a estratégia.")
        else:
            st.markdown(
                f"• **Dias Alocados:** {qtd_dias_aloc_glob} dia(s)<br>"
                f"• **Combustível:** R$ {tot_gas_glob:,.2f} • **Pedágio:** R$ {tot_ped_glob:,.2f} • **Lucro Líq.:** R$ {tot_lucro_glob:,.2f}<br>"
                f"• **Fonte Combustível:** {melhor_conta['banco'] if melhor_conta is not None else 'Sem saldo em conta'}<br>"
                f"• **Fonte Pedágio:** {melhor_cartao['banco'] if melhor_cartao is not None else 'Sem limite livre'}",
                unsafe_allow_html=True
            )

    with st.expander("Auditoria de Riscos & Passivos", expanded=False):
        if total_cheque > 0:
            st.warning(f"Cheque Especial ativo: R$ {total_cheque:,.2f} (custo estimado de R$ {total_cheque*0.08:,.2f}/mês).")
        else:
            st.success("Zero exposição em Cheque Especial.")
        if total_parcelas_mes > 0:
            st.info(f"Comprometimento mensal em parcelas: R$ {total_parcelas_mes:,.2f} (Passivo total: R$ {total_divida_parcelas:,.2f}).")

    # Reembolsos futuros em conta
    reemb_fut_cc = pd.DataFrame()
    if not df_reemb_itens.empty:
        reemb_fut_cc = df_reemb_itens[(df_reemb_itens.get("status", "Efetivado") == "Previsto") & (df_reemb_itens["acao"] == "Creditar em Conta Corrente")]
    if not reemb_fut_cc.empty:
        with st.expander("Alocação de Reembolsos Futuros em Conta", expanded=False):
            tot_r_cc = float(reemb_fut_cc["valor"].sum())
            st.info(f"Você possui R$ {tot_r_cc:,.2f} previstos para Conta Corrente. Priorize zerar cheque especial ou manter como capital de giro para combustível.")

    st.markdown('</div>', unsafe_allow_html=True)

# ================= PÁGINAS =================
if st.session_state.menu_nav == "Overview":
    col_main_left, col_main_right = st.columns([1.15, 1.0], gap="medium")
    with col_main_left:
        render_calendario_alocacoes_e_calc()
    with col_main_right:
        render_tech_chart_svg()
        render_advisor_box()

    # Ledger Recente Recolhível
    st.markdown('<div class="tech-panel">', unsafe_allow_html=True)
    ct1, ct2 = st.columns([4, 1.2])
    with ct1:
        st.markdown(f'<div class="panel-hdr-title">◈ Ledger de Transações ({len(df_tx)})</div>', unsafe_allow_html=True)
    with ct2:
        if st.button("Expandir" if st.session_state.recolher_extrato_lista else "Recolher", key="btn_rec_dash_tx"):
            st.session_state.recolher_extrato_lista = not st.session_state.recolher_extrato_lista
            st.rerun()

    if st.session_state.recolher_extrato_lista:
        st.caption(f"Ledger recolhido ({len(df_tx)} registros). Clique em Expandir para visualizar.")
    elif df_tx.empty:
        st.caption("Nenhuma movimentação registrada.")
    else:
        for _, row in df_tx.head(8).iterrows():
            is_s = row["tipo"] == "Saída"
            st.markdown(f"""
            <div class="ledger-row">
                <div>
                    <div style="font-size:0.78rem;font-weight:600;color:#f8fafc;">{row['descricao']}</div>
                    <div style="font-family:'JetBrains Mono',monospace;font-size:0.62rem;color:#64748b;">{row['data']} · {row['banco']} · {row['categoria']}</div>
                </div>
                <div style="font-family:'JetBrains Mono',monospace;font-weight:700;font-size:0.84rem;color:{'#fb7185' if is_s else '#34d399'};">
                    {'-' if is_s else '+'} R$ {row['valor']:,.2f}
                </div>
            </div>
            """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.menu_nav == "Calendário de Alocação":
    render_calendario_alocacoes_e_calc()

elif st.session_state.menu_nav == "Bancos & Contas":
    cols_b = st.columns(2, gap="medium")
    for idx_b, (_, b) in enumerate(df_bancos.iterrows()):
        with cols_b[idx_b % 2]:
            b_saldo = float(b["saldo_conta"])
            tem_c = (b.get("tem_cartao", 1) == 1)
            lim_tot = float(b.get("limite_cartao", 0.0))
            lim_lib = float(b.get("limite_liberado", 0.0))
            lim_exib = lim_lib if lim_lib > 0 else max(0.0, lim_tot - float(b["fatura_atual"]))
            st.markdown(f"""
            <div class="bank-card">
                <div style="display:flex;justify-content:space-between;align-items:center;">
                    <span style="font-weight:700;font-size:0.88rem;color:#f8fafc;display:flex;align-items:center;gap:8px;">
                        <span style="width:8px;height:8px;border-radius:2px;background:{b['cor_identificador']};display:inline-block;"></span>
                        {b['banco']}
                    </span>
                    <span class="kpi-tag {'tag-cyan' if tem_c else 'tag-emerald'}">{'CONTA + CRÉDITO' if tem_c else 'CONTA CORRENTE'}</span>
                </div>
                <div class="bank-grid">
                    <div class="bank-stat"><div class="bank-stat-lbl">Saldo Conta</div><div class="bank-stat-val">R$ {b_saldo:,.2f}</div></div>
                    <div class="bank-stat"><div class="bank-stat-lbl">Cheque Especial</div><div class="bank-stat-val" style="color:{'#fb7185' if b['cheque_especial_usado']>0 else '#94a3b8'};">R$ {b['cheque_especial_usado']:,.2f}</div></div>
                    {f'<div class="bank-stat"><div class="bank-stat-lbl">Fatura (Venc {int(b.get("dia_vencimento",10))} / Fech {int(b.get("dia_fechamento",3))})</div><div class="bank-stat-val" style="color:#fb7185;">R$ {b["fatura_atual"]:,.2f}</div></div><div class="bank-stat"><div class="bank-stat-lbl">Limite Livre / Total</div><div class="bank-stat-val" style="color:#34d399;">R$ {lim_exib:,.2f} <span style="font-size:0.65rem;color:#64748b;">/ {lim_tot:,.0f}</span></div></div>' if tem_c else ''}
                </div>
            </div>
            """, unsafe_allow_html=True)

            if tem_c and float(b["fatura_atual"]) > 0:
                with st.expander(f"Pagar Fatura {b['banco']} (R$ {b['fatura_atual']:,.2f})", expanded=False):
                    cp1, cp2 = st.columns(2)
                    with cp1:
                        b_pag = st.selectbox("Debitar de qual conta?", df_bancos["banco"].tolist(), key=f"pag_fat_src_{b['banco']}")
                    with cp2:
                        v_pag = st.number_input("Valor a Pagar (R$)", min_value=0.01, value=float(b["fatura_atual"]), step=10.0, key=f"pag_fat_val_{b['banco']}")
                    if st.button("Confirmar Pagamento", key=f"btn_pag_fat_{b['banco']}", type="primary"):
                        pagar_fatura_cartao(b["banco"], b_pag, v_pag)
                        st.success("Fatura abatida com sucesso!")
                        st.rerun()

elif st.session_state.menu_nav == "Reembolsos & Rateio":
    st.markdown('<div class="tech-panel">', unsafe_allow_html=True)
    st.markdown('<div class="panel-hdr"><span class="panel-hdr-title">◈ Rateio & Destinação de Reembolso KM</span><span class="panel-hdr-sub">AUTO-DISTRIBUIÇÃO</span></div>', unsafe_allow_html=True)

    if st.button("Ocultar Formulário" if st.session_state.mostrar_form_rateio else "Novo Rateio de Reembolso", key="toggle_rat_page"):
        st.session_state.mostrar_form_rateio = not st.session_state.mostrar_form_rateio
        st.rerun()

    if st.session_state.mostrar_form_rateio:
        if "qtd_destinos" not in st.session_state: st.session_state.qtd_destinos = 2
        if "reemb_total_val" not in st.session_state: st.session_state["reemb_total_val"] = 617.00
        if "v_A" not in st.session_state: st.session_state["v_A"] = 150.00
        if "v_B" not in st.session_state: st.session_state["v_B"] = round(max(0.0, st.session_state["reemb_total_val"] - st.session_state["v_A"]), 2)
        for l_i in ["C", "D", "E"]:
            if f"v_{l_i}" not in st.session_state: st.session_state[f"v_{l_i}"] = 0.0

        def recalc_dest():
            qtd = st.session_state.get("qtd_destinos", 2)
            tot = float(st.session_state.get("reemb_total_val", 0.0))
            lets = ["A", "B", "C", "D", "E"]
            if qtd == 1: st.session_state["v_A"] = round(tot, 2)
            else:
                s_ant = sum(float(st.session_state.get(f"v_{lets[i]}", 0.0)) for i in range(qtd - 1))
                st.session_state[f"v_{lets[qtd-1]}"] = round(max(0.0, tot - s_ant), 2)

        c_q1, c_q2, c_q3 = st.columns([1.2, 1.2, 1])
        with c_q1: data_receb = st.date_input("Data Recebimento", value=date.today(), key="reemb_dt_pg")
        with c_q2: val_tot_r = st.number_input("Valor Total (R$)", min_value=0.01, step=10.0, key="reemb_total_val", on_change=recalc_dest)
        with c_q3:
            qtd_esc = st.selectbox("Destinos", [1, 2, 3, 4, 5], index=[1, 2, 3, 4, 5].index(st.session_state.qtd_destinos))
            if qtd_esc != st.session_state.qtd_destinos:
                st.session_state.qtd_destinos = qtd_esc
                recalc_dest()
                st.rerun()

        dests = []
        b_list = df_bancos["banco"].tolist()
        lets = ["A", "B", "C", "D", "E"]
        mots = ["Pedágio no Cartão", "Gasolina", "Lucro Líquido Diárias", "Ajuste", "Reserva"]
        for i in range(st.session_state.qtd_destinos):
            lt = lets[i]
            is_ult = (i == st.session_state.qtd_destinos - 1)
            c1, c2, c3, c4 = st.columns([1.2, 1, 1.5, 1.5])
            with c1: bd = st.selectbox(f"Banco ({lt})", b_list, index=min(i, len(b_list)-1), key=f"b_{lt}")
            with c2: vd = st.number_input(f"Valor ({lt})", min_value=0.0, step=10.0, key=f"v_{lt}", on_change=(recalc_dest if not is_ult else None))
            with c3: ad = st.selectbox(f"Ação ({lt})", ["Pagar/Abater Fatura de Cartão", "Abater Cheque Especial", "Creditar em Conta Corrente"], index=min(i, 2), key=f"ac_{lt}")
            with c4: md = st.text_input(f"Motivo ({lt})", value=mots[i], key=f"m_{lt}")
            dests.append({"banco": bd, "acao": ad, "valor": vd, "motivo": md})

        soma_at = sum(d["valor"] for d in dests)
        dif_at = val_tot_r - soma_at
        st.caption(f"Distribuído: **R$ {soma_at:,.2f}** / R$ {val_tot_r:,.2f} • Diferença: **R$ {dif_at:,.2f}**")

        if st.button("Executar Rateio", type="primary"):
            ativos = [d for d in dests if d["valor"] > 0]
            if ativos:
                aplicar_destinacao_reembolso(data_receb.strftime("%Y-%m-%d"), val_tot_r, ativos, efetivar_agora=(data_receb <= date.today()))
                st.session_state.mostrar_form_rateio = False
                st.success("Rateio executado!")
                st.rerun()

    # Destinações Ativas recolhíveis com Edição, Baixa e Estorno
    df_itens_hist = get_reembolsos_itens()
    if not df_itens_hist.empty:
        cda1, cda2 = st.columns([4, 1.2])
        with cda1: st.markdown(f'<div class="panel-hdr-title" style="margin-top:12px;">◈ Destinações Ativas ({len(df_itens_hist)})</div>', unsafe_allow_html=True)
        with cda2:
            if st.button("Expandir" if st.session_state.recolher_dest_reemb else "Recolher", key="rec_da_pg"):
                st.session_state.recolher_dest_reemb = not st.session_state.recolher_dest_reemb
                st.rerun()

        if st.session_state.recolher_dest_reemb:
            st.caption(f"Lista recolhida ({len(df_itens_hist)} itens). Clique em Expandir para visualizar.")
        else:
            if st.session_state.editando_reemb_id is not None:
                reemb_ed_df = df_itens_hist[df_itens_hist["id"] == st.session_state.editando_reemb_id]
                if not reemb_ed_df.empty:
                    r_ed = reemb_ed_df.iloc[0]
                    with st.form("form_ed_reemb_pro"):
                        st.markdown(f"**Editando Destinação #{r_ed['id']}**")
                        try: dt_b = datetime.strptime(str(r_ed["data"]), "%Y-%m-%d").date()
                        except: dt_b = date.today()
                        ce1, ce2, ce3 = st.columns(3)
                        with ce1:
                            ed_dt = st.date_input("Data", value=dt_b)
                            b_l = df_bancos["banco"].tolist()
                            ed_bc = st.selectbox("Banco", b_l, index=b_l.index(r_ed["banco"]) if r_ed["banco"] in b_l else 0)
                        with ce2:
                            ed_vl = st.number_input("Valor", min_value=0.01, value=float(r_ed["valor"]), step=10.0)
                            ac_l = ["Pagar/Abater Fatura de Cartão", "Abater Cheque Especial", "Creditar em Conta Corrente"]
                            ed_ac = st.selectbox("Ação", ac_l, index=ac_l.index(r_ed["acao"]) if r_ed["acao"] in ac_l else 0)
                        with ce3:
                            ed_mt = st.text_input("Motivo", value=str(r_ed["motivo"]))
                        sb1, sb2 = st.columns(2)
                        with sb1:
                            if st.form_submit_button("Salvar"):
                                atualizar_item_destino(int(r_ed["id"]), ed_dt.strftime("%Y-%m-%d"), ed_bc, ed_ac, ed_vl, ed_mt)
                                st.session_state.editando_reemb_id = None
                                st.rerun()
                        with sb2:
                            if st.form_submit_button("Cancelar"):
                                st.session_state.editando_reemb_id = None
                                st.rerun()

            for _, item in df_itens_hist.iterrows():
                st_it = item.get("status", "Efetivado")
                cor_it = "#fbbf24" if st_it == "Previsto" else "#34d399"
                ci, cb1, cb2, cb3 = st.columns([4.2, 0.7, 0.7, 0.7])
                with ci:
                    st.markdown(f'<div class="ledger-row" style="border-left:3px solid {cor_it};"><div><strong>{item["banco"]}</strong> · {item["motivo"]}<br><span style="font-family:JetBrains Mono;font-size:0.62rem;color:#64748b;">{item["data"]} · {item["acao"]} · {st_it.upper()}</span></div><div style="font-family:JetBrains Mono;font-weight:700;color:{cor_it};">R$ {item["valor"]:,.2f}</div></div>', unsafe_allow_html=True)
                with cb1:
                    if st.button("Editar", key=f"ed_r_pg_{item['id']}"):
                        st.session_state.editando_reemb_id = int(item["id"])
                        st.rerun()
                with cb2:
                    if st_it == "Previsto":
                        if st.button("Baixar", key=f"ef_r_pg_{item['id']}"):
                            efetivar_reembolso_item(item["id"])
                            st.rerun()
                with cb3:
                    st.markdown('<div class="btn-clear">', unsafe_allow_html=True)
                    if st.button("Estornar", key=f"est_pg_{item['id']}"):
                        estornar_item_destino(item["id"])
                        st.rerun()
                    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.menu_nav == "Ciclo & Previsões":
    st.markdown('<div class="tech-panel">', unsafe_allow_html=True)
    c_top1, c_top2, c_top3, c_top4 = st.columns([2.5, 1.5, 0.8, 0.8])
    with c_top1:
        st.markdown(f'<div class="panel-hdr-title" style="padding-top:4px;">◈ Ciclo {nome_mes_glob}/{st.session_state.cal_ano}</div>', unsafe_allow_html=True)
    with c_top2:
        opcoes_ciclo = ["Ciclo Completo (04 a 03)", "1ª Parte (Dia 04 a 15)", "2ª Parte (Dia 16 a 03)"]
        modo_sel = st.selectbox("Apuração", opcoes_ciclo, index=opcoes_ciclo.index(st.session_state.modo_ciclo), label_visibility="collapsed")
        if modo_sel != st.session_state.modo_ciclo:
            st.session_state.modo_ciclo = modo_sel
            st.rerun()
    with c_top3:
        if st.button("◀", key="cic_ant_pg"):
            st.session_state.cal_mes = 12 if st.session_state.cal_mes == 1 else st.session_state.cal_mes - 1
            if st.session_state.cal_mes == 12: st.session_state.cal_ano -= 1
            st.rerun()
    with c_top4:
        if st.button("▶", key="cic_prox_pg"):
            st.session_state.cal_mes = 1 if st.session_state.cal_mes == 12 else st.session_state.cal_mes + 1
            if st.session_state.cal_mes == 1: st.session_state.cal_ano += 1
            st.rerun()

    dt_ciclo_ini, dt_ciclo_fim, dt_salario_03 = get_intervalo_ciclo(st.session_state.cal_ano, st.session_state.cal_mes, st.session_state.modo_ciclo)
    dt_full_ini, dt_full_fim, _ = get_intervalo_ciclo(st.session_state.cal_ano, st.session_state.cal_mes, "Ciclo Completo (04 a 03)")

    df_prev_c = df_prev[df_prev["data_prevista"].apply(lambda d: dt_ciclo_ini <= datetime.strptime(d, "%Y-%m-%d").date() <= dt_ciclo_fim)] if not df_prev.empty else pd.DataFrame()
    df_reemb_c = df_reemb_itens[df_reemb_itens["data"].apply(lambda d: dt_ciclo_ini <= datetime.strptime(d, "%Y-%m-%d").date() <= dt_ciclo_fim)] if not df_reemb_itens.empty else pd.DataFrame()

    ent_base = float(df_prev_c[df_prev_c["tipo"] == "Entrada"]["valor"].sum()) if not df_prev_c.empty else 0.0
    sai_base = float(df_prev_c[df_prev_c["tipo"] == "Saída"]["valor"].sum()) if not df_prev_c.empty else 0.0
    reemb_tot_c = float(df_reemb_c["valor"].sum()) if not df_reemb_c.empty else 0.0
    reemb_comp_c = float(df_reemb_c[df_reemb_c["acao"] != "Creditar em Conta Corrente"]["valor"].sum()) if not df_reemb_c.empty else 0.0

    ent_tot_c = ent_base + reemb_tot_c
    sai_tot_c = sai_base + reemb_comp_c
    proj_c = total_saldos + ent_tot_c - sai_tot_c

    st.markdown(f"""
    <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:8px;margin:10px 0;">
        <div class="bank-stat"><div class="bank-stat-lbl">A Receber (Bruto)</div><div class="bank-stat-val" style="color:#34d399;">+ R$ {ent_tot_c:,.2f}</div></div>
        <div class="bank-stat"><div class="bank-stat-lbl">Saídas + Destinados</div><div class="bank-stat-val" style="color:#fb7185;">- R$ {sai_tot_c:,.2f}</div></div>
        <div class="bank-stat"><div class="bank-stat-lbl">Saldo Atual</div><div class="bank-stat-val">R$ {total_saldos:,.2f}</div></div>
        <div class="bank-stat"><div class="bank-stat-lbl">Projeção Final</div><div class="bank-stat-val" style="color:{'#34d399' if proj_c >= 0 else '#fb7185'};">R$ {proj_c:,.2f}</div></div>
    </div>
    """, unsafe_allow_html=True)

    # Calendário Visual do Ciclo (04/MM a 03/MM+1)
    eventos_por_data = {}
    if not df_prev.empty:
        for _, row in df_prev.iterrows():
            try:
                dt_obj = datetime.strptime(row["data_prevista"], "%Y-%m-%d").date()
                if dt_full_ini <= dt_obj <= dt_full_fim:
                    ev_dict = row.to_dict()
                    ev_dict["papel_cal"] = "EntradaLivre" if row["tipo"] == "Entrada" else "SaidaComprometida"
                    eventos_por_data.setdefault(dt_obj, []).append(ev_dict)
            except:
                pass

    if not df_reemb_itens.empty:
        reemb_por_data_rows = {}
        for _, row_r in df_reemb_itens.iterrows():
            try:
                dt_r = datetime.strptime(row_r["data"], "%Y-%m-%d").date()
                if dt_full_ini <= dt_r <= dt_full_fim:
                    reemb_por_data_rows.setdefault(dt_r, []).append(row_r)
            except:
                pass
        for dt_r, lista_r in reemb_por_data_rows.items():
            soma_dest = sum(float(x["valor"]) for x in lista_r if x["acao"] != "Creditar em Conta Corrente")
            if soma_dest > 0:
                eventos_por_data.setdefault(dt_r, []).append({"valor": soma_dest, "papel_cal": "EntradaCobertura"})
            for r_item in lista_r:
                if r_item["acao"] == "Creditar em Conta Corrente":
                    eventos_por_data.setdefault(dt_r, []).append({"valor": r_item["valor"], "papel_cal": "ReembSemDestino"})
                else:
                    eventos_por_data.setdefault(dt_r, []).append({"valor": r_item["valor"], "papel_cal": "SaidaComprometida"})

    start_grid = dt_full_ini - timedelta(days=dt_full_ini.weekday())
    end_grid = dt_full_fim + timedelta(days=(6 - dt_full_fim.weekday()))
    html_cal = '<table class="cal-table"><thead><tr>' + ''.join(f'<th class="cal-th">{d}</th>' for d in ["SEG", "TER", "QUA", "QUI", "SEX", "SÁB", "DOM"]) + '</tr></thead><tbody>'
    cur_dt = start_grid
    while cur_dt <= end_grid:
        html_cal += '<tr>'
        for _ in range(7):
            if not (dt_full_ini <= cur_dt <= dt_full_fim):
                html_cal += f'<td class="cal-cell" style="opacity:0.2;"><span style="color:#64748b;">{cur_dt.day:02d}/{cur_dt.month:02d}</span></td>'
            else:
                classes = ["cal-cell"]
                if cur_dt == hoje: classes.append("today")
                if cur_dt.day in [3, 16]: classes.append("payday")
                badges_html = ""
                if cur_dt in eventos_por_data:
                    evs = eventos_por_data[cur_dt]
                    t_in = any(e["papel_cal"] == "EntradaLivre" for e in evs)
                    t_am = any(e["papel_cal"] == "ReembSemDestino" for e in evs)
                    t_out = any(e["papel_cal"] == "SaidaComprometida" for e in evs)
                    if (t_in or t_am) and t_out: classes.append("has-ambos")
                    elif t_out: classes.append("has-saida")
                    elif t_am: classes.append("has-reemb-livre")
                    elif t_in: classes.append("has-entrada")
                    for ev in evs:
                        p = ev["papel_cal"]
                        cb = "badge-out" if p == "SaidaComprometida" else ("badge-reemb-livre" if p == "ReembSemDestino" else "badge-in")
                        sb = "-" if p == "SaidaComprometida" else "+"
                        badges_html += f'<span class="cal-badge {cb}">{sb}{ev["valor"]:,.0f}</span>'
                lbl_d = f"{cur_dt.day:02d}/{cur_dt.month:02d}" if cur_dt.month != st.session_state.cal_mes else f"{cur_dt.day:02d}"
                cor_n = "#eab308" if cur_dt.day in [3, 16] else ("#38bdf8" if cur_dt == hoje else "#94a3b8")
                html_cal += f'<td class="{" ".join(classes)}"><span style="color:{cor_n};">{lbl_d}</span>{badges_html}</td>'
            cur_dt += timedelta(days=1)
        html_cal += '</tr>'
    html_cal += '</tbody></table>'
    st.markdown(html_cal, unsafe_allow_html=True)

    # Formulário recolhível de Novo Lançamento Previsto
    ca_b1, ca_b2 = st.columns([3, 1])
    with ca_b1:
        if st.button("Ocultar Formulário" if st.session_state.mostrar_form_prev else "Agendar Novo Lançamento", key="tog_fp_pg"):
            st.session_state.mostrar_form_prev = not st.session_state.mostrar_form_prev
            st.rerun()
    with ca_b2:
        st.markdown('<div class="btn-clear">', unsafe_allow_html=True)
        if st.button("Limpar Todos", key="limp_all_p_pg"):
            limpar_todas_previsoes()
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    if st.session_state.mostrar_form_prev:
        with st.form("form_add_prev_pro"):
            cp1, cp2, cp3 = st.columns(3)
            with cp1:
                d_sel = st.date_input("Data Início", value=date.today())
                t_sel = st.selectbox("Tipo", ["Entrada", "Saída"])
            with cp2:
                v_sel = st.number_input("Valor (R$)", min_value=0.01, value=1500.00, step=50.0)
                b_sel = st.selectbox("Banco", df_bancos["banco"].tolist())
            with cp3:
                ds_sel = st.text_input("Descrição", value="Salário / Conta")
                ct_sel = st.selectbox("Categoria", ["Salário", "Renda", "Fatura", "Contas Fixas", "Lazer", "Outros"])
            fx_chk = st.checkbox("Recorrente (Fixo)", value=True)
            m_qtd = st.slider("Repetir por quantos meses?", 1, 12, 1)
            if st.form_submit_button("Confirmar Agendamento"):
                adicionar_previsto(d_sel.strftime("%Y-%m-%d"), ds_sel, v_sel, ct_sel, t_sel, b_sel, m_qtd, 1 if fx_chk else 0)
                st.session_state.mostrar_form_prev = False
                st.rerun()

    # Lista recolhível de Lançamentos do Ciclo
    clc1, clc2 = st.columns([4, 1.2])
    with clc1: st.markdown(f'<div class="panel-hdr-title" style="margin-top:10px;">◈ Lançamentos do Ciclo ({len(df_prev_c)})</div>', unsafe_allow_html=True)
    with clc2:
        if st.button("Expandir" if st.session_state.recolher_lanc_ciclo else "Recolher", key="rec_lc_pg"):
            st.session_state.recolher_lanc_ciclo = not st.session_state.recolher_lanc_ciclo
            st.rerun()

    if st.session_state.recolher_lanc_ciclo:
        st.caption(f"Lista recolhida ({len(df_prev_c)} itens). Clique em Expandir para visualizar.")
    else:
        for _, rp in df_prev_c.iterrows():
            is_e = rp["tipo"] == "Entrada"
            c1, c2, c3 = st.columns([4.4, 0.8, 0.8])
            with c1: st.markdown(f'<div class="ledger-row"><div><strong>{rp["descricao"]}</strong><br><span style="font-family:JetBrains Mono;font-size:0.62rem;color:#64748b;">{rp["data_prevista"]} · {rp["banco"]}</span></div><div style="font-family:JetBrains Mono;font-weight:700;color:{"#34d399" if is_e else "#fb7185"};">{"+" if is_e else "-"} R$ {rp["valor"]:,.2f}</div></div>', unsafe_allow_html=True)
            with c2:
                if st.button("Baixar", key=f"ef_pg_{rp['id']}"):
                    efetivar_previsto(rp["id"])
                    st.rerun()
            with c3:
                st.markdown('<div class="btn-clear">', unsafe_allow_html=True)
                if st.button("Excluir", key=f"dl_pg_{rp['id']}"):
                    remover_previsto(rp["id"])
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.menu_nav == "Cartões & Parcelas":
    st.markdown('<div class="tech-panel">', unsafe_allow_html=True)
    st.markdown('<div class="panel-hdr"><span class="panel-hdr-title">◈ Controle de Compras Parceladas</span><span class="panel-hdr-sub">CRÉDITO ATIVO</span></div>', unsafe_allow_html=True)

    tot_m_p = float(df_parc["valor_parcela"].sum()) if not df_parc.empty else 0.0
    tot_r_p = sum((r["total_parcelas"] - r["parcela_atual"]) * r["valor_parcela"] for _, r in df_parc.iterrows()) if not df_parc.empty else 0.0
    st.markdown(f"""
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-bottom:10px;">
        <div class="bank-stat"><div class="bank-stat-lbl">Comprometido no Mês</div><div class="bank-stat-val" style="color:#38bdf8;">R$ {tot_m_p:,.2f}</div></div>
        <div class="bank-stat"><div class="bank-stat-lbl">Saldo Devedor Restante</div><div class="bank-stat-val" style="color:#fbbf24;">R$ {tot_r_p:,.2f}</div></div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("Ocultar Formulário" if st.session_state.mostrar_form_parc else "Cadastrar Nova Compra Parcelada", key="tog_fparc_pg"):
        st.session_state.mostrar_form_parc = not st.session_state.mostrar_form_parc
        st.rerun()

    if st.session_state.mostrar_form_parc:
        with st.form("form_add_parc_pro"):
            b_cards = df_bancos[df_bancos["tem_cartao"] == 1]["banco"].tolist() or df_bancos["banco"].tolist()
            cp1, cp2, cp3 = st.columns(3)
            with cp1:
                bp = st.selectbox("Cartão", b_cards)
                vp = st.number_input("Valor Parcela (R$)", min_value=0.01, value=150.0, step=10.0)
            with cp2:
                pa = st.number_input("Parcela Atual", min_value=1, max_value=60, value=1)
                pt = st.number_input("Total Parcelas", min_value=1, max_value=60, value=10)
            with cp3:
                dp = st.text_input("Descrição", value="Compra Parcelada")
                cp = st.selectbox("Categoria", ["Eletrônicos", "Casa", "Vestuário", "Veículo", "Saúde", "Outros"])
            if st.form_submit_button("Salvar Compra Parcelada"):
                adicionar_parcela(bp, dp, vp, pa, pt, cp)
                st.session_state.mostrar_form_parc = False
                st.rerun()

    cpl1, cpl2 = st.columns([4, 1.2])
    with cpl1: st.markdown(f'<div class="panel-hdr-title" style="margin-top:10px;">◈ Lista de Parcelas ({len(df_parc)})</div>', unsafe_allow_html=True)
    with cpl2:
        if st.button("Expandir" if st.session_state.recolher_parc_lista else "Recolher", key="rec_pl_pg"):
            st.session_state.recolher_parc_lista = not st.session_state.recolher_parc_lista
            st.rerun()

    if st.session_state.recolher_parc_lista:
        st.caption(f"Lista recolhida ({len(df_parc)} compra(s)). Clique em Expandir para visualizar.")
    else:
        for _, rpc in df_parc.iterrows():
            pct = min(100.0, (rpc["parcela_atual"] / max(1, rpc["total_parcelas"])) * 100)
            c1, c2, c3 = st.columns([4.2, 1.1, 0.7])
            with c1:
                st.markdown(f'<div class="ledger-row"><div><strong>{rpc["descricao"]} ({rpc["banco"]})</strong><br><span style="font-family:JetBrains Mono;font-size:0.62rem;color:#64748b;">{rpc["parcela_atual"]}/{rpc["total_parcelas"]} ({pct:.0f}%) · Fim {rpc["mes_ano_fim"]}</span></div><div style="font-family:JetBrains Mono;font-weight:700;color:#38bdf8;">R$ {rpc["valor_parcela"]:,.2f}</div></div>', unsafe_allow_html=True)
            with c2:
                if rpc["parcela_atual"] < rpc["total_parcelas"]:
                    if st.button(f"+1 ({rpc['parcela_atual']+1}/{rpc['total_parcelas']})", key=f"av_p_{rpc['id']}"):
                        avancar_parcela(rpc["id"])
                        st.rerun()
            with c3:
                st.markdown('<div class="btn-clear">', unsafe_allow_html=True)
                if st.button("Excluir", key=f"dl_pc_{rpc['id']}"):
                    remover_parcela(rpc["id"])
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.menu_nav == "Extrato & OFX":
    tab_ex1, tab_ex2, tab_ex3 = st.tabs(["Extrato & Filtros", "Lançamento Manual", "Importador OFX"])
    with tab_ex1:
        st.markdown('<div class="tech-panel">', unsafe_allow_html=True)
        cf1, cf2, cf3 = st.columns([1.5, 1.5, 2])
        with cf1: f_banco = st.selectbox("Filtrar Banco", ["Todos"] + df_bancos["banco"].tolist())
        with cf2: f_tipo = st.selectbox("Filtrar Tipo", ["Todos", "Saída", "Entrada"])
        with cf3: f_busca = st.text_input("Buscar descrição", placeholder="Ex: Uber, Mercado, Pix...")

        df_tx_f = df_tx.copy()
        if f_banco != "Todos" and not df_tx_f.empty: df_tx_f = df_tx_f[df_tx_f["banco"] == f_banco]
        if f_tipo != "Todos" and not df_tx_f.empty: df_tx_f = df_tx_f[df_tx_f["tipo"] == f_tipo]
        if f_busca.strip() and not df_tx_f.empty: df_tx_f = df_tx_f[df_tx_f["descricao"].str.contains(f_busca.strip(), case=False, na=False)]

        ce1, ce2, ce3 = st.columns([3.5, 1.2, 1.2])
        with ce1: st.markdown(f'<div class="panel-hdr-title">◈ Movimentações ({len(df_tx_f)})</div>', unsafe_allow_html=True)
        with ce2:
            if st.button("Expandir" if st.session_state.recolher_extrato_lista else "Recolher", key="rec_ext_pg"):
                st.session_state.recolher_extrato_lista = not st.session_state.recolher_extrato_lista
                st.rerun()
        with ce3:
            st.markdown('<div class="btn-clear">', unsafe_allow_html=True)
            if st.button("Limpar Tudo", key="limp_ext_pg"):
                limpar_extrato_completo()
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

        if st.session_state.recolher_extrato_lista:
            st.caption(f"Extrato recolhido ({len(df_tx_f)} registros). Clique em Expandir para visualizar.")
        else:
            for _, row in df_tx_f.iterrows():
                is_s = row["tipo"] == "Saída"
                ci, cd = st.columns([5.2, 0.8])
                with ci:
                    st.markdown(f'<div class="ledger-row"><div><strong>{row["descricao"]}</strong><br><span style="font-family:JetBrains Mono;font-size:0.62rem;color:#64748b;">{row["data"]} · {row["banco"]} ({row["meio"]}) · {row["categoria"]}</span></div><div style="font-family:JetBrains Mono;font-weight:700;color:{"#fb7185" if is_s else "#34d399"};">{"-" if is_s else "+"} R$ {row["valor"]:,.2f}</div></div>', unsafe_allow_html=True)
                with cd:
                    st.markdown('<div class="btn-clear">', unsafe_allow_html=True)
                    if st.button("Excluir", key=f"dl_tx_pro_{row['id']}"):
                        remover_transacao_extrato(int(row["id"]))
                        st.rerun()
                    st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with tab_ex2:
        st.markdown('<div class="tech-panel">', unsafe_allow_html=True)
        with st.form("form_manual_pro"):
            cm1, cm2 = st.columns(2)
            with cm1:
                desc_m = st.text_input("Descrição", value="Compra / Pagamento")
                val_m = st.number_input("Valor (R$)", min_value=0.01, value=25.00, step=1.0)
                banco_m = st.selectbox("Banco", df_bancos["banco"].tolist())
            with cm2:
                meio_m = st.selectbox("Método", ["Cartão de Crédito", "Conta Corrente / Pix"])
                cat_m = st.selectbox("Categoria", ["Alimentação", "Transporte", "Lazer", "Contas Fixas", "Saúde", "Outros"])
                tipo_m = st.selectbox("Tipo", ["Saída", "Entrada"])
            if st.form_submit_button("Registrar Transação"):
                adicionar_transacao(datetime.now().strftime("%d/%m %H:%M"), desc_m, val_m, cat_m, banco_m, meio_m, tipo_m)
                st.success("Registrado!")
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    with tab_ex3:
        st.markdown('<div class="tech-panel">', unsafe_allow_html=True)
        tipo_ofx = st.selectbox("Tipo de Arquivo OFX", ["Fatura de Cartão de Crédito", "Extrato de Conta Corrente"])
        b_ofx_list = df_bancos[df_bancos["tem_cartao"] == 1]["banco"].tolist() if "Cartão" in tipo_ofx else df_bancos["banco"].tolist()
        banco_alvo = st.selectbox("Banco", b_ofx_list or df_bancos["banco"].tolist())
        up_ofx = st.file_uploader("Upload arquivo .OFX", type=["ofx"])
        if up_ofx is not None:
            raw_b = up_ofx.read()
            try: txt_ofx = raw_b.decode("utf-8")
            except: txt_ofx = raw_b.decode("latin-1", errors="replace")
            trns_ofx, sal_led = parse_ofx_content(txt_ofx)
            if trns_ofx:
                tot_deb = sum(abs(t["valor"]) for t in trns_ofx if t["valor"] < 0)
                tot_cred = sum(t["valor"] for t in trns_ofx if t["valor"] > 0)
                st.info(f"{len(trns_ofx)} movimentações encontradas · Débitos: R$ {tot_deb:,.2f} · Créditos: R$ {tot_cred:,.2f}")
                if st.button("Processar OFX", type="primary"):
                    conn = sqlite3.connect("financas.db")
                    c = conn.cursor()
                    if "Cartão" in tipo_ofx:
                        v_fat = abs(sal_led) if (sal_led is not None and sal_led != 0) else tot_deb
                        c.execute("SELECT limite_cartao FROM contas_bancarias WHERE banco = ?", (banco_alvo,))
                        r_b = c.fetchone()
                        lim_t = r_b[0] if r_b else 0.0
                        c.execute("UPDATE contas_bancarias SET fatura_atual = ?, limite_liberado = ? WHERE banco = ?", (v_fat, max(0.0, lim_t - v_fat), banco_alvo))
                        for tr in trns_ofx:
                            fid = tr.get("fitid", "")
                            c.execute("SELECT COUNT(*) FROM transacoes WHERE fitid = ? AND banco = ? AND meio = 'Cartão de Crédito'", (fid, banco_alvo))
                            if c.fetchone()[0] == 0:
                                c.execute("INSERT INTO transacoes (data, descricao, valor, categoria, banco, meio, tipo, fitid) VALUES (?, ?, ?, 'OFX / Cartão', ?, 'Cartão de Crédito', ?, ?)", (tr["data"], tr["descricao"], abs(tr["valor"]), banco_alvo, "Saída" if tr["valor"] < 0 else "Entrada", fid))
                    else:
                        v_sal = sal_led if sal_led is not None else (tot_cred - tot_deb)
                        c.execute("UPDATE contas_bancarias SET saldo_conta = ? WHERE banco = ?", (v_sal, banco_alvo))
                        for tr in trns_ofx:
                            fid = tr.get("fitid", "")
                            c.execute("SELECT COUNT(*) FROM transacoes WHERE fitid = ? AND banco = ? AND meio = 'Conta Corrente / Pix'", (fid, banco_alvo))
                            if c.fetchone()[0] == 0:
                                c.execute("INSERT INTO transacoes (data, descricao, valor, categoria, banco, meio, tipo, fitid) VALUES (?, ?, ?, 'OFX / Conta', ?, 'Conta Corrente / Pix', ?, ?)", (tr["data"], tr["descricao"], abs(tr["valor"]), banco_alvo, "Saída" if tr["valor"] < 0 else "Entrada", fid))
                    conn.commit()
                    conn.close()
                    st.success("OFX importado com sucesso!")
                    st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.menu_nav == "Diagnóstico & PDF":
    render_advisor_box()
    st.markdown('<div class="tech-panel">', unsafe_allow_html=True)
    st.markdown('<div class="panel-hdr"><span class="panel-hdr-title">◈ Exportação Executiva</span><span class="panel-hdr-sub">PDF & WHATSAPP</span></div>', unsafe_allow_html=True)
    tot_parc_m = float(df_parc["valor_parcela"].sum()) if not df_parc.empty else 0.0
    tot_rest_p = sum((r["total_parcelas"] - r["parcela_atual"]) * r["valor_parcela"] for _, r in df_parc.iterrows()) if not df_parc.empty else 0.0
    diags_pdf = [{"titulo": "Balanco Consolidado do Ciclo", "desc": f"Saldo em conta R$ {total_saldos:,.2f} | Renda futura livre R$ {renda_futura_livre:,.2f} | Faturas R$ {total_faturas:,.2f}"}]
    pdf_b = gerar_relatorio_pdf(df_bancos, entradas_futuras_brutas, saidas_comprometidas_ciclo, projecao_com_futuro, tot_parc_m, tot_rest_p, diags_pdf)
    txt_wpp = f"*RELATORIO FINANCAS.OS ({dt_hero_ini.strftime('%d/%m')} a {dt_hero_fim.strftime('%d/%m')})*\n• Saldo em Conta: R$ {total_saldos:,.2f}\n• Renda Futura Livre: R$ {renda_futura_livre:,.2f}\n• Faturas: R$ {total_faturas:,.2f}\n• Cheque Especial: R$ {total_cheque:,.2f}"
    c_e1, c_e2 = st.columns(2)
    with c_e1:
        st.download_button("Baixar Relatório PDF", data=pdf_b, file_name=f"relatorio_{dt_hero_ini.strftime('%Y_%m_%d')}.pdf", mime="application/pdf")
    with c_e2:
        st.markdown(f'<a href="https://api.whatsapp.com/send?text={urllib.parse.quote(txt_wpp)}" target="_blank"><button style="width:100%;height:38px;background:#10b981;color:#060911;border:none;border-radius:8px;font-weight:700;font-size:0.76rem;cursor:pointer;">Enviar Resumo WhatsApp</button></a>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.menu_nav == "Configurações":
    st.markdown('<div class="tech-panel">', unsafe_allow_html=True)
    st.markdown('<div class="panel-hdr"><span class="panel-hdr-title">◈ Configuração de Instituições & Limites</span><span class="panel-hdr-sub">DATABASE</span></div>', unsafe_allow_html=True)

    st.markdown('<div class="btn-clear" style="margin-bottom:10px;">', unsafe_allow_html=True)
    if st.button("Zerar Todos os Saldos e Faturas"):
        zerar_saldos_e_faturas()
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    banco_edit = st.selectbox("Instituição", df_bancos["banco"].tolist())
    row_b = df_bancos[df_bancos["banco"] == banco_edit].iloc[0]
    with st.form("form_cfg_pro"):
        possui_c = st.checkbox("Possui Cartão de Crédito ativo", value=bool(row_b.get("tem_cartao", 1)))
        c1, c2, c3 = st.columns(3)
        with c1: n_sal = st.number_input("Saldo Conta (R$)", value=float(row_b["saldo_conta"]), step=10.0)
        with c2: l_chq = st.number_input("Limite Cheque Esp.", value=float(row_b["limite_cheque_especial"]), step=100.0)
        with c3: u_chq = st.number_input("Cheque Usado (R$)", value=float(row_b["cheque_especial_usado"]), step=10.0)
        if possui_c:
            cc1, cc2, cc3, cc4 = st.columns(4)
            with cc1: n_lim = st.number_input("Limite Total", value=float(row_b["limite_cartao"]), step=100.0)
            with cc2: n_fat = st.number_input("Fatura Atual", value=float(row_b["fatura_atual"]), step=10.0)
            with cc3: n_lib = st.number_input("Limite Liberado", value=float(row_b.get("limite_liberado", 0.0)), step=100.0)
            with cc4: d_ven = st.number_input("Dia Vencimento", 1, 31, int(row_b.get("dia_vencimento", 10)))
            d_fec = st.number_input("Dia Fechamento", 1, 31, int(row_b.get("dia_fechamento", 3)))
        else:
            n_lim, n_fat, n_lib, d_ven, d_fec = 0.0, 0.0, 0.0, 10, 3
        if st.form_submit_button("Salvar Configurações"):
            atualizar_banco_completo(banco_edit, 1 if possui_c else 0, n_fat, n_lim, n_lib, n_sal, l_chq, u_chq, d_ven, d_fec)
            st.success("Configurações atualizadas!")
            st.rerun()

    st.markdown('<div class="panel-hdr" style="margin-top:16px;"><span class="panel-hdr-title">◈ Backup & Restauração (.db)</span></div>', unsafe_allow_html=True)
    cb1, cb2 = st.columns(2)
    with cb1:
        if os.path.exists("financas.db"):
            with open("financas.db", "rb") as f_db:
                st.download_button("Exportar Database (.db)", data=f_db.read(), file_name=f"backup_financas_{datetime.now().strftime('%Y_%m_%d')}.db", mime="application/octet-stream")
    with cb2:
        up_db = st.file_uploader("Restaurar .db", type=["db"], label_visibility="collapsed")
        if up_db is not None and st.button("Confirmar Restauração"):
            with open("financas.db", "wb") as f_out:
                f_out.write(up_db.read())
            st.success("Restaurado!")
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
