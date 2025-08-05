'''Multi-step workflow com LangChain - Melhorado'''
"""
Módulo de workflow multi-etapas com LangChain:
Gera uma ideia de negócio, analisa e retorna um relatório estruturado.
Autor: Fabio Lima
"""

from dotenv import load_dotenv, find_dotenv
import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser, PydanticOutputParser
from langchain_core.runnables import (
    RunnableLambda,
    RunnableParallel,
    RunnablePassthrough
)
from pydantic import BaseModel, Field

# ----------------------------------------
# Configurações e carregamento da API
# ----------------------------------------

_ = load_dotenv(find_dotenv())
if not os.getenv("OPENAI_API_KEY"):
    raise ValueError("OPENAI_API_KEY não encontrada no .env")

model = ChatOpenAI(model="gpt-4.1", temperature=0.1)

# ----------------------------------------
# Setup de logging
# ----------------------------------------

logs = []

def log_input(x):
    """Salva a entrada da etapa atual"""
    logs.append({"input": x})
    return x

def log_output(x):
    """Salva a saída da etapa atual"""
    logs[-1]["output"] = x
    return x

log_input_chain = RunnableLambda(log_input)
log_output_chain = RunnableLambda(log_output)

# ----------------------------------------
# ETAPA 1: Gerar ideia de negócio
# ----------------------------------------

ideia_prompt = PromptTemplate(
    input_variables=["industria"],
    template="""
    Você é um consultor de negócios especializado em tecnologia (software).
    Crie uma ideia de software inovadora para a indústria de {industria}.
    A ideia deve estar no ramo de engenharia de reservatórios,
    com foco em recuperação de petróleo em águas profundas no contexto brasileiro.
    Seja objetivo, técnico e criativo.
    """
)

idea_chain = (
    ideia_prompt
    | log_input_chain
    | model
    | StrOutputParser()
    | log_output_chain
)

# ----------------------------------------
# ETAPA 2: Análise da ideia
# ----------------------------------------

analise_prompt = PromptTemplate(
    input_variables=["ideia_negocio"],
    template="""
    Analise a seguinte ideia de negócio:
    Ideia: {ideia_negocio}

    Elabore uma análise com:
    - Investimento necessário (estimado)
    - 3 riscos e 3 soluções (relacionadas)
    - 3 oportunidades de mercado
    - Um resumo executivo da proposta

    Seja claro, direto e objetivo.
    """
)

analysis_chain = (
    analise_prompt
    | log_input_chain
    | model
    | StrOutputParser()
    | log_output_chain
)

# ----------------------------------------
# ETAPA 3: Gerar relatório estruturado
# ----------------------------------------

class AnaliseNegocio(BaseModel):
    """Modelo Pydantic com campos estruturados"""
    oportunidades: list[str]
    riscos: list[str]
    solucoes: list[str]
    resumo_proposta: str

report_prompt = PromptTemplate(
    input_variables=["analise_texto"],
    template="""
    A partir do texto a seguir, extraia os seguintes campos em formato JSON:
    - oportunidades: lista de 3 itens
    - riscos: lista de 3 itens
    - solucoes: lista de 3 itens, cada uma referente a um risco
    - resumo_proposta: resumo executivo da ideia

    Texto:
    {analise_texto}
    """
)

report_chain = (
    report_prompt
    | log_input_chain
    | model
    | PydanticOutputParser(pydantic_object=AnaliseNegocio)
    | log_output_chain
)

# ----------------------------------------
# EXECUÇÃO ETAPA A ETAPA (RECOMENDADO)
# ----------------------------------------

if __name__ == "__main__":
    print("🧪 Executando o fluxo multi-step de forma didática...")

    # Etapa 1: Gera a ideia
    ideia_resultado = idea_chain.invoke({"industria": "Petróleo"})
    print("\n🧠 Ideia gerada:")
    print(ideia_resultado)

    # Etapa 2: Análise da ideia
    analise_resultado = analysis_chain.invoke({"ideia_negocio": ideia_resultado})
    print("\n📊 Análise da ideia:")
    print(analise_resultado)

    # Etapa 3: Relatório estruturado
    relatorio_final = report_chain.invoke({"analise_texto": analise_resultado})
    print("\n📄 Relatório estruturado:")
    print(relatorio_final)

    # Logs
    print("\n📚 Histórico (logs):")
    for i, etapa in enumerate(logs):
        print(f"\n🔸 Etapa {i+1}")
        print("Input:", etapa["input"])
        print("Output:", etapa["output"])

    # ----------------------------------------
    # BONUS: Executar tudo com e2e_chain
    # ----------------------------------------

    print("\n🚀 Executando e2e_chain (encadeado):")

    e2e_chain = (
        RunnablePassthrough()
        | idea_chain
        | RunnableParallel(ideia_negocio=RunnablePassthrough())
        | analysis_chain
        | RunnableParallel(analise_texto=RunnablePassthrough())
        | report_chain
    )

    resultado_e2e = e2e_chain.invoke({"industria": "Petróleo"})

    print("\n📦 Resultado direto da e2e_chain:")
    print(resultado_e2e)

    # Acessar campos individuais (se quiser)
    print("\n✅ Oportunidades:")
    print(resultado_e2e.oportunidades)
    print("\n⚠️ Riscos:")
    print(resultado_e2e.riscos)
    print("\n💡 Soluções:")
    print(resultado_e2e.solucoes)
    print("\n📝 Resumo:")
    print(resultado_e2e.resumo_proposta)
