"""Exemplo Didático: Construindo uma Classe de Chatbot
==================================================

Metodologia: "De Dentro para Fora" - Construir componentes individuais primeiro,
depois conectá-los em uma classe coesa.
"""

import os
from typing import Any

from dotenv import find_dotenv, load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI


class Chatbot:
    """Chatbot simples usando LangChain.
    
    Metodologia de construção:
    1. Componentes individuais (como você já fez)
    2. Conectar componentes na classe
    3. Adicionar métodos de interação
    """

    def __init__(
        self,
        name: str = "Assistant",
        personality: str = "You are a helpful assistant",
        model_name: str = "gpt-3.5-turbo",
        temperature: float = 0.0
    ):
        """Inicializa o chatbot com os componentes básicos.
        
        Args:
            name: Nome do chatbot
            personality: Personalidade/instruções do sistema
            model_name: Nome do modelo LLM
            temperature: Temperatura para criatividade das respostas

        """
        # PASSO 1: Configurar ambiente
        self._setup_environment()

        # PASSO 2: Configurar identidade (Bloco 1)
        self.name = name
        self.personality = personality

        # PASSO 3: Configurar modelo LLM (Bloco 2)
        self.model = self._setup_model(model_name, temperature)

        # PASSO 4: Configurar prompt template (Bloco 3)
        self.prompt_template = self._setup_prompt_template()

        # PASSO 5: Criar a cadeia de processamento
        self.chain = self._create_chain()

    def _setup_environment(self):
        """Configura o ambiente e verifica as credenciais."""
        # Carrega variáveis de ambiente
        _ = load_dotenv(find_dotenv())

        # Verifica se a API key está configurada
        if not os.getenv("OPENAI_API_KEY"):
            raise ValueError("OPENAI_API_KEY não encontrada no arquivo .env")

    def _setup_model(self, model_name: str, temperature: float) -> ChatOpenAI:
        """Configura o modelo LLM (Bloco 2)."""
        return ChatOpenAI(
            model=model_name,
            temperature=temperature,
        )

    def _setup_prompt_template(self) -> ChatPromptTemplate:
        """Configura o template de prompt (Bloco 3)."""
        template = f"""
        {self.personality}
        
        Your name is {self.name}.
        
        User: {{user_input}}
        {self.name}: """

        return ChatPromptTemplate.from_template(template)

    def _create_chain(self):
        """Conecta todos os componentes em uma cadeia de processamento."""
        return (
            {"user_input": RunnablePassthrough()}
            | self.prompt_template
            | self.model
            | StrOutputParser()
        )

    def chat(self, message: str) -> str:
        """Método principal para interagir com o chatbot.
        
        Args:
            message: Mensagem do usuário
            
        Returns:
            Resposta do chatbot

        """
        try:
            response = self.chain.invoke(message)
            return response
        except Exception as e:
            return f"Erro ao processar mensagem: {e!s}"

    def update_personality(self, new_personality: str):
        """Permite atualizar a personalidade do chatbot."""
        self.personality = new_personality
        # Recria o prompt template com a nova personalidade
        self.prompt_template = self._setup_prompt_template()
        # Recria a cadeia
        self.chain = self._create_chain()

    def get_info(self) -> dict[str, Any]:
        """Retorna informações sobre a configuração do chatbot."""
        return {
            "name": self.name,
            "personality": self.personality,
            "model": self.model.model_name,
            "temperature": self.model.temperature
        }


# ============================================================================
# EXEMPLO DE USO - Como testar a classe
# ============================================================================

def test_chatbot():
    """Função para testar o chatbot."""
    # Criando o chatbot
    print("🔧 Criando chatbot...")
    bot = Chatbot(
        name="Tutor",
        personality="You are a helpful programming tutor. Explain concepts clearly and provide examples.",
        temperature=0.7
    )

    # Testando informações
    print("📊 Informações do chatbot:")
    print(bot.get_info())
    print()

    # Testando conversa
    print("💬 Testando conversa:")
    response = bot.chat("O que é uma classe em Python?")
    print(f"Resposta: {response}")
    print()

    # Testando atualização de personalidade
    print("🔄 Atualizando personalidade...")
    bot.update_personality("You are a funny comedian. Always respond with humor.")
    response = bot.chat("O que é uma classe em Python?")
    print(f"Nova resposta: {response}")


if __name__ == "__main__":
    test_chatbot()
