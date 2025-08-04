"""
langchain_ex3.py
Protótipo: Estruturação de mensagens no LangChain com SystemMessage, HumanMessage e AIMessage
O assistente tem papel e comportamento bem definidos para responder sobre Python básico.
"""

from langchain_core.messages import (  # type: ignore
    AIMessage,
    HumanMessage,
    SystemMessage,
)

# 1. Definição do papel e comportamento do assistente
system_msg = SystemMessage(
    content=(
        "Você é um assistente de programação especializado em Python básico. "
        "Responda sempre de forma clara, objetiva, com exemplos simples e incentive o aprendizado."
    )
)

# 2. Mensagem do usuário
human_msg = HumanMessage(content="Como faço um loop for em Python?")

# 3. Simulação de resposta da IA (em protótipos, útil para testar fluxos)
ai_msg = AIMessage(
    content=(
        "Em Python, você pode usar o loop for para iterar sobre uma sequência. Exemplo:\n"
        "```python\nfor i in range(5):\n    print(i)\n```\n"
        "Esse código imprime os números de 0 a 4. O range(5) gera uma sequência de 0 até 4."
    )
)

# 4. Histórico da conversa
messages = [system_msg, human_msg, ai_msg]

# 5. Exemplo de uso: imprime as mensagens do histórico
for msg in messages:
    print(f"[{msg.__class__.__name__}] {msg.content}\n")
