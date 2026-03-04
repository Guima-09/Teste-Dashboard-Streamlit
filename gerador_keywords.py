import json
import pickle
import os
import glob
import config
from utils_legislativo import validar_tag
from embeddings import get_model


def extrair_keywords(dados):
    """
    Percorre todas as proposições de um JSON
    e extrai um conjunto único de keywords/indexações.

    Responsabilidade:
    - limpar
    - validar
    - deduplicar
    - ordenar

    Retorna:
        lista ordenada de keywords únicas.
    """
    unique_keywords = set()

    for projeto in dados:
        texto = projeto.get('keywords') or projeto.get('indexacao')
        if texto:
            for termo in texto.replace(';', ',').split(','):
                tag = validar_tag(termo)
                if tag:
                    unique_keywords.add(tag)

    return sorted(list(unique_keywords))


if __name__ == "__main__":
    print("Carregando modelo de IA...")
    model = get_model()

    padrao_busca = os.path.join(config.PASTA_DADOS, "camara_db_leg*.json")
    arquivos_db = glob.glob(padrao_busca)

    for arquivo in arquivos_db:
        nome_base = os.path.basename(arquivo)
        sufixo = nome_base.replace("camara_db_", "").replace(".json", "")
        arquivo_pkl = os.path.join(config.PASTA_DADOS, f"keywords_embeddings_{sufixo}.pkl")

        print(f"\nProcessando legislatura: {sufixo}")

        with open(arquivo, 'r', encoding='utf-8') as f:
            dados = json.load(f)

        keywords = extrair_keywords(dados)

        if not keywords:
            print("Nenhuma keyword encontrada. Pulando.")
            continue

        precisa_atualizar = True

        # 🔹 NOVA LÓGICA ESSENCIAL:
        # Validação estrutural do cache ao invés de comparação por data
        if os.path.exists(arquivo_pkl):
            try:
                with open(arquivo_pkl, "rb") as f:
                    cache = pickle.load(f)

                if (
                    isinstance(cache, dict)
                    and "keywords_texto" in cache
                    and "keywords_vectors" in cache
                    and len(cache["keywords_texto"]) == len(keywords)
                ):
                    print(f"Cache válido para {sufixo}. Pulando vetorização.")
                    precisa_atualizar = False

            except Exception:
                print("Cache corrompido ou inválido. Regerando.")

        if precisa_atualizar:
            print(f"Vetorizando {len(keywords)} tags...")

            embeddings = model.encode(
                keywords,
                batch_size=64,
                show_progress_bar=True,
                convert_to_tensor=True
            )

            with open(arquivo_pkl, "wb") as f:
                pickle.dump(
                    {
                        "keywords_texto": keywords,
                        "keywords_vectors": embeddings.cpu()
                    },
                    f
                )

            print(f"Salvo: {arquivo_pkl}")