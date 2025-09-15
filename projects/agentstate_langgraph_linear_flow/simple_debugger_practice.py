# 1. IMPORTS ESSENCIAIS
from typing import TypedDict

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import END, StateGraph


# 2. DEFINIÇÃO DO ESTADO (A "Ficha" que viaja pelo sistema)
class AgentState(TypedDict):
    """Define a estrutura de dados que será passada entre os nós.
    É a memória compartilhada do nosso agente.
    """

    original_question: str
    question_clarified: str
    answer: str


# 3. DEFINIÇÃO DOS NÓS (As "Estações de Trabalho")
def reformulate_node(state: AgentState) -> dict[str, str]:
    """Primeira etapa: Pega a pergunta original do estado, a reformula para ser
    mais clara usando um LLM e retorna a atualização para o estado.
    """
    print("\n--- [ENTRANDO NO NÓ 1: Reformulação] ---")
    print(f"  Estado RECEBIDO: {state}")

    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.0)
    original_question = state["original_question"]

    prompt = [
        SystemMessage(
            "Sua tarefa é reformular a pergunta do usuário para que ela seja mais clara e direta. Retorne apenas a pergunta reformulada."
        ),
        HumanMessage(original_question),
    ]
    response = llm.invoke(prompt)
    reformulated = response.content

    print(f"  > Pergunta Reformulada Gerada: '{reformulated}'")

    update_dict = {"question_clarified": reformulated}
    print(f"  Atualização ENVIADA: {update_dict}")
    print("--- [SAINDO DO NÓ 1] ---")

    return update_dict


def answer_node(state: AgentState) -> dict[str, str]:
    """Segunda etapa: Pega a pergunta já clarificada do estado, gera uma
    resposta final usando um LLM (como um tutor de Python) e retorna a
    atualização para o estado.
    """
    print("\n--- [ENTRANDO NO NÓ 2: Resposta] ---")
    print(f"  Estado RECEBIDO: {state}")

    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.0)
    clarified_question = state["question_clarified"]

    prompt = [
        SystemMessage(
            "Você é um tutor expert em métodos de preparação de café. Responda de forma clara e didática."
        ),
        HumanMessage(clarified_question),
    ]
    response = llm.invoke(prompt)
    final_answer = response.content

    update_dict = {"answer": final_answer}
    print(f"  > Resposta Final Gerada (início): '{final_answer[:100]}...'")
    print("  Atualização ENVIADA: {'answer': '...'}")  # Mostrando de forma resumida
    print("--- [SAINDO DO NÓ 2] ---")

    return update_dict


# 4. FUNÇÃO PRINCIPAL (Onde a mágica acontece)
def main():
    """Orquestra a criação e execução do agente."""
    # Carrega a chave da API
    load_dotenv()

    # Monta o workflow
    workflow = StateGraph(AgentState)
    workflow.add_node("reformulate", reformulate_node)
    workflow.add_node("answer", answer_node)

    # Define as conexões (a ordem do fluxo)
    workflow.set_entry_point("reformulate")
    workflow.add_edge("reformulate", "answer")
    workflow.add_edge("answer", END)

    # Compila o grafo
    agent = workflow.compile()

    # Define a pergunta inicial
    user_question = "Como eu faço para preparar um café com filtro clever?"
    initial_state = {"original_question": user_question}

    # --- PONTO DE DEBUG 3: ANTES DE INVOCAR O AGENTE ---
    # Inicia a execução e captura o estado final
    final_state = agent.invoke(initial_state)

    # Exibe o resultado final completo
    print("\n" + "=" * 50)
    print("--- RESULTADO FINAL DO FLUXO ---")
    print(f"Estado Final Completo: {final_state}")
    print("=" * 50)


# 5. PONTO DE ENTRADA DO SCRIPT
if __name__ == "__main__":
    main()
