# core/chain_details.py

# pyright: reportGeneralTypeIssues=false, reportUnknownMemberType=false
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from core.models import MovieInfoData
from core.settings import settings
from typing import Any, Dict
from langchain_core.runnables import Runnable

def create_movie_details_chain() -> Runnable[Dict[str, Any], MovieInfoData]:
    """Cria uma chain que busca informações detalhadas de um único filme."""
    llm = ChatOpenAI(model=settings.model_name, temperature=settings.model_temperature)
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", "Você é um assistente de banco de dados de cinema..."),
        ("human", "Por favor, extraia as seguintes informações para o filme: '{movie_title}'."),
    ])
    structured_llm = llm.with_structured_output(MovieInfoData) #type: ignore
    details_chain = prompt_template | structured_llm #type: ignore
    return details_chain #type: ignore