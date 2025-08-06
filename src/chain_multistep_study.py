# Jupyter Notebook: Estudo de Workflow Multi-Etapas com LangChain (LCEL)

# ## 1. Configuração do ambiente e modelo

import os
from dotenv import load_dotenv, find_dotenv
from langchain_openai import ChatOpenAI

_ = load_dotenv(find_dotenv())
if not os.getenv("OPENAI_API_KEY"):
    raise ValueError("OPENAI_API_KEY não encontrada no .env")

# Instanciação do modelo com temperatura baixa (para respostas determinísticas)
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.0)

# ## 2. Ferramentas auxiliares: Parser, Logging e Utilitários

from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel, RunnableLambda, RunnablePassthrough
from operator import itemgetter
import time

# Parser padrão para extrair texto puro
txt_parser = StrOutputParser()

# Logging com metadados
debug_logs = []

def log_with_timestamp(data):
    debug_logs.append({"timestamp": time.time(), "message": data})

log_chain = RunnableLambda(log_with_timestamp) | RunnablePassthrough()

# ## 3. Definição dos Prompts e Cadeias Modulares

from langchain_core.prompts import PromptTemplate

# Prompt para gerar ideia de negócio
idea_prompt = PromptTemplate.from_template(
    """
    You are a creative business advisor.
    Generate one innovative business idea in the industry: {industry}.
    Provide a brief description.
    """
)
idea_chain = idea_prompt | llm | RunnableParallel(output=txt_parser, log=log_chain)

# Prompt para analisar a ideia
temp_analysis_prompt = PromptTemplate.from_template(
    """
    Analyze the following business idea:
    Idea: {idea}
    Identify 3 strengths and 3 weaknesses.
    """
)
analysis_chain = temp_analysis_prompt | llm | RunnableParallel(output=txt_parser, log=log_chain)

# ## 4. Saída Estruturada com Pydantic

from pydantic import BaseModel, Field

class AnalysisReport(BaseModel):
    strengths: list[str] = Field(description="List of strengths")
    weaknesses: list[str] = Field(description="List of weaknesses")

report_prompt = PromptTemplate.from_template(
    """
    Based on the analysis below, return a structured JSON report:
    {analysis_text}
    """
)

report_chain = report_prompt | llm.with_structured_output(schema=AnalysisReport)

# ## 5. Cadeia de ponta a ponta (multi-etapas)

e2e_chain = (
    idea_chain
    | RunnableParallel(idea=itemgetter("output"))
    | analysis_chain
    | RunnableParallel(analysis_text=itemgetter("output"))
    | report_chain
)

# ## 6. Execução do fluxo completo

if __name__ == "__main__":
    industry_input = {"industry": "educação personalizada com IA"}
    result = e2e_chain.invoke(industry_input)

    print("\nRelatório Final Estruturado:")
    print("✅ Pontos Fortes:", result.strengths)
    print("⚠️ Pontos Fracos:", result.weaknesses)

    print("\n📚 Logs Registrados:", len(debug_logs))
