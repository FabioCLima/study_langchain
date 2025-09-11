# agentstate_langgraph_linear_flow/question_assistant.py

# ! =============================================================================
# ! 1. IMPORTS
# ! =============================================================================
import logging
import sys
from typing import TypedDict

from dotenv import load_dotenv
from langchain_core.exceptions import LangChainError
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import END, StateGraph
from langgraph.graph.graph import CompiledGraph

# ! =============================================================================
# ! 2. CONFIGURAÇÃO DE LOGGING
# ! =============================================================================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("question_assistant.log"),
    ],
)
logger = logging.getLogger(__name__)

# ! =============================================================================
# ! 3. CONSTANTES
# ! =============================================================================
REFORMULATE_NODE = "reformulate"
ANSWER_NODE = "answer"
DEFAULT_MODEL = "gpt-4o-mini"
DEFAULT_TEMPERATURE = 0.0
REFORMULATE_SYSTEM_PROMPT = (
    "Sua tarefa é reformular a pergunta do usuário para que ela seja mais "
    "clara e direta. Retorne apenas a pergunta reformulada."
)
ANSWER_SYSTEM_PROMPT = (
    "Você é um tutor expert em Python. Responda de forma clara, didática "
    "e com exemplos de código."
)
ERROR_LLM_CONFIG = "Falha na configuração do LLM."
ERROR_EMPTY_QUESTION = "A pergunta original não pode estar vazia."
ERROR_EMPTY_CLARIFIED_QUESTION = "A pergunta clarificada não pode estar vazia."
ERROR_INVALID_LLM_TYPE = "O argumento 'llm' deve ser uma instância de ChatOpenAI."
ERROR_USER_QUESTION_EMPTY = "A pergunta do usuário não pode estar vazia."
ERROR_LLM_RESPONSE_NOT_STRING = "A resposta do LLM não é uma string válida."


# ! =============================================================================
# ! 4. CONFIGURAÇÃO
# ! =============================================================================
def setup_llm(
    model: str = DEFAULT_MODEL,
    temperature: float = DEFAULT_TEMPERATURE,
) -> ChatOpenAI:
    """Carrega as variáveis de ambiente e configura o modelo LLM.

    Args:
        model (str): Nome do modelo a ser usado.
        temperature (float): Temperatura para controle de criatividade.

    Returns:
        ChatOpenAI: Uma instância configurada do modelo.

    Raises:
        ValueError: Se as credenciais não estiverem configuradas ou houver
            um erro durante a inicialização do LLM.

    """  # ! CORREÇÃO: Docstring completa
    try:
        load_dotenv()
        llm = ChatOpenAI(model=model, temperature=temperature)
    except LangChainError as e:
        logger.exception("Erro ao configurar LLM")
        raise ValueError(ERROR_LLM_CONFIG) from e
    else:
        logger.info("LLM configurado com sucesso: %s", model)
        return llm


# ! =============================================================================
# ! 5. DEFINIÇÃO DO ESTADO
# ! =============================================================================
class AgentState(TypedDict):
    """Estado compartilhado para o Assistente de Perguntas."""

    original_question: str
    question_clarified: str
    answer: str


# ! =============================================================================
# ! 6. DEFINIÇÃO DOS NÓS (LÓGICA DO AGENTE)
# ! =============================================================================
def reformulate_node(state: AgentState, llm: ChatOpenAI) -> dict[str, str]:
    """Nó para reformular e clarificar a pergunta do usuário.

    Args:
        state (AgentState): O estado compartilhado do workflow.
        llm (ChatOpenAI): O modelo de linguagem configurado.

    Returns:
        dict[str, str]: Um dicionário de atualização com a chave 'question_clarified'.

    Raises:
        ValueError: Se a pergunta original no estado estiver vazia.
        TypeError: Se o conteúdo da resposta do LLM não for uma string.
        LangChainError: Se houver um erro na comunicação com o LLM.

    """  # ! CORREÇÃO: Docstring completa
    original_question = state.get("original_question", "").strip()
    if not original_question:
        raise ValueError(ERROR_EMPTY_QUESTION)

    logger.info("Iniciando reformulação da pergunta")
    try:
        prompt = [
            SystemMessage(REFORMULATE_SYSTEM_PROMPT),
            HumanMessage(original_question),
        ]
        response = llm.invoke(prompt)

        # ! CORREÇÃO: Substituído 'assert' por 'if/raise' para robustez
        if not isinstance(response.content, str):
            raise TypeError(ERROR_LLM_RESPONSE_NOT_STRING)

        reformulated = response.content.strip()

        if not reformulated:
            logger.warning("Resposta vazia do LLM, usando pergunta original")
            reformulated = original_question

    except LangChainError:
        logger.exception("Erro na reformulação")
        raise  # Re-lança a exceção original
    else:
        logger.info("Pergunta reformulada com sucesso: %s...", reformulated[:100])
        return {"question_clarified": reformulated}


