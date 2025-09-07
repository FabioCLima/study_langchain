"""Exemplos de Evolução de Chains no LangChain

Este arquivo demonstra a progressão de chains simples para complexas,
baseado no simple_chain.py como ponto de partida.

Cada exemplo mostra uma evolução específica:
1. Chain básica (como simple_chain.py)
2. Chain com output parser estruturado
3. Chain com múltiplos passos
4. Chain com validação e tratamento de erros
5. Chain com memória e contexto
"""

import os
from typing import Any

from dotenv import find_dotenv, load_dotenv
from langchain_core.memory import ConversationBufferMemory  # type: ignore
from langchain_core.output_parsers import (  # type: ignore
    JsonOutputParser,
    StrOutputParser,
)
from langchain_core.prompts import ChatPromptTemplate  # type: ignore
from langchain_core.runnables import (  # type: ignore
    RunnablePassthrough,
    RunnableSerializable,
)
from langchain_openai import ChatOpenAI  # type: ignore
from pydantic import BaseModel, Field

# Setup básico
_ = load_dotenv(find_dotenv())
if not os.getenv("OPENAI_API_KEY"):
    raise ValueError("OPENAI_API_KEY não encontrada")

# =============================================================================
# EXEMPLO 1: CHAIN BÁSICA (como simple_chain.py)
# =============================================================================


def example_1_basic_chain():
    """Chain básica - ponto de partida."""
    print("🔹 Exemplo 1: Chain Básica")
    print("=" * 50)

    # Modelo
    model = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.5)  # type: ignore

    # Prompt simples
    prompt = ChatPromptTemplate.from_template(
        "Você é um assistente útil. Responda a pergunta: {question}"
    )

    # Output parser básico
    output_parser = StrOutputParser()

    # Chain
    chain: RunnableSerializable[
        dict[str, str], str
    ] = prompt | model | output_parser

    # Execução
    response = chain.invoke({"question": "O que é inteligência artificial?"})
    print(f"Resposta: {response[:100]}...")
    print()


# =============================================================================
# EXEMPLO 2: CHAIN COM OUTPUT PARSER ESTRUTURADO
# =============================================================================


class AIResponse(BaseModel):
    """Estrutura para resposta sobre IA."""

    definition: str = Field(description="Definição clara e concisa")
    examples: list[str] = Field(description="Exemplos práticos")
    importance: str = Field(description="Por que é importante")
    confidence: float = Field(description="Confiança na resposta (0-1)", ge=0.0, le=1.0)


def example_2_structured_chain():
    """Chain com output parser estruturado."""
    print("🔹 Exemplo 2: Chain com Output Parser Estruturado")
    print("=" * 50)

    # Modelo
    model = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.3)  # type: ignore

    # Prompt estruturado
    prompt = ChatPromptTemplate.from_template(
        """Você é um especialista em inteligência artificial.
        
        Analise o conceito: {concept}
        
        Forneça uma resposta estruturada com:
        - Definição clara
        - Exemplos práticos
        - Importância do conceito
        - Nível de confiança na resposta
        
        Responda em formato JSON válido."""
    )

    # Output parser estruturado
    output_parser = JsonOutputParser(pydantic_object=AIResponse)

    # Chain
    chain: RunnableSerializable[
        dict[str, str], AIResponse
    ] = prompt | model | output_parser

    # Execução
    response = chain.invoke({"concept": "Machine Learning"})

    print("Resposta estruturada:")
    print(f"- Definição: {response.definition[:80]}...")
    print(f"- Exemplos: {len(response.examples)} exemplos fornecidos")
    print(f"- Importância: {response.importance[:80]}...")
    print(f"- Confiança: {response.confidence:.2f}")
    print()


# =============================================================================
# EXEMPLO 3: CHAIN COM MÚLTIPLOS PASSOS
# =============================================================================


def example_3_multi_step_chain():
    """Chain com múltiplos passos de processamento."""
    print("🔹 Exemplo 3: Chain com Múltiplos Passos")
    print("=" * 50)

    # Modelo
    model = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.4)  # type: ignore

    # Passo 1: Análise inicial
    analysis_prompt = ChatPromptTemplate.from_template(
        """Analise o conceito: {concept}
        
        Forneça:
        1. Definição básica
        2. Categorias principais
        3. Aplicações práticas
        
        Seja conciso e objetivo."""
    )

    # Passo 2: Geração de exemplos
    examples_prompt = ChatPromptTemplate.from_template(
        """Com base na análise: {analysis}
        
        Gere 3 exemplos práticos e específicos do conceito: {concept}
        
        Cada exemplo deve incluir:
        - Contexto de uso
        - Benefícios
        - Limitações"""
    )

    # Passo 3: Síntese final
    synthesis_prompt = ChatPromptTemplate.from_template(
        """Com base na análise e exemplos:
        
        Análise: {analysis}
        Exemplos: {examples}
        
        Crie uma explicação final clara e didática sobre: {concept}
        
        Inclua:
        - Resumo executivo
        - Pontos-chave
        - Recomendações práticas"""
    )

    # Chain multi-step
    chain: RunnableSerializable[str, str] = (
        {"concept": RunnablePassthrough()}
        | analysis_prompt
        | model
        | StrOutputParser()
        | {"analysis": RunnablePassthrough(), "concept": RunnablePassthrough()}
        | examples_prompt
        | model
        | StrOutputParser()
        | {
            "analysis": RunnablePassthrough(),
            "examples": RunnablePassthrough(),
            "concept": RunnablePassthrough(),
        }
        | synthesis_prompt
        | model
        | StrOutputParser()
    )

    # Execução
    response = chain.invoke("Deep Learning")

    print("Resposta multi-step:")
    print(response[:200] + "...")
    print()


