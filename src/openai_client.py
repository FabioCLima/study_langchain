# langchain-udacity/llm_client/openai_client.py

import os
from pathlib import Path

from dotenv import load_dotenv  # type: ignore
from langchain_openai import ChatOpenAI  # type: ignore
from openai import OpenAI  # type: ignore


# * Exceção customizada para ausência da chave da API
class ApiKeyNotFoundError(Exception):
    """
    Exceção lançada quando a chave OPENAI_API_KEY não é encontrada no arquivo .env.
    Herda de Exception (herança simples em Python).
    Boas práticas: crie exceções específicas para facilitar o tratamento de erros.
    """

    pass


class ApiKeyLoader:
    """
    Utility to load the OpenAI API key from a .env file.
    If no path is provided, it searches for .env in the current and parent directories.
    """

    def __init__(self, env_path: Path | None = None) -> None:
        if env_path is not None:
            if not env_path.exists() or not env_path.is_file():
                raise ValueError(f"Invalid .env path: {env_path}")
            self.env_path = env_path
        else:
            found_env = self._find_env_path()
            if found_env is None:
                raise ValueError(
                    "Could not find a .env file in current or parent directories."
                )
            self.env_path = found_env

    def _find_env_path(self) -> Path | None:
        """Searches for a .env file in current and parent directories."""
        current = Path(__file__).resolve().parent
        for parent in [current, *current.parents]:
            candidate = parent / ".env"
            if candidate.exists() and candidate.is_file():
                return candidate
        return None

    def get_openai_key(self) -> str:
        load_dotenv(self.env_path)
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ApiKeyNotFoundError("OPENAI_API_KEY not found in .env file.")
        return api_key


class OpenAIClient:
    # * A high-level abstraction for the OpenAI API client
    # * SRP: Esta classe encapsula a configuração e acesso ao cliente OpenAI
    """
    A high-level abstraction layer for interacting with the OpenAI API.
    This class:
    - Encapsulates client configuration
    - Provides a simplified interface

    Args:
        api_key (str): OpenAI API key (must be provided externally)
        >>> client = OpenAIClient("your-api-key")
        >>> openai_client = client.client  # Lazy-loaded property
    """

    def __init__(self, api_key: str) -> None:
        """
        Initializes the OpenAI client configuration (does not create the client
        yet).

        Args:
            api_key (str): Valid OpenAI API key.

        Raises:
            ValueError: If api_key is empty or None.
        """

        if not api_key:
            msg = "OpenAI API key is required"
            raise ValueError(msg)
        self.api_key: str = api_key
        self._client: OpenAI | None = None  # Cache for the OpenAI client

    @property
    def client(self) -> OpenAI:
        """
        Provides lazy-loaded, cached access to the OpenAI client instance.
        # Padrão property: permite acesso como atributo, mas executa lógica de
        # criação.
        # Singleton leve: garante que só um cliente é criado por instância
        Returns:
            OpenAI: Configured and ready-to-use OpenAI client.

        Note:
            The client is created on first access (singleton pattern).
        """
        if self._client is None:  # * first access, creates the client
            self._client = self._create_client()
        return self._client

    def _create_client(self) -> OpenAI:
        """
        Private method for client creation (separated for testability/
        extensibility).

        Returns:
            OpenAI: New OpenAI client instance.
        """
        return OpenAI(api_key=self.api_key)

    def __repr__(self) -> str:
        """
        Debug-friendly representation (masks sensitive API key).

        Returns:
            str: Safe string representation.
        """
        return f"OpenAIClient(api_key='***{self.api_key[-4:]}')"


