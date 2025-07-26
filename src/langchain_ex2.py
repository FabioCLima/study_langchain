# study_langchain/langchain_ex1.py
'''Exemplo de script com o modelo de chat da OpenAI, e o prompt template para gerar o 
prompt para ser usado com o modelo de chat'''

from contextlib import redirect_stdout
from io import StringIO

from langchain.prompts import PromptTemplate  # type: ignore
from langchain_core.messages import (AIMessage, BaseMessage,  # type: ignore
                                     HumanMessage, SystemMessage)
from langchain_openai import ChatOpenAI  # type: ignore

from openai_client import create_analytical_model

# Protótipo: Estruturação de mensagens no LangChain com SystemMessage, HumanMessage e AIMessage
# 1. SystemMessage: Define o papel e o comportamento do assistente
system_msg = SystemMessage(
    content=(
        "Você é um assistente especializado em ensinar Python básico. "
        "Responda sempre de forma clara, objetiva e com exemplos simples. "
        "Seja educado e incentive o aprendizado contínuo."
    )
)

# 2. HumanMessage: Mensagem do usuário (pergunta)
human_msg = HumanMessage(
    content="O que é uma lista em Python e como eu crio uma?"
)

# 3. AIMessage: (Simulação de resposta do modelo)
ai_msg = AIMessage(
    content=(
        "Uma lista em Python é uma estrutura de dados que armazena uma sequência de elementos. "
        "Você pode criar uma lista usando colchetes. Exemplo:\n"
        "```python\nminha_lista = [1, 2, 3, 4]\n```\n"
        "Assim, 'minha_lista' contém quatro números. Você pode adicionar, remover e acessar elementos facilmente."
    )
)

# 4. Estrutura da conversa (histórico)
messages = [system_msg, human_msg, ai_msg]

# 5. Exemplo de uso em um protótipo (imprime as mensagens)
for msg in messages:
    print(f"[{msg.__class__.__name__}] {msg.content}\n")

#* Sem logs de debug ou prints
with redirect_stdout(StringIO()):
    model = create_analytical_model()

prompt = PromptTemplate.from_template(
    "Explique de forma simples e objetiva como usar o modelo de chat da OpenAI - chatgpt para aprender sobre {topico}"
)
msg = prompt.format(topico="langchain")

print("Prompt gerado:", msg)
if model:
    resposta = model.invoke(msg)
    print(f"Resposta:{resposta.content}")  # type: ignore
else:
    print("Erro: modelo não foi criado corretamente.")
