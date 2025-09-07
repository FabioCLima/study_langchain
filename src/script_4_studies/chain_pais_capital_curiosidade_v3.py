"""Script LangChain: Informações de Países com LangSmith Tracing
===========================================================

Este script demonstra como criar uma pipeline no LangChain com monitoramento
via LangSmith para melhor debugging e entendimento das chains.

Funcionalidades demonstradas:
- Pydantic Settings para configuração
- LangSmith para tracing e debugging
- Structured Output para dados tipados
- Chain composition com RunnablePassthrough
- Tratamento de erros e logging
"""

import os

from dotenv import find_dotenv, load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field, SecretStr, ValidationError
from pydantic_settings import BaseSettings

# LangSmith imports para tracing
# LangSmith imports (com tratamento de erro se não estiver instalado)
try:
    import langchain
    from langchain_core.tracers.langchain import LangChainTracer
    from langsmith import Client
    LANGSMITH_AVAILABLE = True
except ImportError:
    # Define uma classe dummy se LangSmith não estiver disponível
    class Client:
        def __init__(self, *args, **kwargs):
            pass
    LANGSMITH_AVAILABLE = False


# ============================================================
# 1. CONFIGURAÇÕES COM LANGSMITH
# ============================================================
class AppSettings(BaseSettings):
    """Configurações da aplicação com suporte ao LangSmith.
    
    O LangSmith oferece:
    - Tracing detalhado de chains
    - Debugging visual
    - Métricas de performance
    - Comparação de execuções
    """

    # Chaves de API obrigatórias
    openai_api_key: SecretStr = Field(
        ...,
        description="Chave da API OpenAI"
    )

    # LangSmith - opcional mas recomendado
    langsmith_api_key: SecretStr | None = Field(
        default=None,
        description="Chave da API LangSmith (opcional)"
    )

    # Configurações do LangSmith
    langsmith_tracing: bool = Field(
        default=False,
        description="Habilitar tracing do LangSmith"
    )

    langsmith_project: str = Field(
        default="country-info-pipeline",
        description="Nome do projeto no LangSmith"
    )

    langsmith_endpoint: str = Field(
        default="https://api.smith.langchain.com",
        description="Endpoint do LangSmith"
    )

    # Configurações do modelo
    model_name: str = Field(
        default="gpt-4o-mini",
        description="Nome do modelo OpenAI"
    )

    temperature_structured: float = Field(
        default=0.1,
        description="Temperature para outputs estruturados"
    )

    temperature_creative: float = Field(
        default=0.7,
        description="Temperature para conteúdo criativo"
    )

    class Config:
        env_file = find_dotenv()
        env_file_encoding = "utf-8"


def setup_langsmith(settings: AppSettings) -> Client | None:
    """Configura o LangSmith para tracing.
    
    Args:
        settings: Configurações da aplicação
        
    Returns:
        Client do LangSmith se configurado, None caso contrário

    """
    if not LANGSMITH_AVAILABLE:
        print("⚠️  LangSmith não está instalado. Instale com: pip install langsmith")
        return None

    if not settings.langsmith_tracing or not settings.langsmith_api_key:
        print("ℹ️  LangSmith tracing desabilitado")
        return None

    try:
        # Configura variáveis de ambiente para LangSmith
        os.environ["LANGCHAIN_TRACING_V2"] = "true"
        os.environ["LANGCHAIN_API_KEY"] = settings.langsmith_api_key.get_secret_value()
        os.environ["LANGCHAIN_PROJECT"] = settings.langsmith_project
        os.environ["LANGCHAIN_ENDPOINT"] = settings.langsmith_endpoint

        # Habilita tracing global (só se langchain estiver disponível)
        if "langchain" in globals():
            langchain.debug = True

        # Cria client do LangSmith
        client = Client(
            api_key=settings.langsmith_api_key.get_secret_value(),
            api_url=settings.langsmith_endpoint
        )

        print("✅ LangSmith configurado!")
        print(f"📊 Projeto: {settings.langsmith_project}")
        print("🔗 Dashboard: https://smith.langchain.com/")

        return client

    except Exception as e:
        print(f"⚠️  Erro ao configurar LangSmith: {e}")
        print("ℹ️  Continuando sem tracing...")
        return None


def load_settings() -> AppSettings:
    """Carrega e valida as configurações.
    
    Returns:
        AppSettings: Configurações validadas
        
    Raises:
        ValidationError: Se alguma configuração obrigatória estiver faltando

    """
    try:
        load_dotenv(find_dotenv())
        return AppSettings()
    except ValidationError as e:
        print(f"❌ Erro nas configurações: {e}")
        print("💡 Certifique-se de ter um arquivo .env com pelo menos OPENAI_API_KEY")
        raise


