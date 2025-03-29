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

st.title("📊 Overview das Aberturas de E-mails")
st.dataframe(df)  # Exibe os dados
