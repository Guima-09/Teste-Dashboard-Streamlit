import streamlit as st
import pesquisa

# ==============================================
# 1) CONFIGURAÇÃO BÁSICA DO APP
# ==============================================
st.set_page_config(
    page_title="Dashboard OASIS",
    layout="wide"
)

st.title("🏛️ Dashboard dos Projetos de Lei - IA OASIS")
st.markdown("Visualização das proposições filtradas e classificadas pela Inteligência Artificial.")

termo_pesquisa = st.text_input(label="Pesquisar Projeto de Lei")

# Usamos o session_state para lembrar que uma pesquisa foi feita
if 'pesquisa_realizada' not in st.session_state:
    st.session_state.pesquisa_realizada = False

if st.button('Pesquisar'):
    # Muda o estado para avisar que temos resultados para mostrar
    st.session_state.pesquisa_realizada = True

# Se o botão foi clicado, roda a função (e mantém na tela!)
if st.session_state.pesquisa_realizada and termo_pesquisa:
    with st.spinner('A IA OASIS está analisando e buscando os dados no banco...'):
        # Certifique-se de que dentro do pesquisa.py NÃO tem outro st.set_page_config
        st.write("Pesquisando, por favor aguarde")
        pesquisa.pesquisar(termo_pesquisa)