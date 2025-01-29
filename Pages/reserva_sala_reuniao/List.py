import streamlit as st
import Controllers.ControllersReservas as ControllersReservas
import pandas as pd
# from st_aggrid import AgGrid

def List():
    customerList = []

    for item in ControllersReservas.selecionarTodos():
        customerList.append([item.id, item.user, item.sala_reuniao, item.dt_reuniao, item.hr_inicio, item.hr_fim])

    df = pd.DataFrame(
        customerList,
        columns=['ID', 'Usuário', 'Sala de reunião', 'Data da reserva', 'Horário de ínicio', 'Horário de fim']
    )

    tab_filtros, tab_reservas = st.tabs(["Filtros", "Reservas"])

    with tab_filtros:
        st.header("Filtros")
        salas = df['Sala de reunião'].unique()
        sala_filtro = st.selectbox("Selecione a sala", options=["Todas"] + sorted(list(salas)))
        data_filtro = st.date_input("Selecione a data (opcional)", value=None, format="DD/MM/YYYY")

        if sala_filtro != "Todas":
            df = df[df['Sala de reunião'] == sala_filtro]

        if data_filtro:
            data_formatada = data_filtro.strftime("%d/%m/%Y")
            df = df[df['Data da reserva'] == data_formatada]

    with tab_reservas:
        st.subheader("Salas de reunião reservadas")
        st.dataframe(df)

def ListUsuarios():
    customerList = []

    for item in ControllersReservas.selecionarTodosUsuarios():
        customerList.append([item.id, item.email, item.senha, item.perfil])

    df = pd.DataFrame(
        customerList,
        columns=['ID', 'E-mail', 'Senha', 'perfil']
    )

    st.dataframe(df)

def ListSalas():
    customerList = []

    for item in ControllersReservas.selecionarSalas():
        customerList.append([item.id, item.sala])

    df = pd.DataFrame(
        customerList,
        columns=['ID', 'Sala']
    )

    st.dataframe(df)