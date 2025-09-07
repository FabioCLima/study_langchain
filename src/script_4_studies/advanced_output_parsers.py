#!/usr/bin/env python3
"""OutputParsers Avançados - Exemplos com LangChain Real
======================================================

Este arquivo demonstra como usar OutputParsers com LangChain real,
incluindo tratamento de erros e validação customizada.

Autor: Tutor LangChain
Data: 2024
"""

from datetime import datetime, timedelta

# Verifica se as dependências estão disponíveis
try:
    from langchain.output_parsers import PydanticOutputParser
    from langchain_core.output_parsers import StrOutputParser
    from langchain_core.prompts import ChatPromptTemplate
    from langchain_openai import ChatOpenAI
    from pydantic import BaseModel, Field, validator
    LANGCHAIN_AVAILABLE = True
except ImportError:
    print("⚠️  LangChain não disponível. Executando em modo simulado.")
    LANGCHAIN_AVAILABLE = False
    # Fallback para dataclasses quando Pydantic não está disponível
    from dataclasses import dataclass as BaseModel
    def Field(*args, **kwargs): return None
    def validator(*args, **kwargs): return lambda x: x


# Modelos Pydantic para OutputParsers
class EventInfo(BaseModel):
    """Informações de um evento com data e hora"""

    event_name: str = Field(description="Nome do evento")
    event_date: datetime = Field(description="Data e hora do evento")
    duration_hours: float | None = Field(default=None, description="Duração em horas")
    is_recurring: bool = Field(description="Se o evento é recorrente")

    @validator("event_date")
    def validate_future_date(cls, v):
        """Valida se a data está no futuro"""
        if v < datetime.now():
            raise ValueError("Data do evento deve estar no futuro")
        return v

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

    @validator("confidence_score")
    def validate_confidence(cls, v):
        """Valida score de confiança"""
        if not 0.0 <= v <= 1.0:
            raise ValueError("Confiança deve estar entre 0 e 1")
        return v

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

    @validator("appointment_date")
    def validate_appointment_date(cls, v):
        """Valida data do compromisso"""
        if v < datetime.now():
            raise ValueError("Compromisso deve estar no futuro")
        return v

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


class TaskInfo(BaseModel):
    """Informações de tarefa com validação complexa"""

    task_name: str = Field(description="Nome da tarefa", min_length=1)
    due_date: datetime = Field(description="Data de vencimento")
    is_completed: bool = Field(description="Se a tarefa está completa")
    is_high_priority: bool = Field(description="Se é alta prioridade")
    estimated_hours: float | None = Field(default=None, description="Horas estimadas", ge=0.0)

    @validator("due_date")
    def validate_future_date(cls, v):
        """Valida se a data está no futuro"""
        if v < datetime.now():
            raise ValueError("Data de vencimento deve estar no futuro")
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
        hours_text = f" - Estimativa: {self.estimated_hours}h" if self.estimated_hours else ""

        return f"{self.get_status_icon()} {self.task_name}{hours_text}\n" \
               f"📅 Vencimento: {self.due_date.strftime('%d/%m/%Y às %H:%M')}\n" \
               f"📊 Status: {status_text}\n" \
               f"🎯 {priority_text}"


