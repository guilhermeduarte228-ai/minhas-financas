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

st.set_page_config(page_title="Minhas Finanças • OLED Pro", page_icon="💳", layout="centered")

# ================= ESTILO OLED MOBILE-FIRST PRO / REVOLUT METAL =================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500;600;700;800&display=swap');

    html, body, .stApp {
        background-color: #000000 !important;
        color: #ffffff !important;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    .block-container {
        max-width: 450px !important;
        padding-top: 0.85rem !important;
        padding-bottom: 5.5rem !important;
        padding-left: 0.85rem !important;
        padding-right: 0.85rem !important;
        background:
            radial-gradient(circle at 0% 18%, rgba(139, 92, 246, 0.14) 0%, transparent 45%),
            radial-gradient(circle at 100% 18%, rgba(34, 211, 238, 0.12) 0%, transparent 45%),
            #000000;
    }

    #MainMenu, footer, header { visibility: hidden; }

    /* Cartão Metálico Revolut Metal / Nubank Pro */
    .metal-card-stage {
        position: relative;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-bottom: 8px;
    }
    .metal-card {
        width: 100%;
        height: 172px;
        border-radius: 20px;
        padding: 18px 20px;
        position: relative;
        overflow: hidden;
        background: linear-gradient(135deg, #27272a 0%, #3f3f46 38%, #18181b 72%, #27272a 100%);
        border: 1px solid rgba(255, 255, 255, 0.18);
        box-shadow:
            0 16px 36px rgba(0, 0, 0, 0.85),
            inset 0 1px 0 rgba(255, 255, 255, 0.28),
            -12px 0 30px rgba(139, 92, 246, 0.22),
            12px 0 30px rgba(34, 211, 238, 0.18);
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }
    .metal-card::before {
        content: "";
        position: absolute;
        top: -40%;
        left: -20%;
        width: 140%;
        height: 140%;
        background: linear-gradient(115deg, transparent 30%, rgba(255,255,255,0.09) 48%, transparent 62%);
        pointer-events: none;
    }
    .metal-card-top {
        display: flex;
        justify-content: space-between;
        align-items: center;
        z-index: 1;
    }
    .metal-tier {
        font-size: 0.85rem;
        font-weight: 600;
        color: #f4f4f5;
        letter-spacing: -0.01em;
    }
    .metal-logo-r {
        font-size: 1.05rem;
        font-weight: 800;
        color: rgba(255, 255, 255, 0.85);
        font-family: 'Inter', sans-serif;
    }
    .metal-chip {
        width: 34px;
        height: 25px;
        border-radius: 6px;
        background: linear-gradient(135deg, #e4e4e7 0%, #a1a1aa 50%, #d4d4d8 100%);
        border: 1px solid rgba(0, 0, 0, 0.35);
        position: relative;
        z-index: 1;
        margin-top: 2px;
    }
    .metal-chip::after {
        content: "";
        position: absolute;
        inset: 4px;
        border: 1px solid rgba(0, 0, 0, 0.25);
        border-radius: 3px;
    }
    .metal-card-bottom {
        display: flex;
        justify-content: space-between;
        align-items: flex-end;
        z-index: 1;
    }
    .metal-bank-name {
        font-size: 0.88rem;
        font-weight: 600;
        color: #e4e4e7;
    }
    .metal-card-meta {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.66rem;
        color: #a1a1aa;
        margin-top: 2px;
    }
    .metal-circles {
        display: flex;
        align-items: center;
    }
    .mc-c1 {
        width: 22px;
        height: 22px;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.35);
    }
    .mc-c2 {
        width: 22px;
        height: 22px;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.65);
        margin-left: -8px;
    }
    .card-dots {
        display: flex;
        justify-content: center;
        gap: 6px;
        margin: 6px 0 12px 0;
    }
    .c-dot {
        width: 5px;
        height: 5px;
        border-radius: 50%;
        background: #3f3f46;
    }
    .c-dot.active {
        width: 14px;
        border-radius: 99px;
        background: #a855f7;
    }

    /* Main Balance Section */
    .main-bal-lbl {
        font-size: 0.78rem;
        font-weight: 500;
        color: #a1a1aa;
        margin-bottom: 2px;
    }
    .main-bal-row {
        display: flex;
        align-items: center;
        gap: 10px;
        flex-wrap: wrap;
        margin-bottom: 4px;
    }
    .main-bal-val {
        font-family: 'Inter', sans-serif;
        font-size: 2.05rem;
        font-weight: 800;
        color: #ffffff;
        letter-spacing: -0.03em;
        line-height: 1.1;
    }
    .pct-pill {
        background: rgba(16, 185, 129, 0.16);
        border: 1px solid rgba(16, 185, 129, 0.32);
        color: #34d399;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.68rem;
        font-weight: 700;
        padding: 3px 8px;
        border-radius: 999px;
    }
    .pct-pill.neg {
        background: rgba(244, 63, 94, 0.16);
        border-color: rgba(244, 63, 94, 0.32);
        color: #fb7185;
    }
    .sub-bal-row {
        font-size: 0.70rem;
        color: #71717a;
        margin-bottom: 12px;
    }

    /* Quick Actions Pills */
    .qa-title {
        font-size: 0.76rem;
        font-weight: 600;
        color: #a1a1aa;
        margin-bottom: 8px;
    }

    /* Bento Cards OLED (Allocation & Earnings) */
    .oled-bento-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 10px;
        margin: 10px 0 12px 0;
    }
    .oled-card {
        background: #0a0a0c;
        border-radius: 18px;
        padding: 13px 14px;
        position: relative;
        overflow: hidden;
    }
    .oled-card.purple-glow {
        border: 1px solid rgba(168, 85, 247, 0.45);
        box-shadow: inset 0 0 24px rgba(168, 85, 247, 0.08);
    }
    .oled-card.cyan-glow {
        border: 1px solid rgba(34, 211, 238, 0.38);
        box-shadow: inset 0 0 24px rgba(34, 211, 238, 0.06);
    }
    .oled-card-hdr {
        display: flex;
        justify-content: space-between;
        align-items: center;
        font-size: 0.80rem;
        font-weight: 600;
        color: #f4f4f5;
        margin-bottom: 6px;
    }
    .oled-card-val {
        font-size: 1.15rem;
        font-weight: 700;
        color: #ffffff;
        margin: 6px 0 10px 0;
        letter-spacing: -0.02em;
    }
    .oled-prog-txt {
        font-size: 0.64rem;
        color: #71717a;
    }
    .oled-prog-txt span.p-purple { color: #c084fc; font-weight: 700; }
    .oled-prog-txt span.p-cyan { color: #38bdf8; font-weight: 700; }

    /* Allocation Calendar Box */
    .alloc-cal-box {
        background: #09090b;
        border: 1px solid rgba(255, 255, 255, 0.10);
        border-radius: 18px;
        padding: 14px;
        margin-bottom: 12px;
    }

    /* Bottom Dual Gradient Cards (Goals & Investment style) */
    .dual-grad-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 10px;
        margin-top: 10px;
        margin-bottom: 12px;
    }
    .grad-card-purple {
        background: linear-gradient(135deg, #4c1d95 0%, #7c3aed 100%);
        border: 1px solid rgba(192, 132, 252, 0.4);
        border-radius: 18px;
        padding: 14px;
        color: #ffffff;
    }
    .grad-card-cyan {
        background: linear-gradient(135deg, #0e7490 0%, #0284c7 100%);
        border: 1px solid rgba(56, 189, 248, 0.4);
        border-radius: 18px;
        padding: 14px;
        color: #ffffff;
    }
    .grad-card-title {
        display: flex;
        justify-content: space-between;
        align-items: center;
        font-size: 0.86rem;
        font-weight: 700;
        margin-bottom: 6px;
    }
    .grad-card-sub {
        font-size: 0.68rem;
        color: rgba(255, 255, 255, 0.82);
        line-height: 1.35;
    }

    /* Botões Streamlit no estilo OLED Dark Pill */
    .stButton > button {
        background: #141418 !important;
        color: #f4f4f5 !important;
        border: 1px solid rgba(255, 255, 255, 0.12) !important;
        border-radius: 999px !important;
        font-size: 0.72rem !important;
        font-weight: 600 !important;
        padding: 0.40rem 0.65rem !important;
        transition: all 0.18s ease !important;
    }
    .stButton > button:hover {
        border-color: #a855f7 !important;
        background: #1e1b29 !important;
        color: #ffffff !important;
    }
    /* Botão Primário (Dias selecionados no Calendário = Pontos Roxos/Ciano iluminados!) */
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #7c3aed 0%, #2563eb 100%) !important;
        border: 1px solid #c084fc !important;
        color: #ffffff !important;
        box-shadow: 0 0 10px rgba(139, 92, 246, 0.5) !important;
    }
    .btn-clear button {
        background: rgba(244, 63, 94, 0.12) !important;
        color: #fb7185 !important;
        border: 1px solid rgba(244, 63, 94, 0.35) !important;
    }
    .btn-action-icon button {
        background: rgba(168, 85, 247, 0.14) !important;
        color: #c084fc !important;
        border: 1px solid rgba(168, 85, 247, 0.35) !important;
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
        padding: 2px 0 !important;
        min-height: 32px !important;
        height: 32px !important;
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 0.66rem !important;
        font-weight: 700 !important;
        border-radius: 8px !important;
        line-height: 1 !important;
    }

    /* Quick Actions 4 colunas fixas mesmo no celular */
    .qa-row [data-testid="stHorizontalBlock"] {
        display: grid !important;
        grid-template-columns: repeat(4, minmax(0, 1fr)) !important;
        gap: 6px !important;
    }
    .qa-row [data-testid="stColumn"],
    .qa-row [data-testid="column"] {
        width: 100% !important;
        min-width: 0 !important;
        padding: 0 !important;
    }
    .qa-row button {
        width: 100% !important;
        padding: 6px 2px !important;
        font-size: 0.68rem !important;
        white-space: nowrap !important;
    }

    /* Bottom Navigation Bar (5 colunas fixas estilo App Nativo) */
    .bottom-nav-wrap [data-testid="stHorizontalBlock"] {
        display: grid !important;
        grid-template-columns: repeat(5, minmax(0, 1fr)) !important;
        gap: 4px !important;
        background: #0d0d11;
        border: 1px solid rgba(255, 255, 255, 0.12);
        border-radius: 18px;
        padding: 6px;
        margin-top: 14px;
    }
    .bottom-nav-wrap [data-testid="stColumn"],
    .bottom-nav-wrap [data-testid="column"] {
        width: 100% !important;
        min-width: 0 !important;
        padding: 0 !important;
    }
    .bottom-nav-wrap button {
        width: 100% !important;
        border-radius: 12px !important;
        padding: 6px 2px !important;
        font-size: 0.64rem !important;
        background: transparent !important;
        border: none !important;
        color: #71717a !important;
    }
    .bottom-nav-wrap button[kind="primary"] {
        background: rgba(56, 189, 248, 0.14) !important;
        color: #38bdf8 !important;
        border: 1px solid rgba(56, 189, 248, 0.35) !important;
        box-shadow: none !important;
    }

    /* Cards internos e listas */
    .oled-list-item {
        background: #0b0b0e;
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 14px;
        padding: 10px 12px;
        margin-bottom: 6px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .parcela-progresso {
        background: #18181b;
        height: 5px;
        border-radius: 99px;
        overflow: hidden;
        margin: 6px 0;
    }
    .parcela-progresso-bar {
        background: linear-gradient(90deg, #8b5cf6 0%, #38bdf8 100%);
        height: 100%;
    }
    .cal-table {
        width: 100%;
        border-collapse: separate;
        border-spacing: 3px;
        margin-top: 6px;
    }
    .cal-th {
        text-align: center;
        font-size: 0.62rem;
        font-weight: 600;
        color: #71717a;
        padding: 3px 0;
    }
    .cal-cell {
        background: #0c0c10;
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 8px;
        height: 44px;
        vertical-align: top;
        padding: 3px;
        text-align: right;
        font-size: 0.62rem;
        font-weight: 600;
    }
    .cal-cell.payday { border-color: #eab308 !important; }
    .cal-cell.today { border-color: #38bdf8 !important; }
    .cal-cell.has-entrada { background: rgba(16, 185, 129, 0.16) !important; border-color: rgba(16, 185, 129, 0.55) !important; }
    .cal-cell.has-saida { background: rgba(244, 63, 94, 0.16) !important; border-color: rgba(244, 63, 94, 0.55) !important; }
    .cal-cell.has-reemb-livre { background: rgba(234, 179, 8, 0.16) !important; border-color: rgba(234, 179, 8, 0.65) !important; }
    .cal-cell.has-ambos { background: rgba(168, 85, 247, 0.16) !important; border-color: rgba(168, 85, 247, 0.55) !important; }
    .cal-badge {
        font-size: 0.52rem;
        font-weight: 700;
        font-family: 'JetBrains Mono', monospace;
        display: block;
        text-align: left;
        margin-top: 1px;
        line-height: 1.05;
    }
    .badge-in { color: #34d399; }
    .badge-out { color: #fb7185; }
    .badge-reemb-livre { color: #fbbf24; }
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

# Valores padrão garantidos para parâmetros de alocação
if st.session_state.get("inp_diaria_aloc", 0.0) == 0.0:
    st.session_state.inp_diaria_aloc = 128.78
if st.session_state.get("inp_gas_aloc", 0.0) == 0.0:
    st.session_state.inp_gas_aloc = 30.00
if st.session_state.get("inp_ped_aloc", 0.0) == 0.0:
    st.session_state.inp_ped_aloc = 25.60

if "aloc_cal_mes" not in st.session_state:
    st.session_state.aloc_cal_mes = st.session_state.cal_mes
if "aloc_cal_ano" not in st.session_state:
    st.session_state.aloc_cal_ano = st.session_state.cal_ano

if "oled_tab" not in st.session_state:
    st.session_state.oled_tab = "Home"

if "card_idx" not in st.session_state:
    st.session_state.card_idx = 0

if "qa_subpanel" not in st.session_state:
    st.session_state.qa_subpanel = None

# ================= CÁLCULOS PRINCIPAIS DO CICLO E ALOCAÇÕES =================
dt_hero_ini, dt_hero_fim, dt_salario_03 = get_intervalo_ciclo(st.session_state.cal_ano, st.session_state.cal_mes, "Ciclo Completo (04 a 03)")
meses_nomes = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]
nome_mes_comp = meses_nomes[st.session_state.cal_mes - 1]

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

# Progresso do ciclo (04 a 03)
total_dias_ciclo = max(1, (dt_hero_fim - dt_hero_ini).days)
dias_passados_ciclo = min(total_dias_ciclo, max(0, (hoje - dt_hero_ini).days))
pct_ciclo = (dias_passados_ciclo / total_dias_ciclo) * 100.0

# Dados das Alocações do mês ativo no Calendário de Alocações
dt_m_ini = date(st.session_state.aloc_cal_ano, st.session_state.aloc_cal_mes, 1)
last_day_m = calendar.monthrange(st.session_state.aloc_cal_ano, st.session_state.aloc_cal_mes)[1]
dt_m_fim = date(st.session_state.aloc_cal_ano, st.session_state.aloc_cal_mes, last_day_m)
df_aloc_mes = pd.DataFrame()
if not df_aloc.empty:
    df_aloc_mes = df_aloc[(df_aloc["data_alocacao"] >= dt_m_ini.strftime("%Y-%m-%d")) & (df_aloc["data_alocacao"] <= dt_m_fim.strftime("%Y-%m-%d"))]

qtd_dias_aloc = len(df_aloc_mes)
tot_diarias_bruto = float(df_aloc_mes["valor_diaria"].sum()) if qtd_dias_aloc > 0 else 0.0
tot_gas_mes = float(df_aloc_mes["valor_gasolina"].sum()) if qtd_dias_aloc > 0 else 0.0
tot_ped_mes = float(df_aloc_mes["valor_pedagio"].sum()) if qtd_dias_aloc > 0 else 0.0
tot_lucro_liq_aloc = tot_diarias_bruto - tot_gas_mes
tot_reembolso_esperado = tot_diarias_bruto + tot_ped_mes
pct_aloc_meta = min(100.0, (qtd_dias_aloc / 22.0) * 100.0)

# ================= TOPO: CARTÃO METÁLICO REVOLUT METAL / NUBANK PRO =================
bancos_records = df_bancos.to_dict("records")
if bancos_records:
    st.session_state.card_idx = st.session_state.card_idx % len(bancos_records)
    b_atual = bancos_records[st.session_state.card_idx]
    b_nome = b_atual["banco"]
    tem_c = (b_atual.get("tem_cartao", 1) == 1)
    lim_tot = float(b_atual.get("limite_cartao", 0.0))
    lim_lib = float(b_atual.get("limite_liberado", 0.0))
    lim_exib = lim_lib if lim_lib > 0 else max(0.0, lim_tot - float(b_atual["fatura_atual"]))
    tier_label = "Metal Credit Pro" if tem_c else "Metal Account"
    meta_card_txt = (
        f"Saldo R$ {b_atual['saldo_conta']:,.2f} · Fatura R$ {b_atual['fatura_atual']:,.2f} · Livre R$ {lim_exib:,.2f}"
        if tem_c else
        f"Saldo R$ {b_atual['saldo_conta']:,.2f} · Cheque Esp. R$ {b_atual['cheque_especial_usado']:,.2f}"
    )

    dots_html = "".join(
        f'<span class="c-dot {"active" if i == st.session_state.card_idx else ""}"></span>'
        for i in range(len(bancos_records))
    )

    st.markdown(f"""
    <div class="metal-card-stage">
        <div class="metal-card">
            <div class="metal-card-top">
                <span class="metal-tier">{tier_label}</span>
                <span class="metal-logo-r">R</span>
            </div>
            <div class="metal-chip"></div>
            <div class="metal-card-bottom">
                <div>
                    <div class="metal-bank-name">{b_nome}</div>
                    <div class="metal-card-meta">{meta_card_txt}</div>
                </div>
                <div class="metal-circles">
                    <span class="mc-c1"></span>
                    <span class="mc-c2"></span>
                </div>
            </div>
        </div>
    </div>
    <div class="card-dots">{dots_html}</div>
    """, unsafe_allow_html=True)

    # Troca discreta de cartão no carrossel
    c_sw1, c_sw2, c_sw3 = st.columns([1.2, 2.6, 1.2])
    with c_sw1:
        if st.button("◀ Ant.", key="prev_metal_card"):
            st.session_state.card_idx = (st.session_state.card_idx - 1) % len(bancos_records)
            st.rerun()
    with c_sw2:
        st.markdown(f'<div style="text-align:center;font-size:0.66rem;color:#71717a;padding-top:6px;">Cartão {st.session_state.card_idx + 1} de {len(bancos_records)} • {b_nome}</div>', unsafe_allow_html=True)
    with c_sw3:
        if st.button("Próx. ▶", key="next_metal_card"):
            st.session_state.card_idx = (st.session_state.card_idx + 1) % len(bancos_records)
            st.rerun()

# ================= MAIN BALANCE (SALDO PRINCIPAL + PÍLULA VERDE) =================
sinal_rf = "+" if renda_futura_livre >= 0 else "-"
pill_cls = "pct-pill" if renda_futura_livre >= 0 else "pct-pill neg"
seta_rf = "↗" if renda_futura_livre >= 0 else "↘"

st.markdown(f"""
<div style="margin-top: 6px;">
    <div class="main-bal-lbl">Main balance • Patrimônio em Conta</div>
    <div class="main-bal-row">
        <span class="main-bal-val">R$ {total_saldos:,.2f}</span>
        <span class="{pill_cls}">{seta_rf} {sinal_rf}R$ {abs(renda_futura_livre):,.2f} livre</span>
    </div>
    <div class="sub-bal-row">
        Noção c/ futuro: <strong style="color:#e4e4e7;">R$ {projecao_com_futuro:,.2f}</strong> · Faturas: <strong style="color:#fb7185;">R$ {total_faturas:,.2f}</strong> · Cheque Esp.: <strong style="color:#fbbf24;">R$ {total_cheque:,.2f}</strong>
    </div>
</div>
""", unsafe_allow_html=True)

# ================= QUICK ACTIONS (4 PÍLULAS HORIZONTAIS) =================
st.markdown('<div class="qa-title">Quick Actions</div>', unsafe_allow_html=True)
st.markdown('<div class="qa-row">', unsafe_allow_html=True)
qa1, qa2, qa3, qa4 = st.columns(4)
with qa1:
    if st.button("✈️ Ciclo", key="qa_ciclo", type="primary" if st.session_state.qa_subpanel == "ciclo" else "secondary"):
        st.session_state.qa_subpanel = None if st.session_state.qa_subpanel == "ciclo" else "ciclo"
        st.session_state.recolher_lanc_ciclo = True
        st.session_state.mostrar_form_prev = False
        st.rerun()
with qa2:
    if st.button("💳 Pagar", key="qa_pagar", type="primary" if st.session_state.qa_subpanel == "pagar" else "secondary"):
        st.session_state.qa_subpanel = None if st.session_state.qa_subpanel == "pagar" else "pagar"
        st.rerun()
with qa3:
    if st.button("⛽ Rateio", key="qa_rateio", type="primary" if st.session_state.qa_subpanel == "rateio" else "secondary"):
        st.session_state.qa_subpanel = None if st.session_state.qa_subpanel == "rateio" else "rateio"
        st.session_state.mostrar_form_rateio = False
        st.session_state.recolher_dest_reemb = True
        st.rerun()
with qa4:
    if st.button("💠 Lançar", key="qa_lancar", type="primary" if st.session_state.qa_subpanel == "lancar" else "secondary"):
        st.session_state.qa_subpanel = None if st.session_state.qa_subpanel == "lancar" else "lancar"
        st.rerun()
st.markdown('</div>', unsafe_allow_html=True)

# ================= PAINEL EXPANSÍVEL DAS QUICK ACTIONS =================
if st.session_state.qa_subpanel == "pagar":
    st.markdown('<div class="alloc-cal-box" style="margin-top:8px;">', unsafe_allow_html=True)
    st.markdown('<div style="font-size:0.82rem;font-weight:700;color:#38bdf8;margin-bottom:8px;">💳 Pagar Fatura de Cartão</div>', unsafe_allow_html=True)
    b_cartoes = df_bancos[df_bancos["tem_cartao"] == 1]["banco"].tolist()
    if not b_cartoes:
        st.info("Nenhum cartão ativo.")
    else:
        c_pf1, c_pf2 = st.columns(2)
        with c_pf1:
            sel_card_p = st.selectbox("Cartão", b_cartoes, key="qa_sel_card")
            fat_atual_sel = float(df_bancos[df_bancos["banco"] == sel_card_p].iloc[0]["fatura_atual"])
            val_pag_f = st.number_input("Valor (R$)", min_value=0.01, value=max(0.01, fat_atual_sel), step=10.0, key="qa_val_fat")
        with c_pf2:
            sel_src_p = st.selectbox("Debitar da Conta", df_bancos["banco"].tolist(), key="qa_sel_src")
            st.caption(f"Fatura atual: **R$ {fat_atual_sel:,.2f}**")
        if st.button("Confirmar Pagamento de Fatura", key="btn_qa_confirm_fat", type="primary"):
            pagar_fatura_cartao(sel_card_p, sel_src_p, val_pag_f)
            st.session_state.qa_subpanel = None
            st.success("Fatura abatida!")
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.qa_subpanel == "lancar":
    st.markdown('<div class="alloc-cal-box" style="margin-top:8px;">', unsafe_allow_html=True)
    modo_l = st.radio("Modo", ["Manual", "Importar .OFX"], horizontal=True, key="qa_modo_l")
    if modo_l == "Manual":
        with st.form("qa_form_manual"):
            c1, c2 = st.columns(2)
            with c1:
                desc = st.text_input("Descrição", value="Compra / Pix")
                val = st.number_input("Valor (R$)", value=25.00, min_value=0.01, step=1.0)
                banco = st.selectbox("Banco", df_bancos["banco"].tolist())
            with c2:
                meio = st.selectbox("Método", ["Cartão de Crédito", "Conta Corrente / Pix"])
                cat = st.selectbox("Categoria", ["Alimentação", "Transporte", "Lazer", "Contas Fixas", "Saúde", "Outros"])
                tipo = st.selectbox("Tipo", ["Saída", "Entrada"])
            if st.form_submit_button("Confirmar Lançamento"):
                adicionar_transacao(datetime.now().strftime("%d/%m %H:%M"), desc, val, cat, banco, meio, tipo)
                st.session_state.qa_subpanel = None
                st.success("Registrado!")
                st.rerun()
    else:
        tipo_ofx = st.selectbox("Tipo OFX", ["💳 Fatura de Cartão de Crédito", "🏦 Extrato de Conta Corrente"], key="qa_t_ofx")
        b_ofx = df_bancos[df_bancos["tem_cartao"] == 1]["banco"].tolist() if "Cartão" in tipo_ofx else df_bancos["banco"].tolist()
        banco_alvo = st.selectbox("Banco", b_ofx or df_bancos["banco"].tolist(), key="qa_b_ofx")
        arq_ofx = st.file_uploader("Arquivo .OFX", type=["ofx"], key="qa_up_ofx")
        if arq_ofx is not None:
            raw_b = arq_ofx.read()
            try: txt_ofx = raw_b.decode("utf-8")
            except: txt_ofx = raw_b.decode("latin-1", errors="replace")
            trns_ofx, sal_led = parse_ofx_content(txt_ofx)
            if trns_ofx:
                tot_deb = sum(abs(t["valor"]) for t in trns_ofx if t["valor"] < 0)
                tot_cred = sum(t["valor"] for t in trns_ofx if t["valor"] > 0)
                st.caption(f"{len(trns_ofx)} itens · Débitos: R$ {tot_deb:,.2f} · Créditos: R$ {tot_cred:,.2f}")
                if st.button("Processar OFX", key="qa_btn_ofx", type="primary"):
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
                    st.session_state.qa_subpanel = None
                    st.success("OFX importado!")
                    st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# ================= HELPER DO CALENDÁRIO DE ALOCAÇÕES + SIMULADOR =================
def render_allocation_calendar_widget():
    meses_aloc_nomes = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]
    nome_m_aloc = meses_aloc_nomes[st.session_state.aloc_cal_mes - 1]

    st.markdown('<div class="alloc-cal-box">', unsafe_allow_html=True)
    ca1, ca2, ca3 = st.columns([3.6, 1.2, 1.2])
    with ca1:
        st.markdown(f'<div style="font-size:0.84rem;font-weight:700;color:#ffffff;padding-top:4px;">Allocation Calendar • {nome_m_aloc}/{st.session_state.aloc_cal_ano}</div>', unsafe_allow_html=True)
    with ca2:
        if st.button("◀", key="aloc_m_ant"):
            if st.session_state.aloc_cal_mes == 1:
                st.session_state.aloc_cal_mes = 12
                st.session_state.aloc_cal_ano -= 1
            else:
                st.session_state.aloc_cal_mes -= 1
            st.rerun()
    with ca3:
        if st.button("▶", key="aloc_m_prox"):
            if st.session_state.aloc_cal_mes == 12:
                st.session_state.aloc_cal_mes = 1
                st.session_state.aloc_cal_ano += 1
            else:
                st.session_state.aloc_cal_mes += 1
            st.rerun()

    cp1, cp2, cp3 = st.columns(3)
    with cp1:
        val_diaria_aloc = st.number_input("Diária (R$)", min_value=0.0, value=float(st.session_state.inp_diaria_aloc), step=1.0, key="inp_diaria_aloc")
    with cp2:
        val_gas_aloc = st.number_input("Gasolina/dia", min_value=0.0, value=float(st.session_state.inp_gas_aloc), step=1.0, key="inp_gas_aloc")
    with cp3:
        val_ped_aloc = st.number_input("Pedágio/dia", min_value=0.0, value=float(st.session_state.inp_ped_aloc), step=1.0, key="inp_ped_aloc")

    datas_marcadas_set = set(df_aloc["data_alocacao"].tolist()) if not df_aloc.empty else set()
    cal_matrix = calendar.monthcalendar(st.session_state.aloc_cal_ano, st.session_state.aloc_cal_mes)
    dias_hdr = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    hdr_html = '<div style="display:grid;grid-template-columns:repeat(7,1fr);gap:4px;margin:6px 0 4px 0;">'
    for dh in dias_hdr:
        hdr_html += f'<div style="text-align:center;font-size:0.62rem;font-weight:600;color:#71717a;">{dh}</div>'
    hdr_html += '</div>'
    st.markdown(hdr_html, unsafe_allow_html=True)

    for sem_idx, semana in enumerate(cal_matrix):
        cols_w = st.columns(7)
        for d_idx, dia_num in enumerate(semana):
            if dia_num == 0:
                cols_w[d_idx].markdown("<div style='height:32px;background:rgba(255,255,255,0.02);border-radius:8px;'></div>", unsafe_allow_html=True)
            else:
                dt_cell = date(st.session_state.aloc_cal_ano, st.session_state.aloc_cal_mes, dia_num)
                dt_cell_str = dt_cell.strftime("%Y-%m-%d")
                is_marked = (dt_cell_str in datas_marcadas_set)
                lbl_btn = f"•{dia_num}" if is_marked else f"{dia_num}"
                if cols_w[d_idx].button(
                    lbl_btn,
                    key=f"cal_aloc_btn_{dt_cell_str}",
                    type="primary" if is_marked else "secondary",
                    help=f"{'Remover' if is_marked else 'Marcar'} {dt_cell.strftime('%d/%m/%Y')}"
                ):
                    toggle_alocacao_dia(dt_cell_str, "Alocação Cliente", val_diaria_aloc, val_gas_aloc, val_ped_aloc)
                    st.rerun()

    ca_act1, ca_act2 = st.columns(2)
    with ca_act1:
        if st.button("⚡ Dias Úteis (Seg–Sex)", key="btn_marcar_uteis_aloc"):
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
        if st.button("🗑️ Limpar Mês", key="btn_limpar_mes_aloc"):
            limpar_alocacoes_periodo(dt_m_ini.strftime("%Y-%m-%d"), dt_m_fim.strftime("%Y-%m-%d"))
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown(f"""
    <div style="background:#111115;border:1px solid rgba(255,255,255,0.08);border-radius:12px;padding:10px;margin-top:8px;">
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:6px;font-size:0.68rem;">
            <div><span style="color:#71717a;">⛽ Gasolina ({qtd_dias_aloc}d):</span> <strong style="color:#fb7185;">R$ {tot_gas_mes:,.2f}</strong></div>
            <div><span style="color:#71717a;">🛣️ Pedágios:</span> <strong style="color:#fbbf24;">R$ {tot_ped_mes:,.2f}</strong></div>
            <div><span style="color:#71717a;">💰 Lucro Livre:</span> <strong style="color:#34d399;">R$ {tot_lucro_liq_aloc:,.2f}</strong></div>
            <div><span style="color:#71717a;">📥 Reembolso:</span> <strong style="color:#38bdf8;">R$ {tot_reembolso_esperado:,.2f}</strong></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if qtd_dias_aloc > 0:
        if st.button(f"🎯 Jogar R$ {tot_reembolso_esperado:,.2f} no Rateio", key="btn_enviar_aloc_rateio"):
            st.session_state["reemb_total_val"] = round(tot_reembolso_esperado, 2)
            st.session_state["qtd_destinos"] = 3
            st.session_state["v_A"] = round(tot_ped_mes, 2)
            st.session_state["v_B"] = round(tot_gas_mes, 2)
            st.session_state["v_C"] = round(max(0.0, tot_reembolso_esperado - tot_ped_mes - tot_gas_mes), 2)
            st.session_state.mostrar_form_rateio = True
            st.session_state.qa_subpanel = "rateio"
            st.rerun()

    # Calculadora Rápida vinculada aos valores do Calendário
    ref_diaria_cal = float(st.session_state.get("inp_diaria_aloc", 128.78))
    ref_gas_cal = float(st.session_state.get("inp_gas_aloc", 30.00))
    ref_ped_cal = float(st.session_state.get("inp_ped_aloc", 25.60))
    dias_default_calc = qtd_dias_aloc if qtd_dias_aloc > 0 else 5

    btn_calc_lbl = (
        "➖ Ocultar Calculadora Rápida"
        if st.session_state.mostrar_calc_km
        else f"🧮 Calculadora Rápida (R$ {ref_diaria_cal:,.2f} + R$ {ref_ped_cal:,.2f})"
    )
    if st.button(btn_calc_lbl, key="toggle_calc_km"):
        st.session_state.mostrar_calc_km = not st.session_state.mostrar_calc_km
        st.rerun()

    if st.session_state.mostrar_calc_km:
        st.markdown('<div style="background:#111115;border:1px solid rgba(255,255,255,0.08);border-radius:12px;padding:10px;margin-top:6px;">', unsafe_allow_html=True)
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
            st.caption(f"⛽ Gasolina: **R$ {gasolina_est:,.2f}**")
            st.caption(f"💰 Lucro Livre: **R$ {diarias_lucro:,.2f}**")
            st.caption(f"🛣️ Pedágios: **R$ {pedagio_total_est:,.2f}**")
            st.markdown(f"**Total:** <span style='color:#34d399;font-weight:800;'>R$ {total_est:,.2f}</span>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ================= HELPER DO RATEIO DE REEMBOLSO =================
def render_rateio_reembolso_box():
    st.markdown('<div class="alloc-cal-box" style="margin-top:8px;">', unsafe_allow_html=True)
    st.markdown('<div style="font-size:0.84rem;font-weight:700;color:#c084fc;margin-bottom:8px;">⛽ Destinar Reembolso KM</div>', unsafe_allow_html=True)

    btn_r_lbl = "➖ Ocultar Formulário de Rateio" if st.session_state.mostrar_form_rateio else "🎯 Lançar / Destinar Reembolso (Rateio)"
    if st.button(btn_r_lbl, key="toggle_form_rateio"):
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

        c1, c2 = st.columns(2)
        with c1: data_receb = st.date_input("Data Recebimento", value=date.today(), key="reemb_data_input")
        with c2: val_tot_r = st.number_input("Valor Total (R$)", min_value=0.01, step=10.0, key="reemb_total_val", on_change=recalc_dest)

        qtd_esc = st.selectbox("Quantos destinos ratear?", [1, 2, 3, 4, 5], index=[1, 2, 3, 4, 5].index(st.session_state.qtd_destinos), key="sel_qtd_destinos_widget")
        if qtd_esc != st.session_state.qtd_destinos:
            st.session_state.qtd_destinos = qtd_esc
            recalc_dest()
            st.rerun()

        dests = []
        b_list = df_bancos["banco"].tolist()
        lets = ["A", "B", "C", "D", "E"]
        mots = ["Pedágio no Cartão de Crédito", "Gasolina no Cheque Especial", "Renda livre / Lucro das diárias", "Outro gasto / Ajuste", "Reserva / Poupança"]
        for i in range(st.session_state.qtd_destinos):
            lt = lets[i]
            is_ult = (i == st.session_state.qtd_destinos - 1)
            cd1, cd2 = st.columns(2)
            with cd1: bd = st.selectbox(f"Banco ({lt})", b_list, index=min(i, len(b_list)-1), key=f"b_{lt}")
            with cd2: vd = st.number_input(f"Valor ({lt})", min_value=0.0, step=10.0, key=f"v_{lt}", on_change=(recalc_dest if not is_ult else None))
            ad = st.selectbox(f"Ação ({lt})", ["Pagar/Abater Fatura de Cartão", "Abater Cheque Especial", "Creditar em Conta Corrente"], index=min(i, 2), key=f"ac_{lt}")
            md = st.text_input(f"Motivo ({lt})", value=mots[i], key=f"m_{lt}")
            dests.append({"banco": bd, "acao": ad, "valor": vd, "motivo": md})

        if st.button("🚀 Executar Rateio", key="btn_executar_rateio_dinamico", type="primary"):
            ativos = [d for d in dests if d["valor"] > 0]
            if ativos:
                aplicar_destinacao_reembolso(data_receb.strftime("%Y-%m-%d"), val_tot_r, ativos, efetivar_agora=(data_receb <= date.today()))
                st.session_state.mostrar_form_rateio = False
                st.success("Rateio executado!")
                st.rerun()

    df_itens_hist = get_reembolsos_itens()
    if not df_itens_hist.empty:
        cda1, cda2 = st.columns([3.5, 1.5])
        with cda1: st.markdown(f'<div style="font-size:0.74rem;font-weight:700;color:#a1a1aa;margin-top:8px;">Destinações Ativas ({len(df_itens_hist)})</div>', unsafe_allow_html=True)
        with cda2:
            if st.button("👁️ Mostrar" if st.session_state.recolher_dest_reemb else "🔼 Recolher", key="btn_toggle_rec_da"):
                st.session_state.recolher_dest_reemb = not st.session_state.recolher_dest_reemb
                st.rerun()
        if st.session_state.recolher_dest_reemb:
            st.caption(f"Lista recolhida ({len(df_itens_hist)} itens).")
        else:
            for _, item in df_itens_hist.iterrows():
                st_it = item.get("status", "Efetivado")
                cor_it = "#fbbf24" if st_it == "Previsto" else "#34d399"
                ci, cb = st.columns([4.2, 1.3])
                with ci:
                    st.markdown(f'<div class="oled-list-item"><div><strong style="font-size:0.76rem;">{item["banco"]}</strong> · <span style="font-size:0.72rem;color:#a1a1aa;">{item["motivo"]}</span><br><span style="font-size:0.62rem;color:#71717a;">{item["data"]} · {item["acao"]}</span></div><div style="font-family:JetBrains Mono;font-weight:700;color:{cor_it};font-size:0.80rem;">R$ {item["valor"]:,.2f}</div></div>', unsafe_allow_html=True)
                with cb:
                    st.markdown('<div class="btn-clear">', unsafe_allow_html=True)
                    if st.button("↩️", key=f"btn_est_{item['id']}", help="Estornar"):
                        estornar_item_destino(item["id"])
                        st.rerun()
                    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ================= HELPER DO CICLO & PREVISÕES =================
def render_ciclo_previsoes_box():
    st.markdown('<div class="alloc-cal-box" style="margin-top:8px;">', unsafe_allow_html=True)
    c_n1, c_n2, c_n3 = st.columns([3.6, 1.2, 1.2])
    with c_n1:
        st.markdown(f'<div style="font-size:0.84rem;font-weight:700;color:#38bdf8;padding-top:4px;">📅 Ciclo {nome_mes_comp}/{st.session_state.cal_ano}</div>', unsafe_allow_html=True)
    with c_n2:
        if st.button("◀", key="m_ant"):
            st.session_state.cal_mes = 12 if st.session_state.cal_mes == 1 else st.session_state.cal_mes - 1
            if st.session_state.cal_mes == 12: st.session_state.cal_ano -= 1
            st.rerun()
    with c_n3:
        if st.button("▶", key="m_prox"):
            st.session_state.cal_mes = 1 if st.session_state.cal_mes == 12 else st.session_state.cal_mes + 1
            if st.session_state.cal_mes == 1: st.session_state.cal_ano += 1
            st.rerun()

    opcoes_ciclo = ["Ciclo Completo (04 a 03)", "1ª Parte (Dia 04 a 15)", "2ª Parte (Dia 16 a 03)"]
    modo_sel = st.selectbox("Período", opcoes_ciclo, index=opcoes_ciclo.index(st.session_state.modo_ciclo), key="sel_modo_ciclo_prev")
    if modo_sel != st.session_state.modo_ciclo:
        st.session_state.modo_ciclo = modo_sel
        st.rerun()

    dt_ciclo_ini, dt_ciclo_fim, _ = get_intervalo_ciclo(st.session_state.cal_ano, st.session_state.cal_mes, st.session_state.modo_ciclo)
    dt_full_ini, dt_full_fim, _ = get_intervalo_ciclo(st.session_state.cal_ano, st.session_state.cal_mes, "Ciclo Completo (04 a 03)")

    df_prev_c = df_prev[df_prev["data_prevista"].apply(lambda d: dt_ciclo_ini <= datetime.strptime(d, "%Y-%m-%d").date() <= dt_ciclo_fim)] if not df_prev.empty else pd.DataFrame()
    df_reemb_c = df_reemb_itens[df_reemb_itens["data"].apply(lambda d: dt_ciclo_ini <= datetime.strptime(d, "%Y-%m-%d").date() <= dt_ciclo_fim)] if not df_reemb_itens.empty else pd.DataFrame()

    ent_b = float(df_prev_c[df_prev_c["tipo"] == "Entrada"]["valor"].sum()) if not df_prev_c.empty else 0.0
    sai_b = float(df_prev_c[df_prev_c["tipo"] == "Saída"]["valor"].sum()) if not df_prev_c.empty else 0.0
    reemb_t = float(df_reemb_c["valor"].sum()) if not df_reemb_c.empty else 0.0
    reemb_cp = float(df_reemb_c[df_reemb_c["acao"] != "Creditar em Conta Corrente"]["valor"].sum()) if not df_reemb_c.empty else 0.0

    ent_tot = ent_b + reemb_t
    sai_tot = sai_b + reemb_cp
    proj_f = total_saldos + ent_tot - sai_tot

    st.markdown(f"""
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:6px;margin:8px 0;font-size:0.70rem;">
        <div style="background:#111115;padding:7px 9px;border-radius:10px;"><span style="color:#71717a;">A Receber:</span> <strong style="color:#34d399;">+R$ {ent_tot:,.2f}</strong></div>
        <div style="background:#111115;padding:7px 9px;border-radius:10px;"><span style="color:#71717a;">Saídas+Dest.:</span> <strong style="color:#fb7185;">-R$ {sai_tot:,.2f}</strong></div>
        <div style="background:#111115;padding:7px 9px;border-radius:10px;"><span style="color:#71717a;">Atual:</span> <strong>R$ {total_saldos:,.2f}</strong></div>
        <div style="background:#111115;padding:7px 9px;border-radius:10px;"><span style="color:#71717a;">Projetado:</span> <strong style="color:{'#34d399' if proj_f >= 0 else '#fb7185'};">R$ {proj_f:,.2f}</strong></div>
    </div>
    """, unsafe_allow_html=True)

    # Tabela visual do ciclo 04 a 03
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
        reemb_rows = {}
        for _, r_r in df_reemb_itens.iterrows():
            try:
                dt_r = datetime.strptime(r_r["data"], "%Y-%m-%d").date()
                if dt_full_ini <= dt_r <= dt_full_fim:
                    reemb_rows.setdefault(dt_r, []).append(r_r)
            except:
                pass
        for dt_r, l_r in reemb_rows.items():
            s_dest = sum(float(x["valor"]) for x in l_r if x["acao"] != "Creditar em Conta Corrente")
            if s_dest > 0:
                eventos_por_data.setdefault(dt_r, []).append({"valor": s_dest, "papel_cal": "EntradaCobertura"})
            for r_it in l_r:
                eventos_por_data.setdefault(dt_r, []).append({
                    "valor": r_it["valor"],
                    "papel_cal": "ReembSemDestino" if r_it["acao"] == "Creditar em Conta Corrente" else "SaidaComprometida"
                })

    start_grid = dt_full_ini - timedelta(days=dt_full_ini.weekday())
    end_grid = dt_full_fim + timedelta(days=(6 - dt_full_fim.weekday()))
    html_cal = '<table class="cal-table"><thead><tr>' + ''.join(f'<th class="cal-th">{d}</th>' for d in ["Seg", "Ter", "Qua", "Qui", "Sex", "Sáb", "Dom"]) + '</tr></thead><tbody>'
    cur_dt = start_grid
    while cur_dt <= end_grid:
        html_cal += '<tr>'
        for _ in range(7):
            if not (dt_full_ini <= cur_dt <= dt_full_fim):
                html_cal += f'<td class="cal-cell" style="opacity:0.2;"><span style="color:#71717a;">{cur_dt.day:02d}/{cur_dt.month:02d}</span></td>'
            else:
                cls = ["cal-cell"]
                if cur_dt == hoje: cls.append("today")
                if cur_dt.day in [3, 16]: cls.append("payday")
                bdg = ""
                if cur_dt in eventos_por_data:
                    evs = eventos_por_data[cur_dt]
                    ti = any(e["papel_cal"] == "EntradaLivre" for e in evs)
                    ta = any(e["papel_cal"] == "ReembSemDestino" for e in evs)
                    to = any(e["papel_cal"] == "SaidaComprometida" for e in evs)
                    if (ti or ta) and to: cls.append("has-ambos")
                    elif to: cls.append("has-saida")
                    elif ta: cls.append("has-reemb-livre")
                    elif ti: cls.append("has-entrada")
                    for ev in evs:
                        p = ev["papel_cal"]
                        cb = "badge-out" if p == "SaidaComprometida" else ("badge-reemb-livre" if p == "ReembSemDestino" else "badge-in")
                        sb = "-" if p == "SaidaComprometida" else "+"
                        bdg += f'<span class="cal-badge {cb}">{sb}{ev["valor"]:,.0f}</span>'
                ld = f"{cur_dt.day:02d}/{cur_dt.month:02d}" if cur_dt.month != st.session_state.cal_mes else f"{cur_dt.day}"
                cn = "#eab308" if cur_dt.day in [3, 16] else ("#38bdf8" if cur_dt == hoje else "#a1a1aa")
                html_cal += f'<td class="{" ".join(cls)}"><span style="color:{cn};">{ld}</span>{bdg}</td>'
            cur_dt += timedelta(days=1)
        html_cal += '</tr>'
    html_cal += '</tbody></table>'
    st.markdown(html_cal, unsafe_allow_html=True)

    # Novo Lançamento Previsto recolhível
    if st.button("➖ Ocultar Formulário" if st.session_state.mostrar_form_prev else "➕ Agendar Lançamento no Ciclo", key="toggle_form_prev"):
        st.session_state.mostrar_form_prev = not st.session_state.mostrar_form_prev
        st.rerun()

    if st.session_state.mostrar_form_prev:
        with st.form("form_add_prev_oled"):
            c1, c2 = st.columns(2)
            with c1:
                d_s = st.date_input("Data", value=date.today())
                t_s = st.selectbox("Tipo", ["Entrada", "Saída"])
                v_s = st.number_input("Valor (R$)", min_value=0.01, value=1500.00, step=50.0)
            with c2:
                ds_s = st.text_input("Descrição", value="Salário Dia 03 / Dia 16")
                b_s = st.selectbox("Banco", df_bancos["banco"].tolist())
                ct_s = st.selectbox("Categoria", ["Salário", "Renda", "Fatura", "Contas Fixas", "Lazer", "Outros"])
            fx_s = st.checkbox("📌 Fixar recorrente", value=True)
            mq_s = st.slider("Repetir meses", 1, 12, 1)
            if st.form_submit_button("💾 Confirmar Agendamento"):
                adicionar_previsto(d_s.strftime("%Y-%m-%d"), ds_s, v_s, ct_s, t_s, b_s, mq_s, 1 if fx_s else 0)
                st.session_state.mostrar_form_prev = False
                st.rerun()

    # Lista de lançamentos do ciclo recolhível
    qtd_lc = len(df_prev_c) + len(df_reemb_c)
    clc1, clc2 = st.columns([3.5, 1.5])
    with clc1: st.markdown(f'<div style="font-size:0.74rem;font-weight:700;color:#a1a1aa;margin-top:8px;">Lançamentos ({qtd_lc})</div>', unsafe_allow_html=True)
    with clc2:
        if st.button("👁️ Mostrar" if st.session_state.recolher_lanc_ciclo else "🔼 Recolher", key="btn_toggle_rec_lc"):
            st.session_state.recolher_lanc_ciclo = not st.session_state.recolher_lanc_ciclo
            st.rerun()
    if st.session_state.recolher_lanc_ciclo:
        st.caption(f"Lista recolhida ({qtd_lc} itens).")
    else:
        for _, rp in df_prev_c.iterrows():
            is_e = rp["tipo"] == "Entrada"
            c1, c2, c3 = st.columns([4, 1, 1])
            with c1:
                st.markdown(f'<div class="oled-list-item"><div><strong style="font-size:0.76rem;">{rp["descricao"]}</strong><br><span style="font-size:0.62rem;color:#71717a;">{rp["data_prevista"]} · {rp["banco"]}</span></div><div style="font-family:JetBrains Mono;font-weight:700;color:{"#34d399" if is_e else "#fb7185"};font-size:0.80rem;">{"+" if is_e else "-"}R$ {rp["valor"]:,.2f}</div></div>', unsafe_allow_html=True)
            with c2:
                if st.button("✅", key=f"btn_efet_{rp['id']}", help="Baixar"):
                    efetivar_previsto(rp["id"])
                    st.rerun()
            with c3:
                st.markdown('<div class="btn-clear">', unsafe_allow_html=True)
                if st.button("🗑️", key=f"del_p_{rp['id']}", help="Excluir"):
                    remover_previsto(rp["id"])
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ================= CONTEÚDO DAS ABAS DA BARRA INFERIOR =================
if st.session_state.oled_tab == "Home":
    if st.session_state.qa_subpanel == "ciclo":
        render_ciclo_previsoes_box()
    elif st.session_state.qa_subpanel == "rateio":
        render_rateio_reembolso_box()

    # 2 Cards Bento OLED (Allocation & Earnings)
    spark_purple_svg = '<svg width="100%" height="34" viewBox="0 0 140 34" fill="none"><path d="M2 28 C18 24, 24 27, 38 19 C52 11, 60 22, 74 16 C88 10, 96 18, 112 12 C124 8, 132 13, 138 6" stroke="#a855f7" stroke-width="2.2" stroke-linecap="round"/></svg>'
    st.markdown(f"""
    <div class="oled-bento-grid">
        <div class="oled-card purple-glow">
            <div class="oled-card-hdr"><span>Allocation</span><span style="color:#71717a;">›</span></div>
            {spark_purple_svg}
            <div class="oled-prog-txt" style="margin-top:6px;">Ciclo • <span class="p-purple">{pct_ciclo:.1f}%</span></div>
        </div>
        <div class="oled-card cyan-glow">
            <div class="oled-card-hdr"><span>Earnings</span><span style="color:#71717a;">›</span></div>
            <div class="oled-card-val">R$ {tot_reembolso_esperado:,.2f}</div>
            <div class="oled-prog-txt">Meta • <span class="p-cyan">{pct_aloc_meta:.1f}% ({qtd_dias_aloc}d)</span></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Allocation Calendar (Matriz interativa de 7 colunas)
    render_allocation_calendar_widget()

    # Dual Gradient Cards Inferiores (AI Advisor & Vencimentos/PDF)
    st.markdown(f"""
    <div class="dual-grad-grid">
        <div class="grad-card-purple">
            <div class="grad-card-title"><span>AI Advisor</span><span>›</span></div>
            <div class="grad-card-sub">Plano gasolina/pedágio & projeção 6 meses</div>
        </div>
        <div class="grad-card-cyan">
            <div class="grad-card-title"><span>Relatório & PDF</span><span>›</span></div>
            <div class="grad-card-sub">Exportar balanço e resumo WhatsApp</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    g_btn1, g_btn2 = st.columns(2)
    with g_btn1:
        if st.button("🧠 Abrir AI Advisor", key="open_adv_home"):
            st.session_state.oled_tab = "Insights"
            st.rerun()
    with g_btn2:
        if st.button("📄 Gerar PDF / WhatsApp", key="open_pdf_home"):
            st.session_state.oled_tab = "Insights"
            st.rerun()

elif st.session_state.oled_tab == "Insights":
    st.markdown('<div class="alloc-cal-box">', unsafe_allow_html=True)
    st.markdown('<div style="font-size:0.90rem;font-weight:700;color:#c084fc;margin-bottom:8px;">🧠 AI Advisor • Diagnóstico & Projeção 6 Meses</div>', unsafe_allow_html=True)

    tot_parc_m = float(df_parc["valor_parcela"].sum()) if not df_parc.empty else 0.0
    tot_div_p = sum(max(0, int(r["total_parcelas"]) - int(r["parcela_atual"])) * float(r["valor_parcela"]) for _, r in df_parc.iterrows()) if not df_parc.empty else 0.0

    proj_6m = []
    for off in range(6):
        dt_r = date(st.session_state.cal_ano, st.session_state.cal_mes, 1) + relativedelta(months=off)
        lbl = f"{meses_nomes[dt_r.month - 1][:3]}/{str(dt_r.year)[2:]}"
        pa = sum(float(rp["valor_parcela"]) for _, rp in df_parc.iterrows() if (int(rp["parcela_atual"]) + off) <= int(rp["total_parcelas"])) if not df_parc.empty else 0.0
        sob = renda_futura_livre + max(0.0, tot_parc_m - pa)
        proj_6m.append((lbl, sob, pa))

    cols_6 = "".join(
        f'<div style="background:#111115;border:1px solid rgba(255,255,255,0.08);border-radius:8px;padding:6px 2px;text-align:center;">'
        f'<div style="font-size:0.58rem;color:#71717a;">{m}</div>'
        f'<div style="font-family:JetBrains Mono;font-size:0.66rem;font-weight:700;color:{"#34d399" if s>=0 else "#fb7185"};">{"+" if s>=0 else ""}{s:,.0f}</div>'
        f'<div style="font-size:0.50rem;color:#52525b;">P:{p:,.0f}</div></div>'
        for m, s, p in proj_6m
    )
    st.markdown(f'<div style="display:grid;grid-template-columns:repeat(6,1fr);gap:4px;margin-bottom:10px;">{cols_6}</div>', unsafe_allow_html=True)

    with st.expander("⛽ Plano Gasolina & Pedágio (Alocações)", expanded=False):
        contas_s = df_bancos[df_bancos["saldo_conta"] > 0].sort_values(by="saldo_conta", ascending=False)
        m_conta = contas_s.iloc[0]["banco"] if not contas_s.empty else "Sem saldo em conta"
        cartoes_d = df_bancos[df_bancos["tem_cartao"] == 1].copy()
        m_card = "Sem limite livre"
        if not cartoes_d.empty:
            cartoes_d["lr"] = cartoes_d.apply(lambda r: float(r["limite_liberado"]) if float(r["limite_liberado"]) > 0 else max(0.0, float(r["limite_cartao"]) - float(r["fatura_atual"])), axis=1)
            val_c = cartoes_d[cartoes_d["lr"] >= 50.0].sort_values(by="lr", ascending=False)
            if not val_c.empty: m_card = val_c.iloc[0]["banco"]
        st.markdown(f"• **Dias marcados:** {qtd_dias_aloc}d · **Gasolina:** R$ {tot_gas_mes:,.2f} · **Pedágio:** R$ {tot_ped_mes:,.2f}<br>• **Fonte Gasolina:** {m_conta}<br>• **Cartão Pedágio:** {m_card}", unsafe_allow_html=True)

    with st.expander("🔍 Onde Está Perdendo Dinheiro & Plano 3 Passos", expanded=False):
        if total_cheque > 0:
            st.warning(f"Cheque Especial em uso: R$ {total_cheque:,.2f} (~R$ {total_cheque*0.08:,.2f}/mês de juros). Zere como prioridade #1.")
        else:
            st.success("Cheque Especial zerado!")
        st.info(f"Parcelas ativas: R$ {tot_parc_m:,.2f}/mês (restante total: R$ {tot_div_p:,.2f}).")

    # Exportação PDF e WhatsApp
    diags_pdf = [{"titulo": "Balanco Consolidado", "desc": f"Saldo R$ {total_saldos:,.2f} | Renda livre R$ {renda_futura_livre:,.2f} | Faturas R$ {total_faturas:,.2f}"}]
    pdf_bytes = gerar_relatorio_pdf(df_bancos, entradas_futuras_brutas, saidas_comprometidas_ciclo, projecao_com_futuro, tot_parc_m, tot_div_p, diags_pdf)
    txt_wpp = f"*RELATÓRIO FINANCEIRO ({dt_hero_ini.strftime('%d/%m')} a {dt_hero_fim.strftime('%d/%m')})*\n• Saldo: R$ {total_saldos:,.2f}\n• Renda Futura Livre: R$ {renda_futura_livre:,.2f}\n• Faturas: R$ {total_faturas:,.2f}"
    ce1, ce2 = st.columns(2)
    with ce1:
        st.download_button("📄 Baixar PDF", data=pdf_bytes, file_name=f"relatorio_{dt_hero_ini.strftime('%Y_%m_%d')}.pdf", mime="application/pdf")
    with ce2:
        st.markdown(f'<a href="https://api.whatsapp.com/send?text={urllib.parse.quote(txt_wpp)}" target="_blank"><button style="width:100%;height:36px;background:#10b981;color:#000;border:none;border-radius:999px;font-weight:700;font-size:0.72rem;cursor:pointer;">📲 WhatsApp</button></a>', unsafe_allow_html=True)

    # Extrato recolhível
    cex1, cex2 = st.columns([3.5, 1.5])
    with cex1: st.markdown(f'<div style="font-size:0.78rem;font-weight:700;color:#a1a1aa;margin-top:10px;">Extrato Completo ({len(df_tx)})</div>', unsafe_allow_html=True)
    with cex2:
        if st.button("👁️ Mostrar" if st.session_state.recolher_extrato_lista else "🔼 Recolher", key="btn_toggle_rec_ext"):
            st.session_state.recolher_extrato_lista = not st.session_state.recolher_extrato_lista
            st.rerun()
    if st.session_state.recolher_extrato_lista:
        st.caption(f"Extrato recolhido ({len(df_tx)} lançamentos).")
    else:
        for _, row in df_tx.iterrows():
            is_s = row["tipo"] == "Saída"
            st.markdown(f'<div class="oled-list-item"><div><strong style="font-size:0.76rem;">{row["descricao"]}</strong><br><span style="font-size:0.62rem;color:#71717a;">{row["data"]} · {row["banco"]}</span></div><div style="font-family:JetBrains Mono;font-weight:700;color:{"#fb7185" if is_s else "#34d399"};font-size:0.80rem;">{"-" if is_s else "+"}R$ {row["valor"]:,.2f}</div></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.oled_tab == "Cards":
    st.markdown('<div class="alloc-cal-box">', unsafe_allow_html=True)
    st.markdown('<div style="font-size:0.88rem;font-weight:700;color:#ffffff;margin-bottom:8px;">💳 Bancos & Compras Parceladas</div>', unsafe_allow_html=True)

    for _, b in df_bancos.iterrows():
        tem_c = (b.get("tem_cartao", 1) == 1)
        lim_t = float(b.get("limite_cartao", 0.0))
        lim_l = float(b.get("limite_liberado", 0.0))
        lim_ex = lim_l if lim_l > 0 else max(0.0, lim_t - float(b["fatura_atual"]))
        st.markdown(f"""
        <div class="oled-list-item" style="border-left:3px solid {b['cor_identificador']};">
            <div>
                <strong style="font-size:0.82rem;">{b['banco']}</strong><br>
                <span style="font-size:0.64rem;color:#a1a1aa;">Saldo: R$ {b['saldo_conta']:,.2f} {f'· Fatura: R$ {b["fatura_atual"]:,.2f} (Venc {int(b.get("dia_vencimento",10))})' if tem_c else ''}</span>
            </div>
            <div style="text-align:right;font-family:JetBrains Mono;font-size:0.76rem;">
                {f'<span style="color:#34d399;font-weight:700;">Livre: R$ {lim_ex:,.2f}</span>' if tem_c else '<span style="color:#71717a;">Conta</span>'}
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Parcelas recolhíveis
    if st.button("➖ Ocultar Formulário" if st.session_state.mostrar_form_parc else "➕ Nova Compra Parcelada", key="toggle_form_parc"):
        st.session_state.mostrar_form_parc = not st.session_state.mostrar_form_parc
        st.rerun()

    if st.session_state.mostrar_form_parc:
        with st.form("form_add_parc_oled"):
            b_cards = df_bancos[df_bancos["tem_cartao"] == 1]["banco"].tolist() or df_bancos["banco"].tolist()
            c1, c2 = st.columns(2)
            with c1:
                bp = st.selectbox("Cartão", b_cards)
                pa = st.number_input("Parcela Atual", 1, 60, 1)
                vp = st.number_input("Valor Parcela", min_value=0.01, value=150.0, step=10.0)
            with c2:
                dp = st.text_input("Descrição", value="Compra Parcelada")
                pt = st.number_input("Total Parcelas", 1, 60, 10)
                cp = st.selectbox("Categoria", ["Eletrônicos", "Casa", "Vestuário", "Veículo", "Saúde", "Outros"])
            if st.form_submit_button("Salvar Parcela"):
                adicionar_parcela(bp, dp, vp, pa, pt, cp)
                st.session_state.mostrar_form_parc = False
                st.rerun()

    cpl1, cpl2 = st.columns([3.5, 1.5])
    with cpl1: st.markdown(f'<div style="font-size:0.76rem;font-weight:700;color:#a1a1aa;margin-top:8px;">Parcelas ({len(df_parc)})</div>', unsafe_allow_html=True)
    with cpl2:
        if st.button("👁️ Mostrar" if st.session_state.recolher_parc_lista else "🔼 Recolher", key="btn_toggle_rec_pl"):
            st.session_state.recolher_parc_lista = not st.session_state.recolher_parc_lista
            st.rerun()
    if st.session_state.recolher_parc_lista:
        st.caption(f"Lista recolhida ({len(df_parc)} compra(s)).")
    else:
        for _, rpc in df_parc.iterrows():
            pct = min(100.0, (rpc["parcela_atual"] / max(1, rpc["total_parcelas"])) * 100)
            st.markdown(f"""
            <div style="background:#111115;border:1px solid rgba(255,255,255,0.08);border-radius:12px;padding:10px;margin-bottom:6px;">
                <div style="display:flex;justify-content:space-between;font-size:0.78rem;">
                    <strong>{rpc['descricao']} ({rpc['banco']})</strong>
                    <span style="color:#38bdf8;font-family:JetBrains Mono;font-weight:700;">R$ {rpc['valor_parcela']:,.2f}</span>
                </div>
                <div class="parcela-progresso"><div class="parcela-progresso-bar" style="width:{pct:.0f}%;"></div></div>
                <div style="font-size:0.64rem;color:#71717a;">{rpc['parcela_atual']}/{rpc['total_parcelas']} · Fim {rpc['mes_ano_fim']}</div>
            </div>
            """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.oled_tab == "Allocation":
    render_allocation_calendar_widget()
    render_rateio_reembolso_box()

elif st.session_state.oled_tab == "Settings":
    st.markdown('<div class="alloc-cal-box">', unsafe_allow_html=True)
    st.markdown('<div style="font-size:0.88rem;font-weight:700;color:#ffffff;margin-bottom:8px;">⚙️ Configurações de Bancos & Backup</div>', unsafe_allow_html=True)

    st.markdown('<div class="btn-clear" style="margin-bottom:8px;">', unsafe_allow_html=True)
    if st.button("⚠️ Zerar Saldos e Faturas", key="btn_zerar_oled"):
        zerar_saldos_e_faturas()
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    banco_edit = st.selectbox("Banco", df_bancos["banco"].tolist())
    row_b = df_bancos[df_bancos["banco"] == banco_edit].iloc[0]
    with st.form("form_cfg_oled"):
        possui_c = st.checkbox("💳 Possui Cartão de Crédito?", value=bool(row_b.get("tem_cartao", 1)))
        n_sal = st.number_input("Saldo Conta (R$)", value=float(row_b["saldo_conta"]), step=10.0)
        l_chq = st.number_input("Limite Cheque Especial (R$)", value=float(row_b["limite_cheque_especial"]), step=100.0)
        u_chq = st.number_input("Cheque Especial Usado (R$)", value=float(row_b["cheque_especial_usado"]), step=10.0)
        if possui_c:
            c1, c2 = st.columns(2)
            with c1:
                n_lim = st.number_input("Limite Total", value=float(row_b["limite_cartao"]), step=100.0)
                n_fat = st.number_input("Fatura Atual", value=float(row_b["fatura_atual"]), step=10.0)
                d_ven = st.number_input("Vencimento", 1, 31, int(row_b.get("dia_vencimento", 10)))
            with c2:
                n_lib = st.number_input("Limite Liberado", value=float(row_b.get("limite_liberado", 0.0)), step=100.0)
                d_fec = st.number_input("Fechamento", 1, 31, int(row_b.get("dia_fechamento", 3)))
        else:
            n_lim, n_fat, n_lib, d_ven, d_fec = 0.0, 0.0, 0.0, 10, 3
        if st.form_submit_button("💾 Salvar Configurações"):
            atualizar_banco_completo(banco_edit, 1 if possui_c else 0, n_fat, n_lim, n_lib, n_sal, l_chq, u_chq, d_ven, d_fec)
            st.success("Salvo!")
            st.rerun()

    st.markdown('<div style="font-size:0.80rem;font-weight:700;color:#a1a1aa;margin:12px 0 6px 0;">Backup (.db)</div>', unsafe_allow_html=True)
    cb1, cb2 = st.columns(2)
    with cb1:
        if os.path.exists("financas.db"):
            with open("financas.db", "rb") as f_db:
                st.download_button("📥 Baixar .db", data=f_db.read(), file_name=f"backup_financas_{datetime.now().strftime('%Y_%m_%d')}.db", mime="application/octet-stream")
    with cb2:
        up_db = st.file_uploader("Restaurar .db", type=["db"], label_visibility="collapsed")
        if up_db is not None and st.button("📤 Restaurar"):
            with open("financas.db", "wb") as f_out:
                f_out.write(up_db.read())
            st.success("Restaurado!")
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# ================= BOTTOM NAVIGATION BAR (5 ABAS) =================
st.markdown('<div class="bottom-nav-wrap">', unsafe_allow_html=True)
bn1, bn2, bn3, bn4, bn5 = st.columns(5)
nav_items = [
    (bn1, "🏠\nHome", "Home"),
    (bn2, "📊\nInsights", "Insights"),
    (bn3, "💳\nCards", "Cards"),
    (bn4, "🎯\nAllocation", "Allocation"),
    (bn5, "⚙️\nSettings", "Settings")
]
for col_n, lbl_n, tab_key in nav_items:
    with col_n:
        if st.button(lbl_n, key=f"bnav_{tab_key}", type="primary" if st.session_state.oled_tab == tab_key else "secondary"):
            st.session_state.oled_tab = tab_key
            st.session_state.recolher_lanc_ciclo = True
            st.session_state.recolher_dest_reemb = True
            st.session_state.recolher_parc_lista = True
            st.session_state.recolher_extrato_lista = True
            st.rerun()
st.markdown('</div>', unsafe_allow_html=True)
