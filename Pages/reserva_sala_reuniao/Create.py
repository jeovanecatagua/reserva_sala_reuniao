import streamlit as st
import Controllers.ControllersReservas as ControllersReservas
import models.reservas as reservas
import datetime as dt
import Pages.reserva_sala_reuniao.validacao_user as acesso
import pandas as pd
import random
import string

def Incluir_usuario():  
    def gerar_senha():
        tamanho_senha = 8
        caracteres = string.ascii_letters + string.digits  # Letras e números
        senha = ''.join(random.choice(caracteres) for i in range(tamanho_senha))
        return senha

    # Chama a função e gera uma senha aleatória
    senha_gerada = gerar_senha()

    with st.form(key="cadastrar_usuario"):
        input_usuario       = st.text_input("**E-mail**", value=None)
        input_senha         = st.text_input("**Senha**", value=senha_gerada, disabled=True)
        input_perfil        = st.selectbox("**Perfil**", options=["Administrador", "Executor"])
        input_button_submit = st.form_submit_button("**Enviar**")

        if input_button_submit:
            if input_usuario is None:
                st.error("O E-mail está em branco.")
                return
            
            usuarios_existentes = ControllersReservas.obter_usuarios_cadastrados(input_usuario) 
            if usuarios_existentes:
                st.error("Usuário já cadastrado")
                return

            reservas.email  = input_usuario
            reservas.senha  = input_senha
            reservas.perfil = input_perfil

            ControllersReservas.Incluir_usuario(reservas)
            st.success(f"Usuário: **{input_usuario}** e Senha: **{input_senha}** cadastrado!" )


def verifica_conflito(sala, data, horario_inicio, horario_fim):
    reservas_existentes = ControllersReservas.obter_reservas_por_sala_e_data(sala, data)

    hora_inicio_dt = dt.datetime.combine(dt.datetime.strptime(data, "%Y-%m-%d").date(), horario_inicio)
    hora_fim_dt    = dt.datetime.combine(dt.datetime.strptime(data, "%Y-%m-%d").date(), horario_fim)

    # Verifica se existe alguma reserva com sobreposição
    for reserva in reservas_existentes:
        reserva_inicio_dt = dt.datetime.strptime(f"{data} {reserva[0]}", "%Y-%m-%d %H:%M:%S")
        reserva_fim_dt    = dt.datetime.strptime(f"{data} {reserva[1]}", "%Y-%m-%d %H:%M:%S")

        print(reserva_inicio_dt, reserva_fim_dt)
        
        if hora_inicio_dt < reserva_fim_dt and hora_fim_dt > reserva_inicio_dt:
            return True  # Conflito encontrado

    return False  # Sem conflito

def Incluir():
    def ListSalasFiltro():
        customerList = []

        for item in ControllersReservas.selecionarSalas():
            customerList.append(item.sala)

        return customerList

    sala_list = ListSalasFiltro()

    # Verifica se o usuário está autenticado
    if "authenticated" not in st.session_state or not st.session_state["authenticated"]:
        st.error("Você precisa estar autenticado para fazer uma reserva.")
        return
    
    # Garante que o usuário autenticado está disponível no session_state
    user = st.session_state.get("user", "")
    
    if not user:
        st.error("Erro ao identificar o usuário autenticado. Faça login novamente.")
        return
    
    with st.form(key="incluir_reserva"):
        input_user = st.text_input("**Usuário**", value=user, disabled=True, key="usuario_autenticado") #st.text_input("Usuário", value=user, disabled=True)        
        input_sala_reuniao = st.selectbox(
            "**Selecione a sala**",
            options=sorted(sala_list)
        )
        input_dt_reuniao = st.date_input("**Escolha uma data para a reunião:**", format="DD/MM/YYYY")
        horario_inicio   = st.time_input("**Horário de início:**", value=None)
        horario_fim      = st.time_input("**Horário de fim:**", value=None)

        input_button_submit = st.form_submit_button("**Enviar**")

    if input_button_submit:
        if horario_inicio is None or horario_fim is None:
            st.error("O horário de início ou de fim está em branco.")
            return
        if horario_inicio >= horario_fim:
            st.error("O horário de término deve ser após o horário de início.")
            return
        print(
            input_sala_reuniao, 
            input_dt_reuniao.strftime("%Y-%m-%d"), 
            horario_inicio, 
            horario_fim
        )
        if verifica_conflito(input_sala_reuniao, input_dt_reuniao.strftime("%Y-%m-%d"), horario_inicio, horario_fim):
            st.error(f"A sala {input_sala_reuniao} já está reservada nesse horário.")
            return

        reservas.user           = input_user
        reservas.sala_reuniao   = input_sala_reuniao
        reservas.dt_reuniao     = input_dt_reuniao
        reservas.hr_inicio      = horario_inicio.strftime("%H:%M:%S")  # Converte para texto
        reservas.hr_fim         = horario_fim.strftime("%H:%M:%S")  # Converte para texto

        ControllersReservas.Incluir(reservas)
        st.success(f"Sala de reunião {input_sala_reuniao} reservada!" )

