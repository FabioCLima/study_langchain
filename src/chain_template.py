'''Template de Fluxo para Chains no LangChain

Este template demonstra o fluxo padrão para criar chains no LangChain
seguindo as melhores práticas e organização de código.

Fluxo de Etapas:
1. Imports e Setup
2. Configuração do Modelo
3. Definição do Prompt
4. Configuração do Output Parser
5. Criação da Chain
6. Execução e Tratamento de Erros
7. Validação e Testes
'''

from dotenv import load_dotenv, find_dotenv
from langchain_openai import ChatOpenAI  # type: ignore
from langchain_core.prompts import ChatPromptTemplate  # type: ignore
from langchain_core.output_parsers import StrOutputParser  # type: ignore
from langchain_core.runnables import RunnablePassthrough  # type: ignore
import os
from typing import Dict, Any, Optional

# =============================================================================
# ETAPA 1: IMPORTS E SETUP
# =============================================================================

def setup_environment() -> None:
    """Configura o ambiente e valida as dependências."""
    # Carrega variáveis de ambiente
    _ = load_dotenv(find_dotenv())
    
    # Valida API key
    if not os.getenv("OPENAI_API_KEY"):
        raise ValueError("OPENAI_API_KEY não encontrada no arquivo .env")
    
    print("✅ Ambiente configurado com sucesso")

# =============================================================================
# ETAPA 2: CONFIGURAÇÃO DO MODELO
# =============================================================================

def create_model(
    model_name: str = "gpt-3.5-turbo",
    temperature: float = 0.5,
    max_tokens: Optional[int] = None
) -> ChatOpenAI:
    """
    Cria e configura o modelo LLM.
    
    Args:
        model_name: Nome do modelo a ser usado
        temperature: Controla criatividade (0.0 = determinístico, 1.0 = muito criativo)
        max_tokens: Número máximo de tokens na resposta
    
    Returns:
        ChatOpenAI: Modelo configurado
    """
    model = ChatOpenAI(
        model=model_name,
        temperature=temperature,
        max_tokens=max_tokens
    )  # type: ignore
    
    print(f"✅ Modelo {model_name} configurado (temperature={temperature})")
    return model

# =============================================================================
# ETAPA 3: DEFINIÇÃO DO PROMPT
# =============================================================================

def create_prompt() -> ChatPromptTemplate:
    """
    Cria o template do prompt.
    
    Returns:
        ChatPromptTemplate: Template do prompt configurado
    """
    prompt = ChatPromptTemplate.from_template(
        """Você é um assistente especializado em {domain}.
        
        Contexto: {context}
        Pergunta: {question}
        
        Instruções específicas:
        - Responda de forma clara e concisa
        - Use exemplos quando apropriado
        - Mantenha o foco no tópico solicitado
        
        Resposta:"""
    )
    
    print("✅ Template de prompt criado")
    return prompt

# =============================================================================
# ETAPA 4: CONFIGURAÇÃO DO OUTPUT PARSER
# =============================================================================

def create_output_parser() -> StrOutputParser:
    """
    Cria o parser de saída.
    
    Returns:
        StrOutputParser: Parser configurado
    """
    output_parser = StrOutputParser()
    print("✅ Output parser configurado")
    return output_parser

# =============================================================================
# ETAPA 5: CRIAÇÃO DA CHAIN
# =============================================================================

def create_chain(
    model: ChatOpenAI,
    prompt: ChatPromptTemplate,
    output_parser: StrOutputParser
) -> Any:
    """
    Cria a chain usando LCEL (LangChain Expression Language).
    
    Args:
        model: Modelo LLM configurado
        prompt: Template do prompt
        output_parser: Parser de saída
    
    Returns:
        Chain configurada
    """
    # Chain básica: prompt -> model -> output_parser
    chain = prompt | model | output_parser
    
    print("✅ Chain criada com sucesso")
    return chain

# =============================================================================
# ETAPA 6: EXECUÇÃO E TRATAMENTO DE ERROS
# =============================================================================

def execute_chain(
    chain: Any,
    input_data: Dict[str, Any],
    retry_count: int = 3
) -> str:
    """
    Executa a chain com tratamento de erros.
    
    Args:
        chain: Chain configurada
        input_data: Dados de entrada
        retry_count: Número de tentativas em caso de erro
    
    Returns:
        str: Resposta da chain
    """
    try:
        response = chain.invoke(input_data)
        print("✅ Chain executada com sucesso")
        return response
    except Exception as e:
        print(f"❌ Erro na execução da chain: {e}")
        if retry_count > 0:
            print(f"🔄 Tentando novamente... ({retry_count} tentativas restantes)")
            return execute_chain(chain, input_data, retry_count - 1)
        raise

# =============================================================================
# ETAPA 7: VALIDAÇÃO E TESTES
# =============================================================================

def validate_response(response: str) -> bool:
    """
    Valida se a resposta está no formato esperado.
    
    Args:
        response: Resposta da chain
    
    Returns:
        bool: True se válida, False caso contrário
    """
    if not response or len(response.strip()) < 10:
        print("⚠️ Resposta muito curta ou vazia")
        return False
    
    print("✅ Resposta validada")
    return True

# =============================================================================
# FUNÇÃO PRINCIPAL - FLUXO COMPLETO
# =============================================================================

def main() -> None:
    """Executa o fluxo completo de criação e execução de uma chain."""
    
    print("🚀 Iniciando criação da chain...")
    
    # Etapa 1: Setup
    setup_environment()
    
    # Etapa 2: Modelo
    model = create_model(
        model_name="gpt-3.5-turbo",
        temperature=0.7
    )
    
    # Etapa 3: Prompt
    prompt = create_prompt()
    
    # Etapa 4: Output Parser
    output_parser = create_output_parser()
    
    # Etapa 5: Chain
    chain = create_chain(model, prompt, output_parser)
    
    # Etapa 6: Execução
    input_data = {
        "domain": "tecnologia",
        "context": "Discussão sobre inteligência artificial",
        "question": "O que é machine learning?"
    }
    
    response = execute_chain(chain, input_data)
    
    # Etapa 7: Validação
    if validate_response(response):
        print("\n📝 Resposta final:")
        print("=" * 50)
        print(response)
        print("=" * 50)
    else:
        print("❌ Falha na validação da resposta")

if __name__ == "__main__":
    main()