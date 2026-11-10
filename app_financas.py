import streamlit as st
import pandas as pd
import sqlite3
import requests
from datetime import datetime

st.set_page_config(page_title="Minhas Finanças", page_icon="⚡", layout="centered")

# Estilo Moderno inspirado na estética modular e limpa do MacroDroid (Dark Card UI / Bento Grid)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;600;700&display=swap');

    * { 
        font-family: 'Plus Jakarta Sans', sans-serif !important; 
        box-sizing: border-box;
    }
    
    /* Fundo escuro fosco e suave */
    .stApp { 
        background: #0f131a !important; 
        color: #f1f5f9; 
    }
    
    .block-container { 
        max-width: 440px !important; 
        padding-top: 1rem !important; 
        padding-bottom: 3.5rem !important;
    }

    #MainMenu, footer, header { visibility: hidden; }

    /* Barra Superior / Header */
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
        background: #1e293b;
        color: #38bdf8;
        border: 1px solid #334155;
        padding: 6px 12px;
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

    /* Card Master Bento Style */
    .md-hero-card {
        background: linear-gradient(145deg, #1e293b 0%, #151d2a 100%);
        border: 1px solid #334155;
        border-radius: 22px;
        padding: 1.3rem;
        margin-bottom: 1.2rem;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3);
        position: relative;
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
        border-top: 1px solid #27354a;
        font-size: 0.75rem;
        color: #94a3b8;
    }

    /* Grid de Blocos Estilo MacroDroid Tiles */
    .tile-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 8px;
        margin-bottom: 1.4rem;
    }
    .md-tile {
        background: #182232;
        border: 1px solid #27364b;
        border-radius: 16px;
        padding: 12px 6px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        text-align: center;
        gap: 6px;
        transition: transform 0.15s ease;
    }
    .md-tile-icon {
        width: 38px;
        height: 38px;
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.1rem;
    }
    .icon-blue { background: #0369a1; color: #38bdf8; }
    .icon-orange { background: #9a3412; color: #fdba74; }
    .icon-emerald { background: #065f46; color: #6ee7b7; }
    .icon-purple { background: #6b21a8; color: #d8b4fe; }
    
    .md-tile-text {
        font-size: 0.66rem;
        font-weight: 700;
        color: #e2e8f0;
    }

    /* Lista de Instituições / Bancos */
    .sec-header {
        font-size: 0.75rem;
        font-weight: 800;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        margin: 1.2rem 0 0.8rem 0;
    }
    .bank-card {
        background: #151d2a;
        border: 1px solid #243247;
        border-radius: 18px;
        padding: 14px;
        margin-bottom: 10px;
        position: relative;
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
    .bank-stat {
        background: #0f1622;
        border: 1px solid #1e2c3f;
        border-radius: 12px;
        padding: 10px;
    }
    .bank-stat-full {
        grid-column: span 2;
        background: #0f1622;
        border: 1px solid #1e2c3f;
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
    .bank-msg {
        font-size: 0.65rem;
        font-weight: 600;
        margin-top: 3px;
    }

    /* Abas */
    .stTabs [data-baseweb="tab-list"] {
        gap: 6px;
        background-color: #151d2a;
        padding: 6px;
        border-radius: 16px;
        border: 1px solid #243247;
    }
    .stTabs [data-baseweb="tab"] {
        height: 36px;
        border-radius: 10px;
        color: #94a3b8;
        font-size: 0.72rem;
        font-weight: 700;
        border: none !important;
        background: transparent;
        padding: 0 10px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #243247 !important;
        color: #38bdf8 !important;
    }
    .stTabs [data-baseweb="tab-highlight"] { display: none; }

    /* Botão Primário */
    .stButton > button {
        width: 100%;
        background: linear-gradient(135deg, #0284c7 0%, #0369a1 100%) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 14px !important;
        font-weight: 800 !important;
        font-size: 0.86rem !important;
        padding: 0.7rem 1rem !important;
        box-shadow: 0 4px 15px rgba(2, 132, 199, 0.3) !important;
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
        CREATE TABLE IF NOT EXISTS contas_bancarias (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            banco TEXT UNIQUE,
            cor_identificador TEXT,
            tem_cartao INTEGER,
            limite_cartao REAL,
            fatura_atual REAL,
            saldo_conta REAL,
            limite_cheque_especial REAL,
            cheque_especial_usado REAL
        )
    """)
    c.execute("SELECT COUNT(*) FROM contas_bancarias")
    if c.fetchone()[0] == 0:
        bancos_dados = [
            ("Nubank", "#a855f7", 1, 5000.00, 1840.50, 0.00, 0.00, 0.00),
            ("Caixa Econômica", "#38bdf8", 1, 3500.00, 920.00, 1250.00, 2000.00, 350.00),
            ("Mercado Pago", "#22d3ee", 1, 2800.00, 430.00, 12.50, 1500.00, 0.00),
            ("Bradesco", "#f43f5e", 1, 4000.00, 780.00, -150.00, 1800.00, 500.00),
            ("Inter", "#fb923c", 1, 6000.00, 610.00, 4210.10, 1000.00, 0.00)
        ]
        c.executemany("""
            INSERT INTO contas_bancarias 
            (banco, cor_identificador, tem_cartao, limite_cartao, fatura_atual, saldo_conta, limite_cheque_especial, cheque_especial_usado)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, bancos_dados)
    conn.commit()
    conn.close()

init_db()

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

def atualizar_banco(banco, fatura, lim_cartao, saldo, lim_cheque, cheque_usado):
    conn = sqlite3.connect("financas.db")
    c = conn.cursor()
    c.execute("""
        UPDATE contas_bancarias 
        SET fatura_atual = ?, limite_cartao = ?, saldo_conta = ?, limite_cheque_especial = ?, cheque_especial_usado = ?
        WHERE banco = ?
    """, (fatura, lim_cartao, saldo, lim_cheque, cheque_usado, banco))
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

# Função de Mensagens Personalizadas de Saldo
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

total_faturas = df_bancos["fatura_atual"].sum()
total_saldos = df_bancos["saldo_conta"].sum()
total_cheque = df_bancos["cheque_especial_usado"].sum()

msg_total, classe_total = get_status_saldo(total_saldos)

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

# Master Hero Card
st.markdown(f"""
<div class="md-hero-card">
    <div class="md-hero-label">Patrimônio em Conta</div>
    <div class="md-hero-val">R$ {total_saldos:,.2f}</div>
    <div class="md-msg-pill {classe_total}">{msg_total}</div>
    <div class="md-hero-footer">
        <span>Faturas: <strong style="color: #ffffff;">R$ {total_faturas:,.2f}</strong></span>
        <span>Cheque Esp.: <strong style="color: #f87171;">R$ {total_cheque:,.2f}</strong></span>
    </div>
</div>
""", unsafe_allow_html=True)

# Grid de Ações / Blocos Estilo MacroDroid
st.markdown("""
<div class="tile-grid">
    <div class="md-tile">
        <div class="md-tile-icon icon-blue">💳</div>
        <span class="md-tile-text">Cartões</span>
    </div>
    <div class="md-tile">
        <div class="md-tile-icon icon-orange">🔄</div>
        <span class="md-tile-text">Pix</span>
    </div>
    <div class="md-tile">
        <div class="md-tile-icon icon-emerald">📊</div>
        <span class="md-tile-text">Gráficos</span>
    </div>
    <div class="md-tile">
        <div class="md-tile-icon icon-purple">⚡</div>
        <span class="md-tile-text">Extrato</span>
    </div>
</div>
""", unsafe_allow_html=True)

# Navegação por Abas
tab_bancos, tab_extrato, tab_novo, tab_ajustes = st.tabs([
    "Bancos", 
    "Extrato", 
    "Lançar", 
    "Ajustes"
])

with tab_bancos:
    st.markdown('<div class="sec-header">Contas & Cartões</div>', unsafe_allow_html=True)
    
    for _, b in df_bancos.iterrows():
        lim_disp = max(0.0, b["limite_cartao"] - b["fatura_atual"])
        b_saldo = b["saldo_conta"]
        msg_banco, cls_banco = get_status_saldo(b_saldo)
        
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
                    <div style="font-size: 0.62rem; color: #64748b; margin-top: 2px;">Disp: R$ {lim_disp:,.2f}</div>
                </div>
                <div class="bank-stat-full">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <span class="bank-stat-lbl">Cheque Especial Usado</span>
                        <span style="font-family: 'JetBrains Mono'; font-size: 0.85rem; font-weight: 700; color: {'#f87171' if b['cheque_especial_usado'] > 0 else '#94a3b8'};">
                            R$ {b['cheque_especial_usado']:,.2f}
                        </span>
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

with tab_extrato:
    st.markdown('<div class="sec-header">Movimentações Recentes</div>', unsafe_allow_html=True)
    if df_tx.empty:
        st.info("Nenhuma transação registrada.")
    else:
        for _, row in df_tx.iterrows():
            is_saida = row["tipo"] == "Saída"
            sinal = "-" if is_saida else "+"
            cor = "#f87171" if is_saida else "#4ade80"
            st.markdown(f"""
            <div style="background: #151d2a; border: 1px solid #243247; border-radius: 14px; padding: 12px; margin-bottom: 8px; display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <div style="font-size: 0.85rem; font-weight: 700; color: #ffffff;">{row['descricao']}</div>
                    <div style="font-size: 0.68rem; color: #64748b;">{row['data']} • {row['banco']}</div>
                </div>
                <div style="font-family: 'JetBrains Mono'; font-weight: 700; font-size: 0.9rem; color: {cor};">
                    {sinal} R$ {row['valor']:,.2f}
                </div>
            </div>
            """, unsafe_allow_html=True)

with tab_novo:
    st.markdown('<div class="sec-header">Nova Transação</div>', unsafe_allow_html=True)
    with st.form("form_novo_lanc"):
        desc = st.text_input("Descrição", value="Mercado / Compra")
        val = st.number_input("Valor (R$)", value=25.00, min_value=0.01, step=1.0)
        banco = st.selectbox("Banco", df_bancos["banco"].tolist())
        meio = st.radio("Método", ["Cartão de Crédito", "Conta Corrente / Pix"], horizontal=True)
        cat = st.selectbox("Categoria", ["Alimentação", "Transporte", "Lazer", "Contas Fixas", "Outros"])
        tipo = st.selectbox("Tipo", ["Saída", "Entrada"])
        
        if st.form_submit_button("Confirmar Lançamento"):
            adicionar_transacao(datetime.now().strftime("%d/%m %H:%M"), desc, val, cat, banco, meio, tipo)
            st.success("Transação registrada com sucesso!")
            st.rerun()

with tab_ajustes:
    st.markdown('<div class="sec-header">Ajuste de Valores Reais</div>', unsafe_allow_html=True)
    banco_edit = st.selectbox("Selecione o Banco", df_bancos["banco"].tolist())
    row_banco = df_bancos[df_bancos["banco"] == banco_edit].iloc[0]
    
    with st.form("form_edit_saldo"):
        novo_saldo = st.number_input("Saldo em Conta (R$)", value=float(row_banco["saldo_conta"]), step=10.0)
        nova_fat = st.number_input("Fatura do Cartão (R$)", value=float(row_banco["fatura_atual"]), step=10.0)
        novo_lim = st.number_input("Limite do Cartão (R$)", value=float(row_banco["limite_cartao"]), step=100.0)
        lim_ch = st.number_input("Limite Cheque Especial (R$)", value=float(row_banco["limite_cheque_especial"]), step=100.0)
        ch_usado = st.number_input("Cheque Especial Usado (R$)", value=float(row_banco["cheque_especial_usado"]), step=10.0)
        
        if st.form_submit_button("Salvar Valores"):
            atualizar_banco(banco_edit, nova_fat, novo_lim, novo_saldo, lim_ch, ch_usado)
            st.success("Valores atualizados!")
            st.rerun()
