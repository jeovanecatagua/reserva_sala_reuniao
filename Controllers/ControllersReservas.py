
import models.reservas as reservas
import sqlite3
import streamlit as st

def get_db_connection():
    return sqlite3.connect("dados_projeto.db", check_same_thread=False)

@st.cache_data

def create_tb():
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tb_reserva_sala_reuniao (
                id           INTEGER PRIMARY KEY AUTOINCREMENT,
                user         TEXT NOT NULL,
                sala_reuniao TEXT NOT NULL,
                dt_reuniao   DATE NOT NULL,
                hr_inicio    TEXT NOT NULL,
                hr_fim       TEXT NOT NULL,
                dt_insert    DATETIME NOT NULL DEFAULT (DATETIME('now', '-3 hours'))
            )
        ''')
        print("Tabela 'tb_reserva_sala_reuniao' criada com sucesso.")
    except sqlite3.OperationalError as e:
        print(f"Erro ao criar tabela 'tb_reserva_sala_reuniao': {e}")

    try:
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tb_reserva_sala_reuniao_bkp (
                id           INTEGER NOT NULL,
                user         TEXT NOT NULL,
                sala_reuniao TEXT NOT NULL,
                dt_reuniao   DATE NOT NULL,
                hr_inicio    TEXT NOT NULL,
                hr_fim       TEXT NOT NULL,
                dt_insert    DATETIME NOT NULL
            )
        ''')
        print("Tabela 'tb_reserva_sala_reuniao_bkp' criada com sucesso.")
    except sqlite3.OperationalError as e:
        print(f"Erro ao criar tabela 'tb_reserva_sala_reuniao_bkp': {e}")

    try:
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tb_usuario (
                id      INTEGER PRIMARY KEY AUTOINCREMENT,
                email   TEXT NOT NULL,
                senha   TEXT NOT NULL,
                perfil  TEXT NOT NULL,
                dt_insert    DATETIME NOT NULL DEFAULT (DATETIME('now', '-3 hours'))
            )'''
        )
        print("Tabela 'tb_usuario' criada com sucesso.")
    except sqlite3.OperationalError as e:
        print(f"Erro ao criar tabela 'tb_usuario': {e}")

    try:
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tb_usuario_bkp (
                id      INTEGER NOT NULL,
                email   TEXT NOT NULL,
                senha   TEXT NOT NULL,
                perfil  TEXT NOT NULL,
                dt_insert    DATETIME NOT NULL
            )'''
        )
        print("Tabela 'tb_usuario_bkp' criada com sucesso.")
    except sqlite3.OperationalError as e:
        print(f"Erro ao criar tabela 'tb_usuario_bkp': {e}")

    try:
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tb_sala (
                id    INTEGER PRIMARY KEY AUTOINCREMENT,
                sala  TEXT NOT NULL,
                dt_insert    DATETIME NOT NULL DEFAULT (DATETIME('now', '-3 hours'))
            )
        ''')
        print("Tabela 'tb_sala' criada com sucesso.")
    except sqlite3.OperationalError as e:
        print(f"Erro ao criar tabela 'tb_sala': {e}")
    
    try:
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tb_sala_bkp (
                id   INTEGER NOT NULL,
                sala TEXT NOT NULL,
                dt_insert    DATETIME NOT NULL
            )
        ''')
        print("Tabela 'tb_sala_bkp' criada com sucesso.")
    except sqlite3.OperationalError as e:
        print(f"Erro ao criar tabela 'tb_sala_bkp': {e}")

    conn.commit()

def Incluir(insert_tb):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(""" 
        INSERT INTO tb_reserva_sala_reuniao (user, sala_reuniao, dt_reuniao, hr_inicio, hr_fim) 
        VALUES(?, ?, ?, ?, ?)""",
        (insert_tb.user, insert_tb.sala_reuniao, insert_tb.dt_reuniao, insert_tb.hr_inicio, insert_tb.hr_fim)
    )
    conn.commit()

    if cursor.lastrowid is None:
        print("Erro: Nenhum usuário foi inserido!")
        return

    cursor.execute("""
        INSERT INTO tb_reserva_sala_reuniao_bkp 
        SELECT * 
        FROM tb_reserva_sala_reuniao
        WHERE id = ?""",
        (cursor.lastrowid,)
    )
    conn.commit()
  