def answer_node(state: AgentState, llm: ChatOpenAI) -> dict[str, str]:
    """Nó para gerar uma resposta educativa baseada na pergunta clarificada.

    Args:
        state (AgentState): O estado compartilhado do workflow.
        llm (ChatOpenAI): O modelo de linguagem configurado.

    Returns:
        dict[str, str]: Um dicionário de atualização com a chave 'answer'.

    Raises:
        ValueError: Se a pergunta clarificada no estado estiver vazia.
        TypeError: Se o conteúdo da resposta do LLM não for uma string.
        LangChainError: Se houver um erro na comunicação com o LLM.

    """  # ! CORREÇÃO: Docstring completa
    reformulated_question = state.get("question_clarified", "").strip()
    if not reformulated_question:
        raise ValueError(ERROR_EMPTY_CLARIFIED_QUESTION)

    logger.info("Iniciando geração da resposta")
    try:
        prompt = [
            SystemMessage(ANSWER_SYSTEM_PROMPT),
            HumanMessage(reformulated_question),
        ]
        response = llm.invoke(prompt)

        # ! CORREÇÃO: Substituído 'assert' por 'if/raise' para robustez
        if not isinstance(response.content, str):
            raise TypeError(ERROR_LLM_RESPONSE_NOT_STRING)

        answer = response.content.strip()

        if not answer:
            logger.warning("Resposta vazia do LLM")
            answer = "Desculpe, não foi possível gerar uma resposta adequada."

    except LangChainError:
        logger.exception("Erro na geração da resposta")
        raise
    else:
        logger.info("Resposta gerada com sucesso")
        return {"answer": answer}


# ==============================================================================
# 7. FÁBRICA DE GRAFOS (GRAPH FACTORY)
# ==============================================================================
def create_graph(llm: ChatOpenAI) -> CompiledGraph:
    """Cria e compila o workflow do LangGraph.

    Args:
        llm (ChatOpenAI): O modelo de linguagem configurado.

    Returns:
        CompiledGraph: Um grafo compilado representando o workflow.

    Raises:
        TypeError: Se o argumento 'llm' não for uma instância de ChatOpenAI.

    """  # ! CORREÇÃO: Docstring completa
    if not isinstance(llm, ChatOpenAI):
        raise TypeError(ERROR_INVALID_LLM_TYPE)

    logger.info("Criando workflow do LangGraph")
    workflow = StateGraph(AgentState)

    workflow.add_node(REFORMULATE_NODE, lambda state: reformulate_node(state, llm))
    workflow.add_node(ANSWER_NODE, lambda state: answer_node(state, llm))

    workflow.set_entry_point(REFORMULATE_NODE)
    workflow.add_edge(REFORMULATE_NODE, ANSWER_NODE)
    workflow.add_edge(ANSWER_NODE, END)

    return workflow.compile()


# ! ==============================================================================
# ! 8. FUNÇÃO PRINCIPAL
# ! ==============================================================================
def main() -> None:
    """Função principal que executa o assistente de perguntas.

    Raises:
        ValueError: Se a pergunta do usuário estiver vazia.

    """  # ! CORREÇÃO: Docstring completa
    logger.info("Inicializando o Agente Assistente de Perguntas...")

    pergunta_usuario = (
        "Como eu consigo medir o tempo de execução de um código em python, "
        "que usa a biblioteca Langgraph?"
    )
    if not pergunta_usuario.strip():
        raise ValueError(ERROR_USER_QUESTION_EMPTY)

    try:
        language_model = setup_llm()
        question_assistant_agent = create_graph(language_model)
        initial_state = {"original_question": pergunta_usuario}
        logger.info("Processando pergunta: %s...", pergunta_usuario[:100])
        final_state = question_assistant_agent.invoke(initial_state)

        print("\n" + "=" * 50)
        print("--- RESULTADO FINAL DO AGENTE ---")
        print(f"Pergunta Original: {final_state.get('original_question')}")
        print(f"Pergunta Clarificada: {final_state.get('question_clarified')}")
        print("-" * 50)
        print(f"Resposta:\n{final_state.get('answer')}")
        print("=" * 50)

        logger.info("Execução concluída com sucesso")
    except (ValueError, TypeError, LangChainError) as e:
        logger.exception("Ocorreu um erro controlado durante a execução")
        print(f"\nERRO: {e}")
        sys.exit(1)
    except Exception:
        logger.exception("Ocorreu um erro inesperado durante a execução")
        print("\nERRO: Ocorreu um erro inesperado. Verifique o arquivo de log.")
        sys.exit(1)


# ! ==============================================================================
# ! 9. BLOCO DE EXECUÇÃO
# ! ==============================================================================
if __name__ == "__main__":
    main()
