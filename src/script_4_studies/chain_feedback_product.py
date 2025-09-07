# Jupyter Notebook: Cadeia de Análise de Feedback de Produto com LangChain

# ## 1. Configuração Inicial

import os

from dotenv import find_dotenv, load_dotenv
from langchain_openai import ChatOpenAI

_ = load_dotenv(find_dotenv())
if not os.getenv("OPENAI_API_KEY"):
    raise ValueError("OPENAI_API_KEY não encontrada no .env")

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.0)

# ## 2. Logging e Parser

import time

from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import (
    RunnableLambda,
    RunnableParallel,
    RunnablePassthrough,
)

debug_logs = []


def log_event(data):
    debug_logs.append({"timestamp": time.time(), "message": data})


log_chain = RunnableLambda(log_event) | RunnablePassthrough()
parser = StrOutputParser()

# ## 3. Prompts e Cadeias Individuais

from langchain_core.prompts import PromptTemplate

# Etapa 1: Extrair o problema principal do feedback
feedback_prompt = PromptTemplate.from_template(
    """
    Você é um analista de produto. A partir do seguinte feedback do usuário,
    extraia o principal problema relatado:

    Feedback: {feedback}

    Resuma em uma frase clara o problema principal.
    """
)
feedback_chain = feedback_prompt | llm | RunnableParallel(output=parser, log=log_chain)

# Etapa 2: Gerar uma sugestão de melhoria
suggestion_prompt = PromptTemplate.from_template(
    """
    Considere o seguinte problema de produto:
    Problema: {problem}

    Sugira uma melhoria concreta e objetiva para a equipe de produto.
    """
)
suggestion_chain = suggestion_prompt | llm | RunnableParallel(output=parser, log=log_chain)

# ## 4. Estruturação com Pydantic

from pydantic import BaseModel, Field


class FeedbackReport(BaseModel):
    problem_summary: str = Field(description="Resumo do problema identificado")
    severity: str = Field(description="Gravidade estimada do problema (baixa, média, alta)")
    category: str = Field(description="Categoria geral do problema")
    suggested_fix: str = Field(description="Solução sugerida para o problema")


report_prompt = PromptTemplate.from_template(
    """
    Com base no problema e na sugestão a seguir, estruture um relatório com os seguintes campos:
    - Resumo do problema
    - Categoria (ex: usabilidade, desempenho, bug, funcionalidade, etc)
    - Gravidade (baixa, média ou alta)
    - Sugestão de solução

    Problema: {problem}
    Sugestão: {suggestion}

    Retorne o resultado em formato JSON estruturado.
    """
)

report_chain = report_prompt | llm.with_structured_output(schema=FeedbackReport)

# ## 5. Composição da Cadeia Final

from operator import itemgetter

full_chain = (
    feedback_chain
    | RunnableParallel(problem=itemgetter("output"))
    | (
        RunnableParallel(
            suggestion=suggestion_chain,
            problem=itemgetter("problem")
        )
    )
    | RunnableParallel(
        problem=itemgetter("problem"),
        suggestion=itemgetter("suggestion")
    )
    | report_chain
)

# ## 6. Execução da Cadeia com um Exemplo

if __name__ == "__main__":
    example_feedback = {
        "feedback": "O aplicativo trava sempre que tento adicionar um novo cartão de crédito. Isso acontece toda vez que clico no botão de salvar."
    }

    report = full_chain.invoke(example_feedback)

    print("\n📋 Relatório Gerado:")
    print("Resumo:", report.problem_summary)
    print("Categoria:", report.category)
    print("Gravidade:", report.severity)
    print("Sugestão:", report.suggested_fix)

    print("\n📚 Total de Logs Registrados:", len(debug_logs))