# ============================================================
# 2. MODELOS DE DADOS
# ============================================================
class CountryInfo(BaseModel):
    """Modelo para informações estruturadas de um país."""

    nome: str = Field(description="Nome oficial do país")
    capital: str = Field(description="Capital do país")

    def __str__(self) -> str:
        return f"{self.nome} - Capital: {self.capital}"


# ============================================================
# 3. CONFIGURAÇÃO DOS MODELOS
# ============================================================
def create_structured_model(settings: AppSettings) -> ChatOpenAI:
    """Cria modelo para outputs estruturados.
    
    Com LangSmith, você poderá ver:
    - Tempo de resposta do modelo
    - Tokens utilizados
    - Custo da operação
    - Prompt exato enviado
    """
    return ChatOpenAI(
        api_key=settings.openai_api_key.get_secret_value(),
        model=settings.model_name,
        temperature=settings.temperature_structured,
        # Adiciona metadados para melhor tracing
        model_kwargs={"metadata": {"component": "structured_output"}}
    ).with_structured_output(CountryInfo)


def create_creative_model(settings: AppSettings) -> ChatOpenAI:
    """Cria modelo para conteúdo criativo.
    
    Com LangSmith, você poderá comparar:
    - Performance entre diferentes temperatures
    - Qualidade das respostas criativas
    - Variabilidade dos outputs
    """
    return ChatOpenAI(
        api_key=settings.openai_api_key.get_secret_value(),
        model=settings.model_name,
        temperature=settings.temperature_creative,
        # Metadados para tracking
        model_kwargs={"metadata": {"component": "creative_content"}}
    )


# ============================================================
# 4. CHAINS COM TRACING MELHORADO
# ============================================================
def create_country_chain(model: ChatOpenAI):
    """Chain para obter informações do país.
    
    O LangSmith mostrará:
    - Input: nome do país
    - Prompt completo enviado ao modelo
    - Resposta estruturada do modelo
    - Tempo de execução
    """
    prompt = ChatPromptTemplate.from_messages([
        ("system",
         "Você é um especialista em geografia mundial. "
         "Forneça informações precisas sobre países. "
         "Responda SEMPRE com o nome oficial do país e sua capital."),
        ("user", "Qual é a capital de {pais}?")
    ])

    # Adiciona nome para melhor identificação no tracing
    chain = prompt | model
    chain.name = "CountryInfoChain"

    return chain


def create_curiosity_chain(model: ChatOpenAI):
    """Chain para curiosidades sobre cidades.
    
    No LangSmith você verá:
    - Como a capital foi extraída da chain anterior
    - Prompt específico para curiosidades
    - Criatividade da resposta (temperature 0.7)
    """
    prompt = ChatPromptTemplate.from_messages([
        ("system",
         "Você é um guia turístico especializado mundial. "
         "Conte curiosidades interessantes, verídicas e pouco conhecidas sobre cidades. "
         "Seja específico e envolvente na sua resposta."),
        ("user", "Conte uma curiosidade fascinante sobre {cidade}")
    ])

    chain = prompt | model
    chain.name = "CuriosityChain"

    return chain


# ============================================================
# 5. PIPELINE COM TRACING DETALHADO
# ============================================================
def create_main_pipeline(settings: AppSettings, langsmith_client: Client | None = None):
    """Cria a pipeline principal com tracing detalhado.
    
    Com LangSmith habilitado, você verá:
    1. Input inicial: {'pais': 'Nome do País'}
    2. Execução da CountryInfoChain
    3. Extração da capital
    4. Execução da CuriosityChain
    5. Formatação final
    6. Tempo total e custos
    """
    # Criar modelos
    structured_model = create_structured_model(settings)
    creative_model = create_creative_model(settings)

    # Criar chains individuais
    country_chain = create_country_chain(structured_model)
    curiosity_chain = create_curiosity_chain(creative_model)

    # Função para extrair capital (com melhor tracing)
    def extract_capital(data: dict) -> dict:
        """Extrai a capital do CountryInfo.
        
        No LangSmith você verá exatamente:
        - Input: objeto CountryInfo completo
        - Output: {'cidade': 'Nome da Capital'}
        """
        capital = data["country_info"].capital
        print(f"🔄 Extraindo capital: {capital}")
        return {"cidade": capital}

    # Sub-chain com nome para tracking
    capital_extractor = RunnableLambda(extract_capital)
    capital_extractor.name = "CapitalExtractor"

    capital_to_curiosity = capital_extractor | curiosity_chain
    capital_to_curiosity.name = "CapitalToCuriosity"

    # Função de formatação com logging
    def format_result(data: dict) -> str:
        """Formata resultado final com logging para debug.
        """
        country = data["country_info"]
        curiosity = data["curiosity"]

        print(f"📊 Formatando resultado para: {country.nome}")

        result = f"""
🌍 INFORMAÇÕES DO PAÍS
{'=' * 50}
📍 País: {country.nome}
🏛️  Capital: {country.capital}

✨ CURIOSIDADE SOBRE {country.capital.upper()}
{'=' * 50}
{curiosity.content}

🔍 Para ver o tracing detalhado desta execução,
   acesse: https://smith.langchain.com/
        """.strip()

        return result

    formatter = RunnableLambda(format_result)
    formatter.name = "ResultFormatter"

    # Pipeline completa com nomes para melhor tracing
    pipeline = (
        RunnablePassthrough.assign(country_info=country_chain)
        | RunnablePassthrough.assign(curiosity=capital_to_curiosity)
        | formatter
    )

    # Nome da pipeline principal
    pipeline.name = "CountryInfoPipeline"

    return pipeline


