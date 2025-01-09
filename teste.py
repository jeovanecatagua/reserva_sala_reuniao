import streamlit as st
import sqlite3
import pandas as pd
import json

# Função para consultar dados do SQLite
@st.cache_data
def consultar_dados():
    try:
        conn = sqlite3.connect("dados_projeto.db")
        query = "SELECT * FROM tb_reserva_sala_reuniao;"
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df
    except Exception as e:
        return pd.DataFrame()  # Retorna DataFrame vazio em caso de erro

# Configuração da página
st.set_page_config(page_title="Aplicação de Reserva de Salas", layout="wide")

# Obter parâmetros da URL
query_params = st.experimental_get_query_params()

# Verificar se o parâmetro "api" está presente e igual a "dados"
if query_params.get("api") == ["dados"]:
    # Consultar dados e retornar como JSON
    df = consultar_dados()
    dados_json = df.to_json(orient="records")
    st.write(dados_json)  # Use st.write() para retornar JSON simples
else:
    # Interface padrão da aplicação
    st.title("Sistema de Reserva de Salas de Reunião")
    st.write("Bem-vindo à aplicação de reserva de salas de reunião!")

    # Mostrar dados como tabela na interface
    df = consultar_dados()
    st.dataframe(df)
