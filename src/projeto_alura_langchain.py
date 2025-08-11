"""
Projeto de langchain versão 3 - Alura (Refatorado e Concluído)

Este script demonstra um fluxo de trabalho multi-etapas com LangChain para criar
um roteiro de viagem personalizado. O processo é o seguinte:

1.  **Sugestão de Destino**: Com base no interesse do usuário (ex: "praias"),
    o sistema sugere uma cidade e o motivo.
2.  **Sugestões Adicionais (em paralelo)**: Uma vez que a cidade é definida,
    o sistema busca simultaneamente:
    a. Sugestões de restaurantes na cidade.
    b. Sugestões de passeios culturais.
3.  **Roteiro Final**: As informações são consolidadas em um único
    roteiro estruturado, pronto para ser exibido ao usuário.

Técnicas e Boas Práticas Demonstradas:
-   **LCEL (LangChain Expression Language)**: Uso do operador `|` para compor cadeias.
-   **Parsers de Saída**: `JsonOutputParser` para garantir saídas estruturadas com Pydantic
    e `StrOutputParser` para saídas de texto simples.
-   **Pydantic**: Definição de modelos de dados para validar e estruturar as saídas do LLM.
-   **RunnableParallel**: Execução de múltiplas cadeias em paralelo para otimizar o tempo de resposta.
-   **Separação de Responsabilidades**: Funções dedicadas para criar cada parte da cadeia
    e para exibir o resultado final.
-   **Código Pythonico**: Nomenclatura clara, tipagem e comentários explicativos.
"""

import os
from operator import itemgetter

from dotenv import find_dotenv, load_dotenv
from langchain_core.output_parsers import JsonOutputParser, StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import Runnable, RunnableParallel, RunnablePassthrough
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field

# --- Configurações e Constantes ---
# É uma boa prática definir constantes no início do script para fácil configuração.
API_KEY_ERROR_MSG = "OPENAI_API_KEY não encontrada no arquivo .env."
MODEL_NAME = "gpt-4-turbo"  # Usando um nome de modelo mais recente e capaz.
MODEL_TEMPERATURE = 0.5


# --- Carregamento da API e Instância do Modelo ---


def carregar_api_key() -> None:
    """Carrega a chave da API OpenAI do ambiente e verifica sua existência."""
    load_dotenv(find_dotenv())
    if not os.getenv("OPENAI_API_KEY"):
        raise ValueError(API_KEY_ERROR_MSG)


# Instanciar o modelo uma vez para ser reutilizado em todas as chains.
# Isso é mais eficiente do que criar uma nova instância em cada função.
carregar_api_key()
model = ChatOpenAI(model=MODEL_NAME, temperature=MODEL_TEMPERATURE)


# --- Definições dos Modelos de Dados (Pydantic) ---


class Destino(BaseModel):
    """
    Define a estrutura de dados para o destino de viagem sugerido.
    Utiliza Pydantic para garantir que a saída do modelo seja consistente.
    """

    cidade: str = Field(description="A cidade recomendada para visitar.")
    motivo: str = Field(
        description="Motivo pelo qual é interessante visitar essa cidade."
    )


class Restaurantes(BaseModel):
    """Estrutura para a lista de restaurantes sugeridos."""

    sugestoes: list[str] = Field(
        description="Uma lista com nomes de 3 a 5 restaurantes recomendados na cidade."
    )


# --- Funções para Criar as Cadeias (Chains) Modulares ---


def criar_chain_sugestao_destino() -> Runnable:
    """
    Cria e retorna uma chain do LangChain para sugerir destinos de viagem.
    Esta é a primeira etapa do nosso fluxo.
    """
    parser_destino = JsonOutputParser(pydantic_object=Destino)

    prompt_destino = ChatPromptTemplate.from_template(
        "Você é um especialista em viagens e turismo. "
        "Sugira uma cidade ideal para alguém com interesse em {interesse}. "
        "Forneça uma sugestão e uma breve justificativa do porquê.\n"
        # A instrução abaixo é crucial para o JsonOutputParser funcionar bem.
        "{format_instructions}",
        partial_variables={
            "format_instructions": parser_destino.get_format_instructions()
        },
    )
    # A chain une o prompt, o modelo e o parser em uma sequência executável.
    return prompt_destino | model | parser_destino


