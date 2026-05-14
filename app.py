import streamlit as st
import plotly.express as px
from main import (
    carregar_ipca, 
    carregar_sm, 
    calcular_poder_de_compra,
    calcular_salario_ipca
)

# Configuração da página (Opcional, mas deixa o portfólio mais profissional)
st.set_page_config(page_title="Simulador de Poder de Compra", layout="wide")

st.title('💰 Simulador do Poder de Compra')
st.markdown('💸 Compare o impacto da inflação (IPCA) no real ao longo do tempo.')

# Início do processamento de dados (ETL Pipeline)
df_ipca = carregar_ipca()
df_sm = carregar_sm()

# --- SEÇÃO 1: CALCULADORA DE INFLAÇÃO ACUMULADA ---
st.header("🧮 Calculadora de Inflação Acumulada")
anos_disponiveis = sorted(list(df_ipca['data'].dt.year.unique()))

periodo = st.select_slider(
    "Selecione o intervalo de anos para a comparação:",
    options=anos_disponiveis,
    value=(1995, 2025)
)
ano_inicial, ano_final = periodo

# Executa lógica de negócio do main.py
valor_corrigido, inflacao_perc = calcular_poder_de_compra(ano_inicial, ano_final, df_ipca)

col1, col2 = st.columns(2)
with col1:
    st.metric(
        label=f"R$ 100,00 no início de {ano_inicial} equivalem ao fim de {ano_final} a:", 
        value=f"R$ {valor_corrigido}"
    )
with col2:
    st.metric(
        label=f"Inflação Acumulada no Período:",
        value=f"{inflacao_perc}%",
        delta=f"+{inflacao_perc}%",
        delta_color="inverse"
    )

# --- SEÇÃO 2: SIMULADOR DE SALÁRIO ---
st.header("👤 Seu Salário Corrigido pela Inflação")
st.subheader('🤑 Veja quanto você precisa ganhar para manter seu poder de compra')

col_ano_ini, col_ano_fim, col_valor = st.columns(3)
with col_ano_ini:
    ano_salario_ini = st.selectbox("De (Ano Inicial):", options=anos_disponiveis, index=0)
with col_ano_fim:
    ano_salario_fim = st.selectbox("Para (Ano Final):", options=anos_disponiveis, index=len(anos_disponiveis) - 1)
with col_valor:
    salario_usuario = st.number_input(f"Salário em {ano_salario_ini} (R$):", min_value=10.0, value=1000.0, step=100.0)

st.markdown("---")

# VALIDAÇÃO LÓGICA (Previne o TypeError e o NameError)
if ano_salario_fim < ano_salario_ini:
    st.warning("⚠️ O ano final deve ser maior ou igual ao ano inicial para calcular o reajuste.")
else:
    salario_necessario = calcular_salario_ipca(salario_usuario, ano_salario_ini, ano_salario_fim, df_ipca)
    
    st.metric(
        label=f"Para manter o poder de compra de R$ {salario_usuario:,.2f} de {ano_salario_ini} até {ano_salario_fim}:",
        value=f"R$ {salario_necessario:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    )

st.markdown("---")

# --- SEÇÃO 3: VISUALIZAÇÃO DE DADOS ---
st.header("📊 Gráficos Históricos (Pós-Plano Real)")

st.subheader('📈 Variação Mensal do IPCA (%)')
fig_ipca = px.line(df_ipca, x='data', y='valor', labels={'data': 'Período', 'valor': 'Variação (%)'}, template='plotly_dark')
fig_ipca.update_traces(line=dict(color='#FF4B4B', width=1.5))
st.plotly_chart(fig_ipca, use_container_width=True)

st.subheader('💵 Evolução do Salário Mínimo (R$)')
fig_sm = px.area(df_sm, x='data', y='valor', labels={'data': 'Período', 'valor': 'Valor (R$)'}, template='plotly_dark')
fig_sm.update_traces(line=dict(color='#00D4B2', width=2), fillcolor='rgba(0, 212, 178, 0.15)')
st.plotly_chart(fig_sm, use_container_width=True)