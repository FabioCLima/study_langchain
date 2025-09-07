"""Uso de um modelo de chat para responder uma pergunta
Usando prompt template para gerar o prompt para ser usado com o modelo de chat.
"""

from typing import Any  # type: ignore

from langchain.prompts import (
    ChatPromptTemplate,  # type: ignore
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)
from langchain_openai import ChatOpenAI  # type: ignore
from openai_client import create_analytical_model

# * 1. Instanciar o modelo de chat
chat: ChatOpenAI = create_analytical_model()

# * 2. Prompt template
system_template = """ Você é um tutor de {linguagem} especializado em ensinar para 
{nivel_user}.

Características do seu ensino:
-Nível: {nivel_user}
-linguagem: {linguagem}
-Estilo: {estilo_ensino}

Suas respostas devem ser {estilo_ensino} e adequadas para o nível {nivel_user}."""

system_prompt = SystemMessagePromptTemplate.from_template(system_template)

# * Template para mensagem do usuário
human_template = """
Tópico: {topico}

Pergunta: {pergunta}

Contexto: {contexto}
"""
human_prompt = HumanMessagePromptTemplate.from_template(human_template)

# * 3 Criar o chat Prompt Template
chat_prompt = ChatPromptTemplate.from_messages([system_prompt, human_prompt])  # type: ignore

# * 4. Perfis de user
usuarios = [
    {
        "nome": "João - Iniciante",
        "linguagem": "Python",
        "nivel_user": "iniciante completo",
        "estilo_ensino": "muito didática, com exemplos simples e analogias",
    },
    {
        "nome": "Maria - Intermediário",
        "linguagem": "Python",
        "nivel_user": "programador intermediário",
        "estilo_ensino": "técnica e direta, com boas práticas",
    },
    {
        "nome": "Pedro - Especialista",
        "linguagem": "Python",
        "nivel_user": "programador especialista",
        "estilo_ensino": "técnica e direta, com boas práticas",
    },
]

# Perguntas para testar
perguntas = [
    {
        "topico": "Estruturas de repetição",
        "pergunta": "Como faço um loop for em Python?",
        "contexto": "Preciso iterar sobre uma lista de números",
    },
    {
        "topico": "Tratamento de exceções",
        "pergunta": "Como usar try/except?",
        "contexto": "Quero evitar que meu programa pare por erros",
    },
    # TODO: Adicione uma terceira pergunta sobre "list comprehensions"
    {
        "topico": "List Comprehensions",
        "pergunta": "Como usar list comprehensions?",
        "contexto": "Quero criar uma lista de números pares",
    },
]


# 4. FUNÇÃO PRINCIPAL DO EXERCÍCIO
def executar_tutoria(usuario: dict[str, Any], pergunta: dict[str, Any]) -> None:
    """TODO: Implemente esta função que:
    1. Formata o prompt usando os templates
    2. Cria o modelo de chat
    3. Obtém a resposta da IA
    4. Exibe o resultado formatado

    Args:
        usuario: Dicionário com dados do usuário
        pergunta: Dicionário com dados da pergunta

    """
    print(f"\n{'=' * 50}")
    print(f"TUTORIA PARA: {usuario['nome']}")
    print(f"{'=' * 50}")

    # TODO: Seu código aqui
    # Dica: Use chat_prompt.format_messages(**usuario, **pergunta)

    # 1. Formatar o prompt usando os templates
    messages = chat_prompt.format_messages(**usuario, **pergunta)

    # 2. Obter a resposta da IA
    response = chat.invoke(messages)

    # 3. Exibir o resultado formatado
    print(f"📚 Tópico: {pergunta['topico']}")
    print(f"❓ Pergunta: {pergunta['pergunta']}")
    print(f"📝 Contexto: {pergunta['contexto']}")
    print("\n🤖 Resposta da IA:")
    print(f"{response.content}")  # type: ignore
    print(f"\n{'=' * 50}")


# 5. EXECUÇÃO DO EXERCÍCIO
def main() -> None:
    """Executa o exercício completo"""
    print("🎓 SISTEMA DE TUTORIA COM PROMPT TEMPLATES")
    print("Testando diferentes perfis de usuário...")

    # TODO: Implemente os loops para testar todas as combinações
    # de usuários e perguntas usando a função executar_tutoria()

    # Testar todas as combinações de usuários e perguntas
    for usuario in usuarios:
        for pergunta in perguntas:
            executar_tutoria(usuario, pergunta)


if __name__ == "__main__":
    main()
