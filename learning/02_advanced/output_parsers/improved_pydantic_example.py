"""🎯 TUTORIAL: LangChain + Pydantic - Structured Output
===================================================

Este exemplo demonstra como usar Pydantic com LangChain para:
1. Validar dados de entrada e saída
2. Garantir formato estruturado das respostas
3. Tornar o código mais robusto e type-safe

"""

import json
from datetime import datetime

from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field


# 📋 MODELO PYDANTIC MELHORADO
class AnswerWithJustification(BaseModel):
    """Modelo que representa uma resposta estruturada com justificativa.

    💡 Por que usar Pydantic aqui?
    - Validação automática de tipos
    - Documentação clara dos campos
    - Serialização JSON automática
    - Integração nativa com LangChain
    """

    answer: str = Field(
        description="Resposta clara e concisa para a pergunta",
        min_length=1,
        max_length=500,
    )

    justification: str = Field(
        description="Explicação detalhada do raciocínio", min_length=10, max_length=1000
    )

    confidence_level: float | None = Field(
        default=None, description="Nível de confiança (0-1) na resposta", ge=0.0, le=1.0
    )

    timestamp: str | None = Field(
        default_factory=lambda: datetime.now().isoformat(),
        description="Timestamp da resposta",
    )

    def display_response(self) -> str:
        """Método para exibir a resposta de forma mais legível.

        🔧 BENEFÍCIO: Evita o scroll infinito no output!
        """
        output = f"""
┌─ 💬 RESPOSTA ─────────────────────────────────────────┐
│ {self.answer}
├─ 🤔 JUSTIFICATIVA ───────────────────────────────────┤
│ {self.justification}
"""

        if self.confidence_level:
            confidence_bar = "█" * int(self.confidence_level * 10)
            output += f"""├─ 📊 CONFIANÇA ───────────────────────────────────────┤
│ {confidence_bar} {self.confidence_level:.1%}
"""

        output += f"""└─ 🕒 {self.timestamp} ──────────────────────────────────┘"""
        return output


# 🚀 CLASSE PRINCIPAL PARA DEMONSTRAÇÃO
class LangChainPydanticDemo:
    """Demonstra o uso de Pydantic com LangChain de forma didática.

    📚 CONCEITOS IMPORTANTES:

    1. **Structured Output**: LangChain força o LLM a retornar dados
       no formato exato do modelo Pydantic

    2. **Type Safety**: Pydantic valida automaticamente os tipos

    3. **Error Handling**: Falhas de validação são capturadas
    """

    def __init__(self, model_name: str = "gpt-3.5-turbo"):
        self.model = ChatOpenAI(
            model=model_name,
            temperature=0.1,  # Baixa criatividade para respostas consistentes
        )

        # 🔑 PONTO CHAVE: with_structured_output() força o formato
        self.structured_model = self.model.with_structured_output(
            AnswerWithJustification
        )

    def ask_question(self, question: str) -> AnswerWithJustification:
        """Faz uma pergunta e retorna resposta estruturada.

        🎯 BENEFÍCIOS do Structured Output:
        - Resposta sempre no formato esperado
        - Validação automática dos dados
        - Facilita integração com APIs e bancos de dados
        """
        try:
            response = self.structured_model.invoke(question)
            return response

        except Exception as e:
            # Em caso de erro, retorna resposta padrão
            return AnswerWithJustification(
                answer="Erro ao processar pergunta",
                justification=f"Erro técnico: {e!s}",
                confidence_level=0.0,
            )

    def demo_multiple_questions(self):
        """Demonstra o uso com múltiplas perguntas para mostrar consistência.
        """
        questions = [
            "O que pesa mais: 1kg de chumbo ou 1kg de algodão?",
            "Por que o céu é azul?",
            "Qual a diferença entre Python e JavaScript?",
        ]

        print("🎓 DEMONSTRAÇÃO: Múltiplas perguntas com formato consistente\n")

        for i, question in enumerate(questions, 1):
            print(f"❓ PERGUNTA {i}: {question}")
            response = self.ask_question(question)
            print(response.display_response())
            print("\n" + "=" * 60 + "\n")


# 📖 EXEMPLOS PRÁTICOS DE USO
def exemplo_basico():
    """Exemplo básico de uso do structured output."""
    print("🔵 EXEMPLO 1: Uso Básico")
    print("-" * 40)

    demo = LangChainPydanticDemo()

    question = "Explique o conceito de recursão em programação"
    response = demo.ask_question(question)

    # ✨ SAÍDA LIMPA - sem scroll infinito!
    print(response.display_response())

    # 💾 BONUS: Fácil conversão para JSON
    print("\n🔧 BONUS - Dados em JSON:")
    print(json.dumps(response.model_dump(), indent=2, ensure_ascii=False))


def exemplo_avancado():
    """Exemplo avançado mostrando validação."""
    print("\n🟢 EXEMPLO 2: Validação com Pydantic")
    print("-" * 40)

    # Tentativa de criar resposta inválida (para mostrar validação)
    try:
        invalid_response = AnswerWithJustification(
            answer="",  # ❌ Inválido: muito curto
            justification="Curto",  # ❌ Inválido: muito curto
            confidence_level=1.5,  # ❌ Inválido: > 1.0
        )
    except Exception as e:
        print(f"❌ VALIDAÇÃO PYDANTIC FUNCIONOU: {e}")

    # ✅ Resposta válida
    valid_response = AnswerWithJustification(
        answer="Python é uma linguagem de programação",
        justification="Python é conhecida por sua sintaxe simples e legível",
        confidence_level=0.9,
    )

    print("\n✅ RESPOSTA VÁLIDA:")
    print(valid_response.display_response())


if __name__ == "__main__":
    print("🎯 TUTORIAL COMPLETO: LangChain + Pydantic\n")

    # Executa exemplos
    exemplo_basico()
    exemplo_avancado()

    # Demonstração completa
    print("\n🎓 DEMONSTRAÇÃO COMPLETA:")
    print("=" * 60)
    demo = LangChainPydanticDemo()
    demo.demo_multiple_questions()

    print("""
🎓 LIÇÕES APRENDIDAS:

1. **Pydantic + LangChain = Dados Estruturados**
   - LLM retorna sempre no formato correto
   - Validação automática de tipos e valores

2. **Benefícios para Produção**
   - Code completion no IDE
   - Documentação automática
   - Integração fácil com APIs

3. **Melhor UX**
   - Saída formatada e legível
   - Sem scroll infinito
   - Informações organizadas

4. **Type Safety**
   - Erros capturados em desenvolvimento
   - Código mais robusto
   - Manutenção facilitada
    """)
