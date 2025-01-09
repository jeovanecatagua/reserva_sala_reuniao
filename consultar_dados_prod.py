import streamlit as st
import sqlite3
import pandas as pd

@st.cache
def consultar_dados():
    conn = sqlite3.connect("dados_projeto.db")
    df = pd.read_sql_query("SELECT * FROM tb_reserva_sala_reuniao", conn)
    conn.close()
    return df

# Configuração da API
st.set_page_config(page_title="API de Dados")

# Rota de dados JSON
if st.experimental_get_query_params().get("api") == ["dados"]:
    df = consultar_dados()
    st.write(df.to_json(orient="records"))
else:
    st.write("Bem-vindo à aplicação!")