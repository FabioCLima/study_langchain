"""Analisador de sentimento."""

import os
from typing import Any

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import Runnable

# --- Componentes LangChain ---
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field, SecretStr

# --- Ferramentas de Configuração e Tipagem ---
from pydantic_settings import BaseSettings, SettingsConfigDict


# * =============================================================================
# * 1. SETUP DE CONFIGURAÇÃO PROFISSIONAL (Usando Pydantic)
# * =============================================================================
class AppSettings(BaseSettings):
    """Carrega e valida as configurações da aplicação a partir de variáveis de
    ambiente.
    """

    OPENAI_API_KEY: SecretStr = Field(..., description="Chave da API da OpenAI")
    LANGCHAIN_TRACING_V2: str = Field(
        "false",
        description="Habilita o tracing com LangSmith",
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


# * =============================================================================
# * 2. DEFINIÇÃO DO MODELO DE SAÍDA (Pydantic)
# * =============================================================================
class AnaliseTexto(BaseModel):
    """Modelo para análise estruturada de texto."""

    sentimento: str = Field(description="Sentimento: positivo, negativo ou neutro")
    confianca: float = Field(description="Nível de confiança de 0 a 1", ge=0, le=1)
    palavras_chave: list[str] = Field(description="Lista de palavras-chave importantes")
    resumo: str = Field(description="Resumo do texto em uma única frase concisa")


# * =============================================================================
# * 3. LÓGICA DA CHAIN
# * =============================================================================
def criar_chain_de_analise(
    llm: ChatOpenAI,
) -> Runnable[dict[str, Any], AnaliseTexto]:
    """Cria e retorna uma chain LCEL para analisar o sentimento de um texto."""
    prompt_instrucao_analise_texto = ChatPromptTemplate(
        [
            (
                "system",
                (
                    "Você é um especialista em análise de sentimentos e "
                    "extração de informações de texto."
                ),
            ),
            (
                "user",
                (
                    "Analise o seguinte texto e retorne os dados no formato "
                    "solicitado: {texto}"
                ),
            ),
        ]
    )

    # Usar with_structured_output diretamente
    llm_estruturado: Runnable[Any, AnaliseTexto] = llm.with_structured_output(
        AnaliseTexto
    )  # type: ignore

    return prompt_instrucao_analise_texto | llm_estruturado  # type: ignore[call-arg]


def main() -> None:
    """Ponto de entrada principal do script."""
    print("🚀 Iniciando análise de texto...")

    try:
        settings = AppSettings()  # type: ignore[call-arg]
        os.environ["LANGCHAIN_TRACING_V2"] = settings.LANGCHAIN_TRACING_V2
    except ValueError as e:
        print(f"❌ Erro de Configuração: {e}")
        print(
            "Certifique-se de que seu arquivo .env existe no mesmo diretório "
            "e contém a 'OPENAI_API_KEY'."
        )
        return

    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.2,
        api_key=settings.OPENAI_API_KEY,  # Passar SecretStr diretamente
    )

    chain_de_analise = criar_chain_de_analise(llm)

    texto_para_analisar = (
        "Estou absolutamente encantado com este produto! A qualidade superou todas "
        "as minhas expectativas. O atendimento ao cliente foi excepcional, e a "
        "entrega foi mais rápida do que o prometido. Recomendo fortemente para "
        "qualquer pessoa que esteja considerando esta compra. Definitivamente "
        "comprarei novamente!"
    )

    print(f"\n📝 Texto a ser analisado:\n---{texto_para_analisar[:100].strip()}...\n")

    resultado = chain_de_analise.invoke({"texto": texto_para_analisar})

    print("=" * 20 + " ANÁLISE COMPLETA " + "=" * 20)
    print(f"🎯 Sentimento: {resultado.sentimento.upper()}")
    print(f"📊 Confiança: {resultado.confianca:.2%}")
    print(f"🏷️  Palavras-chave: {', '.join(resultado.palavras_chave)}")
    print(f"📋 Resumo: {resultado.resumo}")
    print("=" * 59)


if __name__ == "__main__":
    main()