class AdvancedOutputParser:
    """Classe avançada para demonstrar OutputParsers com LangChain"""

    def __init__(self, use_langchain=True):
        self.use_langchain = use_langchain and LANGCHAIN_AVAILABLE

        if self.use_langchain:
            # Configuração do LangChain
            self.llm = ChatOpenAI(model="gpt-4.1", temperature=0)

            # Parsers
            self.event_parser = PydanticOutputParser(pydantic_object=EventInfo)
            self.sentiment_parser = PydanticOutputParser(pydantic_object=SentimentAnalysis)
            self.appointment_parser = PydanticOutputParser(pydantic_object=AppointmentAnalysis)
            self.task_parser = PydanticOutputParser(pydantic_object=TaskInfo)

            # Templates
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

            # Chains
            self.event_chain = self.event_template | self.llm | self.event_parser
            self.sentiment_chain = self.sentiment_template | self.llm | self.sentiment_parser
            self.appointment_chain = self.appointment_template | self.llm | self.appointment_parser
            self.task_chain = self.task_template | self.llm | self.task_parser
        else:
            print("🔧 Executando em modo simulado (sem LangChain)")

    def parse_event_safe(self, text: str) -> EventInfo | None:
        """Parse seguro de evento com tratamento de erro"""
        try:
            if self.use_langchain:
                return self.event_chain.invoke({
                    "text": text,
                    "format_instructions": self.event_parser.get_format_instructions()
                })
            # Simulação para demonstração
            return self._simulate_event_parse(text)
        except Exception as e:
            print(f"❌ Erro ao processar evento: {e}")
            return None

    def parse_sentiment_safe(self, text: str) -> SentimentAnalysis | None:
        """Parse seguro de sentimento com tratamento de erro"""
        try:
            if self.use_langchain:
                return self.sentiment_chain.invoke({
                    "text": text,
                    "format_instructions": self.sentiment_parser.get_format_instructions()
                })
            # Simulação para demonstração
            return self._simulate_sentiment_parse(text)
        except Exception as e:
            print(f"❌ Erro ao processar sentimento: {e}")
            return None

    def parse_appointment_safe(self, text: str) -> AppointmentAnalysis | None:
        """Parse seguro de compromisso com tratamento de erro"""
        try:
            if self.use_langchain:
                return self.appointment_chain.invoke({
                    "text": text,
                    "format_instructions": self.appointment_parser.get_format_instructions()
                })
            # Simulação para demonstração
            return self._simulate_appointment_parse(text)
        except Exception as e:
            print(f"❌ Erro ao processar compromisso: {e}")
            return None

    def parse_task_safe(self, text: str) -> TaskInfo | None:
        """Parse seguro de tarefa com tratamento de erro"""
        try:
            if self.use_langchain:
                return self.task_chain.invoke({
                    "text": text,
                    "format_instructions": self.task_parser.get_format_instructions()
                })
            # Simulação para demonstração
            return self._simulate_task_parse(text)
        except Exception as e:
            print(f"❌ Erro ao processar tarefa: {e}")
            return None

    def _simulate_event_parse(self, text: str) -> EventInfo:
        """Simula parsing de evento"""
        tomorrow = datetime.now() + timedelta(days=1)

        if "reunião" in text.lower():
            return EventInfo(
                event_name="Reunião de Equipe",
                event_date=tomorrow.replace(hour=14, minute=30),
                duration_hours=2.0,
                is_recurring=False
            )
        return EventInfo(
            event_name="Evento Padrão",
            event_date=tomorrow.replace(hour=10, minute=0),
            duration_hours=1.0,
            is_recurring=False
        )

    def _simulate_sentiment_parse(self, text: str) -> SentimentAnalysis:
        """Simula parsing de sentimento"""
        is_positive = any(word in text.lower() for word in ["adorei", "perfeito", "excelente"])
        is_negative = any(word in text.lower() for word in ["quebrado", "urgente", "problema"])
        is_neutral = not (is_positive or is_negative)
        contains_urgency = "urgente" in text.lower()

        return SentimentAnalysis(
            text=text,
            is_positive=is_positive,
            is_negative=is_negative,
            is_neutral=is_neutral,
            contains_urgency=contains_urgency,
            confidence_score=0.8
        )

    def _simulate_appointment_parse(self, text: str) -> AppointmentAnalysis:
        """Simula parsing de compromisso"""
        tomorrow = datetime.now() + timedelta(days=1)

        return AppointmentAnalysis(
            appointment_date=tomorrow.replace(hour=10, minute=0),
            is_urgent="urgente" in text.lower(),
            is_important="importante" in text.lower(),
            requires_preparation="preparar" in text.lower(),
            is_online="online" in text.lower(),
            duration_minutes=60
        )

    def _simulate_task_parse(self, text: str) -> TaskInfo:
        """Simula parsing de tarefa"""
        tomorrow = datetime.now() + timedelta(days=1)

        return TaskInfo(
            task_name="Tarefa Padrão",
            due_date=tomorrow.replace(hour=18, minute=0),
            is_completed=False,
            is_high_priority="alta prioridade" in text.lower(),
            estimated_hours=2.0
        )


