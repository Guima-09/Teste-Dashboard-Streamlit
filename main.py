import streamlit as st
import pesquisa
import dashboard
import subprocess
import sys

st.set_page_config(page_title="Dashboard OASIS", layout="wide")
st.title("🏛️ Dashboard dos Projetos de Lei - IA OASIS")

tab_pesquisa, tab_bd= st.tabs([
    "📊 Pesquisa", 
     "📄 Atualizar Base de Dados (BETA)", 
])

atualizar = False

with tab_pesquisa:
    # Inicia o estado se não existir
    if 'ia_concluida' not in st.session_state:
        st.session_state.ia_concluida = False

    # ==============================================
    # BARRA DE PESQUISA
    # ==============================================
    st.markdown("---")
    st.subheader("🧠 Pesquisa Inteligente")

    col1, col2 = st.columns(2)

    with col1:
        # Caixa de pesquisa ocupando o centro da tela
        tema_pesquisa_principal = st.text_input(
            "Digite o tema ou assunto para filtrar na base da Câmara:",
            help = "Priorize este campo, pois ele tem um peso maior na busca. Frases completas e significativas têm um resultado melhor do que termos curtos e/ou vagos."
        )
    with col2:
        tema_pesquisa_secundaria = st.text_input(
            "Digite o tema ou assunto secundário para filtrar na base da Câmara:",
            help="Este campo é opcional, você pode deixá-lo vazio se quiser. Se usado, a pesquisa o combina com a busca principal em uma média ponderada para o cálculo de similaridade. Este campo tem um peso menor."
        )

    if st.button("Filtrar", type="primary"):
        if (atualizar == False):
            # O st.write agora aparecerá e permanecerá enquanto o spinner rodar
            st.write(f"Buscando por: **{tema_pesquisa_principal}** com o filtro **{tema_pesquisa_secundaria}**")
            
            with st.spinner("Vetorizando pesquisa e analisando o histórico..."):
                # Escrita dos arquivos
                with open('banco_de_dados_local/pesquisa1.txt', 'w', encoding='utf-8') as f:
                    f.write(tema_pesquisa_principal)
                
                with open('banco_de_dados_local/pesquisa2.txt', 'w', encoding='utf-8') as f:
                    f.write(tema_pesquisa_secundaria)

                # Limpa o cache antes de pesquisar para garantir dados novos
                st.cache_data.clear()
                
                # Roda o processamento
                pesquisa.pesquisar()

                # Marca como concluído
                st.session_state.ia_concluida = True
        else:
            st.warning("Atualização de dados iniciada! Atualize a base de dados primeiro!")
        
    st.markdown("---")

    # ==============================================
    # VITRINE (DASHBOARD)
    # ==============================================
    if st.session_state.ia_concluida:
        # Roda o dashboard
        dashboard.rodar_dashboard()

with tab_bd:
    st.subheader(":red[AVISO: Este Botão serve para atualizar a base de dados com os projetos mais recentes. ESSA EXECUÇÂO DEMORA EM MEDIA 1 HORA, cuidado ao prosseguir.]")
    if st.button("Atualizar", type="primary"):
        with st.spinner("Vetorizando pesquisa..."):
            # sys.executable garante que você use o mesmo Python que está rodando o Streamlit
            resultado = subprocess.run([sys.executable, "embeddings.py"], capture_output=True, text=True)
            
            if resultado.returncode == 0:
                st.success("Processo finalizado com sucesso!")
            else:
                st.error("Erro ao executar o script:")
                st.code(resultado.stderr) # Mostra o erro real que aconteceu


    