import sqlite3
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from datetime import date, time
import os 

# Criação do app FastAPI
app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "API está funcionando!"}

DB_PATH = os.getenv("DB_PATH", "dados_projeto.db")
# DB_PATH = "dados_projeto.db"

class Registro(BaseModel):
    id: int
    user: str
    sala_reuniao: str
    dt_reuniao: date
    hr_inicio: time
    hr_fim: time

@app.get("/consultar-dados", response_model=List[Registro])
def consultar_dados():
    print("Executando a rota '/consultar-dados'")
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Consulta os dados
        cursor.execute("SELECT * FROM tb_reserva_sala_reuniao;")
        colunas = [desc[0] for desc in cursor.description]
        registros = cursor.fetchall()
        conn.close()

        return [dict(zip(colunas, registro)) for registro in registros]
    except Exception as e:
        return {"status": "erro", "mensagem": str(e)}