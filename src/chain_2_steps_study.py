from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from pydantic import BaseModel, Field
from dotenv import load_dotenv, find_dotenv


_ = load_dotenv(find_dotenv())

# ---- Definições (sem mudanças) ----
class Cidade(BaseModel):
    nome: str = Field(description="Nome da cidade")
    estado: str = Field(description="Estado da cidade")
    populacao: int = Field(description="População da cidade")
    clima: str = Field(description="Clima da cidade")

model_cidade = ChatOpenAI(model="gpt-4o-mini", temperature=0).with_structured_output(Cidade)
prompt_cidade = ChatPromptTemplate.from_messages([
    ("system", "Você é um assistente que fornece dados de cidades."),
    ("user", "Descreva a cidade {cidade} do Brasil.")
])
chain_cidade = prompt_cidade | model_cidade

model_clima = ChatOpenAI(model="gpt-4o-mini", temperature=0)
prompt_clima = ChatPromptTemplate.from_template(
    "Com base no clima '{clima}', qual tipo de roupa seria adequado para usar? Responda de forma curta e amigável."
)
chain_clima_part = prompt_clima | model_clima

# ---- A Chain Mestre Corrigida ----

# Primeiro, criamos a sub-cadeia para a recomendação.
# Ela espera um dicionário de entrada que já tenha a chave 'cidade_obj'.
sub_chain_recomendacao = (
    RunnableLambda(lambda x: {"clima": x["cidade_obj"].clima})
    | chain_clima_part
)

# Agora, construímos a cadeia principal de forma sequencial
final_chain = (
    # Passo 1: Executa a primeira chain e ADICIONA seu resultado (um objeto Cidade) 
    # ao fluxo de dados sob a chave 'cidade_obj'.
    # A saída deste passo é: {"cidade": "Petrópolis", "cidade_obj": <Objeto Cidade>}
    RunnablePassthrough.assign(cidade_obj=chain_cidade)
    
    # Passo 2: Executa a segunda chain e ADICIONA seu resultado (uma AIMessage)
    # ao fluxo sob a chave 'recomendacao'.
    # A entrada para este passo já contém 'cidade_obj', então a sub_chain_recomendacao funciona.
    # A saída deste passo é: {"cidade": ..., "cidade_obj": ..., "recomendacao": <AIMessage>}
    | RunnablePassthrough.assign(recomendacao=sub_chain_recomendacao)
    
    # Passo 3: Formata a resposta final usando as chaves que foram adicionadas ao fluxo.
    | RunnableLambda(lambda x: 
        f"--- Detalhes da Cidade ---\n"
        f"Nome: {x['cidade_obj'].nome}\n"
        f"Estado: {x['cidade_obj'].estado}\n"
        f"População: {x['cidade_obj'].populacao}\n"
        f"Clima: {x['cidade_obj'].clima}\n\n"
        f"--- Recomendação de Vestuário ---\n"
        f"{x['recomendacao'].content}\n"
    )
)


# ✅ Executando a chain final
resultado_final = final_chain.invoke({"cidade": "Petrópolis"})

print(resultado_final)