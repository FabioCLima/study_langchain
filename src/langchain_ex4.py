"""
langchain_ex4.py
Exemplo simples: papel do agente (SystemMessage), mensagem do usuário (HumanMessage),
resposta da IA (AIMessage), impressão do histórico.
"""

from langchain_core.messages import (  # type: ignore
    AIMessage,
    HumanMessage,
    SystemMessage,
)

from openai_client import create_analytical_model

# 1. Definir o papel do agente
system_msg = SystemMessage(
    content="Você é um assistente de Python básico. Responda de forma clara e objetiva."
)

# 2. Mensagem do usuário
human_msg = HumanMessage(content="Como faço um loop for em Python?")

# 3. Lista original de mensagens
messages = [system_msg, human_msg]

# 4. Instanciar o modelo de chat
chat = create_analytical_model()

# 5. Obter resposta da IA (forma recomendada)
ai_response: AIMessage = chat.invoke(messages)  # type: ignore

# 6. Imprimir lista original de mensagens
print("Mensagens originais:")
for msg in messages:
    print(f"[{msg.__class__.__name__}] {msg.content}\n")  # type: ignore

# 7. Imprimir histórico completo (incluindo resposta da IA)
print("\nHistórico completo:")
full_history: list[SystemMessage | HumanMessage | AIMessage] = [*messages, ai_response]
for msg in full_history:
    print(f"[{msg.__class__.__name__}] {msg.content}\n")  # pyright: ignore[reportUnknownMemberType] # type ignore
