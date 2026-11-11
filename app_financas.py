import streamlit as st
import pandas as pd
import sqlite3
import calendar
from datetime import datetime, date
from dateutil.relativedelta import relativedelta

st.set_page_config(page_title="Minhas Finanças", page_icon="⚡", layout="centered")

# Estilo Moderno Dark Bento UI / MacroDroid (sem quebrar ícones de sistema do Streamlit)
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
    .parcela-badge {
        font-size: 0.68rem;
        font-weight: 800;
        padding: 2px 8px;
        border-radius: 6px;
        background: #1a2538;
        color: #38bdf8;
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
df_parc = get_parcelas()
df_reemb_hist = get_historico_reembolsos()

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

if "copiando_prev" not in st.session_state:
    st.session_state.copiando_prev = None

hoje = date.today()
if "cal_mes" not in st.session_state:
    st.session_state.cal_mes = hoje.month
if "cal_ano" not in st.session_state:
    st.session_state.cal_ano = hoje.year

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
        <span>Faturas Cartão: <strong style="color: #ffffff;">R$ {total_faturas:,.2f}</strong></span>
        <span>Cheque Esp.: <strong style="color: #f87171;">R$ {total_cheque:,.2f}</strong></span>
    </div>
</div>
""", unsafe_allow_html=True)

# RECURSOS RÁPIDOS (2 linhas limpas sem truncar)
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

    # Totais Previstos
    entradas_previstas = df_prev[df_prev["tipo"] == "Entrada"]["valor"].sum() if not df_prev.empty else 0.0
    saidas_previstas = df_prev[df_prev["tipo"] == "Saída"]["valor"].sum() if not df_prev.empty else 0.0
    saldo_projetado = total_saldos + entradas_previstas - saidas_previstas

    # PAINEL DE SALDO PREVISTO A RECEBER E COMPARATIVO
    st.markdown(f"""
    <div style="background: #0d1522; border: 1px solid #1f2f47; border-radius: 14px; padding: 12px; margin: 10px 0 14px 0;">
        <div style="font-size: 0.68rem; font-weight: 700; color: #94a3b8; text-transform: uppercase;">Fluxo Futuro & Comparativo</div>
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 8px; margin-top: 8px;">
            <div style="background: #111a28; padding: 8px 10px; border-radius: 10px; border: 1px solid #1c2a3d;">
                <span style="font-size: 0.62rem; color: #4ade80; font-weight: 700;">PREVISTO A RECEBER</span>
                <div style="font-family: 'JetBrains Mono'; font-size: 1.0rem; font-weight: 800; color: #4ade80;">+ R$ {entradas_previstas:,.2f}</div>
            </div>
            <div style="background: #111a28; padding: 8px 10px; border-radius: 10px; border: 1px solid #1c2a3d;">
                <span style="font-size: 0.62rem; color: #f87171; font-weight: 700;">PREVISTO A PAGAR</span>
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

    # CALENDÁRIO VISUAL COM CORES NOS DIAS PREVISTOS
    c_nav1, c_nav2 = st.columns([3, 2])
    with c_nav1:
        meses_nomes = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]
        st.markdown(f'<span style="font-size: 0.82rem; font-weight: 800; color: #ffffff;">🗓️ {meses_nomes[st.session_state.cal_mes - 1]} de {st.session_state.cal_ano}</span>', unsafe_allow_html=True)
    with c_nav2:
        c_prev_m, c_next_m = st.columns(2)
        with c_prev_m:
            if st.button("◀", key="m_ant"):
                if st.session_state.cal_mes == 1:
                    st.session_state.cal_mes = 12
                    st.session_state.cal_ano -= 1
                else:
                    st.session_state.cal_mes -= 1
                st.rerun()
        with c_next_m:
            if st.button("▶", key="m_prox"):
                if st.session_state.cal_mes == 12:
                    st.session_state.cal_mes = 1
                    st.session_state.cal_ano += 1
                else:
                    st.session_state.cal_mes += 1
                st.rerun()

    ano_sel = st.session_state.cal_ano
    mes_sel = st.session_state.cal_mes
    
    eventos_por_dia = {}
    if not df_prev.empty:
        for _, row in df_prev.iterrows():
            try:
                dt_obj = datetime.strptime(row["data_prevista"], "%Y-%m-%d").date()
                if dt_obj.year == ano_sel and dt_obj.month == mes_sel:
                    dia = dt_obj.day
                    if dia not in eventos_por_dia:
                        eventos_por_dia[dia] = []
                    eventos_por_dia[dia].append(row)
            except:
                pass

    cal_matrix = calendar.monthcalendar(ano_sel, mes_sel)
    dias_semana = ["Seg", "Ter", "Qua", "Qui", "Sex", "Sáb", "Dom"]

    html_cal = '<table class="cal-table"><thead><tr>'
    for d_sem in dias_semana:
        html_cal += f'<th class="cal-th">{d_sem}</th>'
    html_cal += '</tr></thead><tbody>'

    for semana in cal_matrix:
        html_cal += '<tr>'
        for dia in semana:
            if dia == 0:
                html_cal += '<td class="cal-cell" style="background: transparent; border-color: transparent;"></td>'
            else:
                is_today = (dia == hoje.day and mes_sel == hoje.month and ano_sel == hoje.year)
                classes = ["cal-cell"]
                if is_today:
                    classes.append("today")

                badges_html = ""
                if dia in eventos_por_dia:
                    tem_in = any(ev["tipo"] == "Entrada" for ev in eventos_por_dia[dia])
                    tem_out = any(ev["tipo"] == "Saída" for ev in eventos_por_dia[dia])
                    if tem_in and tem_out:
                        classes.append("has-ambos")
                    elif tem_in:
                        classes.append("has-entrada")
                    elif tem_out:
                        classes.append("has-saida")

                    for ev in eventos_por_dia[dia]:
                        cls_b = "badge-in" if ev["tipo"] == "Entrada" else "badge-out"
                        sinal_b = "+" if ev["tipo"] == "Entrada" else "-"
                        v_curto = f"{sinal_b}{ev['valor']:,.0f}".replace(",", ".")
                        badges_html += f'<span class="cal-badge {cls_b}">{v_curto}</span>'

                cls_str = " ".join(classes)
                html_cal += f'<td class="{cls_str}"><span style="color: {"#38bdf8" if is_today else "#94a3b8"};">{dia}</span>{badges_html}</td>'
        html_cal += '</tr>'
    html_cal += '</tbody></table>'

    st.markdown(html_cal, unsafe_allow_html=True)
    st.markdown("""
    <div style="display: flex; gap: 12px; margin: 8px 0 12px 0; font-size: 0.65rem;">
        <span style="color: #4ade80;">🟢 Dia com valor a receber</span>
        <span style="color: #f87171;">🔴 Dia com valor a pagar</span>
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
                desc_prev = st.text_input("Descrição", value="Salário / Pix / Boleto")
                banco_prev = st.selectbox("Banco Envolvido", df_bancos["banco"].tolist())
                cat_prev = st.selectbox("Categoria", ["Renda", "Salário", "Fatura", "Contas Fixas", "Lazer", "Outros"])
            
            st.markdown('<div style="margin-top: 6px; padding: 8px; background: #0d1522; border-radius: 10px; border: 1px solid #1a273b;">', unsafe_allow_html=True)
            fixo_check = st.checkbox("📌 Fixar Renda/Gasto Recorrente (Mesmo dia todos os meses)")
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

    # Lista de Previsões Agendadas
    st.markdown('<div style="font-size: 0.72rem; font-weight: 700; color: #64748b; text-transform: uppercase; margin: 12px 0 6px 0;">Lista Detalhada de Previsões:</div>', unsafe_allow_html=True)
    if df_prev.empty:
        st.info("Nenhuma previsão agendada.")
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
                    if st.button("📋", key=f"btn_cp_{row_p['id']}", help="Copiar este lançamento para outro mês"):
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
        <div style="font-size: 0.72rem; font-weight: 700; color: #38bdf8; text-transform: uppercase;">Como funciona o rateio de reembolso:</div>
        <div style="font-size: 0.68rem; color: #94a3b8; margin-top: 4px; line-height: 1.4;">
            Recebeu o reembolso da empresa? Digite o valor total que caiu e <strong>distribua diretamente para onde o dinheiro deve ir</strong>. O app abate automaticamente a fatura do cartão usado no pedágio, repõe o cheque especial usado no combustível e deixa o lucro das diárias (R$ 100/dia) livre na conta!
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Botão de toggle sem bug de fontes
    btn_calc_label = "➖ Ocultar Calculadora de Estimativa" if st.session_state.mostrar_calc_km else "🧮 Abrir Calculadora de Estimativa (R$ 130/dia + Pedágios)"
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

    with st.form("form_rateio_reembolso"):
        st.markdown('<div style="font-size: 0.8rem; font-weight: 800; color: #ffffff; margin-bottom: 8px;">1. Entrada Total de Reembolso Recebido:</div>', unsafe_allow_html=True)
        c_v1, c_v2 = st.columns(2)
        with c_v1:
            data_receb = st.date_input("Data do Recebimento", value=date.today())
        with c_v2:
            valor_total_recebido = st.number_input("Valor Total que Caiu (R$)", min_value=0.01, value=778.00, step=20.0)

        st.markdown('<div style="font-size: 0.8rem; font-weight: 800; color: #38bdf8; margin: 12px 0 6px 0;">2. Destinar o Valor para Abates e Saldo:</div>', unsafe_allow_html=True)
        st.caption("Distribua o dinheiro. O valor é descontado imediatamente na fatura/cheque selecionado:")

        # Destino A (Layout espaçado em 2 colunas para nunca cortar texto)
        st.markdown('<div style="background: #111a28; padding: 12px; border-radius: 12px; margin-bottom: 10px; border: 1px solid #1c2a3d;">', unsafe_allow_html=True)
        st.markdown('<span style="font-size: 0.72rem; font-weight: 700; color: #38bdf8;">🎯 Destino A (Ex: Pedágio no Cartão)</span>', unsafe_allow_html=True)
        c_a1, c_a2 = st.columns(2)
        with c_a1:
            banco_a = st.selectbox("Banco", df_bancos["banco"].tolist(), index=df_bancos["banco"].tolist().index("Nubank") if "Nubank" in df_bancos["banco"].tolist() else 0, key="b_a")
        with c_a2:
            val_a = st.number_input("Valor (R$)", min_value=0.0, value=128.00, step=10.0, key="v_a")
        acao_a = st.selectbox("Ação a Executar", ["Pagar/Abater Fatura de Cartão", "Abater Cheque Especial", "Creditar em Conta Corrente"], index=0, key="ac_a")
        motivo_a = st.text_input("Identificação / Motivo", value="Pedágio da semana (Cartão de Crédito)", key="m_a")
        st.markdown('</div>', unsafe_allow_html=True)

        # Destino B
        st.markdown('<div style="background: #111a28; padding: 12px; border-radius: 12px; margin-bottom: 10px; border: 1px solid #1c2a3d;">', unsafe_allow_html=True)
        st.markdown('<span style="font-size: 0.72rem; font-weight: 700; color: #fbbf24;">🎯 Destino B (Ex: Repor Gasolina no Cheque Especial)</span>', unsafe_allow_html=True)
        c_b1, c_b2 = st.columns(2)
        with c_b1:
            banco_b = st.selectbox("Banco", df_bancos["banco"].tolist(), index=df_bancos["banco"].tolist().index("Bradesco") if "Bradesco" in df_bancos["banco"].tolist() else 0, key="b_b")
        with c_b2:
            val_b = st.number_input("Valor (R$)", min_value=0.0, value=150.00, step=10.0, key="v_b")
        acao_b = st.selectbox("Ação a Executar", ["Abater Cheque Especial", "Pagar/Abater Fatura de Cartão", "Creditar em Conta Corrente"], index=0, key="ac_b")
        motivo_b = st.text_input("Identificação / Motivo", value="Gasolina tirada do Cheque Especial", key="m_b")
        st.markdown('</div>', unsafe_allow_html=True)

        # Destino C
        sobra_lucro = max(0.0, valor_total_recebido - (val_a + val_b))
        st.markdown('<div style="background: #111a28; padding: 12px; border-radius: 12px; margin-bottom: 10px; border: 1px solid #1c2a3d;">', unsafe_allow_html=True)
        st.markdown('<span style="font-size: 0.72rem; font-weight: 700; color: #4ade80;">🎯 Destino C (Ex: Renda Livre das Diárias de R$ 100)</span>', unsafe_allow_html=True)
        c_c1, c_c2 = st.columns(2)
        with c_c1:
            banco_c = st.selectbox("Banco", df_bancos["banco"].tolist(), index=df_bancos["banco"].tolist().index("Itaú") if "Itaú" in df_bancos["banco"].tolist() else 0, key="b_c")
        with c_c2:
            val_c = st.number_input("Valor (R$)", min_value=0.0, value=float(sobra_lucro), step=10.0, key="v_c")
        acao_c = st.selectbox("Ação a Executar", ["Creditar em Conta Corrente", "Pagar/Abater Fatura de Cartão", "Abater Cheque Especial"], index=0, key="ac_c")
        motivo_c = st.text_input("Identificação / Motivo", value="Renda livre das diárias alocadas", key="m_c")
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

elif st.session_state.bloco_ativo == "advisor":
    st.markdown('<div class="panel-box">', unsafe_allow_html=True)
    c_tit, c_fech = st.columns([5, 1])
    with c_tit:
        st.markdown('<span style="font-weight: 800; color: #38bdf8; font-size: 0.92rem;">🧠 Advisor • Diagnóstico de Saúde Financeira</span>', unsafe_allow_html=True)
    with c_fech:
        if st.button("✕", key="fechar_adv"):
            st.session_state.bloco_ativo = None
            st.rerun()
    
    diagnosticos = []
    
    if total_cheque > 0:
        diagnosticos.append({
            "titulo": "⚠️ Alerta Crítico: Cheque Especial Ativo",
            "tipo": "danger",
            "desc": f"Você está utilizando R$ {total_cheque:,.2f} do limite emergencial. Use o botão ⛽ Destinar para abater o cheque especial assim que receber reembolsos de gasolina da empresa."
        })
    else:
        diagnosticos.append({
            "titulo": "✅ Cheque Especial Zerado",
            "tipo": "success",
            "desc": "Parabéns! Nenhuma das suas contas bancárias está pagando juros de cheque especial."
        })
        
    if total_saldos < total_faturas:
        deficit = total_faturas - total_saldos
        diagnosticos.append({
            "titulo": "🚨 Faturas Maiores que o Saldo Disponível",
            "tipo": "danger",
            "desc": f"Suas faturas somam R$ {total_faturas:,.2f}, enquanto seu saldo total é de R$ {total_saldos:,.2f} (diferença de R$ {deficit:,.2f}). Use a destinação direta de reembolsos para abater o cartão antes do fechamento."
        })
    else:
        folga = total_saldos - total_faturas
        diagnosticos.append({
            "titulo": "🛡️ Faturas Cobertas com Folga",
            "tipo": "success",
            "desc": f"Seu saldo disponível quita 100% das suas faturas atuais e ainda sobram R$ {folga:,.2f} livres."
        })
        
    for diag in diagnosticos:
        cor_borda = "#38bdf8"
        if diag["tipo"] == "danger": cor_borda = "#f87171"
        elif diag["tipo"] == "warning": cor_borda = "#fbbf24"
        elif diag["tipo"] == "success": cor_borda = "#4ade80"
        
        st.markdown(f"""
        <div style="background: #0d1522; border: 1px solid #1d2d42; border-left: 4px solid {cor_borda}; border-radius: 12px; padding: 12px; margin-bottom: 10px;">
            <div style="font-size: 0.82rem; font-weight: 700; color: #ffffff;">{diag['titulo']}</div>
            <div style="font-size: 0.72rem; color: #94a3b8; margin-top: 4px; line-height: 1.4;">{diag['desc']}</div>
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
        st.markdown('<span style="font-weight: 800; color: #38bdf8; font-size: 0.9rem;">📊 Análise Dinâmica dos Seus Gastos</span>', unsafe_allow_html=True)
    with c_fech:
        if st.button("✕", key="fechar_graf"):
            st.session_state.bloco_ativo = None
            st.rerun()
    
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
            # Se limite liberado estiver zerado, exibe a diferença matemática padrão
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
            # BANCO SEM CARTÃO: Fica em branco a parte de fatura/cartão, mostrando só saldo e cheque!
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
    
    # Resumo das Parcelas
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

    # Botão para alternar formulário de nova parcela
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

    # Filtro por Cartão
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
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    if df_tx.empty:
        st.info("Nenhuma transação registrada no extrato.")
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
        
        # OPÇÃO NÃO OBRIGATÓRIA: Possui Cartão de Crédito?
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
                # CAMPO NOVO: LIMITE LIBERADO
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
