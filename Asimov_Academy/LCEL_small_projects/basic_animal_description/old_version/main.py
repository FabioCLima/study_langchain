'''
Entre point do projeto. Utiliza uma estrutura de dados Pydantic para validar
o nome de um animal e retorna uma descrição básica sobre ele
1- chain recebe o nome do animal, a chain intermediária extrai o nome do animal e
aciona o modelo LLM para gerar a descrição do animal.

'''
import os
from utils import llm, AnimalDescricao # Importamos apenas o que vamos usar
from langchain_core.runnables import RunnableLambda
from langchain_core.prompts import ChatPromptTemplate

#* Desabilita o tracing para manter o output limpo nos exercícios
os.environ["LANGCHAIN_TRACING_V2"] = "false"

#* --- 1. A Chain Principal: Gera a descrição de um animal ---
#* Esta é a nossa "unidade de trabalho". Ela sabe como pegar o nome de um animal
#* e transformá-lo em um objeto de descrição.
prompt_gerador_descricao = ChatPromptTemplate.from_template(
    """Você é um biólogo especialista. Forneça uma descrição curta e interessante sobre 
    o animal: {nome_animal}."""
)

chain_geradora_descricao = (
    prompt_gerador_descricao
    # CORREÇÃO: A saída deve ser AnimalDescricao, pois o prompt pede uma descrição.
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

    #* Passo 2: Executar a chain principal para obter o objeto de descrição.
    | chain_geradora_descricao

    #* Passo 3: Formatar o objeto de descrição para uma string legível.
    #* CORREÇÃO: O nome da função aqui deve ser o mesmo que o nome da função definida acima.
    | RunnableLambda(formatar_saida_amigavel)
)


#* --- 4. Teste da Pipeline ---
print("🚀 Executando a pipeline com saída formatada...")

#* A entrada é o que o usuário final forneceria.
resultado_formatado = pipeline_completa.invoke({"animal": "polvo"})

print("\n📌 Resultado Final (Formatado):")
print(resultado_formatado)