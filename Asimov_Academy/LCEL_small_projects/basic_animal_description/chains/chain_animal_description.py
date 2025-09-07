"""Cadeia de processamento para gerar uma descrição de um animal"""

from langchain_core.prompts import ChatPromptTemplate
from models.data_structure import AnimalDescricao
from configurations.config import llm 
from langchain_core.runnables import RunnableLambda

# * Criar a cadeia de processamento
# * 1. Chain geradora
#   -- Criar um prompt que usa a variável {nome_animal}
nome_animal_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """Você é um biólogo especializado em criar descrições de
         animais de forma educativa e envolvente.
         """,
        ),
        (
            "user",
            """Crie uma descrição detalhada sobre o seguinte animal:
         {nome_animal}.

A descrição deve ser bem estruturada, incluindo os seguintes tópicos:
- **Aparência Física:** (tamanho, peso, pelagem/plumagem, cores, etc.)
- **Habitat e Distribuição Geográfica:**
- **Dieta e Hábitos Alimentares:**
- **Comportamento e Socialização:**
- **Curiosidades:** (um ou dois fatos interessantes)""",
        ),
    ]
)

chain_geradora_descricao = (
    nome_animal_prompt
    | llm.with_structured_output(AnimalDescricao)
)

#* --- 2. O Formatador de Saída: Deixa o resultado bonito ---
#* Uma função simples que recebe o objeto Pydantic e retorna uma string amigável.
def formatar_saida_amigavel(animal_obj: AnimalDescricao) -> str:
    """Recebe um objeto AnimalDescricao e retorna uma string formatada."""
    return (
        f"--- 🐾 Informações sobre: {animal_obj.nome} ---\n"
        f"Descrição: {animal_obj.descricao}\n"
        f"-----------------------------------"
    )

#* --- 3. A Pipeline Completa: Conecta todos os passos ---	
#* Esta é a nossa esteira de produção. Ela define o fluxo do início ao fim.
pipeline_completa = (
    #* Passo 1: Adaptar a entrada do usuário.
    #* CORREÇÃO: A lambda deve receber o dict de entrada {"animal": "..."}
    #* e transformá-lo no dict que a chain_geradora_descricao espera: {"nome_animal": "..."}
    RunnableLambda(lambda entrada: {"nome_animal": entrada["animal"]})
    
    #* Passo 2. Executar a chain principal para obter a descrição do aninal
    | chain_geradora_descricao

    #* Passo 3. Formatar a saída para uma string amigável
    | RunnableLambda(formatar_saida_amigavel)
)
