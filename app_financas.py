import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime

st.set_page_config(page_title="Carteira Inteligente", page_icon="💳", layout="centered")

# Injeção de CSS para recriar fielmente o design mobile dark do mockup
st.markdown("""
<style>
    .stApp { background-color: #090d16; color: #f8fafc; }
    .block-container { max-width: 480px !important; padding-top: 1.5rem !important; }
    .header-box { display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.2rem; }
    .user-name { font-size: 1.3rem; font-weight: 700; color: #ffffff; margin: 0; }
    .user-subtitle { font-size: 0.75rem; color: #64748b; margin: 0; }
    .badge-status { background-color: #064e3b; color: #34d399; border: 1px solid #059669; padding: 4px 10px; border-radius: 20px; font-size: 0.7rem; font-weight: 600; display: inline-flex; align-items: center; gap: 5px; }
    .pulse { width: 6px; height: 6px; background-color: #34d399; border-radius: 50%; display: inline-block; }
    .budget-card { background: linear-gradient(135deg, #1e1b4b 0%, #0f172a 100%); border: 1px solid #4338ca; border-radius: 18px; padding: 1.25rem; margin-bottom: 0.8rem; box-shadow: 0 8px 20px rgba(67, 56, 202, 0.25); }
    .budget-tag { font-size: 0.72rem; font-weight: 700; color: #a5b4fc; text-transform: uppercase; margin-bottom: 4px; }
    .budget-val { font-size: 1.9rem; font-weight: 800; color: #ffffff; margin: 0; line-height: 1.2; }
    .budget-sub { font-size: 0.74rem; color: #c7d2fe; margin-top: 6px; }
    .bank-row { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-top: 1rem; margin-bottom: 1.2rem; }
    .bank-card { border-radius: 14px; padding: 0.85rem; display: flex; flex-direction: column; justify-content: space-between; }
    .bank-nu { background: linear-gradient(135deg, #581c87 0%, #2e1065 100%); border: 1px solid #a855f7; }
    .bank-in { background: linear-gradient(135deg, #7c2d12 0%, #431407 100%); border: 1px solid #ea580c; }
    .bank-name { font-size: 0.85rem; font-weight: 700; color: #ffffff; margin: 0; }
    .bank-desc { font-size: 0.68rem; color: #cbd5e1; margin-bottom: 6px; }
    .bank-amt { font-size: 0.95rem; font-weight: 800; color: #ffffff; margin: 0; }
    .tx-row { background-color: #111827; border: 1px solid #1f2937; border-radius: 14px; padding: 0.85rem 1rem; margin-bottom: 0.6rem; display: flex; justify-content: space-between; align-items: center; }
    .tx-name { font-size: 0.82rem; font-weight: 600; color: #f8fafc; margin: 0; }
    .tx-info { font-size: 0.68rem; color: #64748b; margin-top: 2px; }
    .tx-tag { display: inline-block; background-color: #1e293b; color: #94a3b8; border: 1px solid #334155; border-radius: 6px; padding: 2px 7px; font-size: 0.62rem; margin-top: 4px; font-weight: 500; }
    .tx-loss { font-size: 0.9rem; font-weight: 700; color: #ef4444; margin: 0; text-align: right; }
    .tx-gain { font-size: 0.9rem; font-weight: 700; color: #10b981; margin: 0; text-align: right; }
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
            tipo TEXT
        )
    """)
    conn.commit()
    c.execute("SELECT COUNT(*) FROM transacoes")
    if c.fetchone()[0] == 0:
        amostras = [
            (datetime.now().strftime("%d Nov, %H:%M"), "🛒 Supermercado Pão de Açúcar", 248.30, "Alimentação", "Cartão Inter", "Saída"),
            (datetime.now().strftime("%d Nov, %H:%M"), "🍔 iFood Entrega", 68.90, "Alimentação", "Nubank", "Saída"),
            (datetime.now().strftime("%d Nov, %H:%M"), "⚡ Conta de Luz - Enel", 194.15, "Contas Fixas", "Pix Nubank", "Saída"),
            (datetime.now().strftime("%d Nov, %H:%M"), "⛽ Posto Shell", 180.00, "Transporte", "Cartão Inter", "Saída"),
            (datetime.now().strftime("%d Nov, %H:%M"), "💼 Salário / TED Recebida", 6500.00, "Renda", "Conta Inter", "Entrada")
        ]
        c.executemany("INSERT INTO transacoes (data, descricao, valor, categoria, banco, tipo) VALUES (?, ?, ?, ?, ?, ?)", amostras)
        conn.commit()
    conn.close()

init_db()

def get_transacoes():
    conn = sqlite3.connect("financas.db")
    df = pd.read_sql_query("SELECT * FROM transacoes ORDER BY id DESC", conn)
    conn.close()
    return df

def adicionar_transacao(data, desc, valor, cat, banco, tipo):
    conn = sqlite3.connect("financas.db")
    c = conn.cursor()
    c.execute("INSERT INTO transacoes (data, descricao, valor, categoria, banco, tipo) VALUES (?, ?, ?, ?, ?, ?)", (data, desc, valor, cat, banco, tipo))
    conn.commit()
    conn.close()

