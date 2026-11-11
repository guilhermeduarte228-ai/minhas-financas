import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime, date
from dateutil.relativedelta import relativedelta

st.set_page_config(page_title="Minhas Finanças", page_icon="⚡", layout="centered")

# Estilo Moderno Dark Bento UI / MacroDroid
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;600;700&display=swap');

    * { 
        font-family: 'Plus Jakarta Sans', sans-serif !important; 
        box-sizing: border-box;
    }
    
    .stApp { 
        background: #0b0f17 !important; 
        color: #f1f5f9; 
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
    .recursos-wrapper div[data-testid="column"] button {
        background: #141d2a !important;
        border: 1px solid #223247 !important;
        border-radius: 14px !important;
        color: #f1f5f9 !important;
        font-size: 0.68rem !important;
        font-weight: 700 !important;
        padding: 0.45rem 0.1rem !important;
        min-height: 46px !important;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2) !important;
        transition: all 0.2s ease !important;
        white-space: nowrap !important;
    }
    .recursos-wrapper div[data-testid="column"] button:hover {
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

    /* Card Item de Previsão */
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
        gap: 6px;
        background-color: #121a28;
        padding: 6px;
        border-radius: 16px;
        border: 1px solid #1f2d42;
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
        CREATE TABLE IF NOT EXISTS reembolsos_destinados (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data TEXT,
            valor_total REAL,
            detalhes TEXT
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
            cheque_especial_usado REAL,
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
    
    # Migrações seguras: Inter -> Itaú e Mercado Pago Amarelo
    c.execute("UPDATE contas_bancarias SET banco = 'Itaú', cor_identificador = '#ec7000' WHERE banco = 'Inter'")
    c.execute("UPDATE transacoes SET banco = 'Itaú' WHERE banco = 'Inter'")
    c.execute("UPDATE contas_bancarias SET cor_identificador = '#ffe600' WHERE banco = 'Mercado Pago'")
    
    c.execute("SELECT COUNT(*) FROM contas_bancarias")
    if c.fetchone()[0] == 0:
        bancos_dados = [
            ("Nubank", "#a855f7", 1, 5000.00, 1954.00, 0.00, 0.00, 0.00, 10, 3),
            ("Caixa Econômica", "#38bdf8", 1, 3500.00, 0.00, 0.00, 2000.00, 0.00, 15, 8),
            ("Mercado Pago", "#ffe600", 1, 2800.00, 0.00, 0.00, 1500.00, 0.00, 5, 28),
            ("Bradesco", "#f43f5e", 1, 4000.00, 0.00, 0.00, 1800.00, 0.00, 20, 13),
            ("Itaú", "#ec7000", 1, 6000.00, 0.00, 0.00, 1000.00, 0.00, 25, 18)
        ]
        c.executemany("""
            INSERT INTO contas_bancarias 
            (banco, cor_identificador, tem_cartao, limite_cartao, fatura_atual, saldo_conta, limite_cheque_especial, cheque_especial_usado, dia_vencimento, dia_fechamento)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
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

def get_previstos():
    conn = sqlite3.connect("financas.db")
    df = pd.read_sql_query("SELECT * FROM lancamentos_previstos ORDER BY data_prevista ASC", conn)
    conn.close()
    return df

def get_historico_reembolsos():
    conn = sqlite3.connect("financas.db")
    df = pd.read_sql_query("SELECT * FROM reembolsos_destinados ORDER BY id DESC", conn)
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
    conn = sqlite3.connect("financas.db")
    c = conn.cursor()
    c.execute("""
        UPDATE lancamentos_previstos
        SET data_prevista = ?, descricao = ?, valor = ?, categoria = ?, tipo = ?, banco = ?, fixo = ?
        WHERE id = ?
    """, (data_str, desc, valor, cat, tipo, banco, fixo, id_prev))
    conn.commit()
    conn.close()

def remover_previsto(id_prev):
    conn = sqlite3.connect("financas.db")
    c = conn.cursor()
    c.execute("DELETE FROM lancamentos_previstos WHERE id = ?", (id_prev,))
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

def atualizar_banco(banco, fatura, lim_cartao, saldo, lim_cheque, cheque_usado, dia_venc, dia_fech):
    conn = sqlite3.connect("financas.db")
    c = conn.cursor()
    c.execute("""
        UPDATE contas_bancarias 
        SET fatura_atual = ?, limite_cartao = ?, saldo_conta = ?, limite_cheque_especial = ?, cheque_especial_usado = ?, dia_vencimento = ?, dia_fechamento = ?
        WHERE banco = ?
    """, (fatura, lim_cartao, saldo, lim_cheque, cheque_usado, dia_venc, dia_fech, banco))
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

# Executa o rateio e abate direto do reembolso
def aplicar_destinacao_reembolso(data_str, valor_total, lista_destinos):
    conn = sqlite3.connect("financas.db")
    c = conn.cursor()
    logs = []
    
    for item in lista_destinos:
        banco = item["banco"]
        acao = item["acao"]
        val = float(item["valor"])
        motivo = item["motivo"]
        
        if val <= 0:
            continue
            
        logs.append(f"{banco}: R$ {val:,.2f} ({motivo} -> {acao})")
        
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
    c.execute("""
        INSERT INTO reembolsos_destinados (data, valor_total, detalhes)
        VALUES (?, ?, ?)
    """, (data_str, valor_total, detalhe_geral))
    
    conn.commit()
    conn.close()

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
df_reemb_hist = get_historico_reembolsos()

total_faturas = df_bancos["fatura_atual"].sum()
total_saldos = df_bancos["saldo_conta"].sum()
total_cheque = df_bancos["cheque_especial_usado"].sum()

msg_total, classe_total = get_status_saldo(total_saldos)

if "bloco_ativo" not in st.session_state:
    st.session_state.bloco_ativo = "destinar_reembolso"

if "mostrar_form_prev" not in st.session_state:
    st.session_state.mostrar_form_prev = False

if "editando_id" not in st.session_state:
    st.session_state.editando_id = None

if "copiando_prev" not in st.session_state:
    st.session_state.copiando_prev = None

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

# RECURSOS RÁPIDOS
st.markdown('<div class="sec-header">Recursos Rápidos</div>', unsafe_allow_html=True)
st.markdown('<div class="recursos-wrapper">', unsafe_allow_html=True)
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    if st.button("⛽ Destinar", key="btn_km"):
        st.session_state.bloco_ativo = "destinar_reembolso" if st.session_state.bloco_ativo != "destinar_reembolso" else None

with col2:
    if st.button("📅 Previsões", key="btn_prev"):
        st.session_state.bloco_ativo = "previstos" if st.session_state.bloco_ativo != "previstos" else None

with col3:
    if st.button("🧠 Advisor", key="btn_adv"):
        st.session_state.bloco_ativo = "advisor" if st.session_state.bloco_ativo != "advisor" else None

with col4:
    if st.button("💳 Venc.", key="btn_venc"):
        st.session_state.bloco_ativo = "vencimentos" if st.session_state.bloco_ativo != "vencimentos" else None

with col5:
    if st.button("📊 Gráficos", key="btn_graf"):
        st.session_state.bloco_ativo = "graficos" if st.session_state.bloco_ativo != "graficos" else None
st.markdown('</div>', unsafe_allow_html=True)

# ================= ÁREA DINÂMICA =================
if st.session_state.bloco_ativo == "destinar_reembolso":
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
        <div style="font-size: 0.72rem; font-weight: 700; color: #38bdf8; text-transform: uppercase;">Como funciona o rateio de reembolso:</div>
        <div style="font-size: 0.68rem; color: #94a3b8; margin-top: 4px; line-height: 1.4;">
            Recebeu o reembolso da empresa? Digite o valor total que caiu e <strong>distribua diretamente para onde o dinheiro deve ir</strong>. O app abate automaticamente a fatura do cartão usado no pedágio, repõe o cheque especial usado no combustível e deixa o lucro das diárias (R$ 100/dia) livre na conta!
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Calculadora auxiliar de estimativa
    with st.expander("🧮 Calculadora de Estimativa (R$ 130/dia + Pedágios)", expanded=False):
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

    with st.form("form_rateio_reembolso"):
        st.markdown('<div style="font-size: 0.8rem; font-weight: 800; color: #ffffff; margin-bottom: 8px;">1. Entrada Total de Reembolso Recebido:</div>', unsafe_allow_html=True)
        c_v1, c_v2 = st.columns(2)
        with c_v1:
            data_receb = st.date_input("Data do Recebimento", value=date.today())
        with c_v2:
            valor_total_recebido = st.number_input("Valor Total que Caiu (R$)", min_value=0.01, value=778.00, step=20.0)

        st.markdown('<div style="font-size: 0.8rem; font-weight: 800; color: #38bdf8; margin: 12px 0 6px 0;">2. Destinar o Valor para Abates e Saldo:</div>', unsafe_allow_html=True)
        st.caption("Preencha onde cada fatia do dinheiro será aplicada (o valor é descontado imediatamente na conta/fatura selecionada):")

        # Destino 1 (Ex: Pagar Pedágio no Cartão de Crédito)
        st.markdown('<div style="background: #111a28; padding: 10px; border-radius: 12px; margin-bottom: 8px; border: 1px solid #1c2a3d;">', unsafe_allow_html=True)
        st.markdown('<span style="font-size: 0.72rem; font-weight: 700; color: #38bdf8;">🎯 Destino A (Ex: Pedágio no Cartão)</span>', unsafe_allow_html=True)
        c_a1, c_a2, c_a3 = st.columns([1.5, 2.0, 1.5])
        with c_a1:
            banco_a = st.selectbox("Banco", df_bancos["banco"].tolist(), index=df_bancos["banco"].tolist().index("Nubank") if "Nubank" in df_bancos["banco"].tolist() else 0, key="b_a")
        with c_a2:
            acao_a = st.selectbox("Ação", ["Pagar/Abater Fatura de Cartão", "Abater Cheque Especial", "Creditar em Conta Corrente"], index=0, key="ac_a")
        with c_a3:
            val_a = st.number_input("Valor (R$)", min_value=0.0, value=128.00, step=10.0, key="v_a")
        motivo_a = st.text_input("Motivo / Identificação", value="Pedágio da semana (Cartão)", key="m_a")
        st.markdown('</div>', unsafe_allow_html=True)

        # Destino 2 (Ex: Repor Cheque Especial ou Gasolina)
        st.markdown('<div style="background: #111a28; padding: 10px; border-radius: 12px; margin-bottom: 8px; border: 1px solid #1c2a3d;">', unsafe_allow_html=True)
        st.markdown('<span style="font-size: 0.72rem; font-weight: 700; color: #fbbf24;">🎯 Destino B (Ex: Repor Gasolina / Cheque Especial)</span>', unsafe_allow_html=True)
        c_b1, c_b2, c_b3 = st.columns([1.5, 2.0, 1.5])
        with c_b1:
            banco_b = st.selectbox("Banco", df_bancos["banco"].tolist(), index=df_bancos["banco"].tolist().index("Bradesco") if "Bradesco" in df_bancos["banco"].tolist() else 0, key="b_b")
        with c_b2:
            acao_b = st.selectbox("Ação", ["Abater Cheque Especial", "Pagar/Abater Fatura de Cartão", "Creditar em Conta Corrente"], index=0, key="ac_b")
        with c_b3:
            val_b = st.number_input("Valor (R$)", min_value=0.0, value=150.00, step=10.0, key="v_b")
        motivo_b = st.text_input("Motivo / Identificação", value="Gasolina tirada do Cheque Especial", key="m_b")
        st.markdown('</div>', unsafe_allow_html=True)

        # Destino 3 (Ex: Lucro Limpo / Renda Livre das Diárias)
        sobra_lucro = max(0.0, valor_total_recebido - (val_a + val_b))
        st.markdown('<div style="background: #111a28; padding: 10px; border-radius: 12px; margin-bottom: 8px; border: 1px solid #1c2a3d;">', unsafe_allow_html=True)
        st.markdown('<span style="font-size: 0.72rem; font-weight: 700; color: #4ade80;">🎯 Destino C (Ex: Renda Livre / Diárias de R$ 100)</span>', unsafe_allow_html=True)
        c_c1, c_c2, c_c3 = st.columns([1.5, 2.0, 1.5])
        with c_c1:
            banco_c = st.selectbox("Banco", df_bancos["banco"].tolist(), index=df_bancos["banco"].tolist().index("Itaú") if "Itaú" in df_bancos["banco"].tolist() else 0, key="b_c")
        with c_c2:
            acao_c = st.selectbox("Ação", ["Creditar em Conta Corrente", "Pagar/Abater Fatura de Cartão", "Abater Cheque Especial"], index=0, key="ac_c")
        with c_c3:
            val_c = st.number_input("Valor (R$)", min_value=0.0, value=float(sobra_lucro), step=10.0, key="v_c")
        motivo_c = st.text_input("Motivo / Identificação", value="Renda livre das diárias", key="m_c")
        st.markdown('</div>', unsafe_allow_html=True)

        if st.form_submit_button("🚀 Executar Entrada & Destinar Automaticamente"):
            destinos = [
                {"banco": banco_a, "acao": acao_a, "valor": val_a, "motivo": motivo_a},
                {"banco": banco_b, "acao": acao_b, "valor": val_b, "motivo": motivo_b},
                {"banco": banco_c, "acao": acao_c, "valor": val_c, "motivo": motivo_c}
            ]
            aplicar_destinacao_reembolso(data_receb.strftime("%Y-%m-%d"), valor_total_recebido, destinos)
            st.success("Reembolso distribuído com sucesso! Os valores foram abatidos e creditados nos bancos correspondentes.")
            st.rerun()

    # Histórico de Distribuições
    if not df_reemb_hist.empty:
        st.markdown('<div style="font-size: 0.72rem; font-weight: 700; color: #64748b; text-transform: uppercase; margin: 12px 0 6px 0;">Histórico de Reembolsos Destinados:</div>', unsafe_allow_html=True)
        for _, row_h in df_reemb_hist.iterrows():
            st.markdown(f"""
            <div style="background: #0d1522; border: 1px solid #1a273b; border-radius: 12px; padding: 10px; margin-bottom: 6px;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <span style="font-size: 0.8rem; font-weight: 700; color: #ffffff;">📅 {row_h['data']}</span>
                    <span style="font-family: 'JetBrains Mono'; font-weight: 800; font-size: 0.88rem; color: #4ade80;">Total: R$ {row_h['valor_total']:,.2f}</span>
                </div>
                <div style="font-size: 0.65rem; color: #94a3b8; margin-top: 4px; line-height: 1.4;">
                    {row_h['detalhes']}
                </div>
            </div>
            """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

elif st.session_state.bloco_ativo == "previstos":
    entradas_previstas = df_prev[df_prev["tipo"] == "Entrada"]["valor"].sum() if not df_prev.empty else 0.0
    saidas_previstas = df_prev[df_prev["tipo"] == "Saída"]["valor"].sum() if not df_prev.empty else 0.0
    saldo_projetado = total_saldos + entradas_previstas - saidas_previstas
    
    st.markdown('<div class="panel-box">', unsafe_allow_html=True)
    
    # Barra de controle do painel
    c_tit, c_limp, c_fech = st.columns([3, 2, 1])
    with c_tit:
        st.markdown('<span style="font-weight: 800; color: #38bdf8; font-size: 0.92rem;">📅 Lançamentos Previstos</span>', unsafe_allow_html=True)
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

    # COMPARATIVO ATUAL VS PROJETADO
    st.markdown(f"""
    <div style="background: #0d1522; border: 1px solid #1f2f47; border-radius: 14px; padding: 12px; margin: 10px 0 14px 0;">
        <div style="font-size: 0.68rem; font-weight: 700; color: #94a3b8; text-transform: uppercase;">Comparativo: Atual vs. Projetado</div>
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-top: 8px;">
            <div style="background: #111a28; padding: 10px; border-radius: 10px; border: 1px solid #1c2a3d;">
                <span style="font-size: 0.62rem; color: #64748b; font-weight: 700;">SALDO ATUAL</span>
                <div style="font-family: 'JetBrains Mono'; font-size: 1.05rem; font-weight: 800; color: #ffffff;">R$ {total_saldos:,.2f}</div>
            </div>
            <div style="background: #111a28; padding: 10px; border-radius: 10px; border: 1px solid #1c2a3d;">
                <span style="font-size: 0.62rem; color: #38bdf8; font-weight: 700;">SALDO PROJETADO</span>
                <div style="font-family: 'JetBrains Mono'; font-size: 1.05rem; font-weight: 800; color: {'#4ade80' if saldo_projetado >= 0 else '#f87171'};">
                    R$ {saldo_projetado:,.2f}
                </div>
            </div>
        </div>
        <div style="display: flex; justify-content: space-between; font-size: 0.68rem; color: #94a3b8; margin-top: 8px; padding-top: 8px; border-top: 1px solid #1c2a3d;">
            <span>A Receber: <strong style="color: #4ade80;">+ R$ {entradas_previstas:,.2f}</strong></span>
            <span>A Pagar: <strong style="color: #f87171;">- R$ {saidas_previstas:,.2f}</strong></span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # MODAL / FORM DE COPIAR DESPESA PARA OUTRO MÊS
    if st.session_state.copiando_prev is not None:
        c_origem = st.session_state.copiando_prev
        st.markdown("""
        <div style="background: #101c2e; border: 1px solid #a855f7; border-radius: 14px; padding: 12px; margin-bottom: 14px;">
            <span style="font-size: 0.82rem; font-weight: 800; color: #a855f7;">📋 Duplicar / Copiar Lançamento para Outro Mês</span>
        """, unsafe_allow_html=True)
        with st.form("form_copiar_previsto"):
            dt_base_copia = datetime.strptime(c_origem["data_prevista"], "%Y-%m-%d").date() + relativedelta(months=1)
            c_cp1, c_cp2 = st.columns(2)
            with c_cp1:
                nova_data = st.date_input("Nova Data de Vencimento/Entrada", value=dt_base_copia)
                novo_val = st.number_input("Valor Ajustado (R$)", min_value=0.01, value=float(c_origem["valor"]), step=10.0)
            with c_cp2:
                nova_desc = st.text_input("Descrição", value=c_origem["descricao"])
                idx_banco_c = df_bancos["banco"].tolist().index(c_origem["banco"]) if c_origem["banco"] in df_bancos["banco"].tolist() else 0
                novo_banco = st.selectbox("Banco", df_bancos["banco"].tolist(), index=idx_banco_c)
            
            c_salv_cp, c_canc_cp = st.columns(2)
            with c_salv_cp:
                if st.form_submit_button("📋 Confirmar e Lançar no Mês"):
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
                        st.success("Lançamento atualizado com sucesso!")
                        st.rerun()
                with c_canc:
                    if st.form_submit_button("✕ Cancelar Edição"):
                        st.session_state.editando_id = None
                        st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

    # Alternar exibição do Formulário
    btn_txt = "➖ Ocultar Formulário" if st.session_state.mostrar_form_prev else "➕ Agendar Novo Lançamento"
    if st.button(btn_txt, key="toggle_form_prev"):
        st.session_state.mostrar_form_prev = not st.session_state.mostrar_form_prev
        st.rerun()

    if st.session_state.mostrar_form_prev:
        with st.form("form_add_previsto"):
            st.markdown('<div style="font-size: 0.75rem; font-weight: 700; color: #38bdf8; margin-bottom: 8px;">Dados do Lançamento Futuro:</div>', unsafe_allow_html=True)
            c_p1, c_p2 = st.columns(2)
            with c_p1:
                data_sel = st.date_input("Data de Início", value=date.today())
                tipo_prev = st.selectbox("Tipo de Operação", ["Entrada", "Saída"])
                valor_prev = st.number_input("Valor Estimado (R$)", min_value=0.01, value=1500.00, step=50.0)
            with c_p2:
                desc_prev = st.text_input("Descrição", value="Salário / Pix / Boleto")
                banco_prev = st.selectbox("Banco Envolvido", df_bancos["banco"].tolist())
                cat_prev = st.selectbox("Categoria", ["Renda", "Salário", "Fatura", "Contas Fixas", "Lazer", "Outros"])
            
            st.markdown('<div style="margin-top: 6px; padding: 8px; background: #0d1522; border-radius: 10px; border: 1px solid #1a273b;">', unsafe_allow_html=True)
            fixo_check = st.checkbox("📌 Fixar Renda/Gasto Recorrente (Mesmo dia todos os meses)")
            meses_qtd = st.slider("Repetir por quantos meses consecutivos?", min_value=1, max_value=12, value=1)
            st.caption("Exemplo: replique por vários meses e copie despesas variáveis conforme necessário.")
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

    # Lista de Previsões Agendadas
    st.markdown('<div style="font-size: 0.72rem; font-weight: 700; color: #64748b; text-transform: uppercase; margin: 12px 0 6px 0;">Previsões no Calendário:</div>', unsafe_allow_html=True)
    if df_prev.empty:
        st.info("Nenhuma previsão agendada. Toque no botão acima para adicionar uma nova.")
    else:
        for idx, row_p in df_prev.iterrows():
            is_ent = row_p["tipo"] == "Entrada"
            sinal_p = "+" if is_ent else "-"
            cor_p = "#4ade80" if is_ent else "#f87171"
            tag_fixo = " • 📌 Fixa" if row_p.get("fixo", 0) == 1 else ""
            
            col_info, col_botoes = st.columns([3.4, 2.6])
            with col_info:
                st.markdown(f"""
                <div class="prev-item-card" style="margin-bottom: 6px;">
                    <div>
                        <div style="font-size: 0.78rem; font-weight: 700; color: #ffffff;">{row_p['descricao']}</div>
                        <div style="font-size: 0.63rem; color: #94a3b8;">📅 {row_p['data_prevista']} • {row_p['banco']}{tag_fixo}</div>
                    </div>
                    <div style="font-family: 'JetBrains Mono'; font-weight: 800; font-size: 0.85rem; color: {cor_p}; text-align: right;">
                        {sinal_p} R$ {row_p['valor']:,.2f}
                    </div>
                </div>
                """, unsafe_allow_html=True)
            with col_botoes:
                c_cp, c_ed, c_del = st.columns(3)
                with c_cp:
                    st.markdown('<div class="btn-action-icon" style="margin-top: 4px;">', unsafe_allow_html=True)
                    if st.button("📋", key=f"btn_cp_{row_p['id']}", help="Copiar esta despesa/renda para outro mês"):
                        st.session_state.copiando_prev = row_p.to_dict()
                        st.session_state.editando_id = None
                        st.rerun()
                    st.markdown('</div>', unsafe_allow_html=True)
                with c_ed:
                    st.markdown('<div class="btn-action-icon" style="margin-top: 4px;">', unsafe_allow_html=True)
                    if st.button("✏️", key=f"btn_edit_{row_p['id']}", help="Editar este lançamento"):
                        st.session_state.editando_id = row_p["id"]
                        st.session_state.copiando_prev = None
                        st.rerun()
                    st.markdown('</div>', unsafe_allow_html=True)
                with c_del:
                    st.markdown('<div class="btn-clear" style="margin-top: 4px;">', unsafe_allow_html=True)
                    if st.button("🗑️", key=f"del_p_{row_p['id']}", help="Remover esta previsão"):
                        remover_previsto(row_p["id"])
                        if st.session_state.editando_id == row_p["id"]:
                            st.session_state.editando_id = None
                        st.rerun()
                    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

elif st.session_state.bloco_ativo == "advisor":
    st.markdown('<div class="panel-box">', unsafe_allow_html=True)
    c_tit, c_fech = st.columns([5, 1])
    with c_tit:
        st.markdown('<span style="font-weight: 800; color: #38bdf8; font-size: 0.92rem;">🧠 Advisor • Diagnóstico de Saúde Financeira</span>', unsafe_allow_html=True)
    with c
