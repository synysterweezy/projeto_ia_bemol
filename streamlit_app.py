import streamlit as st
import pandas as pd
import databricks.sql

# Configuração da conexão com o Databricks
conn = databricks.sql.connect(
    server_hostname="adb-926216925051160.0.azuredatabricks.net",
    http_path="/sql/1.0/warehouses/ead9637a3263a02e",
    access_token="dapi823b5a9c0a1e369fad19a78773bb59f3"
)

# Consultando os dados do DataFrame unificado
query = "SELECT * FROM marketing.dados_mkt.abertura_email_2025"
df = pd.read_sql(query, conn)

# Converter colunas de data e hora para o tipo correto
df['DATA_ABERTURA'] = pd.to_datetime(df['DATA_ABERTURA'], dayfirst=True)
df['DATA_DISPARO'] = pd.to_datetime(df['DATA_DISPARO'], dayfirst=True)


# --- Formatação da Página ---
st.title("Home | Demo - Análise de Abertura de E-mails")
st.markdown(f"Bem-vindo, usuário!") # Substitua 'usuário' pelo nome do usuário, se disponível.

# --- Resumo ---
st.header("= Resumo")

col1, col2, col3, col4 = st.columns(4)

# Total de Aberturas
total_aberturas = len(df)
col1.metric("Total de Aberturas", total_aberturas, delta=df['DATA_ABERTURA'].nunique()- df['DATA_ABERTURA'].shift().nunique(), delta_color="inverse")


# Total de Clientes Únicos
total_clientes_unicos = df['ID_CLIENTE'].nunique()
col2.metric("Total de Clientes Únicos", total_clientes_unicos,  delta=df['ID_CLIENTE'].nunique() - df['ID_CLIENTE'].shift().nunique(), delta_color="inverse")

# Taxa de Abertura (calcular como você achar melhor)
# Exemplo: considerando clientes únicos
taxa_abertura = (total_clientes_unicos / df['ID_CLIENTE'].nunique()) * 100  # Substitua pelo seu cálculo
col3.metric("Taxa de Abertura", f"{taxa_abertura:.1f}%")  # Formate para exibir como porcentagem



# --- Pedra Mais Frequente ---
pedra_mais_frequente = df['PEDRA'].mode()[0]  # Retorna a pedra mais frequente
col4.metric("Pedra Mais Frequente", pedra_mais_frequente) # Poderia adicionar um delta aqui também, se relevante.


# --- Aberturas de E-mails ---
st.header("= Aberturas de E-mails")

# Filtros de Data (Últimas 24h, 7d, 30d)
selected_time_filter = st.selectbox("Período:", ["Últimas 24h", "Últimos 7d", "Últimos 30d"])


# Aplicar filtro de data
now = pd.Timestamp.now()
if selected_time_filter == "Últimas 24h":
    df_filtered = df[df['DATA_ABERTURA'] >= now - pd.Timedelta(days=1)]
elif selected_time_filter == "Últimos 7d":
    df_filtered = df[df['DATA_ABERTURA'] >= now - pd.Timedelta(days=7)]
elif selected_time_filter == "Últimos 30d":
    df_filtered = df[df['DATA_ABERTURA'] >= now - pd.Timedelta(days=30)]
else:
    df_filtered = df # Mostra todos os dados se nenhum filtro for selecionado



# Seleção de Campanha
campanhas = df_filtered['CAMPANHA'].unique()
selected_campaign = st.multiselect("Selecione a(s) Campanha(s):", campanhas, default=campanhas)
df_filtered = df_filtered[df_filtered['CAMPANHA'].isin(selected_campaign)]

# Exibir tabela com os dados
st.dataframe(df_filtered[['ID_CLIENTE', 'EMAIL', 'DATA_ABERTURA', 'HORA_ABERTURA', 'CAMPANHA', 'PERSONA', 'DATA_DISPARO', 'PEDRA']])


# Número de registros exibidos
st.caption(f"Mostrando {len(df_filtered)} registros.")



# Fechar a conexão
conn.close()
