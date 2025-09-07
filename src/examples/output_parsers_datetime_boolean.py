#!/usr/bin/env python3
"""OutputParsers - Exemplos Práticos com Datetime e Boolean
========================================================

Este arquivo demonstra como usar OutputParsers no LangChain para trabalhar com:
- Datetime: extração e validação de datas
- Boolean: análise de sentimento e flags de status

Autor: Tutor LangChain
Data: 2024
"""

import os
from datetime import datetime

from dotenv import find_dotenv, load_dotenv
from langchain.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field, validator

# Carrega variáveis de ambiente
_ = load_dotenv(find_dotenv())

if not os.getenv("OPENAI_API_KEY"):
    raise ValueError("OPENAI_API_KEY não encontrada no arquivo .env")


class EventInfo(BaseModel):
    """Informações de um evento com data e hora"""

    event_name: str = Field(description="Nome do evento")
    event_date: datetime = Field(description="Data e hora do evento")
    duration_hours: float | None = Field(default=None, description="Duração em horas")
    is_recurring: bool = Field(description="Se o evento é recorrente")

    def display_info(self) -> str:
        """Exibe informações formatadas do evento"""
        recurring_text = "(Recorrente)" if self.is_recurring else "(Único)"
        duration_text = f" - Duração: {self.duration_hours}h" if self.duration_hours else ""

        return f"📅 {self.event_name} {recurring_text}\n" \
               f"   📆 {self.event_date.strftime('%d/%m/%Y às %H:%M')}{duration_text}"


class SentimentAnalysis(BaseModel):
    """Análise de sentimento com valores booleanos"""

    text: str = Field(description="Texto analisado")
    is_positive: bool = Field(description="Se o sentimento é positivo")
    is_negative: bool = Field(description="Se o sentimento é negativo")
    is_neutral: bool = Field(description="Se o sentimento é neutro")
    contains_urgency: bool = Field(description="Se o texto contém urgência")
    confidence_score: float = Field(description="Nível de confiança (0-1)", ge=0.0, le=1.0)

    def get_sentiment_label(self) -> str:
        """Retorna o label do sentimento predominante"""
        if self.is_positive:
            return "😊 POSITIVO"
        if self.is_negative:
            return "😞 NEGATIVO"
        return "😐 NEUTRO"

    def display_analysis(self) -> str:
        """Exibe análise formatada"""
        urgency_icon = "🚨" if self.contains_urgency else "⏰"
        confidence_bar = "█" * int(self.confidence_score * 10)

        return f"📝 TEXTO: {self.text}\n" \
               f"{self.get_sentiment_label()}\n" \
               f"{urgency_icon} Urgência: {'Sim' if self.contains_urgency else 'Não'}\n" \
               f"📊 Confiança: {confidence_bar} {self.confidence_score:.1%}"


class AppointmentAnalysis(BaseModel):
    """Análise de compromissos com datetime e boolean"""

    appointment_date: datetime = Field(description="Data e hora do compromisso")
    is_urgent: bool = Field(description="Se o compromisso é urgente")
    is_important: bool = Field(description="Se o compromisso é importante")
    requires_preparation: bool = Field(description="Se requer preparação prévia")
    is_online: bool = Field(description="Se é uma reunião online")
    duration_minutes: int | None = Field(default=None, description="Duração em minutos")

    def get_priority_level(self) -> str:
        """Determina o nível de prioridade"""
        if self.is_urgent and self.is_important:
            return "🔴 ALTA PRIORIDADE"
        if self.is_important:
            return "🟡 MÉDIA PRIORIDADE"
        return "🟢 BAIXA PRIORIDADE"

    def display_appointment(self) -> str:
        """Exibe informações do compromisso"""
        online_icon = "💻" if self.is_online else "🏢"
        prep_icon = "📋" if self.requires_preparation else "✅"
        duration_text = f" ({self.duration_minutes}min)" if self.duration_minutes else ""

        return f"{self.get_priority_level()}\n" \
               f"📅 {self.appointment_date.strftime('%d/%m/%Y às %H:%M')}{duration_text}\n" \
               f"{online_icon} {'Online' if self.is_online else 'Presencial'}\n" \
               f"{prep_icon} {'Requer preparação' if self.requires_preparation else 'Sem preparação'}"