# =============================================================================
# EXEMPLO 4: CHAIN COM VALIDAÇÃO E TRATAMENTO DE ERROS
# =============================================================================


def validate_concept(concept: str) -> bool:
    """Valida se o conceito é apropriado para análise."""
    forbidden_words = ["pornografia", "violência", "ilegal"]
    return not any(word in concept.lower() for word in forbidden_words)


def safe_chain_execution(
    chain, input_data: dict[str, Any], max_retries: int = 3
) -> str:
    """Executa chain com tratamento de erros."""
    for attempt in range(max_retries):
        try:
            return chain.invoke(input_data)
        except Exception as e:
            if attempt == max_retries - 1:
                return f"Erro após {max_retries} tentativas: {e!s}"
            print(f"Tentativa {attempt + 1} falhou: {e}")
    return "Erro desconhecido"


def example_4_robust_chain():
    """Chain com validação e tratamento de erros robusto."""
    print("🔹 Exemplo 4: Chain com Validação e Tratamento de Erros")
    print("=" * 50)

    # Modelo
    model = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.5)  # type: ignore

    # Prompt
    prompt = ChatPromptTemplate.from_template(
        """Você é um especialista em tecnologia.
        
        Conceito: {concept}
        
        Forneça uma explicação clara e educativa.
        Se o conceito for inadequado, explique por que não pode ser analisado."""
    )

    # Output parser
    output_parser = StrOutputParser()

    # Chain
    chain: RunnableSerializable[
        dict[str, str], str
    ] = prompt | model | output_parser

    # Testes com diferentes inputs
    test_concepts = [
        "Machine Learning",
        "conteúdo inadequado",  # Deve ser rejeitado
        "Blockchain",
    ]

    for concept in test_concepts:
        print(f"Testando conceito: {concept}")

        # Validação
        if not validate_concept(concept):
            print("❌ Conceito rejeitado por validação")
            continue

        # Execução segura
        response = safe_chain_execution(chain, {"concept": concept})
        print(f"✅ Resposta: {response[:100]}...")
        print("-" * 30)
    print()


# =============================================================================
# EXEMPLO 5: CHAIN COM MEMÓRIA E CONTEXTO
# =============================================================================


def example_5_memory_chain():
    """Chain com memória para manter contexto da conversa."""
    print("🔹 Exemplo 5: Chain com Memória e Contexto")
    print("=" * 50)

    # Modelo
    model = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.6)  # type: ignore

    # Prompt que usa histórico
    prompt = ChatPromptTemplate.from_template(
        """Você é um tutor de tecnologia especializado em IA.
        
        Histórico da conversa:
        {chat_history}
        
        Pergunta atual: {question}
        
        Responda de forma contextualizada, referenciando o histórico quando relevante.
        Seja didático e encoraje perguntas de follow-up."""
    )

    # Memória
    memory = ConversationBufferMemory(return_messages=True, memory_key="chat_history")

    # Output parser
    output_parser = StrOutputParser()

    # Chain com memória
    chain: RunnableSerializable[
        dict[str, Any], str
    ] = prompt | model | output_parser

    # Simulação de conversa
    conversation_steps = [
        "O que é inteligência artificial?",
        "Como isso se relaciona com machine learning?",
        "Pode dar exemplos práticos de aplicações?",
        "Quais são os desafios éticos?",
    ]

    print("Simulando conversa com memória:")
    for i, question in enumerate(conversation_steps, 1):
        print(f"\n--- Passo {i} ---")
        print(f"Pergunta: {question}")

        # Executa chain
        response = chain.invoke({"question": question, "chat_history": memory.buffer})

        # Atualiza memória
        memory.save_context({"input": question}, {"output": response})

        print(f"Resposta: {response[:150]}...")
    print()


# =============================================================================
# FUNÇÃO PRINCIPAL
# =============================================================================


def main():
    """Executa todos os exemplos de evolução de chains."""
    print("🚀 Demonstração de Evolução de Chains no LangChain")
    print("=" * 60)
    print()

    # Executa exemplos em ordem de complexidade
    example_1_basic_chain()
    example_2_structured_chain()
    example_3_multi_step_chain()
    example_4_robust_chain()
    example_5_memory_chain()

    print("✅ Demonstração concluída!")
    print("\n💡 Dicas para evolução:")
    print("- Comece sempre com chains simples")
    print("- Adicione complexidade gradualmente")
    print("- Teste cada componente individualmente")
    print("- Documente suas descobertas")
    print("- Reutilize componentes bem-sucedidos")


if __name__ == "__main__":
    main()
