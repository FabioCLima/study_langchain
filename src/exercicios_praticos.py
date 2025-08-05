"""
Exercícios Práticos: Construindo Classes de Chatbot
==================================================

Este arquivo contém exercícios práticos para ajudar você a dominar
a construção de classes de chatbot usando LangChain.
"""

import os
from typing import Dict, Any, List
from dotenv import find_dotenv, load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough


# ============================================================================
# EXERCÍCIO 1: Chatbot Básico
# ============================================================================

def exercicio_1_basico():
    """
    EXERCÍCIO 1: Criar um chatbot básico
    
    Objetivo: Implementar a classe Chatbot mais simples possível
    com apenas os componentes essenciais.
    
    Tarefas:
    1. Criar a classe Chatbot
    2. Implementar __init__ com parâmetros básicos
    3. Implementar método chat()
    4. Testar a funcionalidade
    """
    
    print("🎯 EXERCÍCIO 1: Chatbot Básico")
    print("=" * 50)
    
    # TODO: Implemente a classe Chatbot básica aqui
    class ChatbotBasico:
        def __init__(self, name="Assistant"):
            # Seu código aqui
            pass
        
        def chat(self, message):
            # Seu código aqui
            pass
    
    # TODO: Teste sua implementação
    # bot = ChatbotBasico("Tutor")
    # response = bot.chat("Olá!")
    # print(response)
    
    print("✅ Exercício 1 concluído!")
    print()


# ============================================================================
# EXERCÍCIO 2: Chatbot com Personalidade
# ============================================================================

def exercicio_2_personalidade():
    """
    EXERCÍCIO 2: Adicionar personalidade ao chatbot
    
    Objetivo: Expandir a classe para incluir personalidade configurável
    e diferentes tipos de chatbot.
    
    Tarefas:
    1. Adicionar parâmetro personality ao __init__
    2. Implementar método update_personality()
    3. Criar diferentes tipos de chatbot
    4. Testar mudança de personalidade
    """
    
    print("🎯 EXERCÍCIO 2: Chatbot com Personalidade")
    print("=" * 50)
    
    # Exemplos de personalidades para testar:
    personalidades = {
        "tutor": "You are a helpful programming tutor. Explain concepts clearly and provide examples.",
        "comedian": "You are a funny comedian. Always respond with humor and jokes.",
        "chef": "You are a professional chef. Give cooking advice and recipes.",
        "teacher": "You are a patient teacher. Explain things step by step."
    }
    
    # TODO: Implemente a classe Chatbot com personalidade
    class ChatbotPersonalidade:
        def __init__(self, name="Assistant", personality="You are a helpful assistant"):
            # Seu código aqui
            pass
        
        def chat(self, message):
            # Seu código aqui
            pass
        
        def update_personality(self, new_personality):
            # Seu código aqui
            pass
    
    # TODO: Teste diferentes personalidades
    # bot = ChatbotPersonalidade("Chef", personalidades["chef"])
    # response = bot.chat("Como fazer arroz?")
    # print(response)
    
    print("✅ Exercício 2 concluído!")
    print()


# ============================================================================
# EXERCÍCIO 3: Chatbot com Configurações Avançadas
# ============================================================================

def exercicio_3_configuracoes():
    """
    EXERCÍCIO 3: Adicionar configurações avançadas
    
    Objetivo: Implementar configurações de modelo, validação e tratamento de erros.
    
    Tarefas:
    1. Adicionar configurações de modelo (temperature, max_tokens)
    2. Implementar validação de entrada
    3. Adicionar tratamento de erros
    4. Implementar método get_info()
    """
    
    print("🎯 EXERCÍCIO 3: Chatbot com Configurações Avançadas")
    print("=" * 50)
    
    # TODO: Implemente a classe Chatbot com configurações avançadas
    class ChatbotAvancado:
        def __init__(self, name="Assistant", personality="You are a helpful assistant", 
                     model_name="gpt-3.5-turbo", temperature=0.0, max_tokens=1000):
            # Seu código aqui
            pass
        
        def chat(self, message):
            # Seu código aqui
            # Adicione validação de entrada
            # Adicione tratamento de erros
            pass
        
        def get_info(self):
            # Seu código aqui
            pass
        
        def update_personality(self, new_personality):
            # Seu código aqui
            pass
    
    # TODO: Teste as configurações avançadas
    # bot = ChatbotAvancado("Tutor", temperature=0.7, max_tokens=500)
    # info = bot.get_info()
    # print(info)
    
    print("✅ Exercício 3 concluído!")
    print()


