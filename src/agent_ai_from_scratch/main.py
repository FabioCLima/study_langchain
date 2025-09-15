from dotenv import load_dotenv
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from pydantic import BaseModel
from tools import save_tool, search_tool, wiki_tool

# ---------------------------------------------------------------------------- #
# Carrega variáveis de ambiente (ex.: OPENAI_API_KEY)
# ---------------------------------------------------------------------------- #
load_dotenv()


# ---------------------------------------------------------------------------- #
# Definição do schema de saída (Pydantic)
# ---------------------------------------------------------------------------- #
class ResearchResponse(BaseModel):
    """Estrutura da resposta esperada do agente de pesquisa."""

    topic: str
    summary: str
    sources: list[str]
    tools_used: list[str]


# ---------------------------------------------------------------------------- #
# Configuração do LLM (OpenAI)
# ---------------------------------------------------------------------------- #
# - gpt-4o-mini: mais barato e rápido que GPT-4.1, ideal para prototipagem
# - pode trocar para "gpt-4o" se quiser maior qualidade em tarefas complexas
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# Vincula diretamente o schema Pydantic ao LLM
# Isso garante que o retorno já será uma instância de ResearchResponse
llm_with_structured_output = llm.with_structured_output(ResearchResponse)


# ---------------------------------------------------------------------------- #
# Prompt do agente
# ---------------------------------------------------------------------------- #
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            You are a research assistant that will help generate a research paper.
            Use the available tools when needed.
            Return the final result strictly following the structured schema.
            """,
        ),
        ("placeholder", "{chat_history}"),
        ("human", "{query}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
)


# ---------------------------------------------------------------------------- #
# Ferramentas disponíveis para o agente
# ---------------------------------------------------------------------------- #
tools = [search_tool, wiki_tool, save_tool]


# ---------------------------------------------------------------------------- #
# Criação do agente e executor
# ---------------------------------------------------------------------------- #
agent = create_openai_functions_agent(
    llm=llm_with_structured_output,  # já garante saída no formato ResearchResponse
    tools=tools,
    prompt=prompt,
)

agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    handle_parsing_errors=True,  # robustez extra caso modelo quebre o schema
)


# ---------------------------------------------------------------------------- #
# Execução do fluxo principal
# ---------------------------------------------------------------------------- #
def main() -> None:
    """Executa o agente de pesquisa interativo no terminal."""
    query: str = input("🔎 What can I help you research? ")

    # O AgentExecutor retorna {"output": ResearchResponse(...)}
    result = agent_executor.invoke({"query": query})

    structured_response: ResearchResponse = result["output"]

    print("\n📌 Research Result:")
    print(f"Topic: {structured_response.topic}")
    print(f"Summary: {structured_response.summary}")
    print(f"Sources: {', '.join(structured_response.sources)}")
    print(f"Tools Used: {', '.join(structured_response.tools_used)}")


if __name__ == "__main__":
    main()
