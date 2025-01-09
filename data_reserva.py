import sqlite3
import pandas as pd

DB_PATH = "dados_projeto.db"

def consultar_dados():
    try:
        conn = sqlite3.connect(DB_PATH)
        query = "SELECT * FROM tb_reserva_sala_reuniao;"
        dados = pd.read_sql_query(query, conn)
        conn.close()
        return dados
    except Exception as e:
        return {"status": "erro", "mensagem": str(e)}

# Exemplo de uso
if __name__ == "__main__":
    df = consultar_dados()
    print(df)