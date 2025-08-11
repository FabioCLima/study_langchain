"""Protótipo de estudo - Módulo 1
Fluxo com múltiplas chains e parsers específicos.
"""

# ! Bibliotecas
import os
from typing import Any

from dotenv import load_dotenv, find_dotenv
from langchain_core.runnables import RunnablePassthrough, RunnableParallel
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser, PydanticOutputParser, StrOutputParser
from pydantic import BaseModel, Field, SecretStr

# =============================================================================
# Funções Utilitárias
# =============================================================================
def load_environment_variables() -> str:
    """Carrega variáveis de ambiente e retorna a chave da API do OpenAI."""
    load_dotenv(find_dotenv())
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY não encontrada no arquivo .env")
    return api_key


def create_model(api_key: str) -> ChatOpenAI:
    """Cria e retorna um modelo de linguagem ChatOpenAI."""
    return ChatOpenAI(model="gpt-4.1", api_key=SecretStr(api_key))

# =============================================================================
# Estruturas de Dados
# =============================================================================
# Chain 1 - Destino
class Destino(BaseModel):
    cidade: str = Field(description="Nome da cidade recomendada.")
    motivo: str = Field(description="Motivo da recomendação da cidade.")

# Chain 2 - Lista de Restaurantes
class Restaurante(BaseModel):
    nome: str = Field(description="Nome do restaurante.")
    tipo: str = Field(description="Tipo de culinária do restaurante.")
    descricao: str  = Field(description="Descrição do restaurante.")

class ListaRestaurantes(BaseModel):
    restaurantes: list[Restaurante]

# Chain 3 - Atrações
class Atracao(BaseModel):
    nome: str
    descricao: str

class ListaAtracoes(BaseModel):
    atracoes: list[Atracao]

# =============================================================================
# Funções para cada Chain
# =============================================================================
#* -------- Chain 1: Destino --------
def create_parser_destino() -> JsonOutputParser:
    return JsonOutputParser(pydantic_object=Destino)

def create_prompt_destino(parser: JsonOutputParser) -> ChatPromptTemplate:
    return ChatPromptTemplate.from_template(
        """Sugira uma cidade com base no interesse do usuário: {interesse}.
        Explique o motivo da sugestão da cidade.
        {format_instructions}""",
        partial_variables={"format_instructions": parser.get_format_instructions()}
    )

def create_chain_destino(model: ChatOpenAI) -> Any:
    parser = create_parser_destino()
    prompt = create_prompt_destino(parser)
    return prompt | model | parser  # type: ignore


#* -------- Chain 2: Restaurantes --------
def create_parser_restaurantes() -> PydanticOutputParser[ListaRestaurantes]:
    return PydanticOutputParser(pydantic_object=ListaRestaurantes)

def create_prompt_restaurantes(
    parser: PydanticOutputParser[ListaRestaurantes]
    ) -> ChatPromptTemplate:

    return ChatPromptTemplate.from_template(
        """Você é um assistente especialista em gastronomia e trabalha para a agência de
        viagens.
        
        Para a cidade {cidade}, sugira:
        - 3 restaurantes de comida caseira de boa qualidade
        - 3 restaurantes mais sofisticados
        {format_instructions}""",
        partial_variables={"format_instructions": parser.get_format_instructions()}
    )

def create_chain_restaurantes(model: ChatOpenAI) -> Any:
    parser = create_parser_restaurantes()
    prompt = create_prompt_restaurantes(parser)
    return prompt | model | parser  # type: ignore


# -------- Chain 3: Passeios --------
def create_parser_passeios_culturais() -> StrOutputParser:
    return StrOutputParser()

def create_prompt_passeios_culturais(parser: StrOutputParser) -> ChatPromptTemplate:
    return ChatPromptTemplate.from_template(
        """Sugira 3 passeios culturais na cidade {cidade}.
        Inclua nome e descrição para cada passeio.
        
        Formato da resposta:
        - Nome do passeio 1: Descrição detalhada
        - Nome do passeio 2: Descrição detalhada  
        - Nome do passeio 3: Descrição detalhada"""
    )

def create_chain_passeios_culturais(model: ChatOpenAI) -> Any:
    parser = create_parser_passeios_culturais()
    prompt = create_prompt_passeios_culturais(parser)
    return prompt | model | parser  # type: ignore

# =============================================================================
# Função Principal
# =============================================================================
def main() -> None:
    api_key = load_environment_variables()
    model = create_model(api_key)

    # --- Chain 1: Destino ---
    chain_destino = create_chain_destino(model)
    interesse_usuario = "ecoturismo"
    destino = chain_destino.invoke({"interesse": interesse_usuario})
    cidade = destino["cidade"]
    motivo = destino["motivo"]

    print("\n=== Recomendação de Destino ===")
    print(f"Cidade: {cidade}")
    print(f"Motivo: {motivo}")
    print(f"type(destino): {type(destino)}")

    # --- Chain 2: Restaurantes ---
    chain_restaurantes = create_chain_restaurantes(model)
    restaurantes = chain_restaurantes.invoke({"cidade": cidade})

    print("\n=== Restaurantes Recomendados ===")
    for r in restaurantes.restaurantes:  # 
        print(f"- {r.nome} ({r.tipo}): {r.descricao}")
        
    print(f"type(restaurantes): {type(restaurantes)}")

    # --- Chain 3: Passeios Culturais ---
    chain_passeios_culturais = create_chain_passeios_culturais(model)
    passeios_culturais = chain_passeios_culturais.invoke({"cidade": cidade})

    print("\n=== Passeios Culturais ===")
    print(passeios_culturais)
    print(f"type(passeios_culturais): {type(passeios_culturais)}")
    
    #! Encadeamento de chains - Construção da Chain principal
    print("\n" + "="*50)
    print("=== ROTEIRO COMPLETO DE VIAGEM ===")
    print("=== Chain Encadeada do principio ao fim ===")
    print("="*50)
    
    #* Chain principal que orquestra todas as outras
    roteiro_viagem = (
        RunnablePassthrough.assign(
            destino_info = chain_destino
        )
        |
        RunnablePassthrough.assign(
            sugestoes = RunnableParallel(
                restaurantes = (
                    {"cidade": lambda x: x["destino_info"]["cidade"]}
                    | chain_restaurantes
                ),
                passeios_culturais = (
                {"cidade": lambda x: x["destino_info"]["cidade"]}
                | chain_passeios_culturais
                ),
              )
            )
        )
    
    resultado_completo = roteiro_viagem.invoke({"interesse": interesse_usuario})
    
    print("\n" + "="*50)
    print("=== Roteiro de Viagem Completo ===")
    print("="*50)
    
    print(f"Destino: {resultado_completo['destino_info']['cidade']}")   
    print(f"Motivo: {resultado_completo['destino_info']['motivo']}")
    
    print("\n=== Restaurantes Recomendados ===")
    for r in resultado_completo['sugestoes']['restaurantes'].restaurantes:
        print(f"- {r.nome} ({r.tipo}): {r.descricao}")
    
    print("\n=== Passeios Culturais ===")
    print(resultado_completo['sugestoes']['passeios_culturais'])
    
    print("\n" + "="*50)
    print("✨ Roteiro de viagem gerado com sucesso! ✨")
    print("="*50)   
# =============================================================================
# Execução
# =============================================================================
if __name__ == "__main__":
    main()

  