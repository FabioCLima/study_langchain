import json
import os
from typing import Any

from dotenv import find_dotenv, load_dotenv
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
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


# Configurar o parser
parser_destino = JsonOutputParser(pydantic_object=Destino)

# Configurar o prompt
prompt_destino = ChatPromptTemplate.from_template(
    """Sugira uma cidade com base no interesse do usuário, {interesse}.
    Explique o motivo da sugestão da cidade.\n{format_instructions}""",
    partial_variables={"format_instructions": parser_destino.get_format_instructions()}
)

# Criar a chain
chain_destino = prompt_destino | model | parser_destino  # type: ignore

# Executar a chain
response_destino = chain_destino.invoke({"interesse": "ecoturismo"})  # type: ignore

# Código corrigido para lidar com o problema do JsonOutputParser
# O problema é que response_destino está retornando um dicionário em vez de um objeto Pydantic

# 1. Inspecionando o tipo e acessando os atributos
print(f"O tipo da variável 'response' é: {type(response_destino)}")
print("-" * 40)

# Verifica se é um dicionário ou objeto Pydantic
if isinstance(response_destino, dict):
    print(f"Cidade Sugerida: {response_destino['cidade']}")
    print(f"Motivo da Sugestão: {response_destino['motivo']}")
else:
    # Se for um objeto Pydantic
    print(f"Cidade Sugerida: {response_destino.cidade}")
    print(f"Motivo da Sugestão: {response_destino.motivo}")

print("-" * 40)

# 2. Melhorando a visualização com .model_dump() e json.dumps()
print("\n✅ Saída formatada como JSON (ideal para logs e debug):")

# Converte para dicionário se necessário
if isinstance(response_destino, dict):
    response_dict: dict[str, Any] = response_destino
else:
    # Se for um objeto Pydantic, converte para dicionário
    response_dict = response_destino.model_dump()  # type: ignore

# Usa json.dumps para formatar o dicionário como uma string JSON "bonita"
json_output = json.dumps(
    response_dict,
    indent=2,          # Adiciona indentação para legibilidade
    ensure_ascii=False  # Garante que caracteres como "ç" e "ã" sejam exibidos corretamente
)

print(json_output)

# 3. Alternativa: Forçar a criação de um objeto Pydantic
print("\n🔧 Alternativa: Criando objeto Pydantic a partir do dicionário:")
if isinstance(response_destino, dict):
    # Cria um objeto Pydantic a partir do dicionário
    destino_obj = Destino(**response_destino)  # type: ignore
    print(f"Cidade Sugerida: {destino_obj.cidade}")
    print(f"Motivo da Sugestão: {destino_obj.motivo}")
else:
    print("Já é um objeto Pydantic")