class ChatModelFactory:
    """
    Factory class para criar diferentes tipos de modelos de chat do LangChain.

    Esta classe implementa o padrão Factory Method, permitindo a criação
    de diferentes configurações de modelos ChatOpenAI de forma centralizada
    e reutilizável.

    Args:
        api_key (str): Chave da API da OpenAI

    Example:
        >>> factory = ChatModelFactory("your-api-key")
        >>> analytical_model = factory.create_analytical_model()
        >>> creative_model = factory.create_creative_model()
    """

    def __init__(self, api_key: str) -> None:
        """
        Inicializa a factory com a chave da API.

        Args:
            api_key (str): Chave válida da API da OpenAI

        Raises:
            ValueError: Se a api_key estiver vazia ou None
        """
        if not api_key:
            msg = "OpenAI API key is required for ChatModelFactory"
            raise ValueError(msg)
        self.api_key: str = api_key

    def create_analytical_model(
        self, model_name: str = "gpt-4", temperature: float = 0.1
    ) -> ChatOpenAI:
        """
        Cria um modelo otimizado para análises e tarefas que requerem precisão.

        Configuração:
        - Temperatura baixa (0.1) para respostas mais determinísticas
        - Modelo GPT-4 por padrão para melhor capacidade analítica

        Args:
            model_name (str): Nome do modelo OpenAI (padrão: "gpt-4")
            temperature (float): Controla a aleatoriedade (padrão: 0.1)

        Returns:
            ChatOpenAI: Instância configurada para análises
        """
        return ChatOpenAI(
            api_key=self.api_key,  # type: ignore
            model=model_name,  # fixed
            temperature=temperature,
        )

    def create_creative_model(
        self, model_name: str = "gpt-3.5-turbo", temperature: float = 0.8
    ) -> ChatOpenAI:
        """
        Cria um modelo otimizado para tarefas criativas.

        Configuração:
        - Temperatura alta (0.8) para respostas mais criativas
        - GPT-3.5-turbo por padrão (mais rápido e econômico)

        Args:
            model_name (str): Nome do modelo OpenAI (padrão: "gpt-3.5-turbo")
            temperature (float): Controla a criatividade (padrão: 0.8)

        Returns:
            ChatOpenAI: Instância configurada para criatividade
        """
        return ChatOpenAI(
            api_key=self.api_key,  # type: ignore
            model=model_name,  # fixed
            temperature=temperature,
        )

    def create_conversational_model(
        self, model_name: str = "gpt-3.5-turbo", temperature: float = 0.7
    ) -> ChatOpenAI:
        """
        Cria um modelo balanceado para conversas naturais.

        Configuração:
        - Temperatura moderada (0.7) para equilíbrio entre precisão e naturalidade
        - GPT-3.5-turbo por padrão para boa performance

        Args:
            model_name (str): Nome do modelo OpenAI (padrão: "gpt-3.5-turbo")
            temperature (float): Controla a naturalidade (padrão: 0.7)

        Returns:
            ChatOpenAI: Instância configurada para conversas
        """
        return ChatOpenAI(
            api_key=self.api_key,  # type: ignore
            model=model_name,  # fixed
            temperature=temperature,
        )

    def create_custom_model(
        self,
        model_name: str,
        temperature: float,
        max_tokens: int = 2048,
        **kwargs: object,
    ) -> ChatOpenAI:
        """
        Cria um modelo com configurações personalizadas.

        Args:
            model_name (str): Nome do modelo OpenAI
            temperature (float): Controla a aleatoriedade (0.0 a 2.0)
            max_tokens (int): Número máximo de tokens na resposta
            **kwargs: Argumentos adicionais para o modelo

        Returns:
            ChatOpenAI: Instância com configurações personalizadas
        """
        return ChatOpenAI(
            api_key=self.api_key,  # type: ignore
            model=model_name,  # fixed
            temperature=temperature,
        )


#! Facilita importação em outros módulos
__all__ = ["ApiKeyLoader", "ChatModelFactory", "OpenAIClient"]


# === FUNÇÃO UTILITÁRIA PARA CRIAR MODELO ANALÍTICO ===
def create_analytical_model() -> ChatOpenAI | None:
    """
    Função utilitária que demonstra o uso completo do módulo para criar
    um modelo analítico.

    Esta função:
    1. Carrega a chave da API do arquivo .env
    2. Cria uma instância da ChatModelFactory
    3. Retorna um modelo configurado para análises

    Returns:
        Optional[ChatOpenAI]: Modelo analítico ou None em caso de erro

    Example:
        >>> model = create_analytical_model()
        >>> if model:
        ...     response = model.invoke("Analise este texto...")
    """
    try:
        env_file_path: Path = Path(__file__).resolve().parent / ".env"
        loader: ApiKeyLoader = ApiKeyLoader(Path(env_file_path))
        openai_api_key = loader.get_openai_key()
        print(f"Chave da API OpenAI carregada com sucesso: ***{openai_api_key[-4:]}")

        chat_factory = ChatModelFactory(openai_api_key)
        analytical_llm = chat_factory.create_analytical_model()
        print("Modelo de chat OpenAI criado com sucesso!")
        return analytical_llm

    except (ValueError, ApiKeyNotFoundError) as e:
        print(f"Erro ao carregar a chave da API: {e}")
        return None


def example_usage() -> None:
    """
    Exemplo didático de uso do módulo, incluindo a nova ChatModelFactory.
    """
    try:
        env_file_path: Path = Path(__file__).resolve().parent / ".env"
        loader: ApiKeyLoader = ApiKeyLoader(Path(env_file_path))
        openai_api_key = loader.get_openai_key()
        print(f"Loaded OpenAI API key: ***{openai_api_key[-4:]}")

        # Exemplo com OpenAI client original
        client = OpenAIClient(openai_api_key)
        openai_client = client.client
        print(f"OpenAI client created: {openai_client}")

        # Exemplo com ChatModelFactory
        chat_factory = ChatModelFactory(openai_api_key)

        # Diferentes tipos de modelos
        analytical_model = chat_factory.create_analytical_model()
        creative_model = chat_factory.create_creative_model()
        conversational_model = chat_factory.create_conversational_model()

        print("✅ Todos os modelos de chat foram criados com sucesso!")
        print(
            f"📊 Modelo analítico: {analytical_model.model_name} (temp: {analytical_model.temperature})"
        )
        print(
            f"🎨 Modelo criativo: {creative_model.model_name} (temp: {creative_model.temperature})"
        )
        print(
            f"💬 Modelo conversacional: {conversational_model.model_name} (temp: {conversational_model.temperature})"
        )

    except (ValueError, ApiKeyNotFoundError) as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    # Exemplo de uso com a nova funcionalidade
    example_usage()

    print("\n" + "=" * 50)
    print("Testando a função create_analytical_model():")
    model = create_analytical_model()
    if model:
        print(f"✅ Modelo criado: {model.model_name}")

# Sugestão didática: Exemplos de importação
# from openai_client import ApiKeyLoader, OpenAIClient, ChatModelFactory, create_analytical_model
#
# # Uso básico
# model = create_analytical_model()
#
# # Uso avançado
# loader = ApiKeyLoader(Path(".env"))
# api_key = loader.get_openai_key()
# factory = ChatModelFactory(api_key)
# analytical_model = factory.create_analytical_model()
# creative_model = factory.create_creative_model()
