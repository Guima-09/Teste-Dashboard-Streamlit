import streamlit as st
import pesquisa
import traceback

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
        st.write("Iniciando a busca...")
        
        # O bloco try/except vai "caçar" onde o código está travando
        try:
            print(">>> Entrando na função pesquisa.pesquisar()...")
            
            # Chama a sua função original
            pesquisa.pesquisar(termo_pesquisa)
            
            print(">>> Função finalizada com sucesso!")
            st.success("Busca concluída!")
            
        except Exception as e:
            # Se algo der errado lá dentro, ele para tudo e avisa aqui:
            print(f"!!! DEU ERRO !!! -> {e}")
            st.error("Ops! Aconteceu um erro interno na pesquisa.")
            
            # Isso vai imprimir o erro completo e a linha exata no seu dashboard
            st.code(traceback.format_exc(), language='python')