class ValidatedTask(BaseModel):
    """Tarefa com validação de data e boolean"""

    task_name: str = Field(description="Nome da tarefa")
    due_date: datetime = Field(description="Data de vencimento")
    is_completed: bool = Field(description="Se a tarefa está completa")
    is_high_priority: bool = Field(description="Se é alta prioridade")

    @validator("due_date")
    def validate_future_date(cls, v):
        """Valida se a data está no futuro"""
        if v < datetime.now():
            raise ValueError("Data deve estar no futuro")
        return v

    @validator("is_completed")
    def validate_completion_logic(cls, v, values):
        """Valida lógica de conclusão"""
        if "due_date" in values:
            due_date = values["due_date"]
            if v and due_date > datetime.now():
                print("⚠️  Aviso: Tarefa marcada como completa antes da data de vencimento")
        return v

    def get_status_icon(self) -> str:
        """Retorna ícone baseado no status"""
        if self.is_completed:
            return "✅"
        if self.is_high_priority:
            return "🔴"
        return "🟡"

    def display_task(self) -> str:
        """Exibe informações da tarefa"""
        days_until_due = (self.due_date - datetime.now()).days
        status_text = "Concluída" if self.is_completed else f"Pendente ({days_until_due} dias)"
        priority_text = "Alta Prioridade" if self.is_high_priority else "Prioridade Normal"

        return f"{self.get_status_icon()} {self.task_name}\n" \
               f"📅 Vencimento: {self.due_date.strftime('%d/%m/%Y às %H:%M')}\n" \
               f"📊 Status: {status_text}\n" \
               f"🎯 {priority_text}"