def criar_chain_sugestao_restaurantes() -> Runnable:
    """
    Cria uma chain que sugere restaurantes com base em uma cidade.
    Esta chain espera um dicionário com a chave "cidade" como entrada.
    """
    parser_restaurante = JsonOutputParser(pydantic_object=Restaurantes)

    prompt_restaurantes = ChatPromptTemplate.from_template(
        "Com base na cidade {cidade}, sugira uma lista de 3 a 5 restaurantes "
        "altamente qualificados pela sua culinária local ou única.\n"
        "{format_instructions}",
        partial_variables={
            "format_instructions": parser_restaurante.get_format_instructions()
        },
    )
    return prompt_restaurantes | model | parser_restaurante


def criar_chain_sugestao_passeios() -> Runnable:
    """
    Cria uma chain que sugere passeios culturais com base em uma cidade.
    Esta chain espera um dicionário com a chave "cidade" como entrada.
    """
    parser_cultural = StrOutputParser()

    prompt_cultural = ChatPromptTemplate.from_template(
        "Você é um guia turístico local. Sugira 3 atividades ou locais "
        "culturais imperdíveis no entorno da {cidade}. "
        "Seja criativo e forneça uma breve descrição para cada sugestão."
    )
    return prompt_cultural | model | parser_cultural


# --- Composição da Chain Principal e Execução ---


def exibir_roteiro(roteiro: dict) -> None:
    """
    Exibe o roteiro de viagem de forma formatada e amigável.
    Esta função lida apenas com a apresentação dos dados.
    """
    destino = roteiro.get("destino", {})
    restaurantes = roteiro.get("restaurantes", {}).get("sugestoes", [])
    passeios = roteiro.get("passeios", "Nenhuma sugestão de passeio encontrada.")

    print("\n" + "=" * 50)
    print("✈️ ROTEIRO DE VIAGEM PERSONALIZADO ✈️")
    print("=" * 50)

    if destino:
        print(f"\n📍 Destino Sugerido: {destino.get('cidade')}")
        print(f"🤔 Por quê? {destino.get('motivo')}")
    else:
        print("\n📍 Destino não pôde ser sugerido.")

    if restaurantes:
        print("\n🍽️ Sugestões de Restaurantes:")
        for r in restaurantes:
            print(f"  - {r}")
    else:
        print("\n🍽️ Nenhuma sugestão de restaurante encontrada.")

    if passeios:
        print("\n🏛️ Sugestões de Passeios Culturais:")
        print(passeios)

    print("\n" + "=" * 50)


def main() -> None:
    """
    Função principal que orquestra a criação e execução da chain completa.
    """
    # 1. Criação das chains individuais
    chain_destino = criar_chain_sugestao_destino()
    chain_restaurantes = criar_chain_sugestao_restaurantes()
    chain_passeios = criar_chain_sugestao_passeios()

    # 2. Composição da chain principal
    # O `RunnablePassthrough` é usado para passar a entrada original (`interesse`)
    # adiante no fluxo, caso seja necessário. Aqui, focamos em passar o resultado
    # da primeira chain para as chains paralelas.
    map_chain = RunnableParallel(
        destino=chain_destino,
        # Passa o dicionário de entrada original para a próxima etapa
        original_input=RunnablePassthrough(),
    )

    # A chain final combina tudo.
    # O fluxo é:
    # 1. `map_chain` é executado. Sua saída será:
    #    {'destino': {'cidade': '...', 'motivo': '...'}, 'original_input': {'interesse': '...'}}
    # 2. O resultado de `map_chain` é passado para o próximo `RunnableParallel`.
    # 3. As chains de restaurantes e passeios são executadas em paralelo.
    #    - Elas precisam da chave 'cidade', que extraímos de `destino` usando `itemgetter`.
    #    - `itemgetter('destino')` pega o dicionário de destino.
    #    - `itemgetter('cidade')` (dentro da sub-chain) pega o valor da cidade.
    # 4. O resultado final é um dicionário consolidado.
    roteiro_chain = map_chain | RunnableParallel(
        destino=itemgetter("destino"),
        restaurantes=itemgetter("destino") | chain_restaurantes,
        passeios=itemgetter("destino") | chain_passeios,
    )

    # 3. Execução do fluxo
    try:
        interesse_usuario = "praias paradisíacas no Brasil"
        print(f"Buscando roteiro de viagem para interesse em: '{interesse_usuario}'...")

        # O método 'invoke' executa a chain completa e retorna o dicionário final.
        roteiro_final = roteiro_chain.invoke({"interesse": interesse_usuario})

        # A função de exibição formata e imprime o resultado.
        exibir_roteiro(roteiro_final)

    except ValueError as e:
        print(f"❌ Erro de configuração: {e}")
    except Exception as e:
        print(f"🚨 Ocorreu um erro inesperado durante a execução: {e}")


# Bloco que garante que o código principal só será executado quando
# o script for rodado diretamente.
if __name__ == "__main__":
    main()