import streamlit as st
import Pages.reserva_sala_reuniao.Create as PagesCreateReserva
import Pages.reserva_sala_reuniao.List as PagesListReserva
import Pages.reserva_sala_reuniao.validacao_user as acesso
from Controllers.ControllersReservas import create_tb, obter_perfil_usuario

create_tb()
print("Tabelas criadas com sucesso!")


st.markdown(
    """
    <style>
    /* Mudar o fundo para cinza */
    .stApp {
        background-color: #FCFCFC; /* Cor cinza claro */
    }

    /* Estilizar o título */
    .stMarkdown h1 {
        color: #000000; /* Cor cinza escuro */
        text-align: center;
    }

    /* Estilo básico dos botões */
    .stButton button {
        border: 2px solid #007BFF; /* Borda azul */
        background-color: white; /* Fundo branco */
        color: #007BFF; /* Texto azul */
        padding: 5px 12px;
        border-radius: 12px;
        cursor: pointer;
        font-size: 16px;
        transition: all 0.3s ease; /* Suaviza a transição */
    }

    /* Estilo ao passar o mouse */
    .stButton button:hover {
        background-color: #007BFF; /* Fundo azul */
        color: white; /* Texto branco */
        border-color: #0056b3; /* Borda um pouco mais escura */
    }

    /* Remove estilos padrão ao focar ou clicar */
    .stButton button:focus {
        outline: none; /* Remove o contorno de foco */
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div style="text-align: center;">
        <img src="https://catagua.com.br/wp-content/uploads/2022/01/cropped-catagua-construtora-180x50.png.webp" alt="Logo Catagua">
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown( #titulo Reserva de Salas
    """
    <h1 style="text-align: center; font-size: 34px;">Systems</h1>
    """,
    unsafe_allow_html=True
)

# CSS para o conteúdo fixo
st.markdown(
    """
    <style>
    /* Estiliza o conteúdo fixo no rodapé */
    .fixed-footer {
        position: fixed;
        bottom: 10px; /* Espaço do rodapé */
        right: 10px; /* Espaço da lateral */
        background-color: rgba(255, 255, 255, 0.8); /* Fundo semitransparente */
        padding: 5px 10px; /* Espaço interno */
        border-radius: 5px; /* Bordas arredondadas */
        box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1); /* Sombra */
        font-size: 14px; /* Tamanho da fonte */
        z-index: 1000; /* Garante que fique sobre outros elementos */
    }
    </style>

    """,
    unsafe_allow_html=True
    #     <div class="fixed-footer">
    #     <img src="https://example.com/sua-imagem.png" alt="Logo" width="120"><br>
    #     <p>Seu texto fixo aqui!</p>
    # </div>
)

def usuario_adm():
    # Criar colunas para botões
    col1, col2, col3, col4, col5, col6, col7 = st.columns(7)
    with col1:
        st.sidebar.title("Reserva")
        reservar_button = st.sidebar.button("Reservar Sala", key="reservar_button")
    with col2:
        cancelar_button = st.sidebar.button("Cancelar Reserva", key="cancelar_button")
    with col3:
        st.sidebar.title("Cadastro")
        incluir_usuario_button = st.sidebar.button("Cadastrar Usuário", key="cadastrar_usuario_button")
    # with col4:
    #     alterar_usuario_button = st.sidebar.button("Alterar Usuário", key="alterar_usuario_button")
    with col5:
        excluir_usuario_button = st.sidebar.button("Excluir Usuário", key="excluir_usuario_button")
    with col6:
        incluir_sala_button = st.sidebar.button("Cadastrar Sala", key="cadastrar_sala_button")
    with col7:
        excluir_sala_button = st.sidebar.button("Excluir Sala", key="excluir_sala_button")

    # Armazenar estado atual no session_state
    if "active_page" not in st.session_state:
        st.session_state["active_page"] = "listar"  # Página inicial padrão

    # Navegar entre páginas com base nos botões
    if reservar_button:
        st.session_state["active_page"] = "reservar"
    elif cancelar_button:
        st.session_state["active_page"] = "cancelar"
    elif incluir_usuario_button:
        st.session_state["active_page"] = "cadastrarUsuario"
    # elif alterar_usuario_button:
    #     st.session_state["active_page"] = "alterarUsuario"
    elif excluir_usuario_button:
        st.session_state["active_page"] = "excluirUsuario"
    elif incluir_sala_button:
        st.session_state["active_page"] = "cadastrarSala"
    elif excluir_sala_button:
        st.session_state["active_page"] = "excluirSala"

    # Renderizar a página atual
    if st.session_state["active_page"] == "reservar":
        PagesCreateReserva.Incluir()
        PagesListReserva.List()
    elif st.session_state["active_page"] == "cancelar":
        PagesCreateReserva.Excluir()
        PagesListReserva.List()
    elif st.session_state["active_page"] == "cadastrarUsuario":
        PagesCreateReserva.Incluir_usuario()
        PagesListReserva.ListUsuarios()
    # elif st.session_state["active_page"] == "alterarUsuario":
    #     PagesCreateReserva.AlterarUsuario()
    #     PagesListReserva.ListUsuarios()
    elif st.session_state["active_page"] == "excluirUsuario":
        PagesCreateReserva.ExcluirUsuario()
        PagesListReserva.ListUsuarios()
    elif st.session_state["active_page"] == "cadastrarSala":
        PagesCreateReserva.cadastrar_sala()
        PagesListReserva.ListSalas()
    elif st.session_state["active_page"] == "excluirSala":
        PagesCreateReserva.ExcluirSala()
        PagesListReserva.ListSalas()

def usuario_exec():
    # Criar colunas para botões
    col1, col2 = st.columns(2)
    with col1:
        st.sidebar.title("Reserva")
        reservar_button = st.sidebar.button("Reservar Sala", key="reservar_button")
    with col2:
        cancelar_button = st.sidebar.button("Cancelar Reserva", key="cancelar_button")

    # Armazenar estado atual no session_state
    if "active_page" not in st.session_state:
        st.session_state["active_page"] = "listar"  # Página inicial padrão

    # Navegar entre páginas com base nos botões
    if reservar_button:
        st.session_state["active_page"] = "reservar"
    elif cancelar_button:
        st.session_state["active_page"] = "cancelar"

    # Renderizar a página atual
    if st.session_state["active_page"] == "reservar":
        PagesCreateReserva.Incluir()
        PagesListReserva.List()
    elif st.session_state["active_page"] == "cancelar":
        PagesCreateReserva.Excluir()
        PagesListReserva.List()

# Verifica se o usuário está autenticado
if acesso.authenticate_user():
    perfil = obter_perfil_usuario(st.session_state["user"])
    print(perfil)
    if perfil == "Administrador":
        usuario_adm()
    elif perfil == "Executor":
        usuario_exec()

# PagesCreateReserva.Incluir_usuario()
# PagesListReserva.ListUsuarios()