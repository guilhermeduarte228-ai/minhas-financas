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

st.set_page_config(page_title="Minhas Finanças", page_icon="⚡", layout="centered")

# Estilo Moderno Dark Bento UI / MacroDroid
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;600;700&display=swap');

    html, body, .stApp {
        background-color: #0b0f17 !important;
        color: #f1f5f9;
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    .block-container { 
        max-width: 440px !important; 
        padding-top: 1rem !important; 
        padding-bottom: 3.5rem !important;
    }

    #MainMenu, footer, header { visibility: hidden; }

    /* Barra Superior */
    .md-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 1.2rem;
        padding: 4px 2px;
    }
    .md-title-box h2 {
        font-size: 1.25rem;
        font-weight: 800;
        color: #ffffff;
        margin: 0;
        letter-spacing: -0.4px;
    }
    .md-title-box span {
        font-size: 0.72rem;
        color: #94a3b8;
        font-weight: 500;
    }
    .md-status-badge {
        display: flex;
        align-items: center;
        gap: 6px;
        background: #162032;
        color: #38bdf8;
        border: 1px solid #223249;
        padding: 5px 12px;
        border-radius: 9999px;
        font-size: 0.7rem;
        font-weight: 700;
    }
    .md-dot-active {
        width: 8px;
        height: 8px;
        background-color: #22c55e;
        border-radius: 50%;
        box-shadow: 0 0 8px rgba(34, 197, 94, 0.6);
    }

    /* Card Master */
    .md-hero-card {
        background: linear-gradient(145deg, #182335 0%, #101826 100%);
        border: 1px solid #24354f;
        border-radius: 22px;
        padding: 1.3rem;
        margin-bottom: 1.2rem;
        box-shadow: 0 12px 28px -6px rgba(0, 0, 0, 0.4);
    }
    .md-hero-label {
        font-size: 0.68rem;
        font-weight: 700;
        color: #94a3b8;
        text-transform: uppercase;
        letter-spacing: 0.8px;
    }
    .md-hero-val {
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 2.1rem;
        font-weight: 800;
        color: #ffffff;
        margin: 6px 0 10px 0;
        letter-spacing: -1px;
    }
    .md-msg-pill {
        display: inline-block;
        padding: 4px 10px;
        border-radius: 8px;
        font-size: 0.72rem;
        font-weight: 700;
        margin-bottom: 10px;
    }
    .msg-danger { background: rgba(239, 68, 68, 0.15); color: #f87171; border: 1px solid rgba(239, 68, 68, 0.3); }
    .msg-warning { background: rgba(245, 158, 11, 0.15); color: #fbbf24; border: 1px solid rgba(245, 158, 11, 0.3); }
    .msg-success { background: rgba(34, 197, 94, 0.15); color: #4ade80; border: 1px solid rgba(34, 197, 94, 0.3); }
    .msg-neutral { background: rgba(148, 163, 184, 0.15); color: #cbd5e1; border: 1px solid rgba(148, 163, 184, 0.3); }

    .md-hero-footer {
        display: flex;
        justify-content: space-between;
        padding-top: 10px;
        border-top: 1px solid #202e44;
        font-size: 0.75rem;
        color: #94a3b8;
    }

    /* Botões de Recursos Rápidos */
    .recursos-box {
        margin-bottom: 1.2rem;
    }
    .recursos-box button {
        background: #141d2a !important;
        border: 1px solid #223247 !important;
        border-radius: 14px !important;
        color: #f1f5f9 !important;
        font-size: 0.74rem !important;
        font-weight: 700 !important;
        padding: 0.55rem 0.2rem !important;
        min-height: 48px !important;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2) !important;
        transition: all 0.2s ease !important;
        width: 100% !important;
    }
    .recursos-box button:hover {
        border-color: #38bdf8 !important;
        color: #38bdf8 !important;
        transform: translateY(-1px) !important;
    }

    /* Bancos / Cards */
    .sec-header {
        font-size: 0.75rem;
        font-weight: 800;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        margin: 1.2rem 0 0.8rem 0;
    }
    .bank-card {
        background: #121a28;
        border: 1px solid #1f2d42;
        border-radius: 18px;
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
        font-size: 0.88rem;
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
    .bank-grid-single {
        display: grid;
        grid-template-columns: 1fr;
        gap: 8px;
    }
    .bank-stat {
        background: #0c121c;
        border: 1px solid #182436;
        border-radius: 12px;
        padding: 10px;
    }
    .bank-stat-full {
        grid-column: span 2;
        background: #0c121c;
        border: 1px solid #182436;
        border-radius: 12px;
        padding: 10px;
    }
    .bank-stat-lbl {
        font-size: 0.62rem;
        color: #64748b;
        font-weight: 700;
        text-transform: uppercase;
    }
    .bank-stat-val {
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 0.95rem;
        font-weight: 700;
        color: #ffffff;
        margin-top: 3px;
    }

    /* Painel Expansível */
    .panel-box {
        background: #141e2e;
        border: 1px solid #23354f;
        border-radius: 18px;
        padding: 16px;
        margin-top: 0.8rem;
        margin-bottom: 1.4rem;
    }

    /* Card Item de Previsão / Parcela */
    .prev-item-card {
        background: #0d1522;
        border: 1px solid #1a273b;
        border-radius: 12px;
        padding: 10px 12px;
        margin-bottom: 8px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    .parcela-card {
        background: #111a28;
        border: 1px solid #1e2c40;
        border-radius: 14px;
        padding: 12px;
        margin-bottom: 10px;
    }
    .parcela-top {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 6px;
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

    /* Botão de Limpar / Danger */
    .btn-clear button {
        background: rgba(239, 68, 68, 0.12) !important;
        color: #f87171 !important;
        border: 1px solid rgba(239, 68, 68, 0.35) !important;
        border-radius: 10px !important;
        font-size: 0.7rem !important;
        font-weight: 700 !important;
        padding: 0.35rem 0.6rem !important;
    }
    .btn-clear button:hover {
        background: rgba(239, 68, 68, 0.25) !important;
        border-color: #f87171 !important;
    }

    /* Botão de Ação / Ícone */
    .btn-action-icon button {
        background: rgba(56, 189, 248, 0.12) !important;
        color: #38bdf8 !important;
        border: 1px solid rgba(56, 189, 248, 0.35) !important;
        border-radius: 10px !important;
        font-size: 0.72rem !important;
        font-weight: 700 !important;
        padding: 0.35rem 0.5rem !important;
    }
    .btn-action-icon button:hover {
        background: rgba(56, 189, 248, 0.25) !important;
        border-color: #38bdf8 !important;
    }

    /* Abas */
    .stTabs [data-baseweb="tab-list"] {
        gap: 4px;
        background-color: #121a28;
        padding: 6px;
        border-radius: 16px;
        border: 1px solid #1f2d42;
    }
    .stTabs [data-baseweb="tab"] {
        height: 36px;
        border-radius: 10px;
        color: #94a3b8;
        font-size: 0.70rem;
        font-weight: 700;
        border: none !important;
        background: transparent;
        padding: 0 8px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #1f2d42 !important;
        color: #38bdf8 !important;
    }
    .stTabs [data-baseweb="tab-highlight"] { display: none; }

    form button {
        width: 100%;
        background: linear-gradient(135deg, #0284c7 0%, #0369a1 100%) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 14px !important;
        font-weight: 800 !important;
        font-size: 0.86rem !important;
        padding: 0.7rem 1rem !important;
    }

    /* Tabela do Calendário Visual */
    .cal-table {
        width: 100%;
        border-collapse: separate;
        border-spacing: 4px;
        margin-top: 8px;
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
        position: relative;
    }
    .cal-cell.payday {
        border-color: #eab308 !important;
        box-shadow: inset 0 0 6px rgba(234, 179, 8, 0.35);
    }
    .cal-cell.today {
        border-color: #38bdf8 !important;
        box-shadow: 0 0 6px rgba(56, 189, 248, 0.4);
    }
    .cal-cell.has-entrada {
        background: rgba(34, 197, 94, 0.16) !important;
        border-color: rgba(34, 197, 94, 0.65) !important;
    }
    .cal-cell.has-saida {
        background: rgba(239, 68, 68, 0.16) !important;
        border-color: rgba(239, 68, 68, 0.65) !important;
    }
    .cal-cell.has-reemb-livre {
        background: rgba(234, 179, 8, 0.16) !important;
        border-color: rgba(234, 179, 8, 0.75) !important;
    }
    .cal-cell.has-ambos {
        background: rgba(245, 158, 11, 0.16) !important;
        border-color: rgba(245, 158, 11, 0.65) !important;
    }
    .cal-badge {
        font-size: 0.54rem;
        font-weight: 800;
        font-family: 'JetBrains Mono', monospace;
        display: block;
        text-align: left;
        margin-top: 2px;
        border-radius: 3px;
        padding: 1px 2px;
        line-height: 1.1;
    }
    .badge-in { color: #4ade80; }
    .badge-out { color: #f87171; }
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

# Barra Superior
st.markdown("""
<div class="md-header">
    <div class="md-title-box">
        <h2>Painel Financeiro</h2>
        <span>Visão Integrada de Bancos</span>
    </div>
    <div class="md-status-badge">
        <span class="md-dot-active"></span>
        Sincronizado
    </div>
</div>
""", unsafe_allow_html=True)

# Calcula Renda Futura LÍQUIDA/LIVRE do Ciclo Ativo (04/MM a 03/MM+1)
# Desconta tudo o que já está comprometido (saídas previstas no ciclo + reembolsos futuros destinados a abater dívidas)
dt_hero_ini, dt_hero_fim, _ = get_intervalo_ciclo(st.session_state.cal_ano, st.session_state.cal_mes, "Ciclo Completo (04 a 03)")

entradas_futuras_brutas = 0.0
saidas_comprometidas_ciclo = 0.0

if not df_prev.empty:
    for _, r_p in df_prev.iterrows():
        try:
            d_p = datetime.strptime(r_p["data_prevista"], "%Y-%m-%d").date()
            if dt_hero_ini <= d_p <= dt_hero_fim:
                if r_p["tipo"] == "Entrada":
                    entradas_futuras_brutas += float(r_p["valor"])
                elif r_p["tipo"] == "Saída":
                    saidas_comprometidas_ciclo += float(r_p["valor"])
        except:
            pass

reembolsos_livres_futuros = 0.0
reembolsos_comprometidos_futuros = 0.0
if not df_reemb_itens.empty:
    for _, r_ri in df_reemb_itens.iterrows():
        if r_ri.get("status", "Efetivado") == "Previsto":
            try:
                d_r = datetime.strptime(r_ri["data"], "%Y-%m-%d").date()
                in_window = (dt_hero_ini <= d_r <= dt_hero_fim)
            except:
                in_window = True
            if in_window:
                if r_ri["acao"] == "Creditar em Conta Corrente":
                    reembolsos_livres_futuros += float(r_ri["valor"])
                else:
                    # Destinado a abater fatura de cartão ou cheque especial já comprometido
                    reembolsos_comprometidos_futuros += float(r_ri["valor"])

renda_futura_livre = (entradas_futuras_brutas - saidas_comprometidas_ciclo) + reembolsos_livres_futuros
projecao_com_futuro = total_saldos + renda_futura_livre

sinal_rf = "+" if renda_futura_livre >= 0 else "-"
cor_rf = "#4ade80" if renda_futura_livre >= 0 else "#f87171"
borda_rf = "rgba(56, 189, 248, 0.35)" if renda_futura_livre >= 0 else "rgba(248, 113, 113, 0.45)"
bg_rf = "rgba(56, 189, 248, 0.08)" if renda_futura_livre >= 0 else "rgba(239, 68, 68, 0.10)"

# Master Hero Card com Separação Clara: Patrimônio Real vs Renda Futura Livre (Descontado o Comprometido)
st.markdown(f"""
<div class="md-hero-card">
    <div style="display: grid; grid-template-columns: 1.15fr 1fr; gap: 10px; align-items: start;">
        <div>
            <div class="md-hero-label">Patrimônio Real em Conta</div>
            <div class="md-hero-val" style="font-size: 1.75rem; margin: 4px 0 8px 0;">R$ {total_saldos:,.2f}</div>
            <div class="md-msg-pill {classe_total}" style="margin-bottom: 0; font-size: 0.66rem;">{msg_total}</div>
        </div>
        <div style="background: {bg_rf}; border: 1px dashed {borda_rf}; border-radius: 14px; padding: 10px;">
            <div style="font-size: 0.60rem; font-weight: 800; color: #38bdf8; text-transform: uppercase; letter-spacing: 0.5px;">⏳ Renda Futura Livre</div>
            <div style="font-family: 'JetBrains Mono', monospace; font-size: 1.12rem; font-weight: 800; color: {cor_rf}; margin: 4px 0;">{sinal_rf} R$ {abs(renda_futura_livre):,.2f}</div>
            <div style="font-size: 0.58rem; color: #94a3b8; line-height: 1.25;">
                Bruto: R$ {(entradas_futuras_brutas + reembolsos_livres_futuros):,.2f} • Comprom.: -R$ {saidas_comprometidas_ciclo:,.2f}<br>
                Noção c/ futuro livre: <strong style="color: #e2e8f0;">R$ {projecao_com_futuro:,.2f}</strong>
            </div>
        </div>
    </div>
    <div class="md-hero-footer" style="margin-top: 12px;">
        <span>Faturas Cartão: <strong style="color: #ffffff;">R$ {total_faturas:,.2f}</strong></span>
        <span>Cheque Esp.: <strong style="color: #f87171;">R$ {total_cheque:,.2f}</strong></span>
    </div>
</div>
""", unsafe_allow_html=True)

# RECURSOS RÁPIDOS
st.markdown('<div class="sec-header">Recursos Rápidos</div>', unsafe_allow_html=True)
st.markdown('<div class="recursos-box">', unsafe_allow_html=True)
r_col1, r_col2 = st.columns(2)
with r_col1:
    if st.button("📅 Previsões & Calendário", key="btn_prev"):
        st.session_state.bloco_ativo = "previstos" if st.session_state.bloco_ativo != "previstos" else None
with r_col2:
    if st.button("⛽ Destinar Reembolso", key="btn_km"):
        st.session_state.bloco_ativo = "destinar_reembolso" if st.session_state.bloco_ativo != "destinar_reembolso" else None

r_col3, r_col4, r_col5 = st.columns(3)
with r_col3:
    if st.button("🧠 Advisor", key="btn_adv"):
        st.session_state.bloco_ativo = "advisor" if st.session_state.bloco_ativo != "advisor" else None
with r_col4:
    if st.button("💳 Vencimentos", key="btn_venc"):
        st.session_state.bloco_ativo = "vencimentos" if st.session_state.bloco_ativo != "vencimentos" else None
with r_col5:
    if st.button("📊 Gráficos", key="btn_graf"):
        st.session_state.bloco_ativo = "graficos" if st.session_state.bloco_ativo != "graficos" else None
st.markdown('</div>', unsafe_allow_html=True)

# ================= ÁREA DINÂMICA =================
if st.session_state.bloco_ativo == "previstos":
    st.markdown('<div class="panel-box">', unsafe_allow_html=True)
    
    c_tit, c_limp, c_fech = st.columns([3, 2, 1])
    with c_tit:
        st.markdown('<span style="font-weight: 800; color: #38bdf8; font-size: 0.92rem;">📅 Ciclo & Previsões</span>', unsafe_allow_html=True)
    with c_limp:
        st.markdown('<div class="btn-clear">', unsafe_allow_html=True)
        if st.button("🗑️ Limpar Todos", key="btn_limpar_prev", help="Apaga todas as previsões agendadas"):
            limpar_todas_previsoes()
            st.session_state.editando_id = None
            st.session_state.copiando_prev = None
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    with c_fech:
        if st.button("✕", key="fechar_prev", help="Recolher painel"):
            st.session_state.bloco_ativo = None
            st.rerun()

    # Seletor de Período do Ciclo (Competência do Mês: Dia 04 a Dia 03 do mês seguinte)
    opcoes_ciclo = ["Ciclo Completo (04 a 03)", "1ª Parte (Dia 04 a 15)", "2ª Parte (Dia 16 a 03)"]
    modo_sel = st.selectbox(
        "Período de Apuração:",
        opcoes_ciclo,
        index=opcoes_ciclo.index(st.session_state.modo_ciclo),
        key="sel_modo_ciclo_prev"
    )
    if modo_sel != st.session_state.modo_ciclo:
        st.session_state.modo_ciclo = modo_sel
        st.rerun()

    dt_ciclo_ini, dt_ciclo_fim, dt_salario_03 = get_intervalo_ciclo(st.session_state.cal_ano, st.session_state.cal_mes, st.session_state.modo_ciclo)
    dt_full_ini, dt_full_fim, _ = get_intervalo_ciclo(st.session_state.cal_ano, st.session_state.cal_mes, "Ciclo Completo (04 a 03)")

    meses_nomes = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]
    nome_mes_comp = meses_nomes[st.session_state.cal_mes - 1]

    st.markdown(f"""
    <div style="background: #101929; border: 1px solid #243652; border-radius: 10px; padding: 8px 10px; margin-bottom: 10px; font-size: 0.7rem; color: #cbd5e1;">
        📆 <strong>Competência {nome_mes_comp}/{st.session_state.cal_ano}:</strong> {dt_ciclo_ini.strftime('%d/%m/%Y')} até {dt_ciclo_fim.strftime('%d/%m/%Y')}
        <div style="font-size: 0.62rem; color: #eab308; margin-top: 2px;">💰 Adiantamento dia 16/{st.session_state.cal_mes:02d} • Salário de {nome_mes_comp} fecha em {dt_salario_03.strftime('%d/%m/%Y')}</div>
    </div>
    """, unsafe_allow_html=True)

    # Filtrar previsões e reembolsos estritamente dentro do ciclo (04/MM a 03/MM+1)
    df_prev_ciclo = pd.DataFrame()
    if not df_prev.empty:
        mask_p = []
        for _, r in df_prev.iterrows():
            try:
                d_obj = datetime.strptime(r["data_prevista"], "%Y-%m-%d").date()
                mask_p.append(dt_ciclo_ini <= d_obj <= dt_ciclo_fim)
            except:
                mask_p.append(False)
        df_prev_ciclo = df_prev[mask_p]

    df_reemb_ciclo = pd.DataFrame()
    if not df_reemb_itens.empty:
        mask_r = []
        for _, r in df_reemb_itens.iterrows():
            try:
                d_obj = datetime.strptime(r["data"], "%Y-%m-%d").date()
                mask_r.append(dt_ciclo_ini <= d_obj <= dt_ciclo_fim)
            except:
                mask_r.append(False)
        df_reemb_ciclo = df_reemb_itens[mask_r]

    entradas_prev_base = df_prev_ciclo[df_prev_ciclo["tipo"] == "Entrada"]["valor"].sum() if not df_prev_ciclo.empty else 0.0
    saidas_prev_base = df_prev_ciclo[df_prev_ciclo["tipo"] == "Saída"]["valor"].sum() if not df_prev_ciclo.empty else 0.0

    reemb_total_ciclo = 0.0
    reemb_livre_ciclo = 0.0
    reemb_comprometido_ciclo = 0.0
    if not df_reemb_ciclo.empty:
        for _, rr_c in df_reemb_ciclo.iterrows():
            v_rr = float(rr_c["valor"])
            reemb_total_ciclo += v_rr
            if rr_c["acao"] == "Creditar em Conta Corrente":
                reemb_livre_ciclo += v_rr
            else:
                reemb_comprometido_ciclo += v_rr

    # Tudo que entra de fato entra (Salários + Total de Reembolsos)
    entradas_previstas = entradas_prev_base + reemb_total_ciclo
    # E o que já sai destinado entra nas saídas/destinados (Contas a pagar + Reembolsos destinados a cartão/cheque)
    saidas_previstas = saidas_prev_base + reemb_comprometido_ciclo
    saldo_projetado = total_saldos + entradas_previstas - saidas_previstas

    # PAINEL DE SALDO PREVISTO A RECEBER E COMPARATIVO DO CICLO
    st.markdown(f"""
    <div style="background: #0d1522; border: 1px solid #1f2f47; border-radius: 14px; padding: 12px; margin: 6px 0 14px 0;">
        <div style="font-size: 0.68rem; font-weight: 700; color: #94a3b8; text-transform: uppercase;">Balanço {nome_mes_comp} ({dt_ciclo_ini.strftime('%d/%m')} a {dt_ciclo_fim.strftime('%d/%m')})</div>
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 8px; margin-top: 8px;">
            <div style="background: #111a28; padding: 8px 10px; border-radius: 10px; border: 1px solid #1c2a3d;">
                <span style="font-size: 0.62rem; color: #4ade80; font-weight: 700;">TOTAL A RECEBER (BRUTO)</span>
                <div style="font-family: 'JetBrains Mono'; font-size: 1.0rem; font-weight: 800; color: #4ade80;">+ R$ {entradas_previstas:,.2f}</div>
            </div>
            <div style="background: #111a28; padding: 8px 10px; border-radius: 10px; border: 1px solid #1c2a3d;">
                <span style="font-size: 0.62rem; color: #f87171; font-weight: 700;">SAÍDAS + DESTINADOS</span>
                <div style="font-family: 'JetBrains Mono'; font-size: 1.0rem; font-weight: 800; color: #f87171;">- R$ {saidas_previstas:,.2f}</div>
            </div>
        </div>
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 8px; margin-top: 8px;">
            <div style="background: #111a28; padding: 8px 10px; border-radius: 10px; border: 1px solid #1c2a3d;">
                <span style="font-size: 0.62rem; color: #64748b; font-weight: 700;">SALDO ATUAL EM CONTA</span>
                <div style="font-family: 'JetBrains Mono'; font-size: 0.95rem; font-weight: 800; color: #ffffff;">R$ {total_saldos:,.2f}</div>
            </div>
            <div style="background: #111a28; padding: 8px 10px; border-radius: 10px; border: 1px solid #1c2a3d;">
                <span style="font-size: 0.62rem; color: #38bdf8; font-weight: 700;">SALDO PROJETADO FINAL</span>
                <div style="font-family: 'JetBrains Mono'; font-size: 0.95rem; font-weight: 800; color: {'#4ade80' if saldo_projetado >= 0 else '#f87171'};">
                    R$ {saldo_projetado:,.2f}
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # CALENDÁRIO DO CICLO (04/MM até 03/MM+1)
    c_nav1, c_nav2 = st.columns([3, 2])
    with c_nav1:
        st.markdown(f'<span style="font-size: 0.82rem; font-weight: 800; color: #ffffff;">🗓️ Ciclo {nome_mes_comp}/{st.session_state.cal_ano}</span>', unsafe_allow_html=True)
    with c_nav2:
        c_prev_m, c_next_m = st.columns(2)
        with c_prev_m:
            if st.button("◀", key="m_ant", help="Ciclo Anterior"):
                if st.session_state.cal_mes == 1:
                    st.session_state.cal_mes = 12
                    st.session_state.cal_ano -= 1
                else:
                    st.session_state.cal_mes -= 1
                st.rerun()
        with c_next_m:
            if st.button("▶", key="m_prox", help="Próximo Ciclo"):
                if st.session_state.cal_mes == 12:
                    st.session_state.cal_mes = 1
                    st.session_state.cal_ano += 1
                else:
                    st.session_state.cal_mes += 1
                st.rerun()

    # Mapeia eventos por data completa (date object) dentro do ciclo completo (04/MM a 03/MM+1)
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
        # Agrupa o total de reembolso que entra em cada data (para mostrar a entrada real + o destino que sai)
        reemb_por_data_rows = {}
        for _, row_r in df_reemb_itens.iterrows():
            try:
                dt_r = datetime.strptime(row_r["data"], "%Y-%m-%d").date()
                if dt_full_ini <= dt_r <= dt_full_fim:
                    reemb_por_data_rows.setdefault(dt_r, []).append(row_r)
            except:
                pass

        for dt_r, lista_r in reemb_por_data_rows.items():
            # 1) Registra a entrada do reembolso naquela data:
            #    - Se houver parte destinada a pagamento, mostra a entrada que cobriu os destinos em verde (`+soma_destinada`)
            #    - Cada item sem destinação (Conta Corrente) entra em amarelo (`+valor`)
            soma_destinada_dia = sum(float(x["valor"]) for x in lista_r if x["acao"] != "Creditar em Conta Corrente")
            if soma_destinada_dia > 0:
                eventos_por_data.setdefault(dt_r, []).append({
                    "descricao": "⛽ Entrada Reembolso (Para Destinos)",
                    "valor": soma_destinada_dia,
                    "tipo": "Entrada",
                    "papel_cal": "EntradaCobertura",
                    "banco": "Reembolso",
                    "is_reembolso": True
                })
            for r_item in lista_r:
                if r_item["acao"] == "Creditar em Conta Corrente":
                    # Entrada sem destinação de pagamento -> linha amarela
                    eventos_por_data.setdefault(dt_r, []).append({
                        "descricao": f"⛽ Reembolso s/ Destinação: {r_item['motivo']}",
                        "valor": r_item["valor"],
                        "tipo": "Entrada",
                        "papel_cal": "ReembSemDestino",
                        "banco": r_item["banco"],
                        "is_reembolso": True
                    })
                else:
                    # Saída destinada (Cartão / Cheque Especial) -> linha vermelha
                    eventos_por_data.setdefault(dt_r, []).append({
                        "descricao": f"🎯 Destino: {r_item['motivo']}",
                        "valor": r_item["valor"],
                        "tipo": "Saída",
                        "papel_cal": "SaidaComprometida",
                        "banco": r_item["banco"],
                        "is_reembolso": True
                    })

    # Constrói as semanas de 04/MM até 03/MM+1
    start_grid = dt_full_ini - timedelta(days=dt_full_ini.weekday())
    end_grid = dt_full_fim + timedelta(days=(6 - dt_full_fim.weekday()))
    dias_semana = ["Seg", "Ter", "Qua", "Qui", "Sex", "Sáb", "Dom"]

    html_cal = '<table class="cal-table"><thead><tr>'
    for d_sem in dias_semana:
        html_cal += f'<th class="cal-th">{d_sem}</th>'
    html_cal += '</tr></thead><tbody>'

    cur_dt = start_grid
    while cur_dt <= end_grid:
        html_cal += '<tr>'
        for _ in range(7):
            in_cycle = (dt_full_ini <= cur_dt <= dt_full_fim)
            if not in_cycle:
                html_cal += f'<td class="cal-cell" style="opacity: 0.25;"><span style="color: #64748b; font-size: 0.58rem;">{cur_dt.day:02d}/{cur_dt.month:02d}</span></td>'
            else:
                is_today = (cur_dt == hoje)
                is_payday = (cur_dt.day in [3, 16])
                classes = ["cal-cell"]
                if is_today:
                    classes.append("today")
                if is_payday:
                    classes.append("payday")

                badges_html = ""
                if cur_dt in eventos_por_data:
                    evs = eventos_por_data[cur_dt]
                    tem_in_livre = any(ev["papel_cal"] == "EntradaLivre" for ev in evs)
                    tem_reemb_amarelo = any(ev["papel_cal"] == "ReembSemDestino" for ev in evs)
                    tem_out_comp = any(ev["papel_cal"] == "SaidaComprometida" for ev in evs)

                    if (tem_in_livre or tem_reemb_amarelo) and tem_out_comp:
                        classes.append("has-ambos")
                    elif tem_out_comp:
                        # Se entrou reembolso e já saiu 100% destinado (ex: dia 18), marca o card em vermelho!
                        classes.append("has-saida")
                    elif tem_reemb_amarelo and not tem_in_livre:
                        classes.append("has-reemb-livre")
                    elif tem_in_livre:
                        classes.append("has-entrada")

                    for ev in evs:
                        papel = ev["papel_cal"]
                        if papel == "SaidaComprometida":
                            cls_b = "badge-out"
                            sinal_b = "-"
                        elif papel == "ReembSemDestino":
                            cls_b = "badge-reemb-livre"
                            sinal_b = "+"
                        else:
                            cls_b = "badge-in"
                            sinal_b = "+"
                        v_curto = f"{sinal_b}{ev['valor']:,.0f}".replace(",", ".")
                        badges_html += f'<span class="cal-badge {cls_b}">{v_curto}</span>'

                cls_str = " ".join(classes)
                cor_num = "#eab308" if is_payday else ("#38bdf8" if is_today else "#94a3b8")
                lbl_dia = f"{cur_dt.day:02d}/{cur_dt.month:02d}" if cur_dt.month != st.session_state.cal_mes else f"{cur_dt.day}"
                tag_dia = f"💰{lbl_dia}" if is_payday else lbl_dia
                html_cal += f'<td class="{cls_str}"><span style="color: {cor_num};">{tag_dia}</span>{badges_html}</td>'
            cur_dt += timedelta(days=1)
        html_cal += '</tr>'
    html_cal += '</tbody></table>'

    st.markdown(html_cal, unsafe_allow_html=True)
    st.markdown(f"""
    <div style="display: flex; flex-wrap: wrap; gap: 10px; margin: 8px 0 12px 0; font-size: 0.64rem;">
        <span style="color: #eab308;">💰 16/{st.session_state.cal_mes:02d} e {dt_salario_03.strftime('%d/%m')} (Salários)</span>
        <span style="color: #4ade80;">🟢 Entrada</span>
        <span style="color: #fbbf24;">🟡 Reembolso s/ Destinação</span>
        <span style="color: #f87171;">🔴 Saída / Já Destinado</span>
    </div>
    """, unsafe_allow_html=True)

    # MODAL DE COPIAR DESPESA
    if st.session_state.copiando_prev is not None:
        c_origem = st.session_state.copiando_prev
        st.markdown("""
        <div style="background: #101c2e; border: 1px solid #a855f7; border-radius: 14px; padding: 12px; margin-bottom: 14px;">
            <span style="font-size: 0.82rem; font-weight: 800; color: #a855f7;">📋 Copiar Lançamento para Outro Mês</span>
        """, unsafe_allow_html=True)
        with st.form("form_copiar_previsto"):
            dt_base_copia = datetime.strptime(c_origem["data_prevista"], "%Y-%m-%d").date() + relativedelta(months=1)
            c_cp1, c_cp2 = st.columns(2)
            with c_cp1:
                nova_data = st.date_input("Nova Data", value=dt_base_copia)
                novo_val = st.number_input("Valor (R$)", min_value=0.01, value=float(c_origem["valor"]), step=10.0)
            with c_cp2:
                nova_desc = st.text_input("Descrição", value=c_origem["descricao"])
                idx_banco_c = df_bancos["banco"].tolist().index(c_origem["banco"]) if c_origem["banco"] in df_bancos["banco"].tolist() else 0
                novo_banco = st.selectbox("Banco", df_bancos["banco"].tolist(), index=idx_banco_c)
            
            c_salv_cp, c_canc_cp = st.columns(2)
            with c_salv_cp:
                if st.form_submit_button("📋 Confirmar Cópia"):
                    adicionar_previsto(nova_data.strftime("%Y-%m-%d"), nova_desc, novo_val, c_origem["categoria"], c_origem["tipo"], novo_banco, 1, c_origem.get("fixo", 0))
                    st.session_state.copiando_prev = None
                    st.success("Lançamento copiado com sucesso!")
                    st.rerun()
            with c_canc_cp:
                if st.form_submit_button("✕ Cancelar"):
                    st.session_state.copiando_prev = None
                    st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    # PAINEL DE EDIÇÃO
    if st.session_state.editando_id is not None:
        item_edit = df_prev[df_prev["id"] == st.session_state.editando_id]
        if not item_edit.empty:
            row_edit = item_edit.iloc[0]
            st.markdown("""
            <div style="background: #101c2e; border: 1px solid #38bdf8; border-radius: 14px; padding: 12px; margin-bottom: 14px;">
                <span style="font-size: 0.82rem; font-weight: 800; color: #38bdf8;">✏️ Editando Lançamento</span>
            """, unsafe_allow_html=True)
            with st.form("form_editar_previsto"):
                e_data_base = datetime.strptime(row_edit["data_prevista"], "%Y-%m-%d").date()
                c_e1, c_e2 = st.columns(2)
                with c_e1:
                    e_data = st.date_input("Data do Lançamento", value=e_data_base)
                    e_tipo = st.selectbox("Tipo de Operação", ["Entrada", "Saída"], index=0 if row_edit["tipo"] == "Entrada" else 1)
                    e_valor = st.number_input("Valor (R$)", min_value=0.01, value=float(row_edit["valor"]), step=50.0)
                with c_e2:
                    e_desc = st.text_input("Descrição", value=row_edit["descricao"])
                    idx_banco = df_bancos["banco"].tolist().index(row_edit["banco"]) if row_edit["banco"] in df_bancos["banco"].tolist() else 0
                    e_banco = st.selectbox("Banco", df_bancos["banco"].tolist(), index=idx_banco)
                    cats = ["Renda", "Salário", "Fatura", "Contas Fixas", "Lazer", "Outros"]
                    idx_cat = cats.index(row_edit["categoria"]) if row_edit["categoria"] in cats else 0
                    e_cat = st.selectbox("Categoria", cats, index=idx_cat)
                
                e_fixo = st.checkbox("Fixar este lançamento (Renda/Gasto Recorrente)", value=bool(row_edit.get("fixo", 0)))
                
                c_salv, c_canc = st.columns(2)
                with c_salv:
                    if st.form_submit_button("💾 Salvar Alterações"):
                        atualizar_previsto(row_edit["id"], e_data.strftime("%Y-%m-%d"), e_desc, e_valor, e_cat, e_tipo, e_banco, 1 if e_fixo else 0)
                        st.session_state.editando_id = None
                        st.success("Lançamento atualizado!")
                        st.rerun()
                with c_canc:
                    if st.form_submit_button("✕ Cancelar"):
                        st.session_state.editando_id = None
                        st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

    # Alternar Formulário de Novo Lançamento
    btn_txt = "➖ Ocultar Formulário" if st.session_state.mostrar_form_prev else "➕ Agendar Novo Lançamento"
    if st.button(btn_txt, key="toggle_form_prev"):
        st.session_state.mostrar_form_prev = not st.session_state.mostrar_form_prev
        st.rerun()

    if st.session_state.mostrar_form_prev:
        with st.form("form_add_previsto"):
            st.markdown('<div style="font-size: 0.75rem; font-weight: 700; color: #38bdf8; margin-bottom: 8px;">Dados do Lançamento:</div>', unsafe_allow_html=True)
            c_p1, c_p2 = st.columns(2)
            with c_p1:
                data_sel = st.date_input("Data de Início", value=date.today())
                tipo_prev = st.selectbox("Tipo de Operação", ["Entrada", "Saída"])
                valor_prev = st.number_input("Valor Estimado (R$)", min_value=0.01, value=1500.00, step=50.0)
            with c_p2:
                desc_prev = st.text_input("Descrição", value="Salário Dia 03 / Dia 16")
                banco_prev = st.selectbox("Banco Envolvido", df_bancos["banco"].tolist())
                cat_prev = st.selectbox("Categoria", ["Salário", "Renda", "Fatura", "Contas Fixas", "Lazer", "Outros"])
            
            st.markdown('<div style="margin-top: 6px; padding: 8px; background: #0d1522; border-radius: 10px; border: 1px solid #1a273b;">', unsafe_allow_html=True)
            fixo_check = st.checkbox("📌 Fixar Renda/Gasto Recorrente (Mesmo dia todos os meses)", value=True)
            meses_qtd = st.slider("Repetir por quantos meses consecutivos?", min_value=1, max_value=12, value=1)
            st.markdown('</div>', unsafe_allow_html=True)
                
            if st.form_submit_button("💾 Confirmar Agendamento"):
                adicionar_previsto(
                    data_sel.strftime("%Y-%m-%d"), 
                    desc_prev, 
                    valor_prev, 
                    cat_prev, 
                    tipo_prev, 
                    banco_prev, 
                    meses_repetir=meses_qtd,
                    fixo=1 if fixo_check else 0
                )
                st.session_state.mostrar_form_prev = False
                st.success(f"Previsão agendada com sucesso para {meses_qtd} mês(es)!")
                st.rerun()

    # Lista de Previsões do Ciclo Ativo (com botão ✅ Efetivar)
    st.markdown(f'<div style="font-size: 0.72rem; font-weight: 700; color: #64748b; text-transform: uppercase; margin: 12px 0 6px 0;">Lançamentos deste Ciclo ({dt_ciclo_ini.strftime("%d/%m")} a {dt_ciclo_fim.strftime("%d/%m")}):</div>', unsafe_allow_html=True)
    if df_prev_ciclo.empty and df_reemb_ciclo.empty:
        st.info("Nenhuma previsão agendada dentro deste período.")
    else:
        for idx, row_p in df_prev_ciclo.iterrows():
            is_ent = row_p["tipo"] == "Entrada"
            sinal_p = "+" if is_ent else "-"
            cor_p = "#4ade80" if is_ent else "#f87171"
            tag_fixo = " • 📌 Fixa" if row_p.get("fixo", 0) == 1 else ""
            
            st.markdown(f"""
            <div class="prev-item-card" style="margin-bottom: 4px;">
                <div>
                    <div style="font-size: 0.78rem; font-weight: 700; color: #ffffff;">{row_p['descricao']}</div>
                    <div style="font-size: 0.63rem; color: #94a3b8;">📅 {row_p['data_prevista']} • {row_p['banco']}{tag_fixo}</div>
                </div>
                <div style="font-family: 'JetBrains Mono'; font-weight: 800; font-size: 0.85rem; color: {cor_p}; text-align: right;">
                    {sinal_p} R$ {row_p['valor']:,.2f}
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            c_ef, c_cp, c_ed, c_del = st.columns([1.6, 1, 1, 1])
            with c_ef:
                st.markdown('<div class="btn-action-icon" style="margin-bottom: 8px;">', unsafe_allow_html=True)
                if st.button("✅ Baixar", key=f"btn_efet_{row_p['id']}", help="Efetivar no saldo do banco e extrato"):
                    efetivar_previsto(row_p["id"])
                    st.success("Efetivado no banco!")
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)
            with c_cp:
                st.markdown('<div class="btn-action-icon" style="margin-bottom: 8px;">', unsafe_allow_html=True)
                if st.button("📋", key=f"btn_cp_{row_p['id']}", help="Copiar para outro mês"):
                    st.session_state.copiando_prev = row_p.to_dict()
                    st.session_state.editando_id = None
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)
            with c_ed:
                st.markdown('<div class="btn-action-icon" style="margin-bottom: 8px;">', unsafe_allow_html=True)
                if st.button("✏️", key=f"btn_edit_{row_p['id']}", help="Editar"):
                    st.session_state.editando_id = int(row_p["id"])
                    st.session_state.copiando_prev = None
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)
            with c_del:
                st.markdown('<div class="btn-clear" style="margin-bottom: 8px;">', unsafe_allow_html=True)
                if st.button("🗑️", key=f"del_p_{row_p['id']}", help="Excluir"):
                    remover_previsto(row_p["id"])
                    if st.session_state.editando_id == int(row_p["id"]):
                        st.session_state.editando_id = None
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)

        for idx_r, row_r in df_reemb_ciclo.iterrows():
            is_r_livre = (row_r["acao"] == "Creditar em Conta Corrente")
            cor_borda_r = "#fbbf24" if is_r_livre else "#f87171"
            cor_val_r = "#fbbf24" if is_r_livre else "#f87171"
            sinal_val_r = "+" if is_r_livre else "-"
            tag_dest_r = "🟡 Sem destinação (Conta)" if is_r_livre else "🔴 Já destinado (Saída)"
            col_info_r, col_botoes_r = st.columns([4.8, 1.2])
            with col_info_r:
                st.markdown(f"""
                <div class="prev-item-card" style="margin-bottom: 6px; border-left: 3px solid {cor_borda_r};">
                    <div>
                        <div style="font-size: 0.78rem; font-weight: 700; color: #ffffff;">⛽ Reembolso: {row_r['motivo']}</div>
                        <div style="font-size: 0.63rem; color: #94a3b8;">📅 {row_r['data']} • {row_r['banco']} • {tag_dest_r}</div>
                    </div>
                    <div style="font-family: 'JetBrains Mono'; font-weight: 800; font-size: 0.85rem; color: {cor_val_r}; text-align: right;">
                        {sinal_val_r} R$ {row_r['valor']:,.2f}
                    </div>
                </div>
                """, unsafe_allow_html=True)
            with col_botoes_r:
                st.markdown('<div class="btn-clear" style="margin-top: 4px;">', unsafe_allow_html=True)
                if st.button("↩️", key=f"del_prev_reemb_{row_r['id']}", help="Estornar esta destinação"):
                    estornar_item_destino(row_r["id"])
                    st.success("Reembolso estornado!")
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

elif st.session_state.bloco_ativo == "destinar_reembolso":
    st.markdown('<div class="panel-box">', unsafe_allow_html=True)
    c_tit, c_fech = st.columns([5, 1])
    with c_tit:
        st.markdown('<span style="font-weight: 800; color: #38bdf8; font-size: 0.92rem;">⛽ Entrada & Destinação de Reembolso KM</span>', unsafe_allow_html=True)
    with c_fech:
        if st.button("✕", key="fechar_km"):
            st.session_state.bloco_ativo = None
            st.rerun()

    st.markdown("""
    <div style="background: #0d1522; border: 1px solid #1f2f47; border-radius: 14px; padding: 12px; margin: 10px 0 14px 0;">
        <div style="font-size: 0.72rem; font-weight: 700; color: #38bdf8; text-transform: uppercase;">Rateio Flexível de Reembolso:</div>
        <div style="font-size: 0.68rem; color: #94a3b8; margin-top: 4px; line-height: 1.4;">
            Digite o valor total recebido e <strong>escolha exatamente quantos destinos</strong> você quer (1, 2, 3 ou mais). O app só abate e lança nas contas e faturas que você definir!
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Botão de toggle para calculadora de estimativa
    btn_calc_label = "➖ Ocultar Calculadora" if st.session_state.mostrar_calc_km else "🧮 Calculadora de Estimativa (R$ 130/dia + Pedágios)"
    if st.button(btn_calc_label, key="toggle_calc_km"):
        st.session_state.mostrar_calc_km = not st.session_state.mostrar_calc_km
        st.rerun()

    if st.session_state.mostrar_calc_km:
        st.markdown('<div style="background: #111a28; border: 1px solid #1c2a3d; border-radius: 12px; padding: 12px; margin-bottom: 14px;">', unsafe_allow_html=True)
        c_c1, c_c2 = st.columns(2)
        with c_c1:
            dias_est = st.number_input("Dias de alocação", min_value=1, value=5, step=1)
            pedagio_dia = st.number_input("Pedágio diário (Ida + Volta)", min_value=0.0, value=25.60, step=1.0)
        with c_c2:
            gasolina_est = dias_est * 30.0
            diarias_lucro = dias_est * 100.0
            pedagio_total_est = dias_est * pedagio_dia
            total_est = (dias_est * 130.0) + pedagio_total_est
            st.caption(f"⛽ Gasolina (R$ 30/dia): **R$ {gasolina_est:,.2f}**")
            st.caption(f"💰 Lucro Livre (R$ 100/dia): **R$ {diarias_lucro:,.2f}**")
            st.caption(f"🛣️ Pedágios Cartão: **R$ {pedagio_total_est:,.2f}**")
            st.markdown(f"**Total Esperado:** <span style='color: #4ade80; font-weight: 800;'>R$ {total_est:,.2f}</span>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Escolha de quantos destinos o usuário quer configurar
    if "qtd_destinos" not in st.session_state:
        st.session_state.qtd_destinos = 2

    def recalcular_diferenca_destinos():
        qtd = st.session_state.get("qtd_destinos", 2)
        total = float(st.session_state.get("reemb_total_val", 0.0))
        letras_cb = ["A", "B", "C", "D", "E"]
        if qtd == 1:
            st.session_state["v_A"] = round(total, 2)
        else:
            soma_anteriores = 0.0
            for i in range(qtd - 1):
                soma_anteriores += float(st.session_state.get(f"v_{letras_cb[i]}", 0.0))
            ultima_letra = letras_cb[qtd - 1]
            st.session_state[f"v_{ultima_letra}"] = round(max(0.0, total - soma_anteriores), 2)

    c_sel_q1, c_sel_q2 = st.columns([2.5, 1.5])
    with c_sel_q1:
        st.markdown('<div style="font-size: 0.78rem; font-weight: 700; color: #ffffff; padding-top: 8px;">Quantos destinos quer ratear?</div>', unsafe_allow_html=True)
    with c_sel_q2:
        qtd_escolhida = st.selectbox(
            "Qtd", 
            [1, 2, 3, 4, 5], 
            index=[1, 2, 3, 4, 5].index(st.session_state.qtd_destinos),
            label_visibility="collapsed",
            key="sel_qtd_destinos_widget"
        )
        if qtd_escolhida != st.session_state.qtd_destinos:
            st.session_state.qtd_destinos = qtd_escolhida
            recalcular_diferenca_destinos()
            st.rerun()

    # Inicializa valores na sessão se ainda não existirem
    if "reemb_total_val" not in st.session_state:
        st.session_state["reemb_total_val"] = 617.00
    if "v_A" not in st.session_state:
        st.session_state["v_A"] = 150.00
    if "v_B" not in st.session_state:
        st.session_state["v_B"] = round(max(0.0, st.session_state["reemb_total_val"] - st.session_state["v_A"]), 2)
    for l_init in ["C", "D", "E"]:
        if f"v_{l_init}" not in st.session_state:
            st.session_state[f"v_{l_init}"] = 0.0

    st.markdown('<div style="background: #0d1522; border: 1px solid #1e2d44; border-radius: 14px; padding: 12px; margin-top: 8px; margin-bottom: 12px;">', unsafe_allow_html=True)
    st.markdown('<div style="font-size: 0.8rem; font-weight: 800; color: #ffffff; margin-bottom: 8px;">1. Entrada Total de Reembolso Recebido:</div>', unsafe_allow_html=True)
    c_v1, c_v2 = st.columns(2)
    with c_v1:
        data_receb = st.date_input("Data do Recebimento / Agendamento", value=date.today(), key="reemb_data_input")
    with c_v2:
        valor_total_recebido = st.number_input(
            "Valor Total (R$)", 
            min_value=0.01, 
            step=10.0, 
            key="reemb_total_val",
            on_change=recalcular_diferenca_destinos
        )

    is_reemb_efetivado = (data_receb <= date.today())
    if is_reemb_efetivado:
        st.markdown(f"""
        <div style="background: rgba(34, 197, 94, 0.12); border: 1px solid rgba(34, 197, 94, 0.35); border-radius: 10px; padding: 7px 10px; margin: 6px 0 8px 0; font-size: 0.68rem; color: #4ade80;">
            ✅ <strong>Data de hoje/passada ({data_receb.strftime('%d/%m/%Y')}):</strong> Os saldos, faturas ou cheque especial serão atualizados imediatamente.
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div style="background: rgba(234, 179, 8, 0.12); border: 1px solid rgba(234, 179, 8, 0.35); border-radius: 10px; padding: 7px 10px; margin: 6px 0 8px 0; font-size: 0.68rem; color: #eab308;">
            ⏳ <strong>Data Futura ({data_receb.strftime('%d/%m/%Y')}):</strong> Não mexe no seu saldo/fatura hoje. Será abatido/creditado automaticamente no dia <strong>{data_receb.strftime('%d/%m/%Y')}</strong>!
        </div>
        """, unsafe_allow_html=True)

    st.markdown(f'<div style="font-size: 0.8rem; font-weight: 800; color: #38bdf8; margin: 12px 0 6px 0;">2. Configurar os {st.session_state.qtd_destinos} Destino(s):</div>', unsafe_allow_html=True)
    st.caption("Ao digitar o valor em um destino, a diferença restante é calculada automaticamente no próximo:")

    destinos_coletados = []
    bancos_list = df_bancos["banco"].tolist()
    cores_letras = ["#38bdf8", "#fbbf24", "#4ade80", "#a855f7", "#f43f5e"]
    letras = ["A", "B", "C", "D", "E"]
    sugestoes_motivos = [
        "Pedágio no Cartão de Crédito",
        "Gasolina no Cheque Especial",
        "Renda livre / Lucro das diárias",
        "Outro gasto / Ajuste",
        "Reserva / Poupança"
    ]

    for idx_d in range(st.session_state.qtd_destinos):
        letra = letras[idx_d]
        cor = cores_letras[idx_d % len(cores_letras)]
        sugestao_banco = idx_d if idx_d < len(bancos_list) else 0
        is_ultimo = (idx_d == st.session_state.qtd_destinos - 1)
        tag_auto = " • ⚡ Diferença Automática" if (is_ultimo and st.session_state.qtd_destinos > 1) else ""
        
        st.markdown(f"""
        <div style="background: #111a28; padding: 12px; border-radius: 12px; margin-bottom: 10px; border: 1px solid #1c2a3d;">
            <span style="font-size: 0.72rem; font-weight: 700; color: {cor};">🎯 Destino {letra}{tag_auto}</span>
        """, unsafe_allow_html=True)
        
        c_d1, c_d2 = st.columns(2)
        with c_d1:
            banco_d = st.selectbox(f"Banco ({letra})", bancos_list, index=sugestao_banco, key=f"b_{letra}")
        with c_d2:
            val_d = st.number_input(
                f"Valor R$ ({letra})", 
                min_value=0.0, 
                step=10.0, 
                key=f"v_{letra}",
                on_change=(recalcular_diferenca_destinos if not is_ultimo else None)
            )

        acao_d = st.selectbox(
            f"Ação ({letra})", 
            ["Pagar/Abater Fatura de Cartão", "Abater Cheque Especial", "Creditar em Conta Corrente"], 
            index=0 if idx_d == 0 else (1 if idx_d == 1 else 2), 
            key=f"ac_{letra}"
        )
        motivo_d = st.text_input(
            f"Identificação / Motivo ({letra})", 
            value=sugestoes_motivos[idx_d % len(sugestoes_motivos)], 
            key=f"m_{letra}"
        )
        st.markdown('</div>', unsafe_allow_html=True)
        
        destinos_coletados.append({
            "banco": banco_d,
            "acao": acao_d,
            "valor": val_d,
            "motivo": motivo_d
        })

    # Conferência em tempo real da soma dos destinos vs total recebido
    soma_atual = sum(d["valor"] for d in destinos_coletados)
    diferenca_atual = valor_total_recebido - soma_atual
    cor_conf = "#4ade80" if abs(diferenca_atual) < 0.01 else "#fbbf24"
    status_conf = "✅ 100% Rateado" if abs(diferenca_atual) < 0.01 else (f"⚠️ Falta destinar: R$ {diferenca_atual:,.2f}" if diferenca_atual > 0 else f"⚠️ Excedeu em: R$ {abs(diferenca_atual):,.2f}")

    st.markdown(f"""
    <div style="background: #111a28; border: 1px solid #223249; border-radius: 10px; padding: 8px 12px; margin-bottom: 10px; display: flex; justify-content: space-between; align-items: center; font-size: 0.72rem;">
        <span style="color: #94a3b8;">Distribuído: <strong style="color: #ffffff;">R$ {soma_atual:,.2f}</strong> / R$ {valor_total_recebido:,.2f}</span>
        <span style="color: {cor_conf}; font-weight: 800;">{status_conf}</span>
    </div>
    """, unsafe_allow_html=True)

    if st.button("🚀 Executar Entrada & Destinar Automaticamente", key="btn_executar_rateio_dinamico", type="primary"):
        destinos_ativos = [d for d in destinos_coletados if d["valor"] > 0]
        if not destinos_ativos:
            st.error("Informe um valor maior que zero em pelo menos um destino!")
        else:
            aplicar_destinacao_reembolso(data_receb.strftime("%Y-%m-%d"), valor_total_recebido, destinos_ativos, efetivar_agora=is_reemb_efetivado)
            if is_reemb_efetivado:
                st.success(f"Reembolso de R$ {valor_total_recebido:,.2f} efetivado nos saldos e faturas!")
            else:
                st.success(f"Reembolso futuro de R$ {valor_total_recebido:,.2f} agendado para {data_receb.strftime('%d/%m/%Y')}! Ele só alterará seus saldos/faturas nessa data.")
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    # Histórico de Destinações com Edição, Baixa e Estorno Individual
    df_itens_hist = get_reembolsos_itens()
    if not df_itens_hist.empty:
        st.markdown('<div style="font-size: 0.72rem; font-weight: 700; color: #64748b; text-transform: uppercase; margin: 12px 0 6px 0;">Destinações Ativas (Editar, Baixa & Estorno):</div>', unsafe_allow_html=True)

        # Formulário de Edição de Destinação
        if st.session_state.editando_reemb_id is not None:
            reemb_edit_df = df_itens_hist[df_itens_hist["id"] == st.session_state.editando_reemb_id]
            if not reemb_edit_df.empty:
                r_ed = reemb_edit_df.iloc[0]
                st.markdown("""
                <div style="background: #101c2e; border: 1px solid #38bdf8; border-radius: 14px; padding: 12px; margin-bottom: 12px;">
                    <span style="font-size: 0.82rem; font-weight: 800; color: #38bdf8;">✏️ Editando Destinação de Reembolso</span>
                """, unsafe_allow_html=True)
                with st.form("form_editar_destinacao_reemb"):
                    try:
                        dt_ed_base = datetime.strptime(str(r_ed["data"]), "%Y-%m-%d").date()
                    except:
                        dt_ed_base = date.today()

                    c_er1, c_er2 = st.columns(2)
                    with c_er1:
                        ed_dt_r = st.date_input("Data Prevista / Efetivação", value=dt_ed_base)
                        b_list_r = df_bancos["banco"].tolist()
                        idx_br = b_list_r.index(r_ed["banco"]) if r_ed["banco"] in b_list_r else 0
                        ed_banco_r = st.selectbox("Banco Destino", b_list_r, index=idx_br)
                    with c_er2:
                        ed_val_r = st.number_input("Valor (R$)", min_value=0.01, value=float(r_ed["valor"]), step=10.0)
                        acoes_r = ["Pagar/Abater Fatura de Cartão", "Abater Cheque Especial", "Creditar em Conta Corrente"]
                        idx_ar = acoes_r.index(r_ed["acao"]) if r_ed["acao"] in acoes_r else 0
                        ed_acao_r = st.selectbox("Ação / Finalidade", acoes_r, index=idx_ar)

                    ed_motivo_r = st.text_input("Identificação / Motivo", value=str(r_ed["motivo"]))

                    c_br1, c_br2 = st.columns(2)
                    with c_br1:
                        if st.form_submit_button("💾 Salvar Alteração"):
                            atualizar_item_destino(
                                int(r_ed["id"]),
                                ed_dt_r.strftime("%Y-%m-%d"),
                                ed_banco_r,
                                ed_acao_r,
                                ed_val_r,
                                ed_motivo_r
                            )
                            st.session_state.editando_reemb_id = None
                            st.success("Destinação atualizada com sucesso!")
                            st.rerun()
                    with c_br2:
                        if st.form_submit_button("✕ Cancelar"):
                            st.session_state.editando_reemb_id = None
                            st.rerun()
                st.markdown("</div>", unsafe_allow_html=True)

        for _, item in df_itens_hist.iterrows():
            st_item = item.get("status", "Efetivado")
            badge_st = "⏳ Previsto" if st_item == "Previsto" else "✅ Efetivado"
            cor_st = "#eab308" if st_item == "Previsto" else "#4ade80"
            c_info_d, c_btn_est = st.columns([3.5, 2.5])
            with c_info_d:
                st.markdown(f"""
                <div style="background: #0d1522; border: 1px solid #1a273b; border-left: 3px solid {cor_st}; border-radius: 10px; padding: 8px 10px; margin-bottom: 6px;">
                    <div style="display: flex; justify-content: space-between;">
                        <span style="font-weight: 700; color: #ffffff; font-size: 0.76rem;">{item['banco']} • {item['acao']}</span>
                        <span style="color: {cor_st}; font-family: 'JetBrains Mono'; font-weight: 700; font-size: 0.8rem;">R$ {item['valor']:,.2f}</span>
                    </div>
                    <div style="font-size: 0.63rem; color: #94a3b8;">📅 {item['data']} • {item['motivo']} • <strong style="color:{cor_st};">{badge_st}</strong></div>
                </div>
                """, unsafe_allow_html=True)
            with c_btn_est:
                if st_item == "Previsto":
                    cb1, cb2, cb3 = st.columns(3)
                    with cb1:
                        st.markdown('<div class="btn-action-icon" style="margin-top: 4px;">', unsafe_allow_html=True)
                        if st.button("✏️", key=f"btn_ed_reemb_{item['id']}", help="Editar destinação futura"):
                            st.session_state.editando_reemb_id = int(item["id"])
                            st.rerun()
                        st.markdown('</div>', unsafe_allow_html=True)
                    with cb2:
                        st.markdown('<div class="btn-action-icon" style="margin-top: 4px;">', unsafe_allow_html=True)
                        if st.button("✅", key=f"btn_ef_reemb_{item['id']}", help="Confirmar que caiu na conta"):
                            efetivar_reembolso_item(item["id"])
                            if st.session_state.editando_reemb_id == int(item["id"]):
                                st.session_state.editando_reemb_id = None
                            st.success("Reembolso efetivado!")
                            st.rerun()
                        st.markdown('</div>', unsafe_allow_html=True)
                    with cb3:
                        st.markdown('<div class="btn-clear" style="margin-top: 4px;">', unsafe_allow_html=True)
                        if st.button("↩️", key=f"btn_est_{item['id']}", help="Cancelar/Excluir"):
                            estornar_item_destino(item["id"])
                            if st.session_state.editando_reemb_id == int(item["id"]):
                                st.session_state.editando_reemb_id = None
                            st.rerun()
                        st.markdown('</div>', unsafe_allow_html=True)
                else:
                    cb1, cb2 = st.columns(2)
                    with cb1:
                        st.markdown('<div class="btn-action-icon" style="margin-top: 4px;">', unsafe_allow_html=True)
                        if st.button("✏️", key=f"btn_ed_reemb_{item['id']}", help="Editar destinação"):
                            st.session_state.editando_reemb_id = int(item["id"])
                            st.rerun()
                        st.markdown('</div>', unsafe_allow_html=True)
                    with cb2:
                        st.markdown('<div class="btn-clear" style="margin-top: 4px;">', unsafe_allow_html=True)
                        if st.button("↩️", key=f"btn_est_{item['id']}", help="Desfazer e estornar este valor"):
                            estornar_item_destino(item["id"])
                            if st.session_state.editando_reemb_id == int(item["id"]):
                                st.session_state.editando_reemb_id = None
                            st.success("Destinação estornada!")
                            st.rerun()
                        st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

elif st.session_state.bloco_ativo == "advisor":
    st.markdown('<div class="panel-box">', unsafe_allow_html=True)
    c_tit, c_fech = st.columns([5, 1])
    with c_tit:
        st.markdown('<span style="font-weight: 800; color: #38bdf8; font-size: 0.92rem;">🧠 Advisor • Diagnóstico Completo & Plano de Virada</span>', unsafe_allow_html=True)
    with c_fech:
        if st.button("✕", key="fechar_adv"):
            st.session_state.bloco_ativo = None
            st.rerun()

    diagnosticos = []

    # --- DADOS CONSOLIDADOS DO CICLO ATUAL (04/MM a 03/MM+1) ---
    dt_adv_ini, dt_adv_fim, _ = get_intervalo_ciclo(st.session_state.cal_ano, st.session_state.cal_mes, "Ciclo Completo (04 a 03)")
    meses_pt_adv = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]
    nome_mes_adv = meses_pt_adv[st.session_state.cal_mes - 1]

    entradas_fixas_ou_prev = 0.0
    saidas_fixas_ou_prev = 0.0
    saidas_por_categoria = {}

    if not df_prev.empty:
        for _, r_p in df_prev.iterrows():
            try:
                d_p = datetime.strptime(r_p["data_prevista"], "%Y-%m-%d").date()
                if dt_adv_ini <= d_p <= dt_adv_fim:
                    v_p = float(r_p["valor"])
                    if r_p["tipo"] == "Entrada":
                        entradas_fixas_ou_prev += v_p
                    else:
                        saidas_fixas_ou_prev += v_p
                        cat_p = str(r_p.get("categoria", "Outros"))
                        saidas_por_categoria[cat_p] = saidas_por_categoria.get(cat_p, 0.0) + v_p
            except:
                pass

    # Reembolsos previstos no ciclo
    reemb_livre_adv = 0.0
    reemb_dest_adv = 0.0
    if not df_reemb_itens.empty:
        for _, r_ri in df_reemb_itens.iterrows():
            try:
                d_r = datetime.strptime(r_ri["data"], "%Y-%m-%d").date()
                if dt_adv_ini <= d_r <= dt_adv_fim:
                    if r_ri["acao"] == "Creditar em Conta Corrente":
                        reemb_livre_adv += float(r_ri["valor"])
                    else:
                        reemb_dest_adv += float(r_ri["valor"])
            except:
                pass

    # Análise detalhada das compras parceladas
    total_parcelas_mes = df_parc["valor_parcela"].sum() if not df_parc.empty else 0.0
    total_divida_parcelas = sum(max(0, int(r["total_parcelas"]) - int(r["parcela_atual"])) * float(r["valor_parcela"]) for _, r in df_parc.iterrows()) if not df_parc.empty else 0.0

    # --- 1. PROJEÇÃO MÊS A MÊS (6 MESES) PARA DESCOBRIR QUANDO COMEÇA A SOBRAR MAIS DINHEIRO ---
    # Calcula renda recorrente mensal base (salários/rendas fixas ou entradas do ciclo atual) e gastos recorrentes base
    renda_mensal_base = entradas_fixas_ou_prev
    if renda_mensal_base == 0 and not df_prev.empty:
        # Fallback: média das entradas cadastradas por mês
        renda_mensal_base = df_prev[df_prev["tipo"] == "Entrada"]["valor"].sum() / max(1, len(df_prev[df_prev["tipo"] == "Entrada"]["data_prevista"].str[:7].unique()))

    # Gastos fixos/recorrentes mensais (excluindo faturas variáveis se já estiverem nas parcelas, mas considerando contas fixas)
    gastos_mensais_base = saidas_fixas_ou_prev

    projecoes_6m = []
    mes_virada_nome = None
    ganho_mensal_virada = 0.0

    for offset_m in range(0, 6):
        dt_ref_m = date(st.session_state.cal_ano, st.session_state.cal_mes, 1) + relativedelta(months=offset_m)
        m_idx = dt_ref_m.month
        y_val = dt_ref_m.year
        label_m = f"{meses_pt_adv[m_idx - 1][:3]}/{str(y_val)[2:]}"

        # Parcelas ainda ativas nesse mês futuro (parcela_atual + offset_m <= total_parcelas)
        parc_ativas_m = 0.0
        parc_quitadas_ate_aqui = 0.0
        if not df_parc.empty:
            for _, rp in df_parc.iterrows():
                p_at = int(rp["parcela_atual"])
                p_tot = int(rp["total_parcelas"])
                v_p = float(rp["valor_parcela"])
                if (p_at + offset_m) <= p_tot:
                    parc_ativas_m += v_p
                else:
                    parc_quitadas_ate_aqui += v_p

        # Entradas e saídas previstas especificamente naquele ciclo futuro (se o usuário já repetiu meses)
        dt_c_i, dt_c_f, _ = get_intervalo_ciclo(y_val, m_idx, "Ciclo Completo (04 a 03)")
        ent_m = 0.0
        sai_m = 0.0
        if not df_prev.empty:
            for _, r_pr in df_prev.iterrows():
                try:
                    dp_obj = datetime.strptime(r_pr["data_prevista"], "%Y-%m-%d").date()
                    if dt_c_i <= dp_obj <= dt_c_f:
                        if r_pr["tipo"] == "Entrada":
                            ent_m += float(r_pr["valor"])
                        else:
                            sai_m += float(r_pr["valor"])
                except:
                    pass

        if ent_m == 0.0:
            ent_m = renda_mensal_base
        if sai_m == 0.0:
            sai_m = gastos_mensais_base

        # Se o usuário não lançou a fatura/parcelas dentro das saídas previstas daquele mês, adiciona a diferença das parcelas
        # Para evitar dupla contagem no mês 0, comparamos a redução de parcelas em relação ao mês atual
        alivio_parcelas = max(0.0, total_parcelas_mes - parc_ativas_m)
        sobra_estimada_m = (ent_m - sai_m) + alivio_parcelas + (reemb_livre_adv if offset_m == 0 else 0.0)

        projecoes_6m.append({
            "mes": label_m,
            "parcelas": parc_ativas_m,
            "alivio": alivio_parcelas,
            "sobra": sobra_estimada_m
        })

        if offset_m > 0 and mes_virada_nome is None and alivio_parcelas >= 100.0 and sobra_estimada_m > 0:
            mes_virada_nome = f"{meses_pt_adv[m_idx - 1]}/{y_val}"
            ganho_mensal_virada = alivio_parcelas

    # Se não houve alívio >= 100 por parcelas, identifica o primeiro mês com sobra positiva relevante
    if mes_virada_nome is None:
        for idx_p, item_p in enumerate(projecoes_6m):
            if idx_p > 0 and item_p["sobra"] > projecoes_6m[0]["sobra"] + 50.0:
                dt_v = date(st.session_state.cal_ano, st.session_state.cal_mes, 1) + relativedelta(months=idx_p)
                mes_virada_nome = f"{meses_pt_adv[dt_v.month - 1]}/{dt_v.year}"
                ganho_mensal_virada = item_p["sobra"] - projecoes_6m[0]["sobra"]
                break

    # Card Destaque: Previsão de Quando Vai Começar a Sobrar Mais Dinheiro
    sobra_atual_ciclo = projecoes_6m[0]["sobra"] if projecoes_6m else 0.0
    if mes_virada_nome:
        resumo_virada_html = (
            f"Hoje sua sobra líquida projetada em <strong>{nome_mes_adv}</strong> é de "
            f"<strong style='color: {'#4ade80' if sobra_atual_ciclo >= 0 else '#f87171'};'>R$ {sobra_atual_ciclo:,.2f}</strong>. "
            f"Com o encerramento natural das suas parcelas atuais, o <strong>ponto de virada será em {mes_virada_nome}</strong>, "
            f"quando você passará a ter <strong style='color: #4ade80;'>+ R$ {ganho_mensal_virada:,.2f}/mês</strong> extras livres no orçamento!"
        )
    elif total_parcelas_mes > 0:
        # Calcula o mês exato em que a primeira parcela termina
        menor_restante = min(max(1, int(r["total_parcelas"]) - int(r["parcela_atual"]) + 1) for _, r in df_parc.iterrows())
        dt_fim_prim = date(st.session_state.cal_ano, st.session_state.cal_mes, 1) + relativedelta(months=menor_restante)
        mes_fim_str = f"{meses_pt_adv[dt_fim_prim.month - 1]}/{dt_fim_prim.year}"
        resumo_virada_html = (
            f"Hoje você compromete <strong>R$ {total_parcelas_mes:,.2f}/mês</strong> com compras parceladas (saldo devedor total de R$ {total_divida_parcelas:,.2f}). "
            f"Se não fizer novas parcelas, seu orçamento começa a aliviar a partir de <strong>{mes_fim_str}</strong>."
        )
    else:
        resumo_virada_html = (
            f"Sua sobra líquida projetada em <strong>{nome_mes_adv}</strong> é de "
            f"<strong style='color: {'#4ade80' if sobra_atual_ciclo >= 0 else '#f87171'};'>R$ {sobra_atual_ciclo:,.2f}</strong>. "
            f"Como você não tem parcelas longas pesando nos próximos meses, cortar os ralos abaixo aumenta sua sobra imediatamente já no próximo ciclo."
        )

    # Mini tabela visual de 6 meses dentro do Advisor
    cols_6m_html = ""
    for p6 in projecoes_6m:
        c_s = "#4ade80" if p6["sobra"] >= 0 else "#f87171"
        cols_6m_html += f"""
        <div style="background: #111a28; border: 1px solid #1e2d44; border-radius: 8px; padding: 6px 4px; text-align: center;">
            <div style="font-size: 0.60rem; color: #94a3b8; font-weight: 700;">{p6['mes']}</div>
            <div style="font-family: 'JetBrains Mono'; font-size: 0.68rem; font-weight: 800; color: {c_s}; margin-top: 2px;">
                {'+' if p6['sobra'] >= 0 else ''}{p6['sobra']:,.0f}
            </div>
            <div style="font-size: 0.52rem; color: #64748b; margin-top: 1px;">Parc: {p6['parcelas']:,.0f}</div>
        </div>
        """

    st.markdown(f"""
    <div style="background: linear-gradient(145deg, #132136 0%, #0d1624 100%); border: 1px solid #2b456b; border-radius: 14px; padding: 12px; margin: 8px 0 12px 0;">
        <div style="font-size: 0.74rem; font-weight: 800; color: #38bdf8; text-transform: uppercase;">📈 Projeção de Virada (Próximos 6 Meses)</div>
        <div style="font-size: 0.72rem; color: #e2e8f0; margin-top: 5px; line-height: 1.45;">{resumo_virada_html}</div>
        <div style="display: grid; grid-template-columns: repeat(6, 1fr); gap: 4px; margin-top: 10px;">
            {cols_6m_html}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # --- 2. ONDE VOCÊ ESTÁ PERDENDO DINHEIRO (RALOS FINANCEIROS DETECTADOS) ---
    ralos = []
    if total_cheque > 0:
        juros_est_mes = total_cheque * 0.08  # ~8% ao mês média cheque especial
        ralos.append(
            f"<strong>1. Juros de Cheque Especial (R$ {total_cheque:,.2f} em uso):</strong> Você está perdendo cerca de "
            f"<strong style='color:#f87171;'>R$ {juros_est_mes:,.2f}/mês</strong> só em juros rotativos. Zerar isso é a prioridade #1."
        )

    if renda_mensal_base > 0 and total_parcelas_mes > 0:
        pct_parc_renda = (total_parcelas_mes / renda_mensal_base) * 100
        if pct_parc_renda >= 25.0:
            ralos.append(
                f"<strong>2. Bola de Neve no Cartão ({pct_parc_renda:.0f}% da renda):</strong> Suas parcelas somam "
                f"<strong>R$ {total_parcelas_mes:,.2f}/mês</strong> (totalizando R$ {total_divida_parcelas:,.2f} a pagar). "
                f"Evite qualquer compra parcelada nova pelos próximos 60 dias para destravar seu fluxo."
            )

    # Verifica gastos no extrato por categoria (ex: Lazer, Alimentação, Transporte)
    if not df_tx.empty:
        tx_saidas = df_tx[df_tx["tipo"] == "Saída"].copy()
        if not tx_saidas.empty:
            gastos_cat = tx_saidas.groupby("categoria")["valor"].sum().sort_values(ascending=False)
            top_cat = gastos_cat.index[0]
            top_cat_val = float(gastos_cat.iloc[0])
            if top_cat_val > 150.0:
                ralos.append(
                    f"<strong>3. Maior Vazamento no Extrato ({top_cat}):</strong> Você já acumulou "
                    f"<strong>R$ {top_cat_val:,.2f}</strong> lançados em <em>{top_cat}</em>. "
                    f"Reduzir 20% dessa categoria economiza <strong>R$ {top_cat_val * 0.20:,.2f}</strong> direto no seu bolso."
                )

    # Verifica dinheiro parado em conta sem rendimento ou fatura alta
    if total_faturas > total_saldos and total_faturas > 0:
        gap_fat = total_faturas - total_saldos
        ralos.append(
            f"<strong>4. Descasamento de Caixa (Faturas vs. Saldo):</strong> Suas faturas atuais (R$ {total_faturas:,.2f}) "
            f"superam seu saldo real em conta (R$ {total_saldos:,.2f}) em <strong>R$ {gap_fat:,.2f}</strong>. "
            f"Isso obriga você a depender integralmente do próximo salário para cobrir gastos já feitos."
        )

    if not ralos:
        ralos.append("Nenhum vazamento grave de juros ou excesso de parcelas detectado hoje. Mantenha o controle rígido dos gastos variáveis para acelerar sua reserva.")

    diagnosticos.append({
        "titulo": "🔍 Onde Você Está Perdendo Dinheiro & Como Ajustar:",
        "tipo": "danger" if (total_cheque > 0 or total_faturas > total_saldos) else "warning",
        "desc": "<br>• ".join([""] + ralos)[5:]
    })

    # --- 3. CAMINHO PRÁTICO PARA SOBRAR DINHEIRO (PLANO DE AÇÃO EM 3 PASSOS) ---
    passo1 = (
        f"<strong>Passo 1 (Estancar Juros):</strong> Use os reembolsos de KM e entradas dos dias 03/16 para manter o Cheque Especial em <strong>R$ 0,00</strong>."
        if total_cheque > 0 else
        "<strong>Passo 1 (Proteção):</strong> Mantenha o Cheque Especial zerado e concentre combustível/pedágio apenas no cartão com maior prazo."
    )
    passo2 = (
        f"<strong>Passo 2 (Trava de Parcelas):</strong> Congele novos parcelamentos até liquidar as parcelas atuais (R$ {total_parcelas_mes:,.2f}/mês)."
        if total_parcelas_mes > 0 else
        "<strong>Passo 2 (Compra à Vista):</strong> Continue sem parcelas pesadas e priorize pagamentos no Pix com desconto."
    )
    meta_reserva = max(100.0, round(renda_mensal_base * 0.10, 2)) if renda_mensal_base > 0 else 200.0
    passo3 = (
        f"<strong>Passo 3 (Pague-se Primeiro):</strong> Assim que cair o salário do dia 03 ou 16, separe imediatamente "
        f"<strong>R$ {meta_reserva:,.2f} (10% da renda)</strong> em uma conta separada (Nubank/Mercado Pago) antes de pagar contas variáveis."
    )
    diagnosticos.append({
        "titulo": "🧭 Caminho para Ajustar Sua Vida Financeira:",
        "tipo": "success",
        "desc": f"{passo1}<br>{passo2}<br>{passo3}"
    })

    # --- 4. ANÁLISE DE REEMBOLSOS FUTUROS DESTINADOS À CONTA CORRENTE ---
    reemb_fut_cc = pd.DataFrame()
    if not df_reemb_itens.empty:
        reemb_fut_cc = df_reemb_itens[
            (df_reemb_itens.get("status", "Efetivado") == "Previsto") &
            (df_reemb_itens["acao"] == "Creditar em Conta Corrente")
        ]

    if not reemb_fut_cc.empty:
        total_reemb_cc = reemb_fut_cc["valor"].sum()
        bancos_dest_cc = ", ".join(reemb_fut_cc["banco"].unique())
        contas_com_cheque = df_bancos[df_bancos["cheque_especial_usado"] > 0].sort_values(by="cheque_especial_usado", ascending=False)
        cartoes_ativos = df_bancos[df_bancos["tem_cartao"] == 1].copy()
        if not cartoes_ativos.empty:
            cartoes_ativos["uso_pct"] = cartoes_ativos.apply(
                lambda r: (r["fatura_atual"] / r["limite_cartao"] * 100) if r["limite_cartao"] > 0 else 0.0,
                axis=1
            )

        if not contas_com_cheque.empty:
            pior_cheque = contas_com_cheque.iloc[0]
            val_abater = min(total_reemb_cc, float(pior_cheque["cheque_especial_usado"]))
            sobra_apos_cheque = max(0.0, total_reemb_cc - val_abater)
            msg_acao_reemb = (
                f"Você agendou <strong>R$ {total_reemb_cc:,.2f}</strong> de reembolso futuro para cair em Conta Corrente ({bancos_dest_cc}). "
                f"<strong>Recomendação:</strong> Assim que cair, transfira <strong>R$ {val_abater:,.2f}</strong> para cobrir o Cheque Especial do "
                f"<strong>{pior_cheque['banco']}</strong> (R$ {pior_cheque['cheque_especial_usado']:,.2f})."
            )
            if sobra_apos_cheque > 0:
                msg_acao_reemb += f" Os <strong>R$ {sobra_apos_cheque:,.2f}</strong> restantes deixe rendendo em conta para gasolina."
            diagnosticos.append({
                "titulo": "💡 Destino Ideal para o Reembolso Futuro em Conta:",
                "tipo": "warning",
                "desc": msg_acao_reemb
            })
        elif not cartoes_ativos.empty and cartoes_ativos["uso_pct"].max() >= 70.0:
            cartao_apertado = cartoes_ativos.sort_values(by="uso_pct", ascending=False).iloc[0]
            val_adiantar = min(total_reemb_cc, float(cartao_apertado["fatura_atual"]))
            diagnosticos.append({
                "titulo": "💡 Destino Ideal para o Reembolso Futuro em Conta:",
                "tipo": "info",
                "desc": (
                    f"Você tem <strong>R$ {total_reemb_cc:,.2f}</strong> previstos para Conta Corrente ({bancos_dest_cc}). "
                    f"Como o cartão <strong>{cartao_apertado['banco']}</strong> está com <strong>{cartao_apertado['uso_pct']:.0f}% do limite comprometido</strong>, "
                    f"vale adiantar <strong>R$ {val_adiantar:,.2f}</strong> nessa fatura para liberar limite para os próximos pedágios."
                )
            })
        else:
            diagnosticos.append({
                "titulo": "💡 Destino Ideal para o Reembolso Futuro em Conta:",
                "tipo": "success",
                "desc": (
                    f"Você tem <strong>R$ {total_reemb_cc:,.2f}</strong> previstos para cair em Conta Corrente ({bancos_dest_cc}). "
                    f"Com Cheque Especial zerado e faturas controladas, <strong>mantenha esse valor rendendo em conta</strong> para pagar a gasolina das próximas alocações à vista!"
                )
            })

    # --- 5. ESTRATÉGIA PARA PAGAR GASOLINA E PEDÁGIO DAS PRÓXIMAS ALOCAÇÕES ---
    dia_hoje = date.today().day
    cartoes_disp = df_bancos[df_bancos["tem_cartao"] == 1].copy()
    melhor_cartao_msg = ""

    if not cartoes_disp.empty:
        def score_cartao(row):
            lim_t = float(row["limite_cartao"])
            fat = float(row["fatura_atual"])
            lim_lib = float(row["limite_liberado"]) if float(row["limite_liberado"]) > 0 else max(0.0, lim_t - fat)
            dia_f = int(row.get("dia_fechamento", 3))
            dia_v = int(row.get("dia_vencimento", 10))
            if dia_hoje >= dia_f:
                dias_prazo = (30 - dia_hoje) + dia_v
                status_ciclo = "Fatura recém-fechada (máximo prazo)"
            else:
                dias_prazo = dia_v - dia_hoje if dia_v > dia_hoje else (30 - dia_hoje) + dia_v
                status_ciclo = f"Fecha dia {dia_f}"
            return pd.Series([lim_lib, dias_prazo, status_ciclo])

        cartoes_disp[["lim_real", "dias_prazo", "status_ciclo"]] = cartoes_disp.apply(score_cartao, axis=1)
        cartoes_com_limite = cartoes_disp[cartoes_disp["lim_real"] >= 100.0].sort_values(by=["dias_prazo", "lim_real"], ascending=[False, False])

        if not cartoes_com_limite.empty:
            top_c = cartoes_com_limite.iloc[0]
            melhor_cartao_msg = (
                f"<strong>Use o Cartão {top_c['banco']}</strong> para Pedágio e Gasolina: ele tem "
                f"<strong>R$ {top_c['lim_real']:,.2f}</strong> de limite liberado real, {top_c['status_ciclo']} "
                f"e vence dia {int(top_c['dia_vencimento'])} (~{int(top_c['dias_prazo'])} dias de prazo)."
            )

    if total_saldos >= 200.0 and melhor_cartao_msg:
        desc_estrategia = (
            f"<strong>1º Opção (Recomendada):</strong> {melhor_cartao_msg}<br>"
            f"<strong>2º Opção (À vista):</strong> Você também possui R$ {total_saldos:,.2f} em conta se preferir pagar no débito/Pix.<br>"
            f"<strong>🚫 Evite Cheque Especial:</strong> Nunca use o cheque especial enquanto tiver saldo em conta ou limite no cartão."
        )
        tipo_est = "success"
    elif melhor_cartao_msg:
        desc_estrategia = (
            f"<strong>NÃO use o Cheque Especial!</strong> Seu saldo em conta está baixo (R$ {total_saldos:,.2f}), mas você tem limite no crédito. "
            f"{melhor_cartao_msg}"
        )
        tipo_est = "info"
    else:
        desc_estrategia = (
            f"<strong>Atenção:</strong> Seus cartões estão sem limite livre suficiente (ou desativados) e seu saldo atual é R$ {total_saldos:,.2f}. "
            f"Utilize o <strong>Cheque Especial de menor taxa</strong> apenas pelo valor exato da gasolina/pedágio da viagem e "
            f"registre imediatamente na aba <strong>⛽ Destinar Reembolso</strong> para cobrir assim que a empresa pagar."
        )
        tipo_est = "warning"

    diagnosticos.append({
        "titulo": "⛽ Melhor Forma de Pagar Gasolina & Pedágio Agora:",
        "tipo": tipo_est,
        "desc": desc_estrategia
    })

    for diag in diagnosticos:
        cor_borda = "#38bdf8"
        if diag["tipo"] == "danger": cor_borda = "#f87171"
        elif diag["tipo"] == "warning": cor_borda = "#fbbf24"
        elif diag["tipo"] == "success": cor_borda = "#4ade80"
        
        st.markdown(f"""
        <div style="background: #0d1522; border: 1px solid #1d2d42; border-left: 4px solid {cor_borda}; border-radius: 12px; padding: 12px; margin-bottom: 10px;">
            <div style="font-size: 0.82rem; font-weight: 700; color: #ffffff;">{diag['titulo']}</div>
            <div style="font-size: 0.72rem; color: #94a3b8; margin-top: 4px; line-height: 1.45;">{diag['desc']}</div>
        </div>
        """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

elif st.session_state.bloco_ativo == "vencimentos":
    st.markdown('<div class="panel-box">', unsafe_allow_html=True)
    c_tit, c_fech = st.columns([5, 1])
    with c_tit:
        st.markdown('<span style="font-weight: 800; color: #38bdf8; font-size: 0.9rem;">💳 Vencimento & Fechamento das Faturas</span>', unsafe_allow_html=True)
    with c_fech:
        if st.button("✕", key="fechar_venc"):
            st.session_state.bloco_ativo = None
            st.rerun()
    
    bancos_com_cartao = df_bancos[df_bancos["tem_cartao"] == 1]["banco"].tolist()
    if not bancos_com_cartao:
        st.info("Nenhum banco configurado com cartão de crédito. Ative a opção na aba 'Ajustes'.")
    else:
        banco_venc = st.selectbox("Selecione o Cartão para Configurar", bancos_com_cartao, key="sel_banco_venc")
        info_banco = df_bancos[df_bancos["banco"] == banco_venc].iloc[0]
        
        c_venc1, c_venc2 = st.columns(2)
        with c_venc1:
            dia_fech = st.number_input("Melhor dia de compra (Fechamento)", min_value=1, max_value=31, value=int(info_banco.get("dia_fechamento", 3)))
        with c_venc2:
            dia_venc = st.number_input("Dia do Vencimento", min_value=1, max_value=31, value=int(info_banco.get("dia_vencimento", 10)))
            
        if st.button("💾 Salvar Datas deste Cartão", key="salvar_datas"):
            atualizar_vencimentos(banco_venc, dia_venc, dia_fech)
            st.success(f"Datas de {banco_venc} salvas: Fechamento dia {dia_fech} • Vencimento dia {dia_venc}!")
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

elif st.session_state.bloco_ativo == "graficos":
    st.markdown('<div class="panel-box">', unsafe_allow_html=True)
    c_tit, c_fech = st.columns([5, 1])
    with c_tit:
        st.markdown('<span style="font-weight: 800; color: #38bdf8; font-size: 0.92rem;">📊 Diagnóstico da Competência (04 a 03)</span>', unsafe_allow_html=True)
    with c_fech:
        if st.button("✕", key="fechar_diag_inteligente"):
            st.session_state.bloco_ativo = None
            st.rerun()

    dt_ciclo_ini, dt_ciclo_fim, dt_prox_03 = get_intervalo_ciclo(st.session_state.cal_ano, st.session_state.cal_mes, "Ciclo Completo (04 a 03)")
    st.caption(f"Período analisado: **{dt_ciclo_ini.strftime('%d/%m/%Y')}** até **{dt_ciclo_fim.strftime('%d/%m/%Y')}** (Renda dias 03 e 16)")

    tot_saldo = df_bancos["saldo_conta"].sum()
    tot_faturas = df_bancos[df_bancos["tem_cartao"] == 1]["fatura_atual"].sum()
    tot_cheque = df_bancos["cheque_especial_usado"].sum()
    
    # Filtra previsões do ciclo 03 a 03
    entradas_prev_base = 0.0
    tot_saidas_mes = 0.0
    if not df_prev.empty:
        for _, r in df_prev.iterrows():
            try:
                d_obj = datetime.strptime(r["data_prevista"], "%Y-%m-%d").date()
                if dt_ciclo_ini <= d_obj <= dt_ciclo_fim:
                    if r["tipo"] == "Entrada":
                        entradas_prev_base += float(r["valor"])
                    else:
                        tot_saidas_mes += float(r["valor"])
            except:
                pass

    entradas_reemb_total = 0.0
    if not df_reemb_itens.empty:
        for _, r in df_reemb_itens.iterrows():
            try:
                d_obj = datetime.strptime(r["data"], "%Y-%m-%d").date()
                if dt_ciclo_ini <= d_obj <= dt_ciclo_fim:
                    entradas_reemb_total += float(r["valor"])
            except:
                pass

    tot_entradas_mes = entradas_prev_base + entradas_reemb_total
    saldo_projetado_mes = tot_saldo + tot_entradas_mes - tot_saidas_mes
    
    tot_parc_mes = df_parc["valor_parcela"].sum() if not df_parc.empty else 0.0
    tot_restante_parc = sum((r["total_parcelas"] - r["parcela_atual"]) * r["valor_parcela"] for _, r in df_parc.iterrows()) if not df_parc.empty else 0.0

    st.markdown(f'''
    <div style="background: #0d1522; border: 1px solid #1f2f47; border-radius: 14px; padding: 12px; margin: 8px 0 12px 0;">
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 8px;">
            <div style="background: #111a28; padding: 8px; border-radius: 10px; border: 1px solid #1c2a3d;">
                <span style="font-size: 0.62rem; color: #94a3b8; font-weight: 700;">SALDO TOTAL EM CONTA</span>
                <div style="font-family: 'JetBrains Mono'; font-size: 0.95rem; font-weight: 800; color: #ffffff;">R$ {tot_saldo:,.2f}</div>
            </div>
            <div style="background: #111a28; padding: 8px; border-radius: 10px; border: 1px solid #1c2a3d;">
                <span style="font-size: 0.62rem; color: #f87171; font-weight: 700;">FATURAS DE CARTÃO</span>
                <div style="font-family: 'JetBrains Mono'; font-size: 0.95rem; font-weight: 800; color: #f87171;">R$ {tot_faturas:,.2f}</div>
            </div>
            <div style="background: #111a28; padding: 8px; border-radius: 10px; border: 1px solid #1c2a3d;">
                <span style="font-size: 0.62rem; color: #4ade80; font-weight: 700;">ENTRADAS DO CICLO</span>
                <div style="font-family: 'JetBrains Mono'; font-size: 0.95rem; font-weight: 800; color: #4ade80;">+ R$ {tot_entradas_mes:,.2f}</div>
            </div>
            <div style="background: #111a28; padding: 8px; border-radius: 10px; border: 1px solid #1c2a3d;">
                <span style="font-size: 0.62rem; color: #38bdf8; font-weight: 700;">PROJEÇÃO ATÉ DIA 03</span>
                <div style="font-family: 'JetBrains Mono'; font-size: 0.95rem; font-weight: 800; color: {'#4ade80' if saldo_projetado_mes >= 0 else '#f87171'};">
                    R$ {saldo_projetado_mes:,.2f}
                </div>
            </div>
        </div>
        <div style="display: flex; justify-content: space-between; font-size: 0.66rem; color: #94a3b8; margin-top: 8px; padding-top: 6px; border-top: 1px solid #1c2a3d;">
            <span>Cheque Especial: <strong style="color: {'#f87171' if tot_cheque > 0 else '#4ade80'};">R$ {tot_cheque:,.2f}</strong></span>
            <span>Parcelas no Ciclo: <strong style="color: #fbbf24;">R$ {tot_parc_mes:,.2f}</strong></span>
        </div>
    </div>
    ''', unsafe_allow_html=True)

    diagnosticos = []
    if tot_cheque > 0:
        diagnosticos.append({
            "titulo": "Eliminação de Cheque Especial",
            "tipo": "danger",
            "desc": f"Existe saldo emergencial em uso de R$ {tot_cheque:,.2f}. Use o recebimento do dia 03 ou 16 (ou reembolsos KM) para zerar este limite antes de qualquer gasto variável."
        })
    else:
        diagnosticos.append({
            "titulo": "Cheque Especial Preservado",
            "tipo": "success",
            "desc": "Nenhuma conta está pagando juros emergenciais neste ciclo."
        })
        
    if tot_faturas > (tot_saldo + tot_entradas_mes):
        deficit = tot_faturas - (tot_saldo + tot_entradas_mes)
        diagnosticos.append({
            "titulo": "Risco de Financiamento de Fatura",
            "tipo": "danger",
            "desc": f"Suas faturas (R$ {tot_faturas:,.2f}) superam sua liquidez projetada até o dia 03 em R$ {deficit:,.2f}. Evite passar novas despesas no crédito e priorize o abatimento direto."
        })
    else:
        diagnosticos.append({
            "titulo": "Cobertura Integral das Faturas",
            "tipo": "success",
            "desc": "A soma do saldo atual com as entradas dos dias 03 e 16 cobre 100% das faturas deste fechamento."
        })
        
    if tot_entradas_mes > 0:
        pct_parc = (tot_parc_mes / tot_entradas_mes) * 100
        if pct_parc > 35:
            diagnosticos.append({
                "titulo": "Comprometimento de Renda em Parcelas",
                "tipo": "warning",
                "desc": f"As parcelas somam R$ {tot_parc_mes:,.2f} ({pct_parc:.1f}% das entradas do ciclo). Evite novos parcelamentos até liquidar parte do saldo restante (R$ {tot_restante_parc:,.2f})."
            })

    st.markdown('<div style="font-size: 0.74rem; font-weight: 800; color: #ffffff; margin-bottom: 6px;">📋 O QUE VOCÊ DEVE FAZER:</div>', unsafe_allow_html=True)
    for d in diagnosticos:
        cor_borda = "#ef4444" if d["tipo"] == "danger" else ("#fbbf24" if d["tipo"] == "warning" else "#22c55e")
        st.markdown(f'''
        <div style="background: #0d1522; border-left: 4px solid {cor_borda}; border-radius: 8px; padding: 8px 10px; margin-bottom: 6px;">
            <div style="font-size: 0.78rem; font-weight: 700; color: #ffffff;">{d['titulo']}</div>
            <div style="font-size: 0.68rem; color: #94a3b8; line-height: 1.3; margin-top: 2px;">{d['desc']}</div>
        </div>
        ''', unsafe_allow_html=True)

    st.markdown('<div style="font-size: 0.74rem; font-weight: 800; color: #38bdf8; margin: 12px 0 6px 0;">📤 EXPORTAR OU ENVIAR:</div>', unsafe_allow_html=True)

    pdf_bytes = gerar_relatorio_pdf(df_bancos, tot_entradas_mes, tot_saidas_mes, saldo_projetado_mes, tot_parc_mes, tot_restante_parc, diagnosticos)
    
    texto_whatsapp = (
        f"*RELATÓRIO FINANCEIRO (CICLO {dt_ciclo_ini.strftime('%d/%m')} a {dt_ciclo_fim.strftime('%d/%m')})*\\n"
        f"Gerado em: {datetime.now().strftime('%d/%m/%Y às %H:%M')}\\n\\n"
        f"• *Saldo em Conta:* R$ {tot_saldo:,.2f}\\n"
        f"• *Faturas Totais:* R$ {tot_faturas:,.2f}\\n"
        f"• *Cheque Especial em Uso:* R$ {tot_cheque:,.2f}\\n"
        f"• *Entradas do Ciclo (03 e 16):* R$ {tot_entradas_mes:,.2f}\\n"
        f"• *Saídas Previstas:* R$ {tot_saidas_mes:,.2f}\\n"
        f"• *Projeção até dia 03:* R$ {saldo_projetado_mes:,.2f}\\n"
        f"• *Parcelas no Ciclo:* R$ {tot_parc_mes:,.2f} (Restante: R$ {tot_restante_parc:,.2f})\\n\\n"
        f"*DIAGNÓSTICO E AÇÕES:*\\n"
    )
    for d in diagnosticos:
        texto_whatsapp += f"- {d['titulo']}: {d['desc']}\\n"

    url_whatsapp = "https://api.whatsapp.com/send?text=" + urllib.parse.quote(texto_whatsapp)

    col_exp1, col_exp2 = st.columns(2)
    with col_exp1:
        st.download_button(
            label="📄 Baixar Relatório (PDF)",
            data=pdf_bytes,
            file_name=f"relatorio_ciclo_{dt_ciclo_ini.strftime('%Y_%m_%d')}.pdf",
            mime="application/pdf",
            key="btn_download_relatorio_pdf"
        )
    with col_exp2:
        st.markdown(f'''
        <a href="{url_whatsapp}" target="_blank" style="text-decoration: none;">
            <button style="width: 100%; min-height: 38px; background: #25d366; color: white; border: none; border-radius: 10px; font-weight: 700; font-size: 0.74rem; cursor: pointer;">
                📲 Enviar p/ WhatsApp
            </button>
        </a>
        ''', unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

# Abas Principais (Com aba 'Parcelas' ao lado de 'Bancos')
tab_bancos, tab_parcelas, tab_extrato, tab_novo, tab_ajustes = st.tabs([
    "Bancos",
    "Parcelas", 
    "Extrato Completo", 
    "Lançar", 
    "Ajustes"
])

with tab_bancos:
    st.markdown('<div class="sec-header">Contas & Cartões</div>', unsafe_allow_html=True)
    
    for _, b in df_bancos.iterrows():
        b_saldo = b["saldo_conta"]
        msg_banco, cls_banco = get_status_saldo(b_saldo)
        tem_cartao = (b.get("tem_cartao", 1) == 1)
        
        if tem_cartao:
            lim_total = b.get("limite_cartao", 0.0)
            lim_liberado = b.get("limite_liberado", 0.0)
            lim_exibir = lim_liberado if lim_liberado > 0 else max(0.0, lim_total - b["fatura_atual"])
            
            dia_v = int(b.get("dia_vencimento", 10))
            dia_f = int(b.get("dia_fechamento", 3))
            
            st.markdown(f"""
            <div class="bank-card">
                <div class="bank-card-top">
                    <span class="bank-badge">
                        <span class="bank-dot" style="background-color: {b['cor_identificador']};"></span>
                        {b['banco']}
                    </span>
                    <span class="md-msg-pill {cls_banco}" style="margin-bottom: 0; font-size: 0.65rem;">
                        {msg_banco}
                    </span>
                </div>
                <div class="bank-grid">
                    <div class="bank-stat">
                        <div class="bank-stat-lbl">Saldo Conta</div>
                        <div class="bank-stat-val">R$ {b_saldo:,.2f}</div>
                    </div>
                    <div class="bank-stat">
                        <div class="bank-stat-lbl">Fatura Cartão</div>
                        <div class="bank-stat-val" style="color: #38bdf8;">R$ {b['fatura_atual']:,.2f}</div>
                        <div style="font-size: 0.62rem; color: #64748b; margin-top: 2px;">Vence dia {dia_v} (Fecha {dia_f})</div>
                    </div>
                    <div class="bank-stat">
                        <div class="bank-stat-lbl">Limite do Cartão (Total)</div>
                        <div class="bank-stat-val" style="color: #cbd5e1; font-size: 0.88rem;">R$ {lim_total:,.2f}</div>
                    </div>
                    <div class="bank-stat">
                        <div class="bank-stat-lbl">Limite Liberado (De Fato)</div>
                        <div class="bank-stat-val" style="color: #4ade80; font-size: 0.88rem;">R$ {lim_exibir:,.2f}</div>
                    </div>
                    <div class="bank-stat-full">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <div>
                                <span class="bank-stat-lbl">Status Cartão</span>
                                <div style="font-size: 0.75rem; font-weight: 700; color: #94a3b8;">Cartão Ativo</div>
                            </div>
                            <div style="text-align: right;">
                                <span class="bank-stat-lbl">Cheque Especial Usado</span>
                                <div style="font-family: 'JetBrains Mono'; font-size: 0.85rem; font-weight: 700; color: {'#f87171' if b['cheque_especial_usado'] > 0 else '#94a3b8'};">
                                    R$ {b['cheque_especial_usado']:,.2f}
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            # BANCO SEM CARTÃO
            st.markdown(f"""
            <div class="bank-card">
                <div class="bank-card-top">
                    <span class="bank-badge">
                        <span class="bank-dot" style="background-color: {b['cor_identificador']};"></span>
                        {b['banco']} <span style="font-size: 0.65rem; color: #64748b; font-weight: 500;">(Sem cartão de crédito)</span>
                    </span>
                    <span class="md-msg-pill {cls_banco}" style="margin-bottom: 0; font-size: 0.65rem;">
                        {msg_banco}
                    </span>
                </div>
                <div class="bank-grid-single">
                    <div class="bank-stat" style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <div class="bank-stat-lbl">Saldo em Conta Corrente</div>
                            <div class="bank-stat-val" style="font-size: 1.15rem;">R$ {b_saldo:,.2f}</div>
                        </div>
                        <div style="text-align: right;">
                            <div class="bank-stat-lbl">Cheque Especial Usado</div>
                            <div style="font-family: 'JetBrains Mono'; font-size: 0.9rem; font-weight: 700; color: {'#f87171' if b['cheque_especial_usado'] > 0 else '#94a3b8'};">
                                R$ {b['cheque_especial_usado']:,.2f}
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

# NOVA ABA DE PARCELAS
with tab_parcelas:
    st.markdown('<div class="sec-header">Controle de Compras Parceladas</div>', unsafe_allow_html=True)
    
    if not df_parc.empty:
        total_mensal_parcelas = df_parc["valor_parcela"].sum()
        total_saldo_restante = sum((row["total_parcelas"] - row["parcela_atual"]) * row["valor_parcela"] for _, row in df_parc.iterrows())
    else:
        total_mensal_parcelas = 0.0
        total_saldo_restante = 0.0

    st.markdown(f"""
    <div style="background: #0d1522; border: 1px solid #1f2f47; border-radius: 14px; padding: 12px; margin-bottom: 12px;">
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 8px;">
            <div style="background: #111a28; padding: 8px 10px; border-radius: 10px; border: 1px solid #1c2a3d;">
                <span style="font-size: 0.62rem; color: #38bdf8; font-weight: 700;">TOTAL PARCELAS ESTE MÊS</span>
                <div style="font-family: 'JetBrains Mono'; font-size: 1.0rem; font-weight: 800; color: #ffffff;">R$ {total_mensal_parcelas:,.2f}</div>
            </div>
            <div style="background: #111a28; padding: 8px 10px; border-radius: 10px; border: 1px solid #1c2a3d;">
                <span style="font-size: 0.62rem; color: #fbbf24; font-weight: 700;">SALDO DEVEDOR RESTANTE</span>
                <div style="font-family: 'JetBrains Mono'; font-size: 1.0rem; font-weight: 800; color: #fbbf24;">R$ {total_saldo_restante:,.2f}</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    btn_p_label = "➖ Ocultar Formulário" if st.session_state.mostrar_form_parc else "➕ Cadastrar Nova Compra Parcelada"
    if st.button(btn_p_label, key="toggle_form_parc"):
        st.session_state.mostrar_form_parc = not st.session_state.mostrar_form_parc
        st.rerun()

    if st.session_state.mostrar_form_parc:
        with st.form("form_add_parcela"):
            st.markdown('<div style="font-size: 0.78rem; font-weight: 800; color: #38bdf8; margin-bottom: 8px;">Nova Compra Parcelada:</div>', unsafe_allow_html=True)
            bancos_cartao_disp = df_bancos[df_bancos["tem_cartao"] == 1]["banco"].tolist()
            if not bancos_cartao_disp:
                bancos_cartao_disp = df_bancos["banco"].tolist()

            c_parc1, c_parc2 = st.columns(2)
            with c_parc1:
                banco_p = st.selectbox("Cartão de Crédito", bancos_cartao_disp)
                p_atual = st.number_input("Parcela Atual (que está pagando)", min_value=1, max_value=60, value=1, step=1)
                v_parc = st.number_input("Valor da Parcela (R$)", min_value=0.01, value=150.00, step=10.0)
            with c_parc2:
                desc_p = st.text_input("Descrição da Compra", value="Compra Parcelada")
                p_total = st.number_input("Total de Parcelas (ex: 10x)", min_value=1, max_value=60, value=10, step=1)
                cat_p = st.selectbox("Categoria", ["Eletrônicos", "Casa", "Vestuário", "Veículo", "Saúde", "Outros"])

            if st.form_submit_button("💾 Salvar Compra Parcelada"):
                adicionar_parcela(banco_p, desc_p, v_parc, p_atual, p_total, cat_p)
                st.session_state.mostrar_form_parc = False
                st.success("Compra parcelada cadastrada com sucesso!")
                st.rerun()

    bancos_cartao_filtro = ["Todos os Cartões"] + df_bancos[df_bancos["tem_cartao"] == 1]["banco"].tolist()
    sel_filtro_cartao = st.selectbox("Filtrar por Cartão:", bancos_cartao_filtro, key="filtro_cartao_parcelas")

    df_parc_filtrado = df_parc if sel_filtro_cartao == "Todos os Cartões" else df_parc[df_parc["banco"] == sel_filtro_cartao]

    if df_parc_filtrado.empty:
        st.info("Nenhuma compra parcelada registrada para este cartão.")
    else:
        for _, row_pc in df_parc_filtrado.iterrows():
            p_at = row_pc["parcela_atual"]
            p_tot = row_pc["total_parcelas"]
            v_parc_row = row_pc["valor_parcela"]
            restante_compra = max(0, p_tot - p_at) * v_parc_row
            pct = min(100.0, (p_at / p_tot) * 100) if p_tot > 0 else 0

            st.markdown(f"""
            <div class="parcela-card">
                <div class="parcela-top">
                    <div>
                        <span style="font-size: 0.84rem; font-weight: 800; color: #ffffff;">{row_pc['descricao']}</span>
                        <div style="font-size: 0.65rem; color: #94a3b8;">Cartão {row_pc['banco']} • {row_pc['categoria']}</div>
                    </div>
                    <div style="text-align: right;">
                        <span style="font-family: 'JetBrains Mono'; font-weight: 800; font-size: 0.88rem; color: #38bdf8;">R$ {v_parc_row:,.2f}/mês</span>
                    </div>
                </div>
                <div class="parcela-progresso">
                    <div class="parcela-progresso-bar" style="width: {pct:.1f}%;"></div>
                </div>
                <div style="display: flex; justify-content: space-between; align-items: center; font-size: 0.68rem; margin-top: 4px;">
                    <span style="color: #cbd5e1; font-weight: 700;">Parcela {p_at} de {p_tot} ({pct:.0f}% paga)</span>
                    <span style="color: #fbbf24; font-weight: 700;">Falta: R$ {restante_compra:,.2f}</span>
                </div>
                <div style="font-size: 0.65rem; color: #4ade80; font-weight: 700; margin-top: 3px;">
                    🏁 Término previsto: {row_pc['mes_ano_fim']}
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            c_btn_parc1, c_btn_parc2 = st.columns([3, 1])
            with c_btn_parc1:
                if p_at < p_tot:
                    if st.button(f"Pagar +1 Parcela ({p_at + 1}/{p_tot})", key=f"avancar_{row_pc['id']}"):
                        avancar_parcela(row_pc["id"])
                        st.rerun()
                else:
                    st.caption("✅ Compra 100% quitada!")
            with c_btn_parc2:
                st.markdown('<div class="btn-clear">', unsafe_allow_html=True)
                if st.button("🗑️", key=f"del_parc_{row_pc['id']}", help="Excluir esta compra"):
                    remover_parcela(row_pc["id"])
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)

with tab_extrato:
    c_ext_t, c_ext_b = st.columns([3.5, 1.5])
    with c_ext_t:
        st.markdown('<div class="sec-header" style="margin-top: 0.5rem;">Histórico Geral</div>', unsafe_allow_html=True)
    with c_ext_b:
        st.markdown('<div class="btn-clear" style="margin-top: 0.3rem;">', unsafe_allow_html=True)
        if st.button("🗑️ Limpar Extrato", key="btn_limpar_extrato_aba"):
            limpar_extrato_completo()
            st.session_state.editando_tx_id = None
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    # Formulário de Edição de Transação do Extrato
    if st.session_state.editando_tx_id is not None:
        tx_edit_df = df_tx[df_tx["id"] == st.session_state.editando_tx_id]
        if not tx_edit_df.empty:
            r_tx = tx_edit_df.iloc[0]
            st.markdown("""
            <div style="background: #101c2e; border: 1px solid #38bdf8; border-radius: 14px; padding: 12px; margin-bottom: 14px;">
                <span style="font-size: 0.82rem; font-weight: 800; color: #38bdf8;">✏️ Editando Transação do Extrato</span>
            """, unsafe_allow_html=True)
            with st.form("form_editar_tx_extrato"):
                c_tx1, c_tx2 = st.columns(2)
                with c_tx1:
                    tx_desc = st.text_input("Descrição", value=str(r_tx["descricao"]))
                    tx_val = st.number_input("Valor (R$)", min_value=0.01, value=float(r_tx["valor"]), step=5.0)
                    tx_tipo = st.selectbox("Tipo", ["Saída", "Entrada"], index=0 if r_tx["tipo"] == "Saída" else 1)
                with c_tx2:
                    tx_data = st.text_input("Data", value=str(r_tx["data"]))
                    b_list = df_bancos["banco"].tolist()
                    idx_b_tx = b_list.index(r_tx["banco"]) if r_tx["banco"] in b_list else 0
                    tx_banco = st.selectbox("Banco", b_list, index=idx_b_tx)
                    meios_list = ["Cartão de Crédito", "Conta Corrente / Pix"]
                    idx_m_tx = meios_list.index(r_tx["meio"]) if r_tx["meio"] in meios_list else 1
                    tx_meio = st.selectbox("Método", meios_list, index=idx_m_tx)
                
                cats_tx = ["Alimentação", "Transporte", "Lazer", "Contas Fixas", "Saúde", "Salário", "Reembolso KM", "OFX / Cartão", "OFX / Conta", "Outros"]
                idx_c_tx = cats_tx.index(r_tx["categoria"]) if r_tx["categoria"] in cats_tx else len(cats_tx) - 1
                tx_cat = st.selectbox("Categoria", cats_tx, index=idx_c_tx)

                c_tx_b1, c_tx_b2 = st.columns(2)
                with c_tx_b1:
                    if st.form_submit_button("💾 Salvar Alteração"):
                        atualizar_transacao_extrato(int(r_tx["id"]), tx_data, tx_desc, tx_val, tx_cat, tx_banco, tx_meio, tx_tipo)
                        st.session_state.editando_tx_id = None
                        st.success("Transação atualizada e saldo recalculado!")
                        st.rerun()
                with c_tx_b2:
                    if st.form_submit_button("✕ Cancelar"):
                        st.session_state.editando_tx_id = None
                        st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

    if df_tx.empty:
        st.info("Nenhuma transação registrada no extrato.")
    else:
        for _, row in df_tx.iterrows():
            is_saida = row["tipo"] == "Saída"
            sinal = "-" if is_saida else "+"
            cor = "#f87171" if is_saida else "#4ade80"
            c_tx_info, c_tx_acts = st.columns([4, 1.4])
            with c_tx_info:
                st.markdown(f"""
                <div style="background: #121a28; border: 1px solid #1f2d42; border-radius: 14px; padding: 10px 12px; margin-bottom: 6px; display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <div style="font-size: 0.82rem; font-weight: 700; color: #ffffff;">{row['descricao']}</div>
                        <div style="font-size: 0.65rem; color: #64748b;">{row['data']} • {row['banco']} ({row['meio']})</div>
                        <span style="font-size: 0.60rem; background: #1a2538; color: #38bdf8; padding: 2px 6px; border-radius: 4px;">{row['categoria']}</span>
                    </div>
                    <div style="font-family: 'JetBrains Mono'; font-weight: 700; font-size: 0.88rem; color: {cor};">
                        {sinal} R$ {row['valor']:,.2f}
                    </div>
                </div>
                """, unsafe_allow_html=True)
            with c_tx_acts:
                c_ed_t, c_dl_t = st.columns(2)
                with c_ed_t:
                    st.markdown('<div class="btn-action-icon" style="margin-top: 6px;">', unsafe_allow_html=True)
                    if st.button("✏️", key=f"ed_tx_{row['id']}", help="Editar lançamento"):
                        st.session_state.editando_tx_id = int(row["id"])
                        st.rerun()
                    st.markdown('</div>', unsafe_allow_html=True)
                with c_dl_t:
                    st.markdown('<div class="btn-clear" style="margin-top: 6px;">', unsafe_allow_html=True)
                    if st.button("🗑️", key=f"dl_tx_{row['id']}", help="Excluir lançamento"):
                        remover_transacao_extrato(int(row["id"]))
                        if st.session_state.editando_tx_id == int(row["id"]):
                            st.session_state.editando_tx_id = None
                        st.rerun()
                    st.markdown('</div>', unsafe_allow_html=True)

with tab_novo:
    st.markdown('<div class="sec-header">Lançamentos & Importações</div>', unsafe_allow_html=True)
    
    modo_lanc = st.radio("Como deseja lançar?", ["✍️ Manual", "📂 Importar Arquivo OFX"], horizontal=True, key="modo_lanc_radio")
    
    if modo_lanc == "✍️ Manual":
        with st.form("form_novo_lanc"):
            desc = st.text_input("Descrição", value="Mercado / Compra")
            val = st.number_input("Valor (R$)", value=25.00, min_value=0.01, step=1.0)
            banco = st.selectbox("Banco", df_bancos["banco"].tolist())
            
            info_b = df_bancos[df_bancos["banco"] == banco].iloc[0]
            opcoes_meio = ["Conta Corrente / Pix"]
            if info_b.get("tem_cartao", 1) == 1:
                opcoes_meio.insert(0, "Cartão de Crédito")
                
            meio = st.radio("Método", opcoes_meio, horizontal=True)
            cat = st.selectbox("Categoria", ["Alimentação", "Transporte", "Lazer", "Contas Fixas", "Saúde", "Outros"])
            tipo = st.selectbox("Tipo", ["Saída", "Entrada"])
            
            if st.form_submit_button("Confirmar Lançamento"):
                adicionar_transacao(datetime.now().strftime("%d/%m %H:%M"), desc, val, cat, banco, meio, tipo)
                st.success("Transação registrada com sucesso!")
                st.rerun()
                
    else:
        st.markdown("""
        <div style="background: #0d1522; border: 1px solid #1f2f47; border-radius: 12px; padding: 10px; margin-bottom: 12px;">
            <span style="font-size: 0.72rem; font-weight: 700; color: #38bdf8;">📥 IMPORTADOR OFX INTELIGENTE</span>
            <div style="font-size: 0.65rem; color: #94a3b8; margin-top: 2px; line-height: 1.3;">
                Suba o arquivo <strong>.OFX</strong> baixado do app do seu banco (extrato de conta corrente ou fatura de cartão de crédito). O sistema lê todas as movimentações e atualiza o saldo ou fatura correspondente automaticamente!
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        tipo_ofx = st.selectbox(
            "Tipo de Arquivo OFX:", 
            ["💳 Fatura de Cartão de Crédito", "🏦 Extrato de Conta Corrente"],
            key="sel_tipo_ofx"
        )
        
        # Filtra bancos pertinentes
        if "Cartão" in tipo_ofx:
            bancos_ofx = df_bancos[df_bancos["tem_cartao"] == 1]["banco"].tolist()
            if not bancos_ofx:
                bancos_ofx = df_bancos["banco"].tolist()
        else:
            bancos_ofx = df_bancos["banco"].tolist()
            
        banco_alvo = st.selectbox("Banco Pertencente:", bancos_ofx, key="banco_alvo_ofx")
        
        arquivo_ofx = st.file_uploader("Selecione o arquivo .OFX:", type=["ofx"], key="uploader_ofx")
        
        if arquivo_ofx is not None:
            try:
                raw_bytes = arquivo_ofx.read()
                try:
                    conteudo_ofx = raw_bytes.decode("utf-8")
                except UnicodeDecodeError:
                    conteudo_ofx = raw_bytes.decode("latin-1", errors="replace")
                    
                transacoes_ofx, saldo_ledger = parse_ofx_content(conteudo_ofx)
                
                if not transacoes_ofx:
                    st.warning("Nenhuma movimentação identificada no arquivo OFX. Verifique se o arquivo está no padrão bancário.")
                else:
                    # Totais do arquivo
                    total_debitos = sum(abs(t["valor"]) for t in transacoes_ofx if t["valor"] < 0)
                    total_creditos = sum(t["valor"] for t in transacoes_ofx if t["valor"] > 0)
                    
                    st.markdown(f"""
                    <div style="background: #111a28; border: 1px solid #1c2a3d; border-radius: 12px; padding: 10px; margin: 10px 0;">
                        <span style="font-size: 0.75rem; font-weight: 800; color: #ffffff;">📄 Resumo do Arquivo OFX:</span>
                        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 8px; margin-top: 6px;">
                            <div style="background: #0c121c; padding: 6px 8px; border-radius: 8px;">
                                <span style="font-size: 0.6rem; color: #94a3b8;">MOVIMENTAÇÕES</span>
                                <div style="font-family: 'JetBrains Mono'; font-weight: 800; font-size: 0.88rem; color: #38bdf8;">{len(transacoes_ofx)} itens</div>
                            </div>
                            <div style="background: #0c121c; padding: 6px 8px; border-radius: 8px;">
                                <span style="font-size: 0.6rem; color: #94a3b8;">{'TOTAL COMPRAS' if 'Cartão' in tipo_ofx else 'TOTAL DÉBITOS'}</span>
                                <div style="font-family: 'JetBrains Mono'; font-weight: 800; font-size: 0.88rem; color: #f87171;">R$ {total_debitos:,.2f}</div>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Opções de atualização
                    if "Cartão" in tipo_ofx:
                        st.markdown('<span style="font-size: 0.72rem; font-weight: 700; color: #38bdf8;">Ações para o Cartão:</span>', unsafe_allow_html=True)
                        atualizar_fatura = st.checkbox("Atualizar valor da Fatura deste Cartão com o total do OFX", value=True)
                        atualizar_extrato_cc = st.checkbox("Gravar todas as compras individuais no Extrato Geral", value=True)
                        
                        valor_final_fatura = abs(saldo_ledger) if (saldo_ledger is not None and saldo_ledger != 0) else total_debitos
                        st.caption(f"Valor a ser definido na fatura de **{banco_alvo}**: **R$ {valor_final_fatura:,.2f}**")
                        
                        if st.button("🚀 Processar e Alimentar Cartão", key="btn_proc_cartao_ofx"):
                            conn = sqlite3.connect("financas.db")
                            c = conn.cursor()
                            
                            if atualizar_fatura:
                                # Atualiza fatura atual e recalcula limite liberado se aplicável
                                c.execute("SELECT limite_cartao FROM contas_bancarias WHERE banco = ?", (banco_alvo,))
                                r_b = c.fetchone()
                                lim_total = r_b[0] if r_b else 0.0
                                novo_liberado = max(0.0, lim_total - valor_final_fatura)
                                c.execute("""
                                    UPDATE contas_bancarias 
                                    SET fatura_atual = ?, limite_liberado = ?
                                    WHERE banco = ?
                                """, (valor_final_fatura, novo_liberado, banco_alvo))
                                
                            if atualizar_extrato_cc:
                                novos_cc = 0
                                for tr in transacoes_ofx:
                                    fitid_val = tr.get("fitid", "")
                                    c.execute("SELECT COUNT(*) FROM transacoes WHERE fitid = ? AND banco = ? AND meio = 'Cartão de Crédito'", (fitid_val, banco_alvo))
                                    if c.fetchone()[0] == 0:
                                        val_trn = abs(tr["valor"])
                                        tipo_trn = "Saída" if tr["valor"] < 0 else "Entrada"
                                        c.execute("""
                                            INSERT INTO transacoes (data, descricao, valor, categoria, banco, meio, tipo, fitid)
                                            VALUES (?, ?, ?, 'OFX / Cartão', ?, 'Cartão de Crédito', ?, ?)
                                        """, (tr["data"], tr["descricao"], val_trn, banco_alvo, tipo_trn, fitid_val))
                                        novos_cc += 1
                                    
                            conn.commit()
                            conn.close()
                            st.success(f"Fatura e compras de {banco_alvo} alimentadas com sucesso pelo OFX!")
                            st.rerun()
                            
                    else:
                        st.markdown('<span style="font-size: 0.72rem; font-weight: 700; color: #38bdf8;">Ações para a Conta Corrente:</span>', unsafe_allow_html=True)
                        atualizar_saldo = st.checkbox("Atualizar Saldo em Conta deste Banco com o saldo do OFX", value=True)
                        atualizar_extrato_conta = st.checkbox("Gravar movimentações no Extrato Geral", value=True)
                        
                        valor_final_saldo = saldo_ledger if saldo_ledger is not None else (total_creditos - total_debitos)
                        st.caption(f"Saldo a ser definido na conta de **{banco_alvo}**: **R$ {valor_final_saldo:,.2f}**")
                        
                        if st.button("🚀 Processar e Alimentar Conta", key="btn_proc_conta_ofx"):
                            conn = sqlite3.connect("financas.db")
                            c = conn.cursor()
                            
                            if atualizar_saldo:
                                c.execute("""
                                    UPDATE contas_bancarias 
                                    SET saldo_conta = ?
                                    WHERE banco = ?
                                """, (valor_final_saldo, banco_alvo))
                                
                            if atualizar_extrato_conta:
                                novos_ct = 0
                                for tr in transacoes_ofx:
                                    fitid_val = tr.get("fitid", "")
                                    c.execute("SELECT COUNT(*) FROM transacoes WHERE fitid = ? AND banco = ? AND meio = 'Conta Corrente / Pix'", (fitid_val, banco_alvo))
                                    if c.fetchone()[0] == 0:
                                        val_trn = abs(tr["valor"])
                                        tipo_trn = "Saída" if tr["valor"] < 0 else "Entrada"
                                        c.execute("""
                                            INSERT INTO transacoes (data, descricao, valor, categoria, banco, meio, tipo, fitid)
                                            VALUES (?, ?, ?, 'OFX / Conta', ?, 'Conta Corrente / Pix', ?, ?)
                                        """, (tr["data"], tr["descricao"], val_trn, banco_alvo, tipo_trn, fitid_val))
                                        novos_ct += 1
                                    
                            conn.commit()
                            conn.close()
                            st.success(f"Saldo e movimentações de {banco_alvo} atualizados com sucesso pelo OFX!")
                            st.rerun()
                            
            except Exception as e:
                st.error(f"Erro ao processar o arquivo OFX: {e}")

with tab_ajustes:
    st.markdown('<div class="sec-header">Ajuste de Limites, Saldos & Cartões</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="btn-clear" style="margin-bottom: 12px;">', unsafe_allow_html=True)
    if st.button("⚠️ Zerar Todos os Saldos e Faturas", key="btn_zerar_saldos_tudo"):
        zerar_saldos_e_faturas()
        st.success("Saldos e faturas zerados!")
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    
    banco_edit = st.selectbox("Selecione o Banco para Configurar", df_bancos["banco"].tolist())
    row_banco = df_bancos[df_bancos["banco"] == banco_edit].iloc[0]
    
    with st.form("form_edit_saldo"):
        st.markdown(f'<div style="font-weight: 800; color: #38bdf8; margin-bottom: 8px;">Configurações de {banco_edit}</div>', unsafe_allow_html=True)
        
        possui_cartao = st.checkbox("💳 Possui Cartão de Crédito neste banco?", value=bool(row_banco.get("tem_cartao", 1)))
        
        novo_saldo = st.number_input("Saldo em Conta Corrente (R$)", value=float(row_banco["saldo_conta"]), step=10.0)
        lim_ch = st.number_input("Limite Cheque Especial (R$)", value=float(row_banco["limite_cheque_especial"]), step=100.0)
        ch_usado = st.number_input("Cheque Especial Usado (R$)", value=float(row_banco["cheque_especial_usado"]), step=10.0)
        
        if possui_cartao:
            st.markdown('<div style="font-size: 0.75rem; font-weight: 700; color: #94a3b8; margin-top: 10px;">Dados do Cartão de Crédito:</div>', unsafe_allow_html=True)
            c_crd1, c_crd2 = st.columns(2)
            with c_crd1:
                novo_lim = st.number_input("Limite Total do Cartão (R$)", value=float(row_banco["limite_cartao"]), step=100.0)
                nova_fat = st.number_input("Fatura Atual (R$)", value=float(row_banco["fatura_atual"]), step=10.0)
                dia_v = st.number_input("Dia do Vencimento", min_value=1, max_value=31, value=int(row_banco.get("dia_vencimento", 10)))
            with c_crd2:
                lim_lib_padrao = float(row_banco.get("limite_liberado", 0.0))
                if lim_lib_padrao == 0.0 and novo_lim > 0:
                    lim_lib_padrao = max(0.0, novo_lim - nova_fat)
                novo_lim_liberado = st.number_input("Limite Liberado (De Fato) (R$)", value=lim_lib_padrao, step=100.0)
                dia_f = st.number_input("Dia de Fechamento", min_value=1, max_value=31, value=int(row_banco.get("dia_fechamento", 3)))
        else:
            nova_fat = 0.0
            novo_lim = 0.0
            novo_lim_liberado = 0.0
            dia_v = int(row_banco.get("dia_vencimento", 10))
            dia_f = int(row_banco.get("dia_fechamento", 3))
            st.caption("ℹ️ Este banco não possui cartão. A tela principal ocultará a seção de fatura e limites.")
        
        if st.form_submit_button("Salvar Configurações"):
            atualizar_banco_completo(
                banco_edit, 
                1 if possui_cartao else 0, 
                nova_fat, 
                novo_lim, 
                novo_lim_liberado,
                novo_saldo, 
                lim_ch, 
                ch_usado, 
                dia_v, 
                dia_f
            )
            st.success("Configurações atualizadas!")
            st.rerun()


    st.markdown('<div class="sec-header" style="margin-top: 1.4rem;">Backup & Segurança dos Dados</div>', unsafe_allow_html=True)
    c_bk1, c_bk2 = st.columns(2)
    with c_bk1:
        if os.path.exists("financas.db"):
            with open("financas.db", "rb") as f_db:
                db_bytes = f_db.read()
            st.download_button(
                label="📥 Baixar Backup (.db)",
                data=db_bytes,
                file_name=f"backup_financas_{datetime.now().strftime('%Y_%m_%d')}.db",
                mime="application/octet-stream",
                key="btn_download_backup_db"
            )
    with c_bk2:
        up_db = st.file_uploader("Restaurar Backup (.db)", type=["db"], key="uploader_restore_db", label_visibility="collapsed")
        if up_db is not None:
            if st.button("📤 Restaurar Arquivo", key="btn_confirm_restore_db"):
                with open("financas.db", "wb") as f_out:
                    f_out.write(up_db.read())
                st.success("Banco de dados restaurado com sucesso!")
                st.rerun()
