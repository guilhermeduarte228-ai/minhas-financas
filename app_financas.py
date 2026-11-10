import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime

st.set_page_config(page_title="Finanças Pro", page_icon="⚡", layout="centered")

# Estilo Ultra-Moderno / Cyber Glassmorphism Fintech
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;600;700&display=swap');

    * { 
        font-family: 'Plus Jakarta Sans', sans-serif !important; 
        box-sizing: border-box;
    }
    
    .stApp { 
        background: radial-gradient(circle at 50% 0%, #061726 0%, #03070b 60%, #000204 100%) !important; 
        color: #f1f5f9; 
    }
    
    .block-container { 
        max-width: 440px !important; 
        padding-top: 1rem !important; 
        padding-bottom: 3rem !important;
    }

    /* Ocultar barra superior nativa e rodapés do Streamlit */
    #MainMenu, footer, header { visibility: hidden; }

    /* Topo / Header Futurista */
    .header-box { 
        display: flex; 
        justify-content: space-between; 
        align-items: center; 
        margin-bottom: 1.2rem; 
        padding: 4px 2px;
    }
    .user-name { 
        font-size: 1.35rem; 
        font-weight: 800; 
        color: #ffffff; 
        letter-spacing: -0.6px; 
        margin: 0; 
    }
    .user-subtitle { 
        font-size: 0.72rem; 
        color: #22d3ee; 
        margin-top: 3px; 
        font-weight: 600;
        letter-spacing: 0.4px;
        text-transform: uppercase;
    }
    
    .pill-badge {
        background: rgba(6, 182, 212, 0.08);
        color: #22d3ee;
        border: 1px solid rgba(6, 182, 212, 0.35);
        padding: 6px 14px;
        border-radius: 9999px;
        font-size: 0.68rem;
        font-weight: 700;
        letter-spacing: 0.5px;
        box-shadow: 0 0 16px rgba(6, 182, 212, 0.2);
        display: flex;
        align-items: center;
        gap: 6px;
    }
    .live-dot {
        width: 6px;
        height: 6px;
        background: #00f2fe;
        border-radius: 50%;
        box-shadow: 0 0 8px #00f2fe;
        display: inline-block;
    }

    /* Master Card Holográfico */
    .master-card {
        background: linear-gradient(135deg, rgba(8, 51, 68, 0.45) 0%, rgba(3, 10, 16, 0.85) 100%);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(34, 211, 238, 0.35);
        border-radius: 26px;
        padding: 1.5rem;
        box-shadow: 0 20px 45px -12px rgba(6, 182, 212, 0.22), inset 0 1px 0 rgba(255, 255, 255, 0.2);
        margin-bottom: 1.4rem;
        position: relative;
        overflow: hidden;
    }
    .master-card::after {
        content: '';
        position: absolute;
        top: -40%;
        right: -20%;
        width: 160px;
        height: 160px;
        background: radial-gradient(circle, rgba(6, 182, 212, 0.25) 0%, transparent 70%);
        pointer-events: none;
    }
    .master-tag { 
        font-size: 0.65rem; 
        font-weight: 800; 
        color: #67e8f9; 
        letter-spacing: 1.5px; 
        text-transform: uppercase; 
    }
    .master-val { 
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 2.2rem; 
        font-weight: 800; 
        color: #ffffff; 
        letter-spacing: -1px; 
        margin: 8px 0; 
        text-shadow: 0 0 20px rgba(6, 182, 212, 0.4);
    }
    .master-sub { 
        font-size: 0.74rem; 
        color: #94a3b8; 
        display: flex;
        justify-content: space-between;
        margin-top: 10px;
        padding-top: 10px;
        border-top: 1px solid rgba(255, 255, 255, 0.08);
    }

    /* Cards dos Bancos - Cyber Fintech */
    .sec-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin: 1.2rem 0 0.7rem 0;
    }
    .sec-title { 
        font-size: 0.72rem; 
        font-weight: 800; 
        color: #64748b; 
        text-transform: uppercase; 
        letter-spacing: 1.2px; 
    }
    
    .bank-card {
        background: linear-gradient(180deg, rgba(15, 23, 42, 0.65) 0%, rgba(8, 14, 23, 0.85) 100%);
        backdrop-filter: blur(14px);
        -webkit-backdrop-filter: blur(14px);
        border: 1px solid rgba(255, 255, 255, 0.07);
        border-radius: 20px;
        padding: 16px;
        margin-bottom: 12px;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
    }
    .bank-card:hover {
        border-color: rgba(34, 211, 238, 0.45);
        transform: translateY(-2px);
        box-shadow: 0 10px 25px -10px rgba(6, 182, 212, 0.25);
    }
    
    .bank-title-bar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 12px;
    }
    .bank-name-badge {
        font-size: 0.88rem;
        font-weight: 800;
        color: #ffffff;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    .bank-glow-pill {
        width: 10px;
        height: 10px;
        border-radius: 50%;
        box-shadow: 0 0 10px currentColor;
    }
    .bank-type-pill {
        font-size: 0.6rem;
        font-weight: 700;
        color: #06b6d4;
        background: rgba(6, 182, 212, 0.08);
        border: 1px solid rgba(6, 182, 212, 0.25);
        padding: 3px 8px;
        border-radius: 9999px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    /* Grid Interno dos Cartões e Contas */
    .metric-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 8px;
    }
    .metric-cell {
        background: rgba(3, 7, 18, 0.45);
        border: 1px solid rgba(255, 255, 255, 0.04);
        border-radius: 14px;
        padding: 10px 12px;
    }
    .metric-cell-full {
        grid-column: span 2;
        background: rgba(3, 7, 18, 0.55);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 14px;
        padding: 10px 12px;
    }
    
    .metric-label-row {
        display: flex;
        align-items: center;
        gap: 6px;
        font-size: 0.64rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.6px;
        color: #64748b;
    }
    .metric-value {
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 0.95rem;
        font-weight: 800;
        color: #ffffff;
        margin-top: 4px;
    }
    .metric-caption {
        font-size: 0.62rem;
        color: #64748b;
        margin-top: 2px;
    }

    /* Cores Neons Específicas */
    .color-fatura { color: #22d3ee; }
    .color-saldo { color: #34d399; }
    .color-alerta { color: #f59e0b; }
    .color-perigo { color: #f87171; }

    /* Estilização Moderna das Abas nativas do Streamlit */
    .stTabs [data-baseweb="tab-list"] {
        gap: 6px;
        background-color: rgba(15, 23, 42, 0.6);
        padding: 6px;
        border-radius: 16px;
        border: 1px solid rgba(255, 255, 255, 0.06);
    }
    .stTabs [data-baseweb="tab"] {
        height: 38px;
        border-radius: 12px;
        color: #94a3b8;
        font-size: 0.74rem;
        font-weight: 700;
        border: none !important;
        background: transparent;
        padding: 0 12px;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, rgba(6, 182, 212, 0.25) 0%, rgba(8, 51, 68, 0.6) 100%) !important;
        color: #22d3ee !important;
        border: 1px solid rgba(34, 211, 238, 0.4) !important;
        box-shadow: 0 0 15px rgba(6, 182, 212, 0.25);
    }
    .stTabs [data-baseweb="tab-highlight"] { display: none; }

    /* Estilização Futurista dos Botões de Ação */
    .stButton > button {
        width: 100%;
        background: linear-gradient(135deg, #06b6d4 0%, #0284c7 100%) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 14px !important;
        font-weight: 800 !important;
        font-size: 0.85rem !important;
        letter-spacing: 0.5px !important;
        padding: 0.65rem 1rem !important;
        box-shadow: 0 0 20px rgba(6, 182, 212, 0.35) !important;
        transition: all 0.2s ease !important;
    }
    .stButton > button:hover {
        transform: translateY(-1px) !important;
        box-shadow: 0 0 28px rgba(6, 182, 212, 0.5) !important;
    }

    /* Linhas do Extrato */
    .tx-item {
        background: rgba(15, 23, 42, 0.45);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 16px;
        padding: 12px 16px;
        margin-bottom: 8px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .tx-title { font-size: 0.86rem; font-weight: 700; color: #ffffff; margin: 0; }
    .tx-meta { font-size: 0.68rem; color: #64748b; margin-top: 3px; }
    .tx-tag { 
        font-size: 0.62rem; 
        color: #22d3ee; 
        background: rgba(6, 182, 212, 0.1); 
        border: 1px solid rgba(6, 182, 212, 0.2); 
        padding: 2px 8px; 
        border-radius: 6px; 
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

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
            tipo TEXT
        )
    """)
    # Migração retroativa de colunas
    c.execute("PRAGMA table_info(transacoes)")
    colunas = [col[1] for col in c.fetchall()]
    if "banco" not in colunas:
        c.execute("ALTER TABLE transacoes ADD COLUMN banco TEXT DEFAULT 'Nubank'")
    if "meio" not in colunas:
        c.execute("ALTER TABLE transacoes ADD COLUMN meio TEXT DEFAULT 'Cartão de Crédito'")

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
            ("Nubank", "#a855f7", 1, 5000.00, 1840.50, 450.00, 0.00, 0.00),
            ("Caixa Econômica", "#38bdf8", 1, 3500.00, 920.00, 1250.00, 2000.00, 350.00),
            ("Mercado Pago", "#22d3ee", 1, 2800.00, 430.00, 510.00, 1500.00, 0.00),
            ("Bradesco", "#f43f5e", 1, 4000.00, 780.00, 320.00, 1800.00, 500.00),
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

df_bancos = get_contas()
df_tx = get_transacoes()

total_faturas = df_bancos["fatura_atual"].sum()
total_saldos_conta = df_bancos["saldo_conta"].sum()
total_cheque_usado = df_bancos["cheque_especial_usado"].sum()

# Topo / Header
st.markdown("""
<div class="header-box">
    <div>
        <h2 class="user-name">Guilherme</h2>
        <div class="user-subtitle">Patrimônio Integrado</div>
    </div>
    <div class="pill-badge">
        <span class="live-dot"></span>
        5 Bancos Ativos
    </div>
</div>
""", unsafe_allow_html=True)

# Master Card com Iluminação Neomórfica
st.markdown(f"""
<div class="master-card">
    <div class="master-tag">Faturas de Cartão</div>
    <div class="master-val">R$ {total_faturas:,.2f}</div>
    <div class="master-sub">
        <span>Saldos: <strong style="color: #ffffff;">R$ {total_saldos_conta:,.2f}</strong></span>
        <span>Cheque Esp.: <strong style="color: #f59e0b;">R$ {total_cheque_usado:,.2f}</strong></span>
    </div>
</div>
""", unsafe_allow_html=True)

# Abas Navegação Futuristas
tab_bancos, tab_extrato, tab_novo, tab_ajustes = st.tabs([
    "Bancos", 
    "Extrato", 
    "Novo Gasto", 
    "Ajustes"
])

with tab_bancos:
    st.markdown('<div class="sec-title">Detalhamento por Instituição</div>', unsafe_allow_html=True)
    
    for _, b in df_bancos.iterrows():
        lim_disp = max(0.0, b["limite_cartao"] - b["fatura_atual"])
        st.markdown(f"""
        <div class="bank-card">
            <div class="bank-title-bar">
                <span class="bank-name-badge">
                    <span class="bank-glow-pill" style="background-color: {b['cor_identificador']}; color: {b['cor_identificador']};"></span>
                    {b['banco']}
                </span>
                <span class="bank-type-pill">Conta & Limite</span>
            </div>
            <div class="metric-grid">
                <div class="metric-cell">
                    <div class="metric-label-row color-fatura">💳 Fatura</div>
                    <div class="metric-value">R$ {b['fatura_atual']:,.2f}</div>
                    <div class="metric-caption">Disp: R$ {lim_disp:,.2f}</div>
                </div>
                <div class="metric-cell">
                    <div class="metric-label-row color-saldo">💰 Saldo</div>
                    <div class="metric-value">R$ {b['saldo_conta']:,.2f}</div>
                    <div class="metric-caption">Disponível</div>
                </div>
                <div class="metric-cell-full">
                    <div class="metric-label-row color-alerta">⚠️ Cheque Especial</div>
                    <div style="display: flex; justify-content: space-between; align-items: baseline; margin-top: 4px;">
                        <span class="metric-value" style="color: {'#f87171' if b['cheque_especial_usado'] > 0 else '#ffffff'}; font-size: 0.88rem;">
                            Usado: R$ {b['cheque_especial_usado']:,.2f}
                        </span>
                        <span style="font-size: 0.65rem; color: #94a3b8; font-weight: 600;">Limite: R$ {b['limite_cheque_especial']:,.2f}</span>
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

with tab_extrato:
    st.markdown('<div class="sec-title">Últimos Movimentos</div>', unsafe_allow_html=True)
    if df_tx.empty:
        st.info("Nenhuma movimentação registrada.")
    else:
        for _, row in df_tx.iterrows():
            is_saida = row["tipo"] == "Saída"
            sinal = "-" if is_saida else "+"
            cls_v = "color-perigo" if is_saida else "color-saldo"
            banco_nome = row.get("banco", "Banco")
            meio_nome = row.get("meio", "Operação")
            st.markdown(f"""
            <div class="tx-item">
                <div>
                    <p class="tx-title">{row["descricao"]}</p>
                    <p class="tx-meta">{row["data"]} • {banco_nome} ({meio_nome})</p>
                    <span class="tx-tag">{row["categoria"]}</span>
                </div>
                <div class="metric-value {cls_v}">{sinal} R$ {row["valor"]:,.2f}</div>
            </div>
            """, unsafe_allow_html=True)

with tab_novo:
    st.markdown('<div class="sec-title">Registrar Movimentação</div>', unsafe_allow_html=True)
    with st.form("form_novo_lancamento"):
        desc = st.text_input("Descrição / Estabelecimento", value="Restaurante / Compra")
        val = st.number_input("Valor (R$)", value=45.00, min_value=0.01, step=1.0)
        banco = st.selectbox("Instituição", df_bancos["banco"].tolist())
        meio = st.radio("Método", ["Cartão de Crédito", "Conta Corrente / Pix"], horizontal=True)
        cat = st.selectbox("Categoria", ["Alimentação", "Transporte", "Saúde", "Contas Fixas", "Lazer", "Renda", "Outros"])
        tipo = st.selectbox("Tipo de Operação", ["Saída", "Entrada"])
        
        if st.form_submit_button("⚡ Registrar Transação"):
            adicionar_transacao(
                datetime.now().strftime("%d %b, %H:%M"), 
                desc, 
                val, 
                cat, 
                banco, 
                meio, 
                tipo
            )
            st.success("Operação realizada com sucesso!")
            st.rerun()

with tab_ajustes:
    st.markdown('<div class="sec-title">Ajuste de Limites & Contratos</div>', unsafe_allow_html=True)
    banco_edit = st.selectbox("Selecionar Banco", df_bancos["banco"].tolist())
    linha = df_bancos[df_bancos["banco"] == banco_edit].iloc[0]
    
    with st.form("form_edit_banco"):
        fat = st.number_input("Fatura Atual do Cartão (R$)", value=float(linha["fatura_atual"]), step=50.0)
        lim_c = st.number_input("Limite Concedido do Cartão (R$)", value=float(linha["limite_cartao"]), step=100.0)
        sal = st.number_input("Saldo Disponível em Conta (R$)", value=float(linha["saldo_conta"]), step=50.0)
        lim_ch = st.number_input("Limite de Cheque Especial (R$)", value=float(linha["limite_cheque_especial"]), step=100.0)
        ch_usado = st.number_input("Cheque Especial Consumido (R$)", value=float(linha["cheque_especial_usado"]), step=50.0)
        
        if st.form_submit_button("💾 Salvar Parâmetros"):
            atualizar_banco(banco_edit, fat, lim_c, sal, lim_ch, ch_usado)
            st.success(f"Parâmetros de {banco_edit} atualizados!")
            st.rerun()
