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

# Seleção de Campanha ou Cliente
selected_option = st.selectbox("Selecione uma Campanha ou Cliente:", ["Todas as Campanhas", "Cliente Específico"])

if selected_option == "Todas as Campanhas":
    st.dataframe(df)

elif selected_option == "Cliente Específico":
    cliente_id = st.text_input("Insira o ID do Cliente:")
    if cliente_id:
        try:
            cliente_id = int(cliente_id)
            df_cliente = df[df["ID_CLIENTE"] == cliente_id]
            if not df_cliente.empty:
                st.dataframe(df_cliente)

                # Integração com o Chatbot (substitua pelo seu endpoint)
                st.sidebar.title("🤖 Chatbot")
                st.sidebar.markdown(f"Converse com o agente sobre o cliente {cliente_id}")
                # Aqui você integraria o seu chatbot usando o endpoint do Databricks

            else:
                st.warning("Cliente não encontrado.")
        except ValueError:
            st.error("ID do cliente inválido. Insira um número inteiro.")

# --- Estatísticas Gerais ---
st.subheader("Estatísticas Gerais")
total_aberturas = len(df)
st.metric("Total de Aberturas", total_aberturas)


# --- Aberturas por Campanha ---
st.subheader("Aberturas por Campanha")
aberturas_campanha = df.groupby("CAMPANHA")["ID_CLIENTE"].count().reset_index()
st.bar_chart(aberturas_campanha, x="CAMPANHA", y="ID_CLIENTE")


# --- Aberturas por Pedra ---
st.subheader("Aberturas por Pedra")
aberturas_pedra = df.groupby("PEDRA")["ID_CLIENTE"].count().reset_index()
st.bar_chart(aberturas_pedra, x="PEDRA", y="ID_CLIENTE")



# Fecha a conexão ao final
conn.close()
