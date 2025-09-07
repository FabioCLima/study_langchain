"""Multi-step workflow com LangChain"""

import os

from dotenv import find_dotenv, load_dotenv
from langchain_core.output_parsers import StrOutputParser  # type: ignore
from langchain_core.prompts import PromptTemplate  # type: ignore
from langchain_core.runnables import (  # type: ignore
    RunnableLambda,
    RunnableParallel,
)
from langchain_openai import ChatOpenAI

# Carrega as variáveis de ambiente
_ = load_dotenv(find_dotenv())

# Verifica se a API key está configurada
if not os.getenv("OPENAI_API_KEY"):
    raise ValueError("OPENAI_API_KEY não encontrada no arquivo .env")

# Configura o modelo
model = ChatOpenAI(model="gpt-4.1", temperature=0.1)  # type: ignore

# ! Multi-step workflow
# ! Gerar um ideia de negócio para uma indústria
# ! Para cada chain, devemos parsear o output e salvar o log


# ! Chain 1: Gerar uma ideia de negócio
logs = []

parser = StrOutputParser()

parser_and_log_output_chain = RunnableParallel(
    output=parser,
    log=RunnableLambda(lambda x: logs.append(x))  # type: ignore
)

template = """
Você é um consultor de negócios especializado em tecnologia (software).
Crie uma ideia de software inovadora para a indústria de {industria}.
A sua ideia de negócio tem que estar no ramo de engenharia de reservatórios.
A ideia deve ser clara e objetiva com foco em recuperação de petróleo,
no contexto da realidade brasileira, ou seja, águas profundas.
"""

ideia_prompt = PromptTemplate(
    input_variables=["industria"],
    template=template.strip()
)
ideia_chain = (
    ideia_prompt
    | model
    | parser_and_log_output_chain
)  # type: ignore

ideia_response = ideia_chain.invoke({"industria": "Petróleo"})  # type: ignore

print(ideia_response["output"])
print("\n")
print(logs)  # type: ignore

# ! Análise da Ideia

template = """
Analise a seguinte ideia de negócio:
Ideia: {ideia_negocio} 
Faça uma análise criteriosa, com respeito a investimento, risco e viabilidade financeira.
Identifique 3 riscos potenciais e 3 possíveis oportunidades. Para cada risco identificado, sugira uma possível solução. Importante entender identificar se as possíveis soluções, podem virar insights para problemas da mesma natureza.
"""

analise_prompt = PromptTemplate(
    input_variables=["ideia_negocio"],
    template=template.strip()
)

analise_chain = (
    analise_prompt
    | model
    | parser_and_log_output_chain
)  # type: ignore

analise_response = analise_chain.invoke({"ideia_negocio": ideia_response["output"]})  # type: ignore

print(analise_response["output"])
print("\n")
print(logs)  # type: ignore


# ! Geração de relatório formatado
template = """
Aqui está uma análise da ideia do negócio:
Oportunidades e Riscos: {oportunidades_e_riscos}
Gere um relatório de negócios estruturado:
"""


class AnaliseNegocio(BaseModel):
    """Oportunidades e Riscos da ideia de negócio"""

    oportunidades: list[str] = Field(description="Oportunidades de negócio")
    riscos: list[str] = Field(description="Riscos de negócio")
    solucoes: list[str] = Field(description="Possíveis soluções para os riscos")


analise_prompt = PromptTemplate(
    input_variables=["oportunidades_e_riscos"],
    template=template.strip()
)

relatorio_chain = (
    analise_prompt
    | model
    | parser_and_log_output_chain
)  # type: ignore

relatorio_response = relatorio_chain.invoke({"oportunidades_e_riscos": analise_response["output"]})  # type: ignore

print(relatorio_response["output"])
print("\n")
print(logs)  # type: ignore
