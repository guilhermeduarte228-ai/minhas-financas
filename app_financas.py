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

st.set_page_config(page_title="FINANCAS.AI • Painel Executivo", page_icon="⚡", layout="wide", initial_sidebar_state="auto")

# ================= CSS MODERNO RESPONSIVO (PC WIDE + MOBILE ADAPTATIVO) =================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500;700;800&display=swap');

    html, body, .stApp {
        background-color: #090d16 !important;
        color: #f1f5f9;
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    .block-container {
        max-width: 1280px !important;
        padding-top: 1.2rem !important;
        padding-bottom: 3rem !important;
        padding-left: 1.4rem !important;
        padding-right: 1.4rem !important;
    }

    @media (max-width: 768px) {
        .block-container {
            padding-top: 0.7rem !important;
            padding-left: 0.75rem !important;
            padding-right: 0.75rem !important;
        }
    }

    #MainMenu, footer { visibility: hidden; }
    header[data-testid="stHeader"] {
        background: transparent !important;
    }

    /* Sidebar Executiva */
    section[data-testid="stSidebar"] {
        background-color: #0d1320 !important;
        border-right: 1px solid #1c283d !important;
    }
    section[data-testid="stSidebar"] .stRadio > div {
        gap: 6px;
    }
    section[data-testid="stSidebar"] label {
        background: #121b2c;
        border: 1px solid #1e2d45;
        border-radius: 12px;
        padding: 10px 12px !important;
        width: 100%;
        transition: all 0.2s ease;
        font-weight: 700 !important;
        font-size: 0.82rem !important;
    }
    section[data-testid="stSidebar"] label:hover {
        border-color: #38bdf8;
        background: #172338;
    }

    /* Header Topo */
    .exec-topbar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        background: linear-gradient(135deg, #111928 0%, #0d1422 100%);
        border: 1px solid #1e2d45;
        border-radius: 18px;
        padding: 14px 18px;
        margin-bottom: 16px;
        flex-wrap: wrap;
        gap: 10px;
    }
    .exec-brand {
        display: flex;
        align-items: center;
        gap: 10px;
    }
    .exec-logo-icon {
        width: 36px;
        height: 36px;
        border-radius: 10px;
        background: linear-gradient(135deg, #38bdf8 0%, #818cf8 100%);
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 800;
        color: #090d16;
        font-size: 1.1rem;
    }
    .exec-title {
        font-size: 1.15rem;
        font-weight: 800;
        color: #ffffff;
        letter-spacing: -0.3px;
        line-height: 1.1;
    }
    .exec-sub {
        font-size: 0.72rem;
        color: #94a3b8;
    }
    .exec-pill {
        background: #162236;
        border: 1px solid #263957;
        color: #38bdf8;
        padding: 6px 12px;
        border-radius: 999px;
        font-size: 0.72rem;
        font-weight: 700;
        display: inline-flex;
        align-items: center;
        gap: 6px;
    }
    .dot-online {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background: #22c55e;
        box-shadow: 0 0 8px #22c55e;
    }

    /* Grade de 4 KPIs no Topo (4 colunas no PC -> 2x2 no Celular!) */
    .kpi-grid-4 {
        display: grid;
        grid-template-columns: repeat(4, minmax(0, 1fr));
        gap: 12px;
        margin-bottom: 16px;
    }
    @media (max-width: 900px) {
        .kpi-grid-4 {
            grid-template-columns: repeat(2, minmax(0, 1fr));
            gap: 8px;
        }
    }
    .kpi-card {
        background: linear-gradient(145deg, #131c2e 0%, #0e1524 100%);
        border: 1px solid #1f2e47;
        border-radius: 18px;
        padding: 14px 16px;
        position: relative;
        overflow: hidden;
    }
    .kpi-card.accent-green { border-top: 3px solid #22c55e; }
    .kpi-card.accent-blue { border-top: 3px solid #38bdf8; }
    .kpi-card.accent-purple { border-top: 3px solid #a855f7; }
    .kpi-card.accent-red { border-top: 3px solid #f43f5e; }

    .kpi-lbl {
        font-size: 0.68rem;
        font-weight: 700;
        color: #94a3b8;
        text-transform: uppercase;
        letter-spacing: 0.6px;
    }
    .kpi-val {
        font-family: 'JetBrains Mono', monospace;
        font-size: 1.45rem;
        font-weight: 800;
        color: #ffffff;
        margin: 6px 0 4px 0;
        letter-spacing: -0.5px;
    }
    @media (max-width: 768px) {
        .kpi-val { font-size: 1.15rem; }
        .kpi-card { padding: 11px 12px; }
    }
    .kpi-foot {
        font-size: 0.68rem;
        color: #94a3b8;
        line-height: 1.3;
    }

    /* Barra de Progresso do Ciclo */
    .ciclo-bar-bg {
        width: 100%;
        height: 7px;
        background: #1b273d;
        border-radius: 999px;
        overflow: hidden;
        margin: 8px 0 6px 0;
    }
    .ciclo-bar-fill {
        height: 100%;
        background: linear-gradient(90deg, #38bdf8 0%, #a855f7 100%);
        border-radius: 999px;
    }

    /* Bento Card Genérico */
    .bento-box {
        background: #111927;
        border: 1px solid #1e2d44;
        border-radius: 18px;
        padding: 16px;
        margin-bottom: 14px;
    }
    .bento-title {
        font-size: 0.85rem;
        font-weight: 800;
        color: #ffffff;
        margin-bottom: 10px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    /* Cards de Bancos */
    .bank-card {
        background: #121a28;
        border: 1px solid #1f2d42;
        border-radius: 16px;
        padding: 14px;
        margin-bottom: 10px;
    }
    .bank-card-top {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 10px;
    }
    .bank-badge {
        font-size: 0.90rem;
        font-weight: 800;
        color: #ffffff;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .bank-dot {
        width: 10px;
        height: 10px;
        border-radius: 4px;
    }
    .bank-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 8px;
    }
    .bank-stat {
        background: #0c121c;
        border: 1px solid #182436;
        border-radius: 10px;
        padding: 9px 10px;
    }
    .bank-stat-lbl {
        font-size: 0.60rem;
        color: #64748b;
        font-weight: 700;
        text-transform: uppercase;
    }
    .bank-stat-val {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.92rem;
        font-weight: 700;
        color: #ffffff;
        margin-top: 2px;
    }

    /* Pills de Status */
    .md-msg-pill {
        display: inline-block;
        padding: 3px 9px;
        border-radius: 8px;
        font-size: 0.66rem;
        font-weight: 700;
    }
    .msg-danger { background: rgba(239, 68, 68, 0.15); color: #f87171; border: 1px solid rgba(239, 68, 68, 0.3); }
    .msg-warning { background: rgba(245, 158, 11, 0.15); color: #fbbf24; border: 1px solid rgba(245, 158, 11, 0.3); }
    .msg-success { background: rgba(34, 197, 94, 0.15); color: #4ade80; border: 1px solid rgba(34, 197, 94, 0.3); }
    .msg-neutral { background: rgba(148, 163, 184, 0.15); color: #cbd5e1; border: 1px solid rgba(148, 163, 184, 0.3); }

    /* Botões */
    .stButton > button {
        border-radius: 12px !important;
        font-weight: 700 !important;
        font-size: 0.78rem !important;
        border: 1px solid #243652 !important;
        transition: all 0.18s ease !important;
    }
    .stButton > button:hover {
        border-color: #38bdf8 !important;
        transform: translateY(-1px);
    }
    .btn-clear button {
        background: rgba(239, 68, 68, 0.12) !important;
        color: #f87171 !important;
        border: 1px solid rgba(239, 68, 68, 0.35) !important;
    }
    .btn-action-icon button {
        background: rgba(56, 189, 248, 0.12) !important;
        color: #38bdf8 !important;
        border: 1px solid rgba(56, 189, 248, 0.35) !important;
    }

    /* Grade do Calendário de Alocações 100% Responsiva no Celular (7 colunas fixas) */
    [data-testid="stHorizontalBlock"]:has(> [data-testid="stColumn"]:nth-child(7)),
    [data-testid="stHorizontalBlock"]:has(> [data-testid="column"]:nth-child(7)) {
        display: grid !important;
        grid-template-columns: repeat(7, minmax(0, 1fr)) !important;
        gap: 3px !important;
        width: 100% !important;
        margin-bottom: 3px !important;
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
        font-size: 0.66rem !important;
        font-weight: 700 !important;
        border-radius: 8px !important;
        line-height: 1 !important;
    }

    /* Tabela do Calendário do Ciclo */
    .cal-table {
        width: 100%;
        border-collapse: separate;
        border-spacing: 4px;
        margin-top: 6px;
    }
    .cal-th {
        text-align: center;
        font-size: 0.65rem;
        font-weight: 700;
        color: #64748b;
        padding: 4px 0;
    }
    .cal-cell {
        background: #0d1522;
        border: 1px solid #1a273b;
        border-radius: 8px;
        height: 48px;
        vertical-align: top;
        padding: 4px;
        text-align: right;
        font-size: 0.65rem;
        font-weight: 600;
    }
    .cal-cell.payday { border-color: #eab308 !important; box-shadow: inset 0 0 6px rgba(234, 179, 8, 0.35); }
    .cal-cell.today { border-color: #38bdf8 !important; box-shadow: 0 0 6px rgba(56, 189, 248, 0.4); }
    .cal-cell.has-entrada { background: rgba(34, 197, 94, 0.16) !important; border-color: rgba(34, 197, 94, 0.65) !important; }
    .cal-cell.has-saida { background: rgba(239, 68, 68, 0.16) !important; border-color: rgba(239, 68, 68, 0.65) !important; }
    .cal-cell.has-reemb-livre { background: rgba(234, 179, 8, 0.16) !important; border-color: rgba(234, 179, 8, 0.75) !important; }
    .cal-cell.has-ambos { background: rgba(245, 158, 11, 0.16) !important; border-color: rgba(245, 158, 11, 0.65) !important; }
    .cal-badge {
        font-size: 0.54rem;
        font-weight: 800;
        font-family: 'JetBrains Mono', monospace;
        display: block;
        text-align: left;
        margin-top: 2px;
        line-height: 1.1;
    }
    .badge-in { color: #4ade80; }
    .badge-out { color: #f87171; }
    .badge-reemb-livre { color: #fbbf24; }

    .prev-item-card {
        background: #0d1522;
        border: 1px solid #1a273b;
        border-radius: 12px;
        padding: 10px 12px;
        margin-bottom: 6px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .parcela-card {
        background: #111a28;
        border: 1px solid #1e2c40;
        border-radius: 14px;
        padding: 12px;
        margin-bottom: 8px;
    }
    .parcela-progresso {
        background: #1a2538;
        height: 6px;
        border-radius: 4px;
        overflow: hidden;
        margin: 8px 0;
    }
    .parcela-progresso-bar {
        background: linear-gradient(90deg, #0284c7 0%, #38bdf8 100%);
        height: 100%;
    }
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


# ================= NAVEGAÇÃO LATERAL (SIDEBAR NO PC / RECOLHIDA NO CELULAR) =================
if "menu_nav" not in st.session_state:
    st.session_state.menu_nav = "📊 Dashboard"

with st.sidebar:
    st.markdown("""
    <div style="display:flex;align-items:center;gap:10px;padding:6px 4px 14px 4px;border-bottom:1px solid #1c283d;margin-bottom:12px;">
        <div class="exec-logo-icon">⚡</div>
        <div>
            <div style="font-size:1.0rem;font-weight:800;color:#ffffff;">FINANCAS.AI</div>
            <div style="font-size:0.66rem;color:#38bdf8;font-weight:700;">Gestão & Alocações</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    opcoes_menu = [
        "📊 Dashboard",
        "🏦 Bancos & Contas",
        "🗓️ Calendário de Alocação",
        "⛽ Reembolsos & KM",
        "📅 Ciclo & Previsões",
        "💳 Cartões & Parcelas",
        "📄 Extrato & Lançar",
        "⚙️ Ajustes & Backup"
    ]
    escolha_menu = st.radio("Navegação", opcoes_menu, index=opcoes_menu.index(st.session_state.menu_nav), label_visibility="collapsed")
    if escolha_menu != st.session_state.menu_nav:
        # Ao trocar de tela, garante que blocos recolhíveis iniciem recolhidos (exceto calendários)
        st.session_state.mostrar_form_prev = False
        st.session_state.mostrar_calc_km = False
        st.session_state.mostrar_form_rateio = False
        st.session_state.recolher_lanc_ciclo = True
        st.session_state.recolher_dest_reemb = True
        st.session_state.recolher_parc_lista = True
        st.session_state.recolher_extrato_lista = True
        st.session_state.menu_nav = escolha_menu
        st.rerun()

# ================= CÁLCULOS GLOBAIS DO CICLO E ALOCAÇÕES =================
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

# Resumo das Alocações do Mês Ativo
dt_aloc_g_ini = date(st.session_state.cal_ano, st.session_state.cal_mes, 1).strftime("%Y-%m-%d")
dt_aloc_g_fim = date(st.session_state.cal_ano, st.session_state.cal_mes, calendar.monthrange(st.session_state.cal_ano, st.session_state.cal_mes)[1]).strftime("%Y-%m-%d")
df_aloc_glob = pd.DataFrame()
if not df_aloc.empty:
    df_aloc_glob = df_aloc[(df_aloc["data_alocacao"] >= dt_aloc_g_ini) & (df_aloc["data_alocacao"] <= dt_aloc_g_fim)]

qtd_dias_aloc_glob = len(df_aloc_glob)
tot_diarias_glob = float(df_aloc_glob["valor_diaria"].sum()) if qtd_dias_aloc_glob > 0 else 0.0
tot_gas_glob = float(df_aloc_glob["valor_gasolina"].sum()) if qtd_dias_aloc_glob > 0 else 0.0
tot_ped_glob = float(df_aloc_glob["valor_pedagio"].sum()) if qtd_dias_aloc_glob > 0 else 0.0
tot_lucro_glob = tot_diarias_glob - tot_gas_glob
tot_reemb_aloc_glob = tot_diarias_glob + tot_ped_glob

# Progresso do ciclo (04 a 03)
total_dias_ciclo = max(1, (dt_hero_fim - dt_hero_ini).days)
dias_passados_ciclo = min(total_dias_ciclo, max(0, (hoje - dt_hero_ini).days))
pct_ciclo = int((dias_passados_ciclo / total_dias_ciclo) * 100)

# ================= BARRA SUPERIOR EXECUTIVA =================
st.markdown(f"""
<div class="exec-topbar">
    <div class="exec-brand">
        <div class="exec-logo-icon">⚡</div>
        <div>
            <div class="exec-title">FINANCAS.AI • {st.session_state.menu_nav}</div>
            <div class="exec-sub">Competência {nome_mes_glob}/{st.session_state.cal_ano} ({dt_hero_ini.strftime('%d/%m')} a {dt_hero_fim.strftime('%d/%m')})</div>
        </div>
    </div>
    <div style="display:flex;align-items:center;gap:8px;">
        <span class="exec-pill"><span class="dot-online"></span> Sincronizado</span>
        <span class="exec-pill" style="color:#eab308;border-color:rgba(234,179,8,0.35);">💰 Dias 03 e 16</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ================= GRADE DE 4 KPIs (4 COLUNAS NO PC -> 2x2 NO CELULAR) =================
sinal_rf = "+" if renda_futura_livre >= 0 else "-"
cor_rf = "#4ade80" if renda_futura_livre >= 0 else "#f87171"

st.markdown(f"""
<div class="kpi-grid-4">
    <div class="kpi-card accent-green">
        <div class="kpi-lbl">💰 Patrimônio Real em Conta</div>
        <div class="kpi-val">R$ {total_saldos:,.2f}</div>
        <div class="kpi-foot"><span class="md-msg-pill {classe_total}">{msg_total}</span></div>
    </div>
    <div class="kpi-card accent-blue">
        <div class="kpi-lbl">⏳ Renda Futura Livre (Ciclo)</div>
        <div class="kpi-val" style="color:{cor_rf};">{sinal_rf} R$ {abs(renda_futura_livre):,.2f}</div>
        <div class="ciclo-bar-bg"><div class="ciclo-bar-fill" style="width:{pct_ciclo}%;"></div></div>
        <div class="kpi-foot">Noção c/ futuro: <strong style="color:#e2e8f0;">R$ {projecao_com_futuro:,.2f}</strong></div>
    </div>
    <div class="kpi-card accent-purple">
        <div class="kpi-lbl">🚗 Alocações ({qtd_dias_aloc_glob} dias)</div>
        <div class="kpi-val" style="color:#38bdf8;">R$ {tot_reemb_aloc_glob:,.2f}</div>
        <div class="kpi-foot">Lucro: <strong style="color:#4ade80;">R$ {tot_lucro_glob:,.2f}</strong> • Gas+Ped: R$ {(tot_gas_glob+tot_ped_glob):,.2f}</div>
    </div>
    <div class="kpi-card accent-red">
        <div class="kpi-lbl">💳 Faturas & Cheque Esp.</div>
        <div class="kpi-val" style="color:#f87171;">R$ {total_faturas:,.2f}</div>
        <div class="kpi-foot">Cheque Especial usado: <strong style="color:{'#f87171' if total_cheque > 0 else '#4ade80'};">R$ {total_cheque:,.2f}</strong></div>
    </div>
</div>
""", unsafe_allow_html=True)

# ================= HELPER DO CALENDÁRIO DE ALOCAÇÃO + CALCULADORA VINCULADA =================
def render_calendario_alocacoes_e_calc():
    if "aloc_cal_mes" not in st.session_state:
        st.session_state.aloc_cal_mes = st.session_state.cal_mes
    if "aloc_cal_ano" not in st.session_state:
        st.session_state.aloc_cal_ano = st.session_state.cal_ano

    meses_aloc_nomes = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]
    nome_m_aloc = meses_aloc_nomes[st.session_state.aloc_cal_mes - 1]

    st.markdown('<div class="bento-box">', unsafe_allow_html=True)
    ca_nav1, ca_nav2, ca_nav3 = st.columns([3.5, 1.2, 1.2])
    with ca_nav1:
        st.markdown(f'<div style="font-size:0.88rem;font-weight:800;color:#38bdf8;padding-top:4px;">🗓️ Calendário de Alocação • {nome_m_aloc}/{st.session_state.aloc_cal_ano}</div>', unsafe_allow_html=True)
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
        val_diaria_aloc = st.number_input("Diária (R$)", min_value=0.0, step=1.0, key="inp_diaria_aloc")
    with cp_a2:
        val_gas_aloc = st.number_input("Gasolina/dia", min_value=0.0, step=1.0, key="inp_gas_aloc")
    with cp_a3:
        val_ped_aloc = st.number_input("Pedágio/dia", min_value=0.0, step=1.0, key="inp_ped_aloc")

    datas_marcadas_set = set(df_aloc["data_alocacao"].tolist()) if not df_aloc.empty else set()
    cal_matrix = calendar.monthcalendar(st.session_state.aloc_cal_ano, st.session_state.aloc_cal_mes)
    dias_hdr = ["Seg", "Ter", "Qua", "Qui", "Sex", "Sáb", "Dom"]
    hdr_html = '<div style="display:grid;grid-template-columns:repeat(7,1fr);gap:3px;margin:6px 0 4px 0;">'
    for dh in dias_hdr:
        hdr_html += f'<div style="text-align:center;font-size:0.64rem;font-weight:700;color:#64748b;">{dh}</div>'
    hdr_html += '</div>'
    st.markdown(hdr_html, unsafe_allow_html=True)

    for sem_idx, semana in enumerate(cal_matrix):
        cols_w = st.columns(7)
        for d_idx, dia_num in enumerate(semana):
            if dia_num == 0:
                cols_w[d_idx].markdown("<div style='height:36px;background:rgba(13,21,34,0.4);border-radius:8px;'></div>", unsafe_allow_html=True)
            else:
                dt_cell = date(st.session_state.aloc_cal_ano, st.session_state.aloc_cal_mes, dia_num)
                dt_cell_str = dt_cell.strftime("%Y-%m-%d")
                is_marked = (dt_cell_str in datas_marcadas_set)
                lbl_btn = f"🚗{dia_num}" if is_marked else f"{dia_num}"
                if cols_w[d_idx].button(
                    lbl_btn,
                    key=f"cal_aloc_btn_{dt_cell_str}",
                    type="primary" if is_marked else "secondary",
                    help=f"{'Remover' if is_marked else 'Marcar'} alocação em {dt_cell.strftime('%d/%m/%Y')}"
                ):
                    toggle_alocacao_dia(dt_cell_str, "Alocação Cliente", val_diaria_aloc, val_gas_aloc, val_ped_aloc)
                    st.rerun()

    dt_m_ini = date(st.session_state.aloc_cal_ano, st.session_state.aloc_cal_mes, 1)
    last_day_m = calendar.monthrange(st.session_state.aloc_cal_ano, st.session_state.aloc_cal_mes)[1]
    dt_m_fim = date(st.session_state.aloc_cal_ano, st.session_state.aloc_cal_mes, last_day_m)

    ca_act1, ca_act2 = st.columns(2)
    with ca_act1:
        if st.button("⚡ Marcar Dias Úteis (Seg-Sex)", key="btn_marcar_uteis_aloc"):
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
    <div style="background:#0d1522;border:1px solid #1f2f47;border-radius:12px;padding:10px;margin-top:8px;">
        <div style="font-size:0.70rem;font-weight:800;color:#38bdf8;text-transform:uppercase;">
            📊 Resumo {nome_m_aloc} ({qtd_dias_aloc} dia(s) marcado(s)):
        </div>
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:6px;margin-top:8px;font-size:0.68rem;">
            <div style="background:#111a28;padding:6px 8px;border-radius:8px;">
                <span style="color:#94a3b8;">⛽ Gasolina:</span><br>
                <strong style="color:#f87171;font-family:'JetBrains Mono';font-size:0.82rem;">R$ {tot_gas_mes:,.2f}</strong>
            </div>
            <div style="background:#111a28;padding:6px 8px;border-radius:8px;">
                <span style="color:#94a3b8;">🛣️ Pedágios:</span><br>
                <strong style="color:#fbbf24;font-family:'JetBrains Mono';font-size:0.82rem;">R$ {tot_ped_mes:,.2f}</strong>
            </div>
            <div style="background:#111a28;padding:6px 8px;border-radius:8px;">
                <span style="color:#94a3b8;">💰 Lucro Líquido:</span><br>
                <strong style="color:#4ade80;font-family:'JetBrains Mono';font-size:0.82rem;">R$ {tot_lucro_liq_aloc:,.2f}</strong>
            </div>
            <div style="background:#111a28;padding:6px 8px;border-radius:8px;">
                <span style="color:#94a3b8;">📥 Reembolso Total:</span><br>
                <strong style="color:#38bdf8;font-family:'JetBrains Mono';font-size:0.82rem;">R$ {tot_reembolso_esperado:,.2f}</strong>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Botão 1-Clique para jogar os valores calculados direto no Rateio de Reembolso!
    if qtd_dias_aloc > 0:
        if st.button(f"🚀 Pré-preencher Rateio de Reembolso (R$ {tot_reembolso_esperado:,.2f})", key="btn_enviar_aloc_rateio"):
            st.session_state["reemb_total_val"] = round(tot_reembolso_esperado, 2)
            st.session_state["qtd_destinos"] = 3
            st.session_state["v_A"] = round(tot_ped_mes, 2)
            st.session_state["v_B"] = round(tot_gas_mes, 2)
            st.session_state["v_C"] = round(max(0.0, tot_reembolso_esperado - tot_ped_mes - tot_gas_mes), 2)
            st.session_state.mostrar_form_rateio = True
            st.session_state.menu_nav = "⛽ Reembolsos & KM"
            st.rerun()

    # Calculadora Rápida vinculada automaticamente aos valores do Calendário
    ref_diaria_cal = float(st.session_state.get("inp_diaria_aloc", 128.78))
    ref_gas_cal = float(st.session_state.get("inp_gas_aloc", 30.00))
    ref_ped_cal = float(st.session_state.get("inp_ped_aloc", 25.60))
    dias_default_calc = qtd_dias_aloc if qtd_dias_aloc > 0 else 5

    btn_calc_lbl = (
        "➖ Ocultar Calculadora Rápida"
        if st.session_state.mostrar_calc_km
        else f"🧮 Calculadora Rápida (R$ {ref_diaria_cal:,.2f}/dia + R$ {ref_ped_cal:,.2f} Pedágio)"
    )
    if st.button(btn_calc_lbl, key="toggle_calc_km"):
        st.session_state.mostrar_calc_km = not st.session_state.mostrar_calc_km
        st.rerun()

    if st.session_state.mostrar_calc_km:
        st.markdown('<div style="background:#0d1522;border:1px solid #1c2a3d;border-radius:12px;padding:10px;margin-top:6px;">', unsafe_allow_html=True)
        c_c1, c_c2 = st.columns(2)
        with c_c1:
            dias_est = st.number_input("Dias de alocação", min_value=1, value=dias_default_calc, step=1, key="calc_dias_est")
            diaria_bruta_unit = st.number_input("Diária (R$)", min_value=0.0, value=ref_diaria_cal, step=1.0, key=f"calc_diaria_{ref_diaria_cal:.2f}")
            gasolina_unit = st.number_input("Gasolina/dia (R$)", min_value=0.0, value=ref_gas_cal, step=1.0, key=f"calc_gas_{ref_gas_cal:.2f}")
            pedagio_dia = st.number_input("Pedágio/dia (R$)", min_value=0.0, value=ref_ped_cal, step=1.0, key=f"calc_ped_{ref_ped_cal:.2f}")
        with c_c2:
            lucro_unit = diaria_bruta_unit - gasolina_unit
            gasolina_est = dias_est * gasolina_unit
            diarias_lucro = dias_est * lucro_unit
            pedagio_total_est = dias_est * pedagio_dia
            total_est = (dias_est * diaria_bruta_unit) + pedagio_total_est
            st.caption(f"⛽ Gasolina: **R$ {gasolina_est:,.2f}**")
            st.caption(f"💰 Lucro Livre: **R$ {diarias_lucro:,.2f}**")
            st.caption(f"🛣️ Pedágios: **R$ {pedagio_total_est:,.2f}**")
            st.markdown(f"**Total Esperado:** <span style='color:#4ade80;font-weight:800;'>R$ {total_est:,.2f}</span>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ================= HELPER DO IA ADVISOR =================
def render_advisor_box():
    st.markdown('<div class="bento-box">', unsafe_allow_html=True)
    st.markdown('<div class="bento-title"><span>🧠 Insights do IA Advisor</span><span style="font-size:0.68rem;color:#38bdf8;">Análise Inteligente</span></div>', unsafe_allow_html=True)

    total_parcelas_mes = float(df_parc["valor_parcela"].sum()) if not df_parc.empty else 0.0
    total_divida_parcelas = sum(max(0, int(r["total_parcelas"]) - int(r["parcela_atual"])) * float(r["valor_parcela"]) for _, r in df_parc.iterrows()) if not df_parc.empty else 0.0

    # Projeção 6 meses
    projecoes_6m = []
    for offset_m in range(6):
        dt_ref_m = date(st.session_state.cal_ano, st.session_state.cal_mes, 1) + relativedelta(months=offset_m)
        label_m = f"{meses_nomes_glob[dt_ref_m.month - 1][:3]}/{str(dt_ref_m.year)[2:]}"
        parc_ativas_m = 0.0
        if not df_parc.empty:
            for _, rp in df_parc.iterrows():
                if (int(rp["parcela_atual"]) + offset_m) <= int(rp["total_parcelas"]):
                    parc_ativas_m += float(rp["valor_parcela"])
        alivio = max(0.0, total_parcelas_mes - parc_ativas_m)
        sobra_m = renda_futura_livre + alivio
        projecoes_6m.append({"mes": label_m, "parcelas": parc_ativas_m, "sobra": sobra_m})

    cols_6m_html = "".join(
        f'<div style="background:#0d1522;border:1px solid #1e2d44;border-radius:8px;padding:6px 3px;text-align:center;">'
        f'<div style="font-size:0.60rem;color:#94a3b8;font-weight:700;">{p6["mes"]}</div>'
        f'<div style="font-family:JetBrains Mono,monospace;font-size:0.68rem;font-weight:800;color:{"#4ade80" if p6["sobra"] >= 0 else "#f87171"};margin-top:2px;">{"+" if p6["sobra"] >= 0 else ""}{p6["sobra"]:,.0f}</div>'
        f'<div style="font-size:0.52rem;color:#64748b;">Parc:{p6["parcelas"]:,.0f}</div>'
        f'</div>'
        for p6 in projecoes_6m
    )
    st.markdown(
        f'<div style="background:linear-gradient(145deg,#132136 0%,#0d1624 100%);border:1px solid #2b456b;border-radius:12px;padding:10px;margin-bottom:10px;">'
        f'<div style="font-size:0.68rem;font-weight:800;color:#38bdf8;text-transform:uppercase;">📈 Projeção de Virada (6 Meses)</div>'
        f'<div style="display:grid;grid-template-columns:repeat(6,1fr);gap:4px;margin-top:8px;">{cols_6m_html}</div>'
        f'</div>',
        unsafe_allow_html=True
    )

    # Orientação Gasolina & Pedágio com base no Calendário de Alocações
    custo_op_aloc = tot_gas_glob + tot_ped_glob
    contas_com_saldo = df_bancos[df_bancos["saldo_conta"] > 0].sort_values(by="saldo_conta", ascending=False)
    melhor_conta = contas_com_saldo.iloc[0] if not contas_com_saldo.empty else None
    cartoes_disp = df_bancos[df_bancos["tem_cartao"] == 1].copy()
    melhor_cartao = None
    if not cartoes_disp.empty:
        cartoes_disp["lim_real"] = cartoes_disp.apply(lambda r: float(r["limite_liberado"]) if float(r["limite_liberado"]) > 0 else max(0.0, float(r["limite_cartao"]) - float(r["fatura_atual"])), axis=1)
        validos = cartoes_disp[cartoes_disp["lim_real"] >= 50.0].sort_values(by="lim_real", ascending=False)
        if not validos.empty:
            melhor_cartao = validos.iloc[0]

    with st.expander("⛽ Plano Mensal de Gasolina & Pedágio (Alocações)", expanded=False):
        if qtd_dias_aloc_glob == 0:
            st.info("Marque seus dias de alocação no Calendário para o Advisor calcular o plano exato do mês.")
        else:
            st.markdown(
                f"• **Dias marcados em {nome_mes_glob}:** {qtd_dias_aloc_glob} dia(s)<br>"
                f"• **Gasolina:** R$ {tot_gas_glob:,.2f} • **Pedágio:** R$ {tot_ped_glob:,.2f} • **Lucro Livre:** R$ {tot_lucro_glob:,.2f}<br>"
                f"• **Conta sugerida p/ Gasolina:** {melhor_conta['banco'] if melhor_conta is not None else 'Sem saldo em conta'}<br>"
                f"• **Cartão sugerido p/ Pedágio:** {melhor_cartao['banco'] if melhor_cartao is not None else 'Sem limite livre'}",
                unsafe_allow_html=True
            )

    with st.expander("🔍 Diagnóstico de Ralos & Caminho de Ajuste", expanded=False):
        if total_cheque > 0:
            st.warning(f"Prioridade #1: Zerar R$ {total_cheque:,.2f} de Cheque Especial (custo estimado de R$ {total_cheque*0.08:,.2f}/mês em juros).")
        else:
            st.success("Cheque Especial zerado! Nenhum juro rotativo ativo.")
        if total_parcelas_mes > 0:
            st.info(f"Parcelas ativas somam R$ {total_parcelas_mes:,.2f}/mês (saldo devedor total: R$ {total_divida_parcelas:,.2f}).")

    st.markdown('</div>', unsafe_allow_html=True)

# ================= PÁGINAS DO DASHBOARD =================
if st.session_state.menu_nav == "📊 Dashboard":
    # No PC: 2 colunas principais (Esquerda: Calendário de Alocação | Direita: Fluxo/Gráfico + Advisor)
    # No Celular: Streamlit empilha automaticamente em 1 coluna responsiva!
    col_main_left, col_main_right = st.columns([1.15, 1.0], gap="medium")

    with col_main_left:
        render_calendario_alocacoes_e_calc()

    with col_main_right:
        # Gráfico de Fluxo & Comparativo por Banco
        st.markdown('<div class="bento-box">', unsafe_allow_html=True)
        st.markdown('<div class="bento-title"><span>📈 Fluxo de Caixa & Bancos</span><span style="font-size:0.68rem;color:#94a3b8;">Visão Comparativa</span></div>', unsafe_allow_html=True)
        chart_df = pd.DataFrame({
            "Banco": df_bancos["banco"],
            "Saldo Conta": df_bancos["saldo_conta"],
            "Fatura Cartão": df_bancos["fatura_atual"]
        }).set_index("Banco")
        st.bar_chart(chart_df, height=210, color=["#22c55e", "#f43f5e"])
        st.markdown('</div>', unsafe_allow_html=True)

        # IA Advisor compacto/recolhível
        render_advisor_box()

    # Linha inferior: Transações Recentes (recolhível)
    st.markdown('<div class="bento-box">', unsafe_allow_html=True)
    ct1, ct2 = st.columns([4, 1.5])
    with ct1:
        st.markdown(f'<div class="bento-title" style="margin-bottom:0;"><span>🧾 Transações Recentes ({len(df_tx)})</span></div>', unsafe_allow_html=True)
    with ct2:
        lbl_rec_dash = "👁️ Mostrar" if st.session_state.recolher_extrato_lista else "🔼 Recolher"
        if st.button(lbl_rec_dash, key="btn_rec_dash_tx"):
            st.session_state.recolher_extrato_lista = not st.session_state.recolher_extrato_lista
            st.rerun()

    if st.session_state.recolher_extrato_lista:
        st.caption(f"Lista recolhida ({len(df_tx)} lançamento(s)). Clique em **👁️ Mostrar** para ver.")
    elif df_tx.empty:
        st.info("Nenhuma transação registrada ainda.")
    else:
        for _, row in df_tx.head(6).iterrows():
            is_s = row["tipo"] == "Saída"
            st.markdown(f"""
            <div class="prev-item-card">
                <div>
                    <div style="font-size:0.80rem;font-weight:700;color:#ffffff;">{row['descricao']}</div>
                    <div style="font-size:0.64rem;color:#94a3b8;">{row['data']} • {row['banco']} • {row['categoria']}</div>
                </div>
                <div style="font-family:'JetBrains Mono';font-weight:800;font-size:0.86rem;color:{'#f87171' if is_s else '#4ade80'};">
                    {'-' if is_s else '+'} R$ {row['valor']:,.2f}
                </div>
            </div>
            """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.menu_nav == "🗓️ Calendário de Alocação":
    render_calendario_alocacoes_e_calc()

elif st.session_state.menu_nav == "🏦 Bancos & Contas":
    cols_b = st.columns(2, gap="medium")
    for idx_b, (_, b) in enumerate(df_bancos.iterrows()):
        with cols_b[idx_b % 2]:
            b_saldo = float(b["saldo_conta"])
            msg_b, cls_b = get_status_saldo(b_saldo)
            tem_c = (b.get("tem_cartao", 1) == 1)
            st.markdown('<div class="bank-card">', unsafe_allow_html=True)
            st.markdown(f"""
            <div class="bank-card-top">
                <span class="bank-badge"><span class="bank-dot" style="background:{b['cor_identificador']};"></span>{b['banco']}</span>
                <span class="md-msg-pill {cls_b}">{msg_b}</span>
            </div>
            """, unsafe_allow_html=True)
            if tem_c:
                lim_tot = float(b.get("limite_cartao", 0.0))
                lim_lib = float(b.get("limite_liberado", 0.0))
                lim_exib = lim_lib if lim_lib > 0 else max(0.0, lim_tot - float(b["fatura_atual"]))
                st.markdown(f"""
                <div class="bank-grid">
                    <div class="bank-stat"><div class="bank-stat-lbl">Saldo Conta</div><div class="bank-stat-val">R$ {b_saldo:,.2f}</div></div>
                    <div class="bank-stat"><div class="bank-stat-lbl">Fatura Atual (Dia {int(b.get('dia_vencimento',10))})</div><div class="bank-stat-val" style="color:#38bdf8;">R$ {b['fatura_atual']:,.2f}</div></div>
                    <div class="bank-stat"><div class="bank-stat-lbl">Limite Liberado</div><div class="bank-stat-val" style="color:#4ade80;">R$ {lim_exib:,.2f}</div></div>
                    <div class="bank-stat"><div class="bank-stat-lbl">Cheque Especial</div><div class="bank-stat-val" style="color:{'#f87171' if b['cheque_especial_usado']>0 else '#94a3b8'};">R$ {b['cheque_especial_usado']:,.2f}</div></div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="bank-grid">
                    <div class="bank-stat"><div class="bank-stat-lbl">Saldo Conta</div><div class="bank-stat-val">R$ {b_saldo:,.2f}</div></div>
                    <div class="bank-stat"><div class="bank-stat-lbl">Cheque Especial</div><div class="bank-stat-val" style="color:{'#f87171' if b['cheque_especial_usado']>0 else '#94a3b8'};">R$ {b['cheque_especial_usado']:,.2f}</div></div>
                </div>
                """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.menu_nav == "⛽ Reembolsos & KM":
    st.markdown('<div class="bento-box">', unsafe_allow_html=True)
    btn_rat = "➖ Ocultar Formulário de Rateio" if st.session_state.mostrar_form_rateio else "🎯 Lançar / Destinar Reembolso (Rateio)"
    if st.button(btn_rat, key="toggle_rat_page"):
        st.session_state.mostrar_form_rateio = not st.session_state.mostrar_form_rateio
        st.rerun()

    if st.session_state.mostrar_form_rateio:
        if "qtd_destinos" not in st.session_state:
            st.session_state.qtd_destinos = 2
        if "reemb_total_val" not in st.session_state:
            st.session_state["reemb_total_val"] = 617.00
        if "v_A" not in st.session_state:
            st.session_state["v_A"] = 150.00
        if "v_B" not in st.session_state:
            st.session_state["v_B"] = round(max(0.0, st.session_state["reemb_total_val"] - st.session_state["v_A"]), 2)
        for l_i in ["C", "D", "E"]:
            if f"v_{l_i}" not in st.session_state:
                st.session_state[f"v_{l_i}"] = 0.0

        def recalc_dest():
            qtd = st.session_state.get("qtd_destinos", 2)
            tot = float(st.session_state.get("reemb_total_val", 0.0))
            lets = ["A", "B", "C", "D", "E"]
            if qtd == 1:
                st.session_state["v_A"] = round(tot, 2)
            else:
                s_ant = sum(float(st.session_state.get(f"v_{lets[i]}", 0.0)) for i in range(qtd - 1))
                st.session_state[f"v_{lets[qtd-1]}"] = round(max(0.0, tot - s_ant), 2)

        c_q1, c_q2 = st.columns(2)
        with c_q1:
            data_receb = st.date_input("Data Recebimento", value=date.today(), key="reemb_dt_pg")
        with c_q2:
            val_tot_r = st.number_input("Valor Total (R$)", min_value=0.01, step=10.0, key="reemb_total_val", on_change=recalc_dest)

        qtd_esc = st.selectbox("Quantos destinos ratear?", [1, 2, 3, 4, 5], index=[1, 2, 3, 4, 5].index(st.session_state.qtd_destinos))
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
            c1, c2, c3 = st.columns([1.3, 1, 1.5])
            with c1:
                bd = st.selectbox(f"Banco ({lt})", b_list, index=min(i, len(b_list)-1), key=f"b_{lt}")
            with c2:
                vd = st.number_input(f"Valor ({lt})", min_value=0.0, step=10.0, key=f"v_{lt}", on_change=(recalc_dest if not is_ult else None))
            with c3:
                ad = st.selectbox(f"Ação ({lt})", ["Pagar/Abater Fatura de Cartão", "Abater Cheque Especial", "Creditar em Conta Corrente"], index=min(i, 2), key=f"ac_{lt}")
            md = st.text_input(f"Motivo ({lt})", value=mots[i], key=f"m_{lt}")
            dests.append({"banco": bd, "acao": ad, "valor": vd, "motivo": md})

        if st.button("🚀 Confirmar Rateio de Reembolso", type="primary"):
            ativos = [d for d in dests if d["valor"] > 0]
            if ativos:
                aplicar_destinacao_reembolso(data_receb.strftime("%Y-%m-%d"), val_tot_r, ativos, efetivar_agora=(data_receb <= date.today()))
                st.session_state.mostrar_form_rateio = False
                st.success("Reembolso registrado!")
                st.rerun()

    # Lista recolhível de destinações ativas
    df_itens_hist = get_reembolsos_itens()
    if not df_itens_hist.empty:
        cda1, cda2 = st.columns([4, 1.5])
        with cda1:
            st.markdown(f'<div class="bento-title" style="margin-top:10px;"><span>Destinações Ativas ({len(df_itens_hist)})</span></div>', unsafe_allow_html=True)
        with cda2:
            if st.button("👁️ Mostrar" if st.session_state.recolher_dest_reemb else "🔼 Recolher", key="rec_da_pg"):
                st.session_state.recolher_dest_reemb = not st.session_state.recolher_dest_reemb
                st.rerun()
        if not st.session_state.recolher_dest_reemb:
            for _, item in df_itens_hist.iterrows():
                ci, cb = st.columns([4.5, 1])
                with ci:
                    st.markdown(f'<div class="prev-item-card"><div><strong>{item["banco"]}</strong> • {item["motivo"]}<br><span style="font-size:0.65rem;color:#94a3b8;">{item["data"]} • {item["acao"]}</span></div><div style="font-family:JetBrains Mono;font-weight:800;color:#4ade80;">R$ {item["valor"]:,.2f}</div></div>', unsafe_allow_html=True)
                with cb:
                    if st.button("↩️", key=f"est_pg_{item['id']}"):
                        estornar_item_destino(item["id"])
                        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.menu_nav == "📅 Ciclo & Previsões":
    st.markdown('<div class="bento-box">', unsafe_allow_html=True)
    st.markdown(f'<div class="bento-title"><span>📅 Ciclo {nome_mes_glob}/{st.session_state.cal_ano} ({dt_hero_ini.strftime("%d/%m")} a {dt_hero_fim.strftime("%d/%m")})</span></div>', unsafe_allow_html=True)
    cn1, cn2, cn3 = st.columns([3, 1, 1])
    with cn2:
        if st.button("◀", key="cic_ant_pg"):
            st.session_state.cal_mes = 12 if st.session_state.cal_mes == 1 else st.session_state.cal_mes - 1
            if st.session_state.cal_mes == 12: st.session_state.cal_ano -= 1
            st.rerun()
    with cn3:
        if st.button("▶", key="cic_prox_pg"):
            st.session_state.cal_mes = 1 if st.session_state.cal_mes == 12 else st.session_state.cal_mes + 1
            if st.session_state.cal_mes == 1: st.session_state.cal_ano += 1
            st.rerun()

    df_prev_c = pd.DataFrame()
    if not df_prev.empty:
        df_prev_c = df_prev[df_prev["data_prevista"].apply(lambda d: dt_hero_ini <= datetime.strptime(d, "%Y-%m-%d").date() <= dt_hero_fim)]

    clc1, clc2 = st.columns([4, 1.5])
    with clc1:
        st.markdown(f"**Lançamentos do Ciclo ({len(df_prev_c)})**")
    with clc2:
        if st.button("👁️ Mostrar" if st.session_state.recolher_lanc_ciclo else "🔼 Recolher", key="rec_lc_pg"):
            st.session_state.recolher_lanc_ciclo = not st.session_state.recolher_lanc_ciclo
            st.rerun()

    if not st.session_state.recolher_lanc_ciclo:
        for _, rp in df_prev_c.iterrows():
            is_e = rp["tipo"] == "Entrada"
            c1, c2, c3 = st.columns([4, 1, 1])
            with c1:
                st.markdown(f'<div class="prev-item-card"><div><strong>{rp["descricao"]}</strong><br><span style="font-size:0.65rem;color:#94a3b8;">{rp["data_prevista"]} • {rp["banco"]}</span></div><div style="font-family:JetBrains Mono;font-weight:800;color:{"#4ade80" if is_e else "#f87171"};">{"+" if is_e else "-"} R$ {rp["valor"]:,.2f}</div></div>', unsafe_allow_html=True)
            with c2:
                if st.button("✅", key=f"ef_pg_{rp['id']}"):
                    efetivar_previsto(rp["id"])
                    st.rerun()
            with c3:
                if st.button("🗑️", key=f"dl_pg_{rp['id']}"):
                    remover_previsto(rp["id"])
                    st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.menu_nav == "💳 Cartões & Parcelas":
    st.markdown('<div class="bento-box">', unsafe_allow_html=True)
    cpl1, cpl2 = st.columns([4, 1.5])
    with cpl1:
        st.markdown(f'<div class="bento-title"><span>💳 Compras Parceladas ({len(df_parc)})</span></div>', unsafe_allow_html=True)
    with cpl2:
        if st.button("👁️ Mostrar" if st.session_state.recolher_parc_lista else "🔼 Recolher", key="rec_pl_pg"):
            st.session_state.recolher_parc_lista = not st.session_state.recolher_parc_lista
            st.rerun()

    if st.session_state.recolher_parc_lista:
        st.caption(f"Lista recolhida ({len(df_parc)} compra(s)). Clique em **👁️ Mostrar** para ver.")
    else:
        for _, rpc in df_parc.iterrows():
            pct = min(100.0, (rpc["parcela_atual"] / max(1, rpc["total_parcelas"])) * 100)
            st.markdown(f"""
            <div class="parcela-card">
                <div style="display:flex;justify-content:space-between;">
                    <strong>{rpc['descricao']} ({rpc['banco']})</strong>
                    <span style="color:#38bdf8;font-family:'JetBrains Mono';font-weight:800;">R$ {rpc['valor_parcela']:,.2f}/mês</span>
                </div>
                <div class="parcela-progresso"><div class="parcela-progresso-bar" style="width:{pct:.0f}%;"></div></div>
                <div style="font-size:0.68rem;color:#94a3b8;">Parcela {rpc['parcela_atual']}/{rpc['total_parcelas']} • Término: {rpc['mes_ano_fim']}</div>
            </div>
            """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.menu_nav == "📄 Extrato & Lançar":
    st.markdown('<div class="bento-box">', unsafe_allow_html=True)
    st.markdown(f'<div class="bento-title"><span>📄 Extrato Completo ({len(df_tx)})</span></div>', unsafe_allow_html=True)
    if st.button("👁️ Mostrar Extrato" if st.session_state.recolher_extrato_lista else "🔼 Recolher Extrato", key="rec_ext_pg"):
        st.session_state.recolher_extrato_lista = not st.session_state.recolher_extrato_lista
        st.rerun()
    if not st.session_state.recolher_extrato_lista:
        for _, row in df_tx.iterrows():
            is_s = row["tipo"] == "Saída"
            st.markdown(f'<div class="prev-item-card"><div><strong>{row["descricao"]}</strong><br><span style="font-size:0.64rem;color:#94a3b8;">{row["data"]} • {row["banco"]} ({row["meio"]})</span></div><div style="font-family:JetBrains Mono;font-weight:800;color:{"#f87171" if is_s else "#4ade80"};">{"-" if is_s else "+"} R$ {row["valor"]:,.2f}</div></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.menu_nav == "⚙️ Ajustes & Backup":
    st.markdown('<div class="bento-box">', unsafe_allow_html=True)
    st.markdown('<div class="bento-title"><span>⚙️ Backup & Segurança</span></div>', unsafe_allow_html=True)
    if os.path.exists("financas.db"):
        with open("financas.db", "rb") as f_db:
            st.download_button("📥 Baixar Backup (.db)", data=f_db.read(), file_name=f"backup_financas_{datetime.now().strftime('%Y_%m_%d')}.db", mime="application/octet-stream")
    st.markdown('</div>', unsafe_allow_html=True)