# ============================================================================
# EXERCÍCIO 4: Chatbot Especializado
# ============================================================================

def exercicio_4_especializado():
    """
    EXERCÍCIO 4: Criar chatbot especializado
    
    Objetivo: Criar uma classe base e classes especializadas que herdam dela.
    
    Tarefas:
    1. Criar classe base ChatbotBase
    2. Criar classes especializadas (TutorChatbot, ChefChatbot, etc.)
    3. Implementar métodos específicos para cada especialização
    4. Testar as diferentes especializações
    """
    
    print("🎯 EXERCÍCIO 4: Chatbot Especializado")
    print("=" * 50)
    
    # TODO: Implemente a hierarquia de classes
    class ChatbotBase:
        def __init__(self, name, personality, model_name="gpt-3.5-turbo", temperature=0.0):
            # Seu código aqui
            pass
        
        def chat(self, message):
            # Seu código aqui
            pass
    
    class TutorChatbot(ChatbotBase):
        def __init__(self, subject="programming"):
            # Seu código aqui
            pass
        
        def explain_concept(self, concept):
            # Método específico para tutores
            pass
    
    class ChefChatbot(ChatbotBase):
        def __init__(self):
            # Seu código aqui
            pass
        
        def get_recipe(self, dish):
            # Método específico para chefs
            pass
    
    # TODO: Teste as classes especializadas
    # tutor = TutorChatbot("Python")
    # chef = ChefChatbot()
    
    print("✅ Exercício 4 concluído!")
    print()


# ============================================================================
# EXERCÍCIO 5: Chatbot com Memória
# ============================================================================

def exercicio_5_memoria():
    """
    EXERCÍCIO 5: Adicionar memória ao chatbot
    
    Objetivo: Implementar memória de conversa para manter contexto.
    
    Tarefas:
    1. Adicionar ConversationBufferMemory
    2. Implementar histórico de conversas
    3. Adicionar método para limpar memória
    4. Testar conversas com contexto
    """
    
    print("🎯 EXERCÍCIO 5: Chatbot com Memória")
    print("=" * 50)
    
    # TODO: Implemente a classe Chatbot com memória
    class ChatbotComMemoria:
        def __init__(self, name="Assistant", personality="You are a helpful assistant"):
            # Seu código aqui
            # Adicione ConversationBufferMemory
            pass
        
        def chat(self, message):
            # Seu código aqui
            # Use a memória para manter contexto
            pass
        
        def clear_memory(self):
            # Seu código aqui
            pass
        
        def get_conversation_history(self):
            # Seu código aqui
            pass
    
    # TODO: Teste a memória
    # bot = ChatbotComMemoria("Tutor")
    # bot.chat("Meu nome é João")
    # bot.chat("Qual é o meu nome?")
    
    print("✅ Exercício 5 concluído!")
    print()


# ============================================================================
# FUNÇÃO PRINCIPAL PARA EXECUTAR OS EXERCÍCIOS
# ============================================================================

def executar_exercicios():
    """Executa todos os exercícios em sequência."""
    
    print("🚀 INICIANDO EXERCÍCIOS PRÁTICOS")
    print("=" * 60)
    print()
    
    # Configurar ambiente
    try:
        _ = load_dotenv(find_dotenv())
        if not os.getenv("OPENAI_API_KEY"):
            print("⚠️ OPENAI_API_KEY não encontrada. Alguns exercícios podem não funcionar.")
            print("💡 Configure sua API key no arquivo .env")
            print()
    except Exception as e:
        print(f"⚠️ Erro ao carregar ambiente: {e}")
        print()
    
    # Executar exercícios
    exercicios = [
        exercicio_1_basico,
        exercicio_2_personalidade,
        exercicio_3_configuracoes,
        exercicio_4_especializado,
        exercicio_5_memoria
    ]
    
    for i, exercicio in enumerate(exercicios, 1):
        try:
            exercicio()
        except Exception as e:
            print(f"❌ Erro no exercício {i}: {e}")
            print()
    
    print("🎉 TODOS OS EXERCÍCIOS CONCLUÍDOS!")
    print("=" * 60)
    print()
    print("💡 Dicas para continuar aprendendo:")
    print("   1. Implemente cada exercício passo a passo")
    print("   2. Teste com diferentes configurações")
    print("   3. Adicione funcionalidades extras")
    print("   4. Integre com interfaces web")
    print("   5. Explore outros componentes do LangChain")


if __name__ == "__main__":
    executar_exercicios() 