# gerar_catalogo.py

import json
from core.logger import logger
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from core.models import CatalogoFilmes
from dotenv import load_dotenv

def main():
    """
    Função principal para gerar o catálogo de filmes e salvá-lo em JSON.
    """
    # 1. Carrega as variáveis de ambiente
    load_dotenv()

    # 2. Torna a escolha do gênero interativa
    genre = ""
    # Continua perguntando enquanto o usuário não digitar nada
    while not genre:
        genre = input("Digite o gênero de filme para o qual deseja gerar o catálogo: ")
        if not genre:
            logger.warning("O gênero não pode ser vazio. Por favor, tente novamente.")

    logger.info(f"Iniciando a geração do catálogo para o gênero: {genre}")

    # 3. Configura o parser Pydantic
    parser = PydanticOutputParser(pydantic_object=CatalogoFilmes)

    # 4. Cria o template do prompt
    prompt_template = ChatPromptTemplate.from_messages(
        [
            ("system", "Você é um assistente especialista em cinema, fluente em português do Brasil."),
            ("human", 
             "Crie um catálogo com 30 filmes excelentes do gênero de {genero}. "
             "Para cada filme, forneça um título e uma sinopse concisa e informativa. "
             "Siga estritamente o formato de saída solicitado.\n"
             "{format_instructions}"
            ),
        ]
    )

    # 5. Configura o modelo LLM
    model = ChatOpenAI(model="gpt-4o", temperature=0.7)

    # 6. Monta a chain de execução
    chain = prompt_template | model | parser

    # 7. Invoca a chain e obtém o resultado
    logger.info("Invocando a chain com o LLM. Isso pode levar um momento...")
    try:
        resultado = chain.invoke({"genero": genre, "format_instructions": parser.get_format_instructions()})
    except Exception as e:
        logger.error(f"Ocorreu um erro ao invocar a chain: {e}")
        return

    # 8. Salva o resultado em um arquivo JSON
    output_path = "data/movie_catalog.json"
    logger.info(f"Salvando o catálogo em {output_path}...")
    
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(resultado.model_dump(), f, ensure_ascii=False, indent=2)
        
        logger.info(f"Catálogo salvo com sucesso em {output_path}!")
    except Exception as e:
        logger.error(f"Ocorreu um erro ao salvar o arquivo JSON: {e}")
        return

    # Exibindo uma amostra do resultado
    logger.info("--- Amostra do Catálogo Gerado ---")
    
    amostra = resultado.filmes[:2]
    
    for i, filme in enumerate(amostra, 1):
        logger.info(f"Filme {i}:")
        logger.info(f"  Título: {filme.title}")
        logger.info(f"  Sinopse: {filme.synopsis}")


if __name__ == "__main__":
    main()