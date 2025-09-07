# langchain_azimov/agente_analista_review.py

import json
from pathlib import Path

from langchain.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from openai_client import ApiKeyLoader, ChatModelFactory
from pydantic import BaseModel, Field


# === MODELO DE SAÍDA PADRÃO (Pydantic) ===
class AnaliseDeReview(BaseModel):
    """Estrutura para extrair e analisar informações de uma review de cliente."""

    nome_produto: str | None = Field(
        description="O nome exato do produto mencionado na review, se houver."
    )
    satisfacao_entrega: bool = Field(
        description="Verdadeiro se o cliente parece satisfeito com a entrega, falso caso contrário."
    )
    comentarios_entrega: str | None = Field(
        description="Frase exata da review que comenta sobre a entrega."
    )
    satisfacao_produto: bool = Field(
        description="Verdadeiro se o cliente parece satisfeito com a qualidade do produto, falso caso contrário."
    )
    comentarios_produto: str | None = Field(
        description="Frase exata da review que comenta sobre a qualidade ou características do produto."
    )
    mencionou_atendimento: bool = Field(
        description="Verdadeiro se o cliente mencionou ter interagido com o atendimento ao cliente."
    )
    satisfacao_atendimento: bool | None = Field(
        description="Se o atendimento foi mencionado, indica se o cliente ficou satisfeito."
    )
    satisfacao_geral_nota: int | None = Field(
        description="Uma nota de satisfação geral de 1 a 10, se mencionada pelo cliente.",
        ge=1,
        le=10,
    )


# === PARSER E PROMPT CONFIGURADO ===
output_parser = PydanticOutputParser(pydantic_object=AnaliseDeReview)

prompt_template = ChatPromptTemplate.from_template(
    """Você é um analista de feedbacks de clientes.

Analise cuidadosamente a review abaixo e preencha todos os campos da estrutura de dados solicitada.

Review:
```{review}```

{format_instructions}
"""
)


# === CARREGANDO O MODELO LLM ===
def create_analytical_model() -> ChatOpenAI | None:
    try:
        env_file_path: Path = Path(__file__).resolve().parent / ".env"
        loader: ApiKeyLoader = ApiKeyLoader(Path(env_file_path))
        openai_api_key = loader.get_openai_key()
        print(f"Chave da API OpenAI carregada com sucesso: {openai_api_key[-4:]}")
        chat_factory = ChatModelFactory(openai_api_key)
        analytical_llm = chat_factory.create_analytical_model()
        print("Modelo de chat OpenAI criado com sucesso!")
        return analytical_llm
    except ValueError as e:
        print(f"Erro ao carregar a chave da API: {e}")
        return None


# === FUNÇÃO PRINCIPAL ===
def main() -> None:
    analytical_llm = create_analytical_model()
    if not analytical_llm:
        print("Erro: modelo não foi carregado.")
        return

    # Review de exemplo
    review_cliente = """Este soprador de folhas é bastante incrível. Ele tem
quatro configurações: sopro de vela, brisa suave, cidade ventosa
e tornado. Chegou em dois dias, bem a tempo para o presente de
aniversário da minha esposa. Acho que minha esposa gostou tanto
que ficou sem palavras. Até agora, fui o único a usá-lo, e tenho
usado em todas as manhãs alternadas para limpar as folhas do
nosso gramado. É um pouco mais caro do que os outros sopradores
de folhas disponíveis no mercado, mas acho que vale a pena pelas
características extras."""

    # Formatando a prompt dinamicamente com instruções do parser
    messages = prompt_template.format_messages(
        review=review_cliente,
        format_instructions=output_parser.get_format_instructions(),
    )

    # Enviando mensagem estruturada ao modelo
    response = analytical_llm.invoke(messages)

    # Parseando a resposta para o formato estruturado (objeto Pydantic)
    response_object = output_parser.parse(response.content)

    # Exibindo resultado formatado
    print("=== Análise da Review em formato JSON ===")
    print(json.dumps(response_object.model_dump(), indent=4, ensure_ascii=False))


if __name__ == "__main__":
    main()
