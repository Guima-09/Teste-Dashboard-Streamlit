import streamlit as st
from sentence_transformers import SentenceTransformer
import config

@st.cache_resource
def get_model():
    return SentenceTransformer(
        config.MODELO_NOME,
        device=config.dispositivo
    )