# roteiro_viagem/config.py

"""Módulo de configuração para aplicação de roteiro de viagem.

Este módulo define as configurações centralizadas da aplicação, incluindo chaves de API,
configurações do LangSmith e parâmetros do modelo de linguagem. Utiliza Pydantic Settings
para validação e carregamento de variáveis de ambiente.

Example:
    Uso básico das configurações:
    
    ```python
    from config import settings
    
    # Acessar configurações
    model = settings.model_name
    temp = settings.temperature
    
    # Acessar chaves secretas
    api_key = settings.openai_api_key.get_secret_value()
    ```

Attributes:
    settings (Settings): Instância global das configurações da aplicação.
"""


from pydantic import SecretStr, field_validator
from pydantic_settings import BaseSettings



class Settings(BaseSettings):
    #* Chaves de API
    """Classe de configurações da aplicação de roteiro de viagem.
    
    Esta classe define todas as configurações necessárias para a aplicação,
    incluindo chaves de API, configurações do LangSmith e parâmetros do modelo.
    As configurações são carregadas automaticamente do arquivo .env.
    
    Attributes:
        openai_api_key (SecretStr): Chave de API da OpenAI para acesso aos modelos GPT.
        langchain_api_key (SecretStr): Chave de API do LangChain para tracing e logging.
        langchain_tracing_v2 (bool): Habilita o tracing v2 do LangSmith. Padrão: True.
        langchain_endpoint (str): URL do endpoint do LangSmith. 
            Padrão: "https://api.smith.langchain.com".
        langchain_project (str): Nome do projeto no LangSmith. 
            Padrão: "roteiro-de-viagem".
        model_name (str): Nome do modelo de linguagem a ser usado. Padrão: "gpt-4o".
        temperature (float): Temperatura para geração de texto (0.0-2.0). Padrão: 0.3.
        max_tokens (int): Número máximo de tokens na resposta. Padrão: 1024.
    
    Note:
        As chaves de API são armazenadas como SecretStr para maior segurança.
        Use .get_secret_value() para acessar o valor real da chave.
    """
    
    openai_api_key: SecretStr
    langchain_api_key: SecretStr

    # Configurações do LangSmith
    langchain_tracing_v2: bool = True
    langchain_endpoint: str = "https://api.smith.langchain.com"
    langchain_project: str = "roteiro-de-viagem"

    # Configurações do modelo
    model_name: str = "gpt-4.1"
    temperature: float = 0.3
    max_tokens: int = 1024

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "extra": "ignore"  # Ignora variáveis extras do .env
    }
    
    #* Validações opcionais
    @field_validator('temperature')
    @classmethod
    def validate_temperature(cls, v: float) -> float:
        """Valida se a temperatura está dentro do intervalo permitido.
        
        Args:
            v (float): Valor da temperatura a ser validado.
            
        Returns:
            float: Valor da temperatura validado.
            
        Raises:
            ValueError: Se a temperatura não estiver entre 0.0 e 2.0.
            
        Note:
            A temperatura controla a aleatoriedade das respostas do modelo.
            Valores menores (próximos a 0) geram respostas mais determinísticas,
            enquanto valores maiores (próximos a 2) geram respostas mais criativas.
        """
        if not 0 <= v <= 2:
            raise ValueError('Temperature deve estar entre 0 e 2')
        return v
    
    @field_validator('max_tokens')
    @classmethod
    def validate_max_tokens(cls, v: int) -> int:
        """Valida se max_tokens é um valor positivo.
        
        Args:
            v (int): Valor de max_tokens a ser validado.
            
        Returns:
            int: Valor de max_tokens validado.
            
        Raises:
            ValueError: Se max_tokens for menor ou igual a zero.
            
        Note:
            max_tokens define o limite máximo de tokens que o modelo pode gerar
            em uma única resposta. Um token é aproximadamente uma palavra ou
            parte de uma palavra.
        """
        
        if v <= 0:
            raise ValueError('max_tokens deve ser positivo')
        return v

# Instância global das configurações
settings = Settings() # type: ignore



if __name__ == "__main__":
    try:
        test_settings = Settings() # type: ignore
        print("✅ Configurações carregadas com sucesso!")
        print(f"Modelo: {test_settings.model_name}")
        print(f"Temperature: {test_settings.temperature}")
        print(f"Max tokens: {test_settings.max_tokens}")
        print(f"Projeto LangChain: {test_settings.langchain_project}")
        print(f"Tracing habilitado: {test_settings.langchain_tracing_v2}")
        # Não imprime as chaves por segurança
    except Exception as e:
        print(f"❌ Erro ao carregar configurações: {e}")
        raise