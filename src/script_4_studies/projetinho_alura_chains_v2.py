"""Projeto de langchain versão 2 - Alura (Refatorado)

Este script utiliza o LangChain para sugerir um destino de viagem
com base no interesse do usuário, retornando a resposta em um formato JSON estruturado.
"""

import os

from dotenv import find_dotenv, load_dotenv
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import Runnable
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field

# --- Configurações e Constantes ---
# É uma boa prática definir constantes no início do script para fácil configuração.
API_KEY_ERROR_MSG = "OPENAI_API_KEY não encontrada no arquivo .env."
MODEL_NAME = "gpt-4-turbo"  # Usando um nome de modelo válido.
MODEL_TEMPERATURE = 0.5


def carregar_api_key() -> None:
    """Carrega a chave da API OpenAI do ambiente e verifica sua existência."""
    load_dotenv(find_dotenv())
    if not os.getenv("OPENAI_API_KEY"):
        raise ValueError(API_KEY_ERROR_MSG)


class Destino(BaseModel):
    """Define a estrutura de dados para o destino de viagem sugerido.
    Utiliza Pydantic para garantir que a saída do modelo seja consistente.
    """

    cidade: str = Field(description="A cidade recomendada para visitar.")
    motivo: str = Field(
        description="Motivo pelo qual é interessante visitar essa cidade."
    )


def criar_chain_de_sugestao() -> Runnable:
    """Cria e retorna uma chain do LangChain para sugerir destinos de viagem.
    """
    # 1. Definição do Modelo LLM
    model = ChatOpenAI(model=MODEL_NAME, temperature=MODEL_TEMPERATURE)

    # 2. Definição do Parser de Saída
    # O parser garante que a resposta do LLM siga a estrutura da classe 'Destino'.
    parser = JsonOutputParser(pydantic_object=Destino)

    # 3. Definição do Prompt Template
    # O template instrui o modelo sobre sua função e o formato de saída esperado.
    prompt = ChatPromptTemplate.from_template(
        "Você é um especialista em viagens e turismo. "
        "Sugira uma cidade ideal para alguém com interesse em {interesse}. "
        "Forneça uma sugestão e uma breve justificativa do porquê.\n"
        # A instrução abaixo é crucial para o JsonOutputParser funcionar bem.
        "{format_instructions}",
        partial_variables={"format_instructions": parser.get_format_instructions()},
    )

    # 4. Criação da Chain com LCEL (LangChain Expression Language)
    # A chain une o prompt, o modelo e o parser em uma sequência executável.
    return prompt | model | parser


def exibir_sugestao(destino: Destino) -> None:
    """Exibe a sugestão de destino de forma formatada e amigável.
    Esta função lida apenas com a apresentação dos dados.
    """
    print("\n--- 💡 Sugestão de Viagem ---")
    print(f"📍 Cidade: {destino.cidade}")
    print(f"🤔 Motivo: {destino.motivo}")
    print("-----------------------------")


def main() -> None:
    """Função principal que executa o fluxo do programa.
    """
    try:
        carregar_api_key()

        chain_interesse = criar_chain_de_sugestao()
        interesse_usuario = "chapadas"

        print(
            f"Buscando sugestão de viagem para interesse em: '{interesse_usuario}'..."
        )

        # O método 'invoke' executa a chain e retorna um dicionário.
        response_dict = chain_interesse.invoke({"interesse": interesse_usuario})

        # A forma mais robusta e "Pythonica" é converter o dicionário para o nosso
        # modelo Pydantic. Isso garante validação e nos dá um objeto com atributos.
        destino_sugerido = Destino(**response_dict)

        # Agora, passamos o objeto estruturado para a função de exibição.
        exibir_sugestao(destino_sugerido)
    except ValueError as e:
        print(f"❌ Erro de configuração: {e}")
    except KeyError as e:
        print(f"🚨 Erro de chave ausente: {e}")
    except TypeError as e:
        print(f"🚨 Erro de tipo: {e}")


# Bloco que garante que o código principal só será executado quando
# o script for rodado diretamente.
if __name__ == "__main__":
    main()