def demo_advanced_parsers():
    """Demonstra parsers avançados com tratamento de erro"""
    print("🎯 EXEMPLO AVANÇADO: OutputParsers com Tratamento de Erro")
    print("=" * 60)

    parser = AdvancedOutputParser(use_langchain=False)  # Simulado para demonstração

    # Teste com diferentes tipos de entrada
    test_cases = [
        "Reunião de equipe amanhã às 14:30 por 2 horas",
        "Adorei o produto! Funciona perfeitamente.",
        "Reunião URGENTE com o cliente amanhã às 10h. É muito importante.",
        "Relatório mensal - vencimento: 15/12/2024 às 18h - alta prioridade"
    ]

    for i, text in enumerate(test_cases, 1):
        print(f"\n📋 Teste {i}: {text}")
        print("-" * 40)

        # Testa diferentes parsers
        event = parser.parse_event_safe(text)
        if event:
            print("📅 Evento:", event.display_info())

        sentiment = parser.parse_sentiment_safe(text)
        if sentiment:
            print("😊 Sentimento:", sentiment.get_sentiment_label())

        appointment = parser.parse_appointment_safe(text)
        if appointment:
            print("📋 Compromisso:", appointment.get_priority_level())

        task = parser.parse_task_safe(text)
        if task:
            print("✅ Tarefa:", task.get_status_icon(), task.task_name)

        print("-" * 40)


def demo_error_handling():
    """Demonstra tratamento de erros em OutputParsers"""
    print("\n🎯 EXEMPLO: Tratamento de Erros")
    print("=" * 60)

    # Testa validação de data passada
    try:
        past_date = datetime.now() - timedelta(days=1)
        event = EventInfo(
            event_name="Evento Passado",
            event_date=past_date,
            duration_hours=1.0,
            is_recurring=False
        )
    except ValueError as e:
        print(f"❌ Validação funcionou: {e}")

    # Testa validação de confiança
    try:
        sentiment = SentimentAnalysis(
            text="Teste",
            is_positive=True,
            is_negative=False,
            is_neutral=False,
            contains_urgency=False,
            confidence_score=1.5  # Inválido: > 1.0
        )
    except ValueError as e:
        print(f"❌ Validação funcionou: {e}")

    # Testa validação de string vazia
    try:
        task = TaskInfo(
            task_name="",  # Inválido: string vazia
            due_date=datetime.now() + timedelta(days=1),
            is_completed=False,
            is_high_priority=False
        )
    except ValueError as e:
        print(f"❌ Validação funcionou: {e}")


def main():
    """Função principal"""
    print("🚀 OUTPUTPARSERS AVANÇADOS - EXEMPLOS PRÁTICOS")
    print("=" * 60)

    demo_advanced_parsers()
    demo_error_handling()

    print("\n📚 CONCEITOS AVANÇADOS")
    print("=" * 60)
    print("""
🎯 Tratamento de Erros:
- Validação automática com Pydantic
- Try/catch para falhas de parsing
- Fallbacks para dados inválidos

🎯 Validação Customizada:
- Validators para regras específicas
- Validação de relacionamentos entre campos
- Mensagens de erro personalizadas

🎯 Type Safety:
- Verificação de tipos em tempo de execução
- Documentação automática dos campos
- Integração com IDEs

🎯 Casos de Uso Reais:
- APIs com respostas estruturadas
- Bancos de dados com schemas
- Sistemas de validação de dados
    """)


if __name__ == "__main__":
    main()
