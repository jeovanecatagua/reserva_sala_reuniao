import streamlit as st
from flask import Flask, jsonify
import sqlite3

# Configurar o Flask
app = Flask(__name__)

@app.route("/consultar-dados", methods=["GET"])
def consultar_dados():
    try:
        conn = sqlite3.connect("dados_projeto.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tb_reserva_sala_reuniao;")
        colunas = [desc[0] for desc in cursor.description]
        registros = cursor.fetchall()
        conn.close()
        return jsonify([dict(zip(colunas, registro)) for registro in registros])
    except Exception as e:
        return jsonify({"status": "erro", "mensagem": str(e)})

# Executar Flask junto com Streamlit
from threading import Thread
def run_flask():
    app.run(port=8502, debug=False)

Thread(target=run_flask).start()

# Aplicação Streamlit
st.title("Minha Aplicação Streamlit")
st.write("Streamlit está rodando junto com o Flask.")
