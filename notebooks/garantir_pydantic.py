import json
import os
from typing import Any, Dict
from dotenv import load_dotenv, find_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser, PydanticOutputParser
from pydantic import BaseModel, Field

# Carregar variáveis de ambiente
load_dotenv(find_dotenv())
openai_api_key = os.getenv("OPENAI_API_KEY")

# Configurar o modelo
model = ChatOpenAI(
    model="gpt-4.1",
    temperature=0,
    api_key=openai_api_key  # type: ignore
)

# Definir a classe Pydantic
class Destino(BaseModel):
    cidade: str = Field(description="Nome da cidade recomendada para o tipo de interesse do usuário.")
    motivo: str = Field(description="Motivo da recomendação da cidade para o interesse específicado pelo usuário.")

# ============================================================================
# OPÇÃO 1: Usar PydanticOutputParser (RECOMENDADO)
# ============================================================================
print("🔧 OPÇÃO 1: Usando PydanticOutputParser")
print("=" * 50)

parser_pydantic = PydanticOutputParser(pydantic_object=Destino)

prompt_pydantic = ChatPromptTemplate.from_template(
    """Sugira uma cidade com base no interesse do usuário, {interesse}.
    Explique o motivo da sugestão da cidade.
    
    {format_instructions}""",
    partial_variables={"format_instructions": parser_pydantic.get_format_instructions()}
)

chain_pydantic = prompt_pydantic | model | parser_pydantic

try:
    response_pydantic = chain_pydantic.invoke({"interesse": "ecoturismo"})
    print(f"Tipo da resposta: {type(response_pydantic)}")
    print(f"É um objeto Pydantic? {isinstance(response_pydantic, Destino)}")
    print(f"Cidade: {response_pydantic.cidade}")
    print(f"Motivo: {response_pydantic.motivo}")
except Exception as e:
    print(f"Erro: {e}")

print("\n")

# ============================================================================
# OPÇÃO 2: Converter dicionário para Pydantic após JsonOutputParser
# ============================================================================
print("🔧 OPÇÃO 2: Convertendo dicionário para Pydantic")
print("=" * 50)

parser_json = JsonOutputParser(pydantic_object=Destino)

prompt_json = ChatPromptTemplate.from_template(
    """Sugira uma cidade com base no interesse do usuário, {interesse}.
    Explique o motivo da sugestão da cidade.
    
    {format_instructions}""",
    partial_variables={"format_instructions": parser_json.get_format_instructions()}
)

chain_json = prompt_json | model | parser_json

try:
    response_dict = chain_json.invoke({"interesse": "ecoturismo"})
    print(f"Tipo da resposta original: {type(response_dict)}")
    
    # Converter dicionário para objeto Pydantic
    if isinstance(response_dict, dict):
        response_pydantic_obj = Destino(**response_dict)
        print(f"Tipo após conversão: {type(response_pydantic_obj)}")
        print(f"É um objeto Pydantic? {isinstance(response_pydantic_obj, Destino)}")
        print(f"Cidade: {response_pydantic_obj.cidade}")
        print(f"Motivo: {response_pydantic_obj.motivo}")
    else:
        print("Já é um objeto Pydantic")
        
except Exception as e:
    print(f"Erro: {e}")

print("\n")

# ============================================================================
# OPÇÃO 3: Função helper para garantir Pydantic
# ============================================================================
print("🔧 OPÇÃO 3: Função helper para garantir Pydantic")
print("=" * 50)

def garantir_pydantic(response: Any, model_class: type) -> BaseModel:
    """
    Garante que a resposta seja um objeto Pydantic.
    
    Args:
        response: Resposta do LangChain (pode ser dict ou Pydantic)
        model_class: Classe Pydantic para converter
    
    Returns:
        Objeto Pydantic
    """
    if isinstance(response, model_class):
        return response
    elif isinstance(response, dict):
        return model_class(**response)
    else:
        raise ValueError(f"Tipo não suportado: {type(response)}")

try:
    response_dict_2 = chain_json.invoke({"interesse": "praias"})
    response_garantido = garantir_pydantic(response_dict_2, Destino)
    
    print(f"Tipo original: {type(response_dict_2)}")
    print(f"Tipo após garantir_pydantic: {type(response_garantido)}")
    print(f"Cidade: {response_garantido.cidade}")
    print(f"Motivo: {response_garantido.motivo}")
    
except Exception as e:
    print(f"Erro: {e}")

print("\n")

# ============================================================================
# OPÇÃO 4: Usar PydanticToolsOutputParser (para ferramentas)
# ============================================================================
print("🔧 OPÇÃO 4: Comparação de parsers")
print("=" * 50)

print("JsonOutputParser:")
print("- Pode retornar dict ou Pydantic (depende da versão)")
print("- Mais flexível")
print("- Menos previsível")

print("\nPydanticOutputParser:")
print("- Sempre retorna objeto Pydantic")
print("- Mais previsível")
print("- Melhor para validação de tipos")

print("\nRecomendação: Use PydanticOutputParser quando precisar garantir objetos Pydantic!")
