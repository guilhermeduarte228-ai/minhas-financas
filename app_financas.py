import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime, date

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
    div[data-testid="column"] button {
        background: #141d2a !important;
        border: 1px solid #223247 !important;
        border-radius: 14px !important;
        color: #f1f5f9 !important;
        font-size: 0.72rem !important;
        font-weight: 700 !important;
        padding: 0.55rem 0.1rem !important;
        min-height: 48px !important;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2) !important;
        transition: all 0.2s ease !important;
        white-space: nowrap !important;
    }
    div[data-testid="column"] button:hover {
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

    /* Painel Expansível de Detalhe */
    .panel-box {
        background: #141e2e;
        border: 1px solid #23354f;
        border-radius: 18px;
        padding: 16px;
        margin-top: 0.8rem;
        margin-bottom: 1.4rem;
    }

    /* Insight Card */
    .insight-card {
        background: #0d1522;
        border: 1px solid #1d2d42;
        border-left: 4px solid #38bdf8;
        border-radius: 12px;
        padding: 12px;
        margin-bottom: 10px;
    }
    .insight-title {
        font-size: 0.82rem;
        font-weight: 700;
        color: #ffffff;
        display: flex;
        align-items: center;
        gap: 6px;
    }
    .insight-desc {
        font-size: 0.72rem;
        color: #94a3b8;
        margin-top: 4px;
        line-height: 1.4;
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

    /* Botão Primário Formulários */
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
            banco TEXT DEFAULT 'Nubank'
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
    
    # Migrações: Inter -> Itaú e cor do Mercado Pago Amarela
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
    
    c.execute("SELECT COUNT(*) FROM lancamentos_previstos")
    if c.fetchone()[0] == 0:
        previstos_ex = [
            (datetime.now().strftime("%Y-%m-05"), "Salário / Rendimentos", 4500.00, "Renda", "Entrada", "Itaú"),
            (datetime.now().strftime("%Y-%m-10"), "Fatura de Cartão", 1954.00, "Fatura", "Saída", "Nubank"),
            (datetime.now().strftime("%Y-%m-15"), "Freelance / Extra", 800.00, "Renda", "Entrada", "Mercado Pago"),
            (datetime.now().strftime("%Y-%m-20"), "Aluguel & Contas", 1400.00, "Contas Fixas", "Saída", "Caixa Econômica")
        ]
        c.executemany("""
            INSERT INTO lancamentos_previstos (data_prevista, descricao, valor, categoria, tipo, banco)
            VALUES (?, ?, ?, ?, ?, ?)
        """, previstos_ex)

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

def adicionar_previsto(data_str, desc, valor, cat, tipo, banco):
    conn = sqlite3.connect("financas.db")
    c = conn.cursor()
    c.execute("""
        INSERT INTO lancamentos_previstos (data_prevista, descricao, valor, categoria, tipo, banco)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (data_str, desc, valor, cat, tipo, banco))
    conn.commit()
    conn.close()

def remover_previsto(id_prev):
    conn = sqlite3.connect("financas.db")
    c = conn.cursor()
    c.execute("DELETE FROM lancamentos_previstos WHERE id = ?", (id_prev,))
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

total_faturas = df_bancos["fatura_atual"].sum()
total_saldos = df_bancos["saldo_conta"].sum()
total_cheque = df_bancos["cheque_especial_usado"].sum()

msg_total, classe_total = get_status_saldo(total_saldos)

if "bloco_ativo" not in st.session_state:
    st.session_state.bloco_ativo = "previstos"

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
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    if st.button("📅 Previsões", key="btn_prev", help="Lançamentos futuros, salários e comparativo"):
        st.session_state.bloco_ativo = "previstos" if st.session_state.bloco_ativo != "previstos" else None

with col2:
    if st.button("🧠 Advisor", key="btn_adv", help="Diagnóstico e orientações inteligentes"):
        st.session_state.bloco_ativo = "advisor" if st.session_state.bloco_ativo != "advisor" else None

with col3:
    if st.button("💳 Venc.", key="btn_venc", help="Configurar datas de vencimento das faturas"):
        st.session_state.bloco_ativo = "vencimentos" if st.session_state.bloco_ativo != "vencimentos" else None

with col4:
    if st.button("📊 Gráficos", key="btn_graf", help="Gráficos dinâmicos de gastos"):
        st.session_state.bloco_ativo = "graficos" if st.session_state.bloco_ativo != "graficos" else None

with col5:
    if st.button("⚖️ Limites", key="btn_lim", help="Visualizar cheque especial e limites"):
        st.session_state.bloco_ativo = "limites" if st.session_state.bloco_ativo != "limites" else None

# ÁREA DINÂMICA
if st.session_state.bloco_ativo == "previstos":
    entradas_previstas = df_prev[df_prev["tipo"] == "Entrada"]["valor"].sum() if not df_prev.empty else 0.0
    saidas_previstas = df_prev[df_prev["tipo"] == "Saída"]["valor"].sum() if not df_prev.empty else 0.0
    saldo_projetado = total_saldos + entradas_previstas - saidas_previstas
    
    st.markdown("""
    <div class="panel-box">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
            <span style="font-weight: 800; color: #38bdf8; font-size: 0.92rem;">📅 Lançamentos Previstos & Comparativo</span>
            <span style="font-size: 0.65rem; color: #94a3b8;">Projeção Futura</span>
        </div>
    """, unsafe_allow_html=True)
    
    # COMPARATIVO ATUAL VS PROJETADO
    st.markdown(f"""
    <div style="background: #0d1522; border: 1px solid #1f2f47; border-radius: 14px; padding: 12px; margin-bottom: 14px;">
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
    
    # Formulário com Calendário Interativo
    with st.expander("➕ Agendar Novo Lançamento Previsto", expanded=False):
        c_p1, c_p2 = st.columns(2)
        with c_p1:
            data_sel = st.date_input("Data Prevista", value=date.today())
            tipo_prev = st.selectbox("Tipo de Operação", ["Entrada", "Saída"])
            valor_prev = st.number_input("Valor Estimado (R$)", min_value=0.01, value=1500.00, step=50.0)
        with c_p2:
            desc_prev = st.text_input("Descrição", value="Salário / Pix / Conta")
            banco_prev = st.selectbox("Banco Destino/Origem", df_bancos["banco"].tolist())
            cat_prev = st.selectbox("Categoria", ["Renda", "Salário", "Fatura", "Contas Fixas", "Lazer", "Outros"])
            
        if st.button("Salvar Previsão no Calendário"):
            adicionar_previsto(data_sel.strftime("%Y-%m-%d"), desc_prev, valor_prev, cat_prev, tipo_prev, banco_prev)
            st.success("Lançamento previsto registrado com sucesso!")
            st.rerun()

    # Lista de Previsões Agendadas
    if not df_prev.empty:
        st.markdown('<div style="font-size: 0.72rem; font-weight: 700; color: #64748b; text-transform: uppercase; margin: 10px 0 6px 0;">Previsões no Calendário:</div>', unsafe_allow_html=True)
        for _, row_p in df_prev.iterrows():
            is_ent = row_p["tipo"] == "Entrada"
            sinal_p = "+" if is_ent else "-"
            cor_p = "#4ade80" if is_ent else "#f87171"
            col_info, col_del = st.columns([5, 1])
            with col_info:
                st.markdown(f"""
                <div style="background: #0d1522; border: 1px solid #1a273b; border-radius: 10px; padding: 8px 12px; margin-bottom: 6px; display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <div style="font-size: 0.8rem; font-weight: 700; color: #ffffff;">{row_p['descricao']}</div>
                        <div style="font-size: 0.65rem; color: #94a3b8;">📅 {row_p['data_prevista']} • {row_p['banco']} ({row_p['categoria']})</div>
                    </div>
                    <div style="font-family: 'JetBrains Mono'; font-weight: 800; font-size: 0.88rem; color: {cor_p};">
                        {sinal_p} R$ {row_p['valor']:,.2f}
                    </div>
                </div>
                """, unsafe_allow_html=True)
            with col_del:
                if st.button("🗑️", key=f"del_prev_{row_p['id']}", help="Excluir previsão"):
                    remover_previsto(row_p["id"])
                    st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

elif st.session_state.bloco_ativo == "advisor":
    st.markdown("""
    <div class="panel-box">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
            <span style="font-weight: 800; color: #38bdf8; font-size: 0.92rem;">🧠 Advisor • Diagnóstico de Saúde Financeira</span>
            <span style="font-size: 0.65rem; color: #94a3b8;">Análise Inteligente</span>
        </div>
    """, unsafe_allow_html=True)
    
    diagnosticos = []
    
    # 1. Cheque Especial
    if total_cheque > 0:
        diagnosticos.append({
            "titulo": "⚠️ Alerta Crítico: Cheque Especial Ativo",
            "tipo": "danger",
            "desc": f"Você está utilizando R$ {total_cheque:,.2f} do limite emergencial. Os juros do cheque especial estão entre os mais caros do mercado (até 8% ao mês). Priorize liquidar este saldo antes de qualquer outro investimento ou gasto supérfluo."
        })
    else:
        diagnosticos.append({
            "titulo": "✅ Cheque Especial Zerado",
            "tipo": "success",
            "desc": "Parabéns! Nenhuma das suas contas bancárias está consumindo limite emergencial ou pagando juros abusivos."
        })
        
    # 2. Relação Fatura vs. Saldo
    if total_saldos < total_faturas:
        deficit = total_faturas - total_saldos
        diagnosticos.append({
            "titulo": "🚨 Faturas Maiores que o Saldo Disponível",
            "tipo": "danger",
            "desc": f"Suas faturas somam R$ {total_faturas:,.2f}, enquanto seu saldo total é de R$ {total_saldos:,.2f} (diferença de R$ {deficit:,.2f}). Se os salários ou recebimentos previstos não cobrirem essa quantia até o vencimento, você corre risco de refinanciamento rotativo."
        })
    else:
        folga = total_saldos - total_faturas
        diagnosticos.append({
            "titulo": "🛡️ Faturas Cobertas com Folga",
            "tipo": "success",
            "desc": f"Seu saldo disponível quita 100% das suas faturas atuais e ainda sobram R$ {folga:,.2f} livres em caixa."
        })
        
    # 3. Concentração de Cartão
    if not df_bancos.empty:
        maior_fatura = df_bancos.sort_values(by="fatura_atual", ascending=False).iloc[0]
        if maior_fatura["fatura_atual"] > 0:
            pct_maior = (maior_fatura["fatura_atual"] / total_faturas) * 100 if total_faturas > 0 else 0
            if pct_maior >= 65:
                diagnosticos.append({
                    "titulo": f"📊 Concentração de Gastos no {maior_fatura['banco']}",
                    "tipo": "warning",
                    "desc": f"{maior_fatura['banco']} representa {pct_maior:.0f}% de toda a sua fatura consolidada. Centralizar gastos ajuda a pontuar, mas exige atenção redobrada à data de fechamento para não embolar compras em meses subsequentes."
                })

    # 4. Regra de Ouro / Indicação Inteligente
    diagnosticos.append({
        "titulo": "💡 Regra dos 3 Dias de Antecedência",
        "tipo": "info",
        "desc": "Transfira o valor das faturas para a conta corrente do respectivo banco pelo menos 24 a 48 horas úteis antes do vencimento para evitar que atrasos no Pix ou fins de semana gerem encargos por atraso."
    })
    
    for diag in diagnosticos:
        cor_borda = "#38bdf8"
        if diag["tipo"] == "danger": cor_borda = "#f87171"
        elif diag["tipo"] == "warning": cor_borda = "#fbbf24"
        elif diag["tipo"] == "success": cor_borda = "#4ade80"
        
        st.markdown(f"""
        <div class="insight-card" style="border-left-color: {cor_borda};">
            <div class="insight-title">{diag['titulo']}</div>
            <div class="insight-desc">{diag['desc']}</div>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("</div>", unsafe_allow_html=True)

elif st.session_state.bloco_ativo == "vencimentos":
    st.markdown("""
    <div class="panel-box">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
            <span style="font-weight: 800; color: #38bdf8; font-size: 0.9rem;">💳 Vencimento & Fechamento das Faturas</span>
            <span style="font-size: 0.65rem; color: #94a3b8;">Configuração Rápida</span>
        </div>
    """, unsafe_allow_html=True)
    
    banco_venc = st.selectbox("Selecione o Cartão para Configurar", df_bancos["banco"].tolist(), key="sel_banco_venc")
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
    st.markdown("""
    <div class="panel-box">
        <div style="font-weight: 800; color: #38bdf8; font-size: 0.9rem; margin-bottom: 10px;">
            📊 Análise Dinâmica dos Seus Gastos
        </div>
    """, unsafe_allow_html=True)
    
    df_gastos = df_tx[df_tx["tipo"] == "Saída"]
    
    if df_gastos.empty:
        st.info("Sem despesas cadastradas para compor os gráficos.")
    else:
        tipo_graf = st.radio("Visualizar Por:", ["Categoria", "Banco / Cartão"], horizontal=True)
        
        if tipo_graf == "Categoria":
            cat_series = df_gastos.groupby("categoria")["valor"].sum()
            st.caption("Total de gastos por categoria:")
            st.bar_chart(cat_series)
        else:
            banco_series = df_gastos.groupby("banco")["valor"].sum()
            st.caption("Distribuição de gastos por instituição:")
            st.bar_chart(banco_series)
            
        st.markdown(f"**Total computado no gráfico:** R$ {df_gastos['valor'].sum():,.2f}")
    st.markdown("</div>", unsafe_allow_html=True)

elif st.session_state.bloco_ativo == "limites":
    st.markdown("""
    <div class="panel-box">
        <div style="font-weight: 800; color: #38bdf8; font-size: 0.9rem; margin-bottom: 10px;">
            ⚖️ Diagnóstico de Limites & Cheque Especial
        </div>
    """, unsafe_allow_html=True)
    total_lim_cartao = df_bancos["limite_cartao"].sum()
    total_disp_cartao = max(0.0, total_lim_cartao - total_faturas)
    
    st.markdown(f"""
    - **Limite Total de Crédito:** R$ {total_lim_cartao:,.2f}
    - **Crédito Livre para Compras:** R$ {total_disp_cartao:,.2f}
    - **Cheque Especial Utilizado:** <span style="color: {'#f87171' if total_cheque > 0 else '#4ade80'}; font-weight: 700;">R$ {total_cheque:,.2f}</span>
    """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# Abas Principais
tab_bancos, tab_extrato, tab_novo, tab_ajustes = st.tabs([
    "Bancos", 
    "Extrato Completo", 
    "Lançar", 
    "Ajustes"
])

with tab_bancos:
    st.markdown('<div class="sec-header">Contas & Cartões</div>', unsafe_allow_html=True)
    
    for _, b in df_bancos.iterrows():
        lim_disp = max(0.0, b["limite_cartao"] - b["fatura_atual"])
        b_saldo = b["saldo_conta"]
        msg_banco, cls_banco = get_status_saldo(b_saldo)
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
                <div class="bank-stat-full">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <span class="bank-stat-lbl">Limite Cartão Livre</span>
                            <div style="font-size: 0.8rem; font-weight: 700; color: #ffffff;">R$ {lim_disp:,.2f}</div>
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

with tab_extrato:
    st.markdown('<div class="sec-header">Histórico Geral de Lançamentos</div>', unsafe_allow_html=True)
    if df_tx.empty:
        st.info("Nenhuma transação registrada.")
    else:
        for _, row in df_tx.iterrows():
            is_saida = row["tipo"] == "Saída"
            sinal = "-" if is_saida else "+"
            cor = "#f87171" if is_saida else "#4ade80"
            st.markdown(f"""
            <div style="background: #121a28; border: 1px solid #1f2d42; border-radius: 14px; padding: 12px; margin-bottom: 8px; display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <div style="font-size: 0.85rem; font-weight: 700; color: #ffffff;">{row['descricao']}</div>
                    <div style="font-size: 0.68rem; color: #64748b;">{row['data']} • {row['banco']} ({row['meio']})</div>
                    <span style="font-size: 0.62rem; background: #1a2538; color: #38bdf8; padding: 2px 6px; border-radius: 4px;">{row['categoria']}</span>
                </div>
                <div style="font-family: 'JetBrains Mono'; font-weight: 700; font-size: 0.9rem; color: {cor};">
                    {sinal} R$ {row['valor']:,.2f}
                </div>
            </div>
            """, unsafe_allow_html=True)

with tab_novo:
    st.markdown('<div class="sec-header">Nova Transação Manual</div>', unsafe_allow_html=True)
    with st.form("form_novo_lanc"):
        desc = st.text_input("Descrição", value="Mercado / Compra")
        val = st.number_input("Valor (R$)", value=25.00, min_value=0.01, step=1.0)
        banco = st.selectbox("Banco", df_bancos["banco"].tolist())
        meio = st.radio("Método", ["Cartão de Crédito", "Conta Corrente / Pix"], horizontal=True)
        cat = st.selectbox("Categoria", ["Alimentação", "Transporte", "Lazer", "Contas Fixas", "Saúde", "Outros"])
        tipo = st.selectbox("Tipo", ["Saída", "Entrada"])
        
        if st.form_submit_button("Confirmar Lançamento"):
            adicionar_transacao(datetime.now().strftime("%d/%m %H:%M"), desc, val, cat, banco, meio, tipo)
            st.success("Transação registrada com sucesso!")
            st.rerun()

with tab_ajustes:
    st.markdown('<div class="sec-header">Ajuste de Limites, Saldos & Datas</div>', unsafe_allow_html=True)
    banco_edit = st.selectbox("Selecione o Banco", df_bancos["banco"].tolist())
    row_banco = df_bancos[df_bancos["banco"] == banco_edit].iloc[0]
    
    with st.form("form_edit_saldo"):
        novo_saldo = st.number_input("Saldo em Conta (R$)", value=float(row_banco["saldo_conta"]), step=10.0)
        nova_fat = st.number_input("Fatura do Cartão (R$)", value=float(row_banco["fatura_atual"]), step=10.0)
        novo_lim = st.number_input("Limite do Cartão (R$)", value=float(row_banco["limite_cartao"]), step=100.0)
        lim_ch = st.number_input("Limite Cheque Especial (R$)", value=float(row_banco["limite_cheque_especial"]), step=100.0)
        ch_usado = st.number_input("Cheque Especial Usado (R$)", value=float(row_banco["cheque_especial_usado"]), step=10.0)
        dia_v = st.number_input("Dia do Vencimento da Fatura", min_value=1, max_value=31, value=int(row_banco.get("dia_vencimento", 10)))
        dia_f = st.number_input("Dia de Fechamento da Fatura", min_value=1, max_value=31, value=int(row_banco.get("dia_fechamento", 3)))
        
        if st.form_submit_button("Salvar Todos os Dados"):
            atualizar_banco(banco_edit, nova_fat, novo_lim, novo_saldo, lim_ch, ch_usado, dia_v, dia_f)
            st.success("Valores e vencimentos atualizados!")
            st.rerun()
