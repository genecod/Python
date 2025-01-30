import sqlite3
import streamlit as st

# Função para conectar ao banco e criar a tabela se não existir
def criar_tabela():
    conn = sqlite3.connect("clientes.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            sexo TEXT NOT NULL,
            email TEXT NOT NULL,
            telefone TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Função para inserir dados no banco
def salvar_cliente(nome,sexo, email, telefone):
    conn = sqlite3.connect("clientes.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO clientes (nome, sexo, email, telefone) VALUES (?, ?, ?, ?)", (nome, sexo, email, telefone))
    conn.commit()
    conn.close()

# Função para listar os clientes
def listar_clientes():
    conn = sqlite3.connect("clientes.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM clientes")
    dados = cursor.fetchall()
    conn.close()
    return dados

# Criar a tabela se ainda não existir
criar_tabela()

st.set_page_config(page_title="Gestão de Clientes", page_icon=":bar_chart:", initial_sidebar_state="collapsed")


# Interface do Streamlit
st.title("Gestão de Clientes")

# Criar menu de navegação
pagina = st.radio("Escolha uma opção:", ["Cadastrar Cliente", "Clientes Cadastrados"])

# ---- Página de Cadastro ----
if pagina == "Cadastrar Cliente":
    st.subheader("Cadastro de Cliente")

    with st.form("form_cliente"):
        nome = st.text_input("Nome")
        sexo = st.selectbox("Sexo", ["selecionar", "Masculino", "Feminino", "Outro"])
        email = st.text_input("E-mail")
        telefone = st.text_input("Telefone")
        cadastrar_cliente = st.form_submit_button("cadastrar cliente")

        if cadastrar_cliente:
            if nome and email:  # Verifica se os campos obrigatórios estão preenchidos
                salvar_cliente(nome, sexo, email, telefone)
                st.success("Cliente salvo com sucesso!")
            else:
                st.error("Por favor, preencha os campos obrigatórios (Nome e E-mail).")

# ---- Página de Listagem ----
elif pagina == "Clientes Cadastrados":
    st.subheader("Clientes Cadastrados")
    
    clientes = listar_clientes()
    
    if clientes:
        for cliente in clientes:
            st.write(f"**Nome:** {cliente[1]} - **Sexo:** {cliente[2]} - **E-mail:** {cliente[3]} - **Telefone:** {cliente[4]}")
    else:
        st.info("Nenhum cliente cadastrado ainda.")
