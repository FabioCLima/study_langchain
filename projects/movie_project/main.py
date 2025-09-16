# main.py
import argparse
import random
import re

import pandas as pd  # 1. Importamos o pandas
from core.settings import settings, setup_environment

setup_environment()


from core.logger import logger
from core.models import MovieInfoData
from core.orchestrator import create_movie_analysis_graph


def sanitize_filename(text: str) -> str:
    """Limpa uma string para ser usada como um nome de arquivo seguro."""
    text = text.lower()
    text = re.sub(r"\s+", "_", text)
    text = re.sub(r"[^\w-]", "", text)
    return text


def main(genre: str):
    """Função principal que executa o grafo de análise de filmes e salva os resultados.
    """
    logger.info(f"🚀 Iniciando a análise completa de filmes do gênero: '{genre}'")

    try:
        movie_graph = create_movie_analysis_graph()
        logger.info("Invocando o grafo com o LLM (isso pode levar um tempo)...")
        graph_result = movie_graph.invoke({"genre": genre})

        suggested_movies = graph_result["suggestion_result"].movies
        detailed_results: list[MovieInfoData] = graph_result["detailed_results"]

        print(f"\n--- Top 10 Filmes de {genre.title()} Recomendados ---")
        for movie_title in suggested_movies:
            print(f"- {movie_title}")
        print("---------------------------------------------------\n")

        if detailed_results:
            sample_movie = random.choice(detailed_results)
            print("--- Amostra Aleatória de Análise Detalhada ---")
            print(f"🎬 Título: {sample_movie.title} ({sample_movie.release_year})")
            print(f"🎬 Diretor: {sample_movie.director}")
            print(f"👥 Atores: {', '.join(sample_movie.main_actors)}")
            print(f"💰 Bilheteria: ${sample_movie.box_office_revenue:,.2f}")
            print(f"🏆 Oscars: {sample_movie.oscars_won}")
            print("----------------------------------------------\n")

            # 2. Convertendo os resultados para um DataFrame do Pandas
            # Usamos model_dump() para transformar cada objeto Pydantic em um dicionário
            df = pd.DataFrame([movie.model_dump() for movie in detailed_results])

            print("--- Análise de Dados (DataFrame) ---")
            print(df)
            print("------------------------------------\n")

            # 3. Salvando os arquivos
            sanitized_genre = sanitize_filename(genre)
            txt_filepath = settings.output_dir / f"filmes_{sanitized_genre}_sugeridos.txt"
            csv_filepath = settings.output_dir / f"analise_{sanitized_genre}_detalhada.csv"

            with open(txt_filepath, "w", encoding="utf-8") as f:
                f.writelines(f"{title}\n" for title in suggested_movies)
            logger.info(f"📝 Lista de sugestões salva em: {txt_filepath}")

            # 4. Usando o método .to_csv() do DataFrame, que é mais simples e robusto
            df.to_csv(csv_filepath, index=False, encoding="utf-8")
            logger.info(f"📊 Análise detalhada salva em: {csv_filepath}")

        logger.success("✅ Processo concluído com sucesso!")

    except Exception as e:
        logger.exception(f"❌ Ocorreu um erro inesperado: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Receba recomendações de filmes por gênero.")
    parser.add_argument("--genre", type=str, required=True, help="O gênero de filme.")
    args = parser.parse_args()
    main(args.genre)
