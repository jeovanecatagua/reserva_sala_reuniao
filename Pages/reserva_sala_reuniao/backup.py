import os
import sqlite3
import streamlit as st
from datetime import datetime

def fazer_backup():
    # Caminho do banco de dados
    db_path = "dados_projeto.db"
    
    # Criar um nome de arquivo único com a data/hora
    backup_filename = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
    
    # Fechar a conexão se estiver aberta
    if os.path.exists(db_path):
        conn = sqlite3.connect(db_path)
        conn.close()  # Fecha a conexão com o banco de dados

    # Criar o arquivo de backup
    with open(backup_filename, "wb") as f:
        # Aqui você colocaria o código que cria o banco de dados
        pass  # Isso é só um exemplo

    # Criar botão de download, centralizado
    st.markdown(
        """
        <style>
        .stDownloadButton {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 30vh;
        }
        </style>
        """, unsafe_allow_html=True
    )

    # Exibir o botão de download
    with open(backup_filename, "rb") as f:
        st.download_button(
            label="Baixar Banco de Dados",
            data=f,
            file_name=backup_filename,
            mime="application/x-sqlite3",
            key="download_db"
        )
