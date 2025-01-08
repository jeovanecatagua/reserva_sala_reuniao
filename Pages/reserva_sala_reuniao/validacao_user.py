import streamlit as st
import sqlite3
import pandas as pd
import time

def verificar_usuario(email, senha):
    con    = sqlite3.connect("dados_projeto.db")
    cursor = con.cursor()

    cursor.execute("SELECT COUNT(*) FROM tb_usuario WHERE email = ? AND senha = ?", (email, senha))
    resultado = cursor.fetchone()[0]

    con.close()

    # Retorna True se encontrar pelo menos um registro
    return resultado > 0

def authenticate_user():
    if "authenticated" in st.session_state and st.session_state["authenticated"]:
        return True 

    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False

    # Exibe campos de login caso o usuário não esteja autenticado
    st.subheader("Login")
    email        = st.text_input("E-mail", key="login_email")
    password     = st.text_input("Senha", type="password", key="login_password")
    login_button = st.button("Entrar")

    # Valida os dados de login
    if login_button:
        if verificar_usuario(email, password):
            # Se a autenticação for bem-sucedida, guarda a informação no session_state
            st.session_state["authenticated"] = True
            st.session_state["user"] = email
            # Exibe o GIF e espera
            with st.spinner("Autenticando..."):
                time.sleep(5) 
            with st.success(f"Bem-vindo, {email}!"):
                time.sleep(2)
            st.rerun()             
            return True 
        else:
            st.error("E-mail ou senha inválidos.")
            return False

    return False