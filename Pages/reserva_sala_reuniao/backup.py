import os
import sqlite3
import shutil
import streamlit as st
from datetime import datetime

def fazer_backup():
    # Caminho do banco de dados original
    db_path = "dados_projeto.db"
    
    # Criar um nome de arquivo único com a data/hora
    backup_filename = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
    
    # Verificar se o banco de dados existe antes de copiar
    if os.path.exists(db_path):
        # Copiar o banco de dados para o arquivo de backup
        shutil.copy2(db_path, backup_filename)

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

        # Criar botão de download
        with open(backup_filename, "rb") as f:
            st.download_button(
                label="Baixar Banco de Dados",
                data=f,
                file_name=backup_filename,
                mime="application/x-sqlite3",
                key="download_db"
            )
    else:
        st.error("Banco de dados não encontrado!")

# Exibir botão para fazer backup
if st.button("Fazer Backup do Banco de Dados"):
    fazer_backup()