def Excluir():
    def List():   
        customerList = []

        for item in ControllersReservas.selecionarTodos():
            customerList.append([item.id])

        df = pd.DataFrame(
            customerList,
            columns=['id']
        )  

        salas  = df['id'].unique()

        return salas
    # Verifica se o usuário está autenticado
    if "authenticated" not in st.session_state or not st.session_state["authenticated"]:
        st.error("Você precisa estar autenticado para fazer uma reserva.")
        return
    
    # Garante que o usuário autenticado está disponível no session_state
    user = st.session_state.get("user", "")
    
    if not user:
        st.error("Erro ao identificar o usuário autenticado. Faça login novamente.")
        return
    
    with st.form(key="incluir_reserva"):
        input_id_reserva = st.selectbox(
            "**ID da Reserva**",
            List()
        )

        input_button_submit = st.form_submit_button("**Enviar**")

    if input_button_submit:
        reservas.id = input_id_reserva

        ControllersReservas.Excluir(reservas)
        st.success(f"Reserva {input_id_reserva} excluída!" )




def AlterarPerfilUsuario():
    def ListEmail():   
        customerList = []

        for item in ControllersReservas.selecionarTodosUsuarios():
            customerList.append([item.email, item.perfil])

        df = pd.DataFrame(
            customerList,
            columns=['email', 'perfil']
        )  

        email = df['email'].unique()
        perfil = df['perfil'].unique()

        return email, perfil
    
    def ListPerfil():   
        customerList = []

        for item in ControllersReservas.selecionarTodosUsuarios():
            customerList.append([item.email, item.perfil])

        df = pd.DataFrame(
            customerList,
            columns=['email', 'perfil']
        )  

        perfil = df['perfil'].unique()

        return perfil
    # Verifica se o usuário está autenticado
    if "authenticated" not in st.session_state or not st.session_state["authenticated"]:
        st.error("Você precisa estar autenticado para excluir.")
        return
    
    # Garante que o usuário autenticado está disponível no session_state
    user = st.session_state.get("user", "")
    
    if not user:
        st.error("Erro ao identificar o usuário autenticado. Faça login novamente.")
        return
    
    with st.form(key="alterar_perfil"):
        input_email = st.selectbox(
            "**E-mail cadastrado**",
            ListEmail()
        )

        input_button_submit = st.form_submit_button("**Enviar**")

    if input_button_submit:
        reservas.email = input_email

        ControllersReservas.ExcluirUsuario(reservas)
        st.success(f"Usuário {input_email} excluído!" )





def ExcluirUsuario():
    def List():   
        customerList = []

        for item in ControllersReservas.selecionarTodosUsuarios():
            customerList.append([item.email])

        df = pd.DataFrame(
            customerList,
            columns=['email']
        )  

        email = df['email'].unique()

        return email
    # Verifica se o usuário está autenticado
    if "authenticated" not in st.session_state or not st.session_state["authenticated"]:
        st.error("Você precisa estar autenticado para excluir.")
        return
    
    # Garante que o usuário autenticado está disponível no session_state
    user = st.session_state.get("user", "")
    
    if not user:
        st.error("Erro ao identificar o usuário autenticado. Faça login novamente.")
        return
    
    with st.form(key="incluir_reserva"):
        input_email = st.selectbox(
            "**E-mail cadastrado**",
            List()
        )

        input_button_submit = st.form_submit_button("**Enviar**")

    if input_button_submit:
        reservas.email = input_email

        ControllersReservas.ExcluirUsuario(reservas)
        st.success(f"Usuário {input_email} excluído!" )

    
def cadastrar_sala():
    with st.form(key="incluir_reserva"):
        sala_reuniao        = st.text_input("**Sala de Reunião**", value=None)
        input_button_submit = st.form_submit_button("**Enviar**")

        if input_button_submit:
            reservas.sala = sala_reuniao

            ControllersReservas.Incluir_sala(reservas)
            st.success(f"Sala de reunião {sala_reuniao} cadastrada!" )

def ExcluirSala():
    def ListSalasFiltro():
        customerList = []

        for item in ControllersReservas.selecionarSalas():
            customerList.append(item.sala)

        return customerList

    sala_list = ListSalasFiltro()
    
    # Verifica se o usuário está autenticado
    if "authenticated" not in st.session_state or not st.session_state["authenticated"]:
        st.error("Você precisa estar autenticado para excluir.")
        return
    
    # Garante que o usuário autenticado está disponível no session_state
    user = st.session_state.get("user", "")
    
    if not user:
        st.error("Erro ao identificar o usuário autenticado. Faça login novamente.")
        return
    
    with st.form(key="excluir_sala"):
        input_sala = st.selectbox(
            "**Sala de reunião**",
            sorted(sala_list)
        )

        input_button_submit = st.form_submit_button("**Enviar**")

        if input_button_submit:
            reservas.sala = input_sala

            ControllersReservas.ExcluirSala(reservas)
            st.success(f"Usuário {input_sala} excluído!" )