def Incluir_usuario(insert_tb_usuario):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(""" 
        INSERT INTO tb_usuario (email, senha, perfil) 
        VALUES(?, ?, ?)""",
        (insert_tb_usuario.email, insert_tb_usuario.senha, insert_tb_usuario.perfil)
    )
    conn.commit()

    if cursor.lastrowid is None:
        print("Erro: Nenhum usuário foi inserido!")
        return
    
    cursor.execute("""
        INSERT INTO tb_usuario_bkp 
        SELECT * 
        FROM tb_usuario
        WHERE id = ?""",
        (cursor.lastrowid,)
    )
    conn.commit()

def Incluir_sala(insert_tb_sala):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(""" 
        INSERT INTO tb_sala (sala)
        VALUES(?)""",
        (insert_tb_sala.sala,)
    )
    conn.commit()

    cursor.execute("""
        INSERT INTO tb_sala_bkp 
        SELECT * 
        FROM tb_sala
        WHERE id = ?""",
        (cursor.lastrowid,)
    )
    conn.commit()

# def Alterar(alterar_tb):
#     count = cursor.execute(""" 
#     UPDATE tb_reserva_sala_reuniao
#     SET 
#         sala_reuniao = ?, 
#         dt_reuniao   = ?,
#         hr_inicio    = ?,
#         hr_fim       = ?
#     WHERE id = ?""",
#     alterar_tb.sala_reuniao, alterar_tb.dt_reuniao, alterar_tb.hr_inicio, alterar_tb.hr_fim).rowcount
#     conn.commit()

def Excluir(excluir_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(""" 
        DELETE FROM tb_reserva_sala_reuniao WHERE id = ?""", 
        (excluir_id.id,)
    )
    conn.commit()

def ExcluirSala(excluir_sala):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(""" 
        DELETE FROM tb_sala WHERE sala = ?""", 
        (excluir_sala.sala,)
    )
    conn.commit()

def ExcluirUsuario(excluir_email):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(""" 
        DELETE FROM tb_usuario WHERE email = ?""", 
        (excluir_email.email,)
    )
    conn.commit()



def AlterarUsuario(alterar_tb_usuario):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(""" 
        UPDATE tb_usuario
        SET   perfil = ?
        WHERE email = ?""",
        (alterar_tb_usuario.email,)
    )
    conn.commit()



def selecionarTodos():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, user, sala_reuniao, strftime('%d/%m/%Y', dt_reuniao) AS dt_reuniao, hr_inicio, hr_fim FROM tb_reserva_sala_reuniao")
    customerList = []

    for row in cursor.fetchall():
        customerList.append(reservas.reserva_sala(row[0], row[1], row[2], row[3], row[4], row[5]))

    return customerList

def selecionarTodosUsuarios():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tb_usuario")
    customerList = []

    for row in cursor.fetchall():
        customerList.append(reservas.usuario(row[0], row[1], row[2], row[3]))

    return customerList

def selecionarSalas():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tb_sala")
    customerList = []

    for row in cursor.fetchall():
        customerList.append(reservas.sala_cadastro(row[0], row[1]))

    return customerList

def obter_reservas_por_sala_e_data(sala, data):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = """
        SELECT 
            hr_inicio, hr_fim
        FROM 
            tb_reserva_sala_reuniao
        WHERE 
            sala_reuniao = ? AND dt_reuniao = ?
    """
    cursor.execute(query, (sala, data))
    reservas = cursor.fetchall()
    conn.commit()
    return reservas


def obter_usuarios_cadastrados(usuario):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = """
        SELECT 
            email
        FROM 
            tb_usuario
        WHERE 
            email = ?
    """
    cursor.execute(query, (usuario,))
    usuario_ = cursor.fetchall()
    conn.commit()
    return usuario_


def obter_perfil_usuario(usuario):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = """
        SELECT 
            perfil
        FROM 
            tb_usuario
        WHERE 
            email = ?
    """
    cursor.execute(query, (usuario,))
    usuario_ = cursor.fetchone()
    conn.commit()
    return usuario_[0] if usuario_ else None