def atualizar_categoria(transacao_id, nova_cat):
    conn = sqlite3.connect("financas.db")
    c = conn.cursor()
    c.execute("UPDATE transacoes SET categoria = ? WHERE id = ?", (nova_cat, transacao_id))
    conn.commit()
    conn.close()

df = get_transacoes()
total_entradas = df[df["tipo"] == "Entrada"]["valor"].sum()
total_saidas = df[df["tipo"] == "Saída"]["valor"].sum()
orcamento_teto = 6000.00
saldo_disponivel = max(0.0, orcamento_teto - total_saidas)

gasto_nu = df[(df["banco"].str.contains("Nubank", case=False, na=False)) & (df["tipo"] == "Saída")]["valor"].sum()
saldo_inter = total_entradas - df[(df["banco"].str.contains("Inter", case=False, na=False)) & (df["tipo"] == "Saída")]["valor"].sum()

# Cabeçalho com saudação e badge de conexão
st.markdown("""
<div class="header-box">
    <div>
        <h2 class="user-name">Olá, Guilherme 👋</h2>
        <p class="user-subtitle">Controle Financeiro Automático</p>
    </div>
    <div class="badge-status">
        <span class="pulse"></span> Open Finance Ativo
    </div>
</div>
""", unsafe_allow_html=True)

# Card Principal (Gradiente Roxo Indigo)
st.markdown(f"""
<div class="budget-card">
    <div class="budget-tag">LIMITE DISPONÍVEL (MÊS)</div>
    <div class="budget-val">R$ {saldo_disponivel:,.2f}</div>
    <div class="budget-sub">Orçamento: R$ {orcamento_teto:,.2f} | Gasto: R$ {total_saidas:,.2f}</div>
</div>
""", unsafe_allow_html=True)

pct = min(1.0, max(0.0, total_saidas / orcamento_teto))
st.progress(pct)

# Cards Laterais Nubank & Inter
st.markdown(f"""
<div class="bank-row">
    <div class="bank-card bank-nu">
        <div><div class="bank-name">Nubank</div><div class="bank-desc">Fatura Atual</div></div>
        <div class="bank-amt">R$ {gasto_nu:,.2f}</div>
    </div>
    <div class="bank-card bank-in">
        <div><div class="bank-name">Inter</div><div class="bank-desc">Conta Corrente</div></div>
        <div class="bank-amt">R$ {saldo_inter:,.2f}</div>
    </div>
</div>
""", unsafe_allow_html=True)

aba1, aba2, aba3 = st.tabs(["📜 Extrato", "⚡ Simular Notificação", "📊 Gráficos"])

with aba1:
    st.caption("ÚLTIMOS LANÇAMENTOS (AUTO-CAPTURA)")
    for idx, row in df.iterrows():
        is_saida = row["tipo"] == "Saída"
        sinal = "-" if is_saida else "+"
        cls_v = "tx-loss" if is_saida else "tx-gain"
        st.markdown(f"""
        <div class="tx-row">
            <div>
                <p class="tx-name">{row["descricao"]}</p>
                <p class="tx-info">{row["data"]} • {row["banco"]}</p>
                <span class="tx-tag">{row["categoria"]}</span>
            </div>
            <div><p class="{cls_v}">{sinal} R$ {row["valor"]:,.2f}</p></div>
        </div>
        """, unsafe_allow_html=True)
        with st.expander(f"Alterar Categoria de {row['descricao'][:22]}..."):
            cats = ["Alimentação", "Transporte", "Contas Fixas", "Lazer", "Saúde", "Educação", "Renda", "Outros"]
            c_idx = cats.index(row["categoria"]) if row["categoria"] in cats else 0
            nova = st.selectbox("Categoria:", cats, index=c_idx, key=f"c_{row['id']}")
            if st.button("Atualizar", key=f"b_{row['id']}"):
                atualizar_categoria(row['id'], nova)
                st.rerun()

with aba2:
    st.markdown("#### Simular Compra Chegando no Cartão")
    with st.form("form_simular"):
        desc = st.text_input("Estabelecimento", value="Cafeteria Espresso")
        val = st.number_input("Valor (R$)", value=18.50, min_value=0.01, step=1.0)
        banco = st.selectbox("Banco / Origem", ["Nubank", "Cartão Inter", "Pix Nubank", "Conta Inter"])
        cat = st.selectbox("Categoria", ["Alimentação", "Transporte", "Lazer", "Contas Fixas", "Outros"])
        tipo = st.selectbox("Tipo", ["Saída", "Entrada"])
        if st.form_submit_button("💥 Disparar Notificação Instantânea"):
            adicionar_transacao(datetime.now().strftime("%d Nov, %H:%M"), desc, val, cat, banco, tipo)
            st.success("Transação registrada com sucesso!")
            st.rerun()

with aba3:
    st.markdown("#### Gastos Consolidados por Categoria")
    saidas = df[df["tipo"] == "Saída"]
    if not saidas.empty:
        g = saidas.groupby("categoria")["valor"].sum().reset_index()
        st.bar_chart(g.set_index("categoria"))