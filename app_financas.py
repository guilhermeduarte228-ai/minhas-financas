import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime

st.set_page_config(page_title="Finanças Pro", page_icon="💳", layout="centered")

# Estilo Obsidiana com Detalhes Turquesa Neon
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

    * { font-family: 'Plus Jakarta Sans', sans-serif !important; }
    .stApp { background: radial-gradient(circle at 50% 0%, #08151f 0%, #04070a 100%) !important; color: #f8fafc; }
    .block-container { max-width: 440px !important; padding-top: 1rem !important; }

    /* Cabeçalho */
    .header-box { display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.2rem; }
    .user-name { font-size: 1.35rem; font-weight: 700; color: #ffffff; letter-spacing: -0.5px; margin: 0; }
    .user-subtitle { font-size: 0.72rem; color: #06b6d4; margin-top: 2px; font-weight: 500; }
    .badge-status { background: rgba(6, 182, 212, 0.1); color: #22d3ee; border: 1px solid rgba(6, 182, 212, 0.3); padding: 5px 12px; border-radius: 9999px; font-size: 0.68rem; font-weight: 600; }

    /* Card Master Geral Glassmorphic */
    .budget-card {
        background: linear-gradient(135deg, rgba(8, 51, 68, 0.45) 0%, rgba(4, 7, 10, 0.8) 100%);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(6, 182, 212, 0.35);
        border-radius: 22px;
        padding: 1.4rem;
        box-shadow: 0 15px 35px -10px rgba(6, 182, 212, 0.2), inset 0 1px 0 rgba(255, 255, 255, 0.15);
        margin-bottom: 1.2rem;
    }
    .budget-tag { font-size: 0.68rem; font-weight: 700; color: #67e8f9; letter-spacing: 1.2px; text-transform: uppercase; }
    .budget-val { font-size: 2.1rem; font-weight: 800; color: #ffffff; letter-spacing: -1px; margin: 6px 0; }
    .budget-sub { font-size: 0.75rem; color: #94a3b8; }

    /* Cards Individuais dos Bancos */
    .sec-title { font-size: 0.76rem; font-weight: 700; color: #64748b; text-transform: uppercase; letter-spacing: 0.8px; margin: 1rem 0 0.6rem 0; }
    
    .bank-card-container {
        background: rgba(15, 23, 42, 0.55);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 18px;
        padding: 14px 16px;
        margin-bottom: 10px;
        transition: transform 0.2s ease;
    }
    .bank-card-container:hover { border-color: rgba(6, 182, 212, 0.4); }
    .bank-header-row { display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; }
    .bank-title-badge { font-size: 0.82rem; font-weight: 700; color: #ffffff; display: flex; align-items: center; gap: 8px; }
    .bank-dot { width: 8px; height: 8px; border-radius: 50%; display: inline-block; }
    
    .detail-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; font-size: 0.72rem; }
    .detail-item { background: rgba(0, 0, 0, 0.35); padding: 8px 10px; border-radius: 12px; border: 1px solid rgba(255, 255, 255, 0.04); }
    .detail-label { color: #64748b; font-size: 0.62rem; text-transform: uppercase; font-weight: 700; }
    .detail-val { font-size: 0.86rem; font-weight: 800; color: #ffffff; margin-top: 2px; }

    .tag-cheque { color: #f59e0b; font-size: 0.65rem; font-weight: 600; }
    .tag-fatura { color: #22d3ee; font-size: 0.65rem; font-weight: 600; }

    /* Extrato Clean */
    .tx-row {
        background: rgba(15, 23, 42, 0.4);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 16px;
        padding: 12px 15px;
        margin-bottom: 8px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .tx-name { font-size: 0.84rem; font-weight: 600; color: #ffffff; margin: 0; }
    .tx-info { font-size: 0.68rem; color: #64748b; margin-top: 2px; }
    .tx-tag { font-size: 0.62rem; color: #22d3ee; background: rgba(6, 182, 212, 0.1); border: 1px solid rgba(6, 182, 212, 0.2); padding: 2px 7px; border-radius: 6px; }
    .tx-loss { font-size: 0.9rem; font-weight: 700; color: #f87171; }
    .tx-gain { font-size: 0.9rem; font-weight: 700; color: #34d399; }
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
            banco TEXT,
            meio TEXT,
            tipo TEXT
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
    conn.commit()
    
    # Cria os 5 bancos com valores iniciais se ainda não existirem
    c.execute("SELECT COUNT(*) FROM contas_bancarias")
    if c.fetchone()[0] == 0:
        bancos_dados = [
            ("Nubank", "#a855f7", 1, 5000.00, 1840.50, 450.00, 0.00, 0.00),
            ("Caixa Econômica", "#3b82f6", 1, 3500.00, 920.00, 1250.00, 2000.00, 350.00),
            ("Mercado Pago", "#06b6d4", 1, 2800.00, 430.00, 510.00, 1500.00, 0.00),
            ("Bradesco", "#ef4444", 1, 4000.00, 780.00, 320.00, 1800.00, 500.00),
            ("Inter", "#f97316", 1, 6000.00, 610.00, 4210.10, 1000.00, 0.00)
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

# Cabeçalho
st.markdown("""
<div class="header-box">
    <div>
        <h2 class="user-name">Olá, Guilherme 👋</h2>
        <p class="user-subtitle">Patrimônio & Cartões Integrados</p>
    </div>
    <div class="badge-status">5 Bancos Ativos</div>
</div>
""", unsafe_allow_html=True)

# Card de Resumo Geral com Iluminação Turquesa
st.markdown(f"""
<div class="budget-card">
    <div class="budget-tag">TOTAL EM FATURAS DE CARTÃO</div>
    <div class="budget-val">R$ {total_faturas:,.2f}</div>
    <div class="budget-sub">
        Saldo em Contas: <b style="color: #ffffff;">R$ {total_saldos_conta:,.2f}</b> | 
        Cheque Esp. Usado: <b style="color: #f59e0b;">R$ {total_cheque_usado:,.2f}</b>
    </div>
</div>
""", unsafe_allow_html=True)

# Abas de navegação
aba_bancos, aba_extrato, aba_nova, aba_ajustes = st.tabs([
    "🏦 Bancos & Cartões", 
    "📜 Extrato", 
    "⚡ Novo Gasto", 
    "⚙️ Ajustar Limites"
])

with aba_bancos:
    st.markdown('<div class="sec-title">Controle Detalhado por Banco</div>', unsafe_allow_html=True)
    
    for idx, b in df_bancos.iterrows():
        lim_disp = max(0.0, b["limite_cartao"] - b["fatura_atual"])
        st.markdown(f"""
        <div class="bank-card-container">
            <div class="bank-header-row">
                <span class="bank-title-badge">
                    <span class="bank-dot" style="background-color: {b['cor_identificador']};"></span>
                    {b['banco']}
                </span>
                <span style="font-size: 0.72rem; color: #64748b;">Cartão & Cheque Especial</span>
            </div>
            <div class="detail-grid">
                <div class="detail-item">
                    <div class="detail-label tag-fatura">💳 Fatura Atual</div>
                    <div class="detail-val">R$ {b['fatura_atual']:,.2f}</div>
                    <div style="font-size: 0.6rem; color: #64748b;">Limite Disp: R$ {lim_disp:,.2f}</div>
                </div>
                <div class="detail-item">
                    <div class="detail-label" style="color: #34d399;">💰 Saldo em Conta</div>
                    <div class="detail-val">R$ {b['saldo_conta']:,.2f}</div>
                    <div style="font-size: 0.6rem; color: #64748b;">Disponível</div>
                </div>
                <div class="detail-item" style="grid-column: span 2;">
                    <div class="detail-label tag-cheque">⚠️ Cheque Especial</div>
                    <div style="display: flex; justify-content: space-between; align-items: baseline;">
                        <span class="detail-val" style="color: {'#ef4444' if b['cheque_especial_usado'] > 0 else '#ffffff'}; font-size: 0.8rem;">
                            Usado: R$ {b['cheque_especial_usado']:,.2f}
                        </span>
                        <span style="font-size: 0.65rem; color: #94a3b8;">Limite: R$ {b['limite_cheque_especial']:,.2f}</span>
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

with aba_extrato:
    st.caption("ÚLTIMOS LANÇAMENTOS REGISTRADOS")
    if df_tx.empty:
        st.info("Nenhuma transação registrada ainda.")
    for idx, row in df_tx.iterrows():
        is_saida = row["tipo"] == "Saída"
        sinal = "-" if is_saida else "+"
        cls_v = "tx-loss" if is_saida else "tx-gain"
        st.markdown(f"""
        <div class="tx-row">
            <div>
                <p class="tx-name">{row["descricao"]}</p>
                <p class="tx-info">{row["data"]} • {row["banco"]} ({row["meio"]})</p>
                <span class="tx-tag">{row["categoria"]}</span>
            </div>
            <div><p class="{cls_v}">{sinal} R$ {row["valor"]:,.2f}</p></div>
        </div>
        """, unsafe_allow_html=True)

with aba_nova:
    st.markdown("#### Registrar Transação")
    with st.form("form_novo_lancamento"):
        desc = st.text_input("Estabelecimento ou Descrição", value="Compra")
        val = st.number_input("Valor (R$)", value=25.00, min_value=0.01, step=1.0)
        banco = st.selectbox("Instituição Bancária", df_bancos["banco"].tolist())
        meio = st.radio("Forma de Pagamento", ["Cartão de Crédito", "Conta Corrente / Pix"], horizontal=True)
        cat = st.selectbox("Categoria", ["Alimentação", "Transporte", "Saúde", "Contas Fixas", "Lazer", "Renda", "Outros"])
        tipo = st.selectbox("Tipo de Operação", ["Saída", "Entrada"])
        
        if st.form_submit_button("⚡ Salvar Lançamento"):
            adicionar_transacao(
                datetime.now().strftime("%d Nov, %H:%M"), 
                desc, 
                val, 
                cat, 
                banco, 
                meio, 
                tipo
            )
            st.success("Transação gravada com sucesso!")
            st.rerun()

with aba_ajustes:
    st.markdown("#### ⚙️ Ajustar Limites e Saldos Reais")
    banco_edit = st.selectbox("Selecione o Banco", df_bancos["banco"].tolist())
    linha = df_bancos[df_bancos["banco"] == banco_edit].iloc[0]
    
    with st.form("form_edit_banco"):
        fat = st.number_input("Fatura Atual do Cartão (R$)", value=float(linha["fatura_atual"]), step=50.0)
        lim_c = st.number_input("Limite Total do Cartão (R$)", value=float(linha["limite_cartao"]), step=100.0)
        sal = st.number_input("Saldo em Conta Corrente (R$)", value=float(linha["saldo_conta"]), step=50.0)
        lim_ch = st.number_input("Limite do Cheque Especial (R$)", value=float(linha["limite_cheque_especial"]), step=100.0)
        ch_usado = st.number_input("Cheque Especial Usado (R$)", value=float(linha["cheque_especial_usado"]), step=50.0)
        
        if st.form_submit_button("💾 Atualizar Banco"):
            atualizar_banco(banco_edit, fat, lim_c, sal, lim_ch, ch_usado)
            st.success(f"Dados do {banco_edit} atualizados!")
            st.rerun()