class OutputParserExamples:
    """Classe principal para demonstrar OutputParsers"""

    def __init__(self, model_name="gpt-4.1"):
        self.llm = ChatOpenAI(model=model_name, temperature=0)

        # Configuração dos parsers
        self.event_parser = PydanticOutputParser(pydantic_object=EventInfo)
        self.sentiment_parser = PydanticOutputParser(pydantic_object=SentimentAnalysis)
        self.appointment_parser = PydanticOutputParser(pydantic_object=AppointmentAnalysis)
        self.task_parser = PydanticOutputParser(pydantic_object=ValidatedTask)

        # Configuração dos templates
        self.event_template = ChatPromptTemplate.from_messages([
            ("system", "Você é um assistente especializado em extrair informações de eventos e datas."),
            ("human", "Extraia as informações do evento do seguinte texto:\n{format_instructions}\n\nTexto: {text}")
        ])

        self.sentiment_template = ChatPromptTemplate.from_messages([
            ("system", "Você é um especialista em análise de sentimento. Analise o texto fornecido."),
            ("human", "Analise o sentimento do seguinte texto:\n{format_instructions}\n\nTexto: {text}")
        ])

        self.appointment_template = ChatPromptTemplate.from_messages([
            ("system", "Você é um assistente especializado em análise de compromissos e agenda."),
            ("human", "Analise o seguinte compromisso:\n{format_instructions}\n\nTexto: {text}")
        ])

        self.task_template = ChatPromptTemplate.from_messages([
            ("system", "Você é um assistente de gerenciamento de tarefas. Analise as informações fornecidas."),
            ("human", "Analise a seguinte tarefa:\n{format_instructions}\n\nTexto: {text}")
        ])

        # Configuração das chains
        self.event_chain = self.event_template | self.llm | self.event_parser
        self.sentiment_chain = self.sentiment_template | self.llm | self.sentiment_parser
        self.appointment_chain = self.appointment_template | self.llm | self.appointment_parser
        self.task_chain = self.task_template | self.llm | self.task_parser

    def demo_datetime_parser(self):
        """Demonstra parser com datetime"""
        print("🎯 EXEMPLO 1: OutputParser com Datetime")
        print("=" * 60)

        texts = [
            "Reunião de equipe amanhã às 14:30 por 2 horas",
            "Standup diário às 9h da manhã",
            "Apresentação do projeto na próxima sexta às 16h"
        ]

        for i, text in enumerate(texts, 1):
            try:
                event = self.event_chain.invoke({
                    "text": text,
                    "format_instructions": self.event_parser.get_format_instructions()
                })

                print(f"\n📋 Exemplo {i}:")
                print(f"Texto: {text}")
                print(event.display_info())
                print("-" * 40)

            except Exception as e:
                print(f"❌ Erro no exemplo {i}: {e}")

    def demo_boolean_parser(self):
        """Demonstra parser com boolean"""
        print("\n🎯 EXEMPLO 2: OutputParser com Boolean")
        print("=" * 60)

        texts = [
            "Adorei o produto! Funciona perfeitamente e superou minhas expectativas.",
            "Preciso de ajuda URGENTE! O sistema está quebrado e não consigo trabalhar!",
            "O serviço é adequado, mas poderia ser melhor."
        ]

        for i, text in enumerate(texts, 1):
            try:
                sentiment = self.sentiment_chain.invoke({
                    "text": text,
                    "format_instructions": self.sentiment_parser.get_format_instructions()
                })

                print(f"\n📋 Exemplo {i}:")
                print(sentiment.display_analysis())
                print("-" * 40)

            except Exception as e:
                print(f"❌ Erro no exemplo {i}: {e}")

    def demo_combined_parser(self):
        """Demonstra parser combinado (datetime + boolean)"""
        print("\n🎯 EXEMPLO 3: OutputParser Combinado (Datetime + Boolean)")
        print("=" * 60)

        texts = [
            "Reunião URGENTE com o cliente amanhã às 10h. É muito importante e preciso preparar a apresentação. Será online por 1 hora.",
            "Café com João na sexta-feira às 15h"
        ]

        for i, text in enumerate(texts, 1):
            try:
                appointment = self.appointment_chain.invoke({
                    "text": text,
                    "format_instructions": self.appointment_parser.get_format_instructions()
                })

                print(f"\n📋 Exemplo {i}:")
                print(f"Texto: {text}")
                print(appointment.display_appointment())
                print("-" * 40)

            except Exception as e:
                print(f"❌ Erro no exemplo {i}: {e}")

    def demo_validation_parser(self):
        """Demonstra parser com validação customizada"""
        print("\n🎯 EXEMPLO 4: OutputParser com Validação Customizada")
        print("=" * 60)

        texts = [
            "Relatório mensal - vencimento: 15/12/2024 às 18h - alta prioridade - não concluída",
            "Revisão de código - vencimento: 20/12/2024 às 14h - prioridade normal - concluída"
        ]

        for i, text in enumerate(texts, 1):
            try:
                task = self.task_chain.invoke({
                    "text": text,
                    "format_instructions": self.task_parser.get_format_instructions()
                })

                print(f"\n📋 Exemplo {i}:")
                print(f"Texto: {text}")
                print(task.display_task())
                print("-" * 40)

            except Exception as e:
                print(f"❌ Erro no exemplo {i}: {e}")

    def run_all_demos(self):
        """Executa todas as demonstrações"""
        print("🚀 OUTPUTPARSERS - EXEMPLOS PRÁTICOS")
        print("=" * 60)

        self.demo_datetime_parser()
        self.demo_boolean_parser()
        self.demo_combined_parser()
        self.demo_validation_parser()

        print("\n📚 RESUMO DOS CONCEITOS")
        print("=" * 60)
        print("""
🎯 OutputParsers com Datetime:
- Extração de datas de textos
- Validação temporal (futuro/passado)
- Formatação personalizada

🎯 OutputParsers com Boolean:
- Análise de sentimento
- Flags de status (urgência, importância)
- Validação lógica

🎯 Benefícios:
- Type Safety com Pydantic
- Estruturação consistente
- Fácil integração com APIs
- Código mais limpo e organizado
        """)


def main():
    """Função principal"""
    try:
        examples = OutputParserExamples()
        examples.run_all_demos()

    except Exception as e:
        print(f"❌ Erro na execução: {e}")


if __name__ == "__main__":
    main()
