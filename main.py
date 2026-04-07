import streamlit as st
import pesquisa
import dashboard
import os
import glob
import config
# Importamos as funções diretamente do seu embeddings.py
from embeddings import get_model, gerar_embeddings_para_legislatura 

st.set_page_config(page_title="Dashboard OASIS", layout="wide")
st.title("🏛️ Dashboard dos Projetos de Lei - IA OASIS")

# Inicializa estados de controle
if 'ia_concluida' not in st.session_state:
    st.session_state.ia_concluida = False
if 'atualizando_db' not in st.session_state:
    st.session_state.atualizando_db = False

tab_pesquisa, tab_bd = st.tabs([
    "📊 Pesquisa", 
    "📄 Atualizar Base de Dados (BETA)", 
])

with tab_pesquisa:
    st.markdown("---")
    st.subheader("🧠 Pesquisa Inteligente")

    # Bloqueia a pesquisa se o banco estiver sendo atualizado
    if st.session_state.atualizando_db:
        st.warning("⚠️ Base de dados em atualização. Por favor, aguarde a conclusão na outra aba.")
    
    col1, col2 = st.columns(2)
    with col1:
        tema_pesquisa_principal = st.text_input("Tema principal:", help="Peso maior na busca.")
    with col2:
        tema_pesquisa_secundaria = st.text_input("Tema secundário (opcional):")

    if st.button("Filtrar", type="primary", disabled=st.session_state.atualizando_db):
        with st.spinner("Vetorizando pesquisa..."):
            # Lógica de escrita de arquivos preservada
            os.makedirs('banco_de_dados_local', exist_ok=True)
            with open('banco_de_dados_local/pesquisa1.txt', 'w', encoding='utf-8') as f:
                f.write(tema_pesquisa_principal)
            with open('banco_de_dados_local/pesquisa2.txt', 'w', encoding='utf-8') as f:
                f.write(tema_pesquisa_secundaria)

            st.cache_data.clear()
            pesquisa.pesquisar()
            st.session_state.ia_concluida = True
        
    st.markdown("---")
    
    if st.session_state.ia_concluida:
        dashboard.rodar_dashboard()

with tab_bd:
    st.subheader(":red[AVISO: Atualização da base de dados com projetos recentes.]")
    st.info("Duração estimada: ~1 hora. Mantenha esta aba aberta.")
    
    # Botão que desabilita a si mesmo enquanto roda
    if st.button("Iniciar Atualização", type="primary", disabled=st.session_state.atualizando_db):
        st.session_state.atualizando_db = True
        
        # Containers para feedback em tempo real
        status_info = st.empty()
        barra_progresso = st.progress(0)
        
        try:
            status_info.write("⏳ Inicializando modelo de IA (isso pode levar um minuto)...")
            model = get_model()
            
            padrao_busca = os.path.join(config.PASTA_DADOS, "camara_db_leg*.json")
            arquivos_json = glob.glob(padrao_busca)
            
            if not arquivos_json:
                st.error("Nenhum arquivo JSON encontrado em " + config.PASTA_DADOS)
            else:
                for arquivo in arquivos_json:
                    # Chama a função do embeddings.py injetando a barra de progresso
                    gerar_embeddings_para_legislatura(
                        model, 
                        arquivo, 
                        pbar=barra_progresso, 
                        status_text=status_info
                    )
                
                st.success("✅ Processo finalizado com sucesso!")
                st.balloons()
        
        except Exception as e:
            st.error(f"Erro crítico durante a atualização: {e}")
        
        finally:
            st.session_state.atualizando_db = False
            # O rerun garante que o estado dos botões 'disabled' seja atualizado
            st.rerun()