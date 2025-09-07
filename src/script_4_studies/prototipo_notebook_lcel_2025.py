# File: src/prototipo_notebook_lcel_2025.py
# Este script é projetado para ser executado célula por célula em um Jupyter Notebook.

# --- [CÉLULA 1] ---
# Imports e Configuração do Ambiente
# Adicionamos asyncio para operações assíncronas e IPython para display no notebook.
import asyncio
import os
from operator import itemgetter

from dotenv import find_dotenv, load_dotenv
from IPython.display import Markdown, clear_output, display
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import Runnable, RunnablePassthrough
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field

print("✅ Célula 1: Imports e configuração concluídos.")

# --- [CÉLULA 2] ---
# Carregamento da API e Instância do Modelo
# A estrutura é mantida, pois é uma boa prática.
API_KEY_ERROR_MSG = "OPENAI_API_KEY não encontrada no arquivo .env."
MODEL_NAME = "gpt-4-turbo"
MODEL_TEMPERATURE = 0.5


def carregar_api_key() -> None:
    """Carrega a chave da API OpenAI do ambiente e verifica sua existência."""
    load_dotenv(find_dotenv())
    if not os.getenv("OPENAI_API_KEY"):
        raise ValueError(API_KEY_ERROR_MSG)
    # Dica para 2025: Ative o LangSmith para observabilidade!
    # os.environ["LANGCHAIN_TRACING_V2"] = "true"
    # os.environ["LANGCHAIN_API_KEY"] = "sua_chave_langsmith"


carregar_api_key()
model = ChatOpenAI(model=MODEL_NAME, temperature=MODEL_TEMPERATURE)

print("✅ Célula 2: Modelo LLM instanciado.")


# --- [CÉLULA 3] ---
# Definições dos Modelos de Dados (Pydantic)
# Nenhuma mudança aqui, Pydantic continua sendo o padrão ouro para estruturação de dados.
class Destino(BaseModel):
    cidade: str = Field(description="A cidade recomendada para visitar.")
    motivo: str = Field(description="Motivo pelo qual é interessante visitar essa cidade.")


class Restaurantes(BaseModel):
    sugestoes: list[str] = Field(description="Uma lista com nomes de 3 a 5 restaurantes recomendados.")


# Adicionamos uma nova chain para a previsão do tempo, como sugerido no plano de estudos.
class PrevisaoTempo(BaseModel):
    previsao: str = Field(description="Uma breve previsão do tempo para a cidade, incluindo temperatura média e condições.")


print("✅ Célula 3: Modelos Pydantic definidos.")

# --- [CÉLULA 4] ---
# Funções para Criar as Cadeias (Chains) Modulares
# A modularidade é excelente e deve ser mantida.
# Adicionamos a chain de previsão do tempo e a de resumo.


def criar_chain_sugestao_destino() -> Runnable:
    prompt_destino = ChatPromptTemplate.from_template(
        "Você é um especialista em viagens. Sugira uma cidade para alguém com interesse em {interesse}. "
        "Forneça a cidade e um motivo."
    )
    # Usando .with_structured_output, a forma mais moderna e robusta.
    return prompt_destino | model.with_structured_output(Destino)


def criar_chain_sugestao_restaurantes() -> Runnable:
    prompt_restaurantes = ChatPromptTemplate.from_template(
        "Com base na cidade {cidade}, sugira 3 restaurantes locais."
    )
    return prompt_restaurantes | model.with_structured_output(Restaurantes)


def criar_chain_sugestao_passeios() -> Runnable:
    prompt_cultural = ChatPromptTemplate.from_template(
        "Sugira 3 passeios culturais na cidade de {cidade}."
    )
    return prompt_cultural | model | StrOutputParser()


def criar_chain_previsao_tempo() -> Runnable:
    prompt_tempo = ChatPromptTemplate.from_template(
        "Forneça uma previsão do tempo para a próxima semana em {cidade}."
    )
    return prompt_tempo | model.with_structured_output(PrevisaoTempo)


def criar_chain_resumo_final() -> Runnable:
    """Uma nova chain que cria um resumo final em Markdown, pronta para streaming."""
    prompt_resumo = ChatPromptTemplate.from_template(
        "Você é um assistente de viagens. Com base nas informações a seguir, crie um roteiro de viagem "
        "atraente e bem formatado em Markdown.\n\n"
        "**Destino:** {destino.cidade}\n"
        "**Motivo:** {destino.motivo}\n\n"
        "**Previsão do Tempo:**\n{previsao.previsao}\n\n"
        "**Sugestões de Restaurantes:**\n{restaurantes.sugestoes}\n\n"
        "**Sugestões de Passeios:**\n{passeios}\n\n"
        "**Interesse Original do Usuário:** {interesse}"
    )
    return prompt_resumo | model | StrOutputParser()


print("✅ Célula 4: Funções de criação de chains prontas.")

# --- [CÉLULA 5] ---
# Composição da Chain Principal com `RunnablePassthrough.assign`
# Esta é a forma mais moderna e legível de compor chains que enriquecem o contexto.

roteiro_chain_completa = RunnablePassthrough.assign(
    # A primeira etapa usa o input original {"interesse": "..."} e adiciona a chave "destino"
    destino=criar_chain_sugestao_destino()
).assign(
    # As próximas etapas usam o contexto já existente (que agora contém "destino")
    # para popular novas chaves em paralelo.
    restaurantes=itemgetter("destino") | criar_chain_sugestao_restaurantes(),
    passeios=itemgetter("destino") | criar_chain_sugestao_passeios(),
    previsao=itemgetter("destino") | criar_chain_previsao_tempo(),
    # Mantemos o interesse original para o resumo final
    interesse=itemgetter("interesse")
) | criar_chain_resumo_final()

print("✅ Célula 5: Chain principal composta com `assign`.")

# --- [CÉLULA 6] ---
# Execução Assíncrona e com Streaming
# Em um notebook, `await` pode ser usado diretamente em células (top-level await).
# O streaming com `astream` oferece uma experiência de usuário muito superior.


async def gerar_roteiro_streaming(interesse_usuario: str):
    """Executa a chain de forma assíncrona e faz o stream do resultado em Markdown."""
    display(Markdown("### ✈️ Gerando seu roteiro de viagem..."))

    full_response = ""
    # O `async for` itera sobre os tokens à medida que chegam.
    async for chunk in roteiro_chain_completa.astream({"interesse": interesse_usuario}):
        full_response += chunk
        clear_output(wait=True)
        display(Markdown(full_response))

    return full_response


print("✅ Célula 6: Função de execução assíncrona pronta. Execute a célula abaixo para começar!")

# --- [CÉLULA 7] ---
# Invocando o Roteiro
# Esta seria a célula que o usuário executa para obter o resultado.


async def run():
    try:
        # Em um notebook, você pode simplesmente usar `await` na célula:
        # await gerar_roteiro_streaming("comida de rua na Ásia")
        await gerar_roteiro_streaming("vinícolas e montanhas")
    except ValueError as e:
        print(f"❌ Erro de configuração: {e}")
    except Exception as e:
        print(f"🚨 Ocorreu um erro inesperado durante a execução: {e}")


if __name__ == "__main__":
    # Para rodar como um script python
    asyncio.run(run())