# ============================================================
# 6. FUNÇÃO PRINCIPAL COM TRACING
# ============================================================
def consultar_pais(
    nome_pais: str,
    settings: AppSettings | None = None,
    enable_tracing: bool = True
) -> str:
    """Consulta informações de um país com tracing opcional.
    
    Args:
        nome_pais: Nome do país
        settings: Configurações (carrega automaticamente se None)
        enable_tracing: Se deve tentar usar LangSmith
        
    Returns:
        str: Informações formatadas

    """
    try:
        # Carrega configurações
        if settings is None:
            settings = load_settings()

        # Configura LangSmith se habilitado
        langsmith_client = None
        if enable_tracing and settings.langsmith_tracing:
            langsmith_client = setup_langsmith(settings)

        # Cria e executa pipeline
        pipeline = create_main_pipeline(settings, langsmith_client)

        # Execução com contexto de tracing
        print(f"🚀 Executando pipeline para: {nome_pais}")
        if langsmith_client:
            print("📊 Tracing habilitado - verifique o LangSmith dashboard")

        resultado = pipeline.invoke({"pais": nome_pais})

        return resultado

    except Exception as e:
        error_msg = f"❌ Erro ao consultar '{nome_pais}': {e!s}"
        print(error_msg)
        return error_msg


# ============================================================
# 7. FUNÇÕES DE ANÁLISE DO LANGSMITH
# ============================================================
def analisar_execucoes(settings: AppSettings, project_name: str | None = None):
    """Analisa execuções no LangSmith (requer configuração).
    
    Esta função demonstra como você pode usar o LangSmith client
    para analisar runs anteriores e obter insights.
    """
    if not LANGSMITH_AVAILABLE:
        print("⚠️  LangSmith não está disponível. Instale com: pip install langsmith")
        return

    if not settings.langsmith_api_key:
        print("⚠️  LangSmith API key não configurada")
        return

    try:
        client = Client(
            api_key=settings.langsmith_api_key.get_secret_value(),
            api_url=settings.langsmith_endpoint
        )

        project = project_name or settings.langsmith_project

        # Busca runs recentes
        runs = list(client.list_runs(project_name=project, limit=5))

        print(f"\n📊 ANÁLISE - Últimas 5 execuções do projeto '{project}':")
        print("=" * 60)

        for i, run in enumerate(runs, 1):
            status = "✅" if not run.error else "❌"
            duration = f"{run.total_time:.2f}s" if run.total_time else "N/A"

            print(f"{i}. {status} {run.name}")
            print(f"   ⏱️  Duração: {duration}")
            print(f"   🆔 ID: {run.id}")
            if run.error:
                print(f"   ❌ Erro: {run.error}")
            print()

    except Exception as e:
        print(f"❌ Erro ao analisar execuções: {e}")


# ============================================================
# 8. EXEMPLO DE USO COM LANGSMITH
# ============================================================
def main():
    """Função principal demonstrando uso com LangSmith."""
    print("🚀 Iniciando aplicação LangChain com LangSmith")
    print("=" * 60)

    try:
        # Carrega configurações
        settings = load_settings()
        print("✅ Configurações carregadas!")

        # Mostra status das configurações
        api_key = settings.openai_api_key.get_secret_value()
        print(f"🔑 OpenAI API: {api_key[:8]}...{api_key[-4:]}")

        if settings.langsmith_api_key:
            ls_key = settings.langsmith_api_key.get_secret_value()
            print(f"📊 LangSmith API: {ls_key[:8]}...{ls_key[-4:]}")
            print(f"🎯 Projeto: {settings.langsmith_project}")
        else:
            print("ℹ️  LangSmith não configurado")

        print(f"🤖 Modelo: {settings.model_name}")
        print()

        # Exemplo de uso
        paises = ["Brasil", "Japão"]

        for pais in paises:
            print(f"🔍 Consultando: {pais}")
            print("-" * 40)

            resultado = consultar_pais(pais, settings)
            print(resultado)
            print("\n" + "=" * 60 + "\n")

        # Análise das execuções (se LangSmith configurado)
        if settings.langsmith_api_key:
            analisar_execucoes(settings)

    except Exception as e:
        print(f"❌ Erro na execução: {e}")
        return 1

    return 0


if __name__ == "__main__":
    exit_code = main()
    exit(exit_code)
