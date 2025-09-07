#!/usr/bin/env python3
"""OutputParsers - Exemplos Simples com Datetime e Boolean
=======================================================

Este arquivo demonstra conceitos de OutputParsers usando apenas a biblioteca padrão Python.
Foca nos conceitos fundamentais de parsing estruturado.

Autor: Tutor LangChain
Data: 2024
"""

import json
import re
from dataclasses import dataclass
from datetime import datetime, timedelta


@dataclass
class EventInfo:
    """Informações de um evento com data e hora"""

    event_name: str
    event_date: datetime
    duration_hours: float | None = None
    is_recurring: bool = False

    def display_info(self) -> str:
        """Exibe informações formatadas do evento"""
        recurring_text = "(Recorrente)" if self.is_recurring else "(Único)"
        duration_text = f" - Duração: {self.duration_hours}h" if self.duration_hours else ""

        return f"📅 {self.event_name} {recurring_text}\n" \
               f"   📆 {self.event_date.strftime('%d/%m/%Y às %H:%M')}{duration_text}"


@dataclass
class SentimentAnalysis:
    """Análise de sentimento com valores booleanos"""

    text: str
    is_positive: bool
    is_negative: bool
    is_neutral: bool
    contains_urgency: bool
    confidence_score: float

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


@dataclass
class AppointmentAnalysis:
    """Análise de compromissos com datetime e boolean"""

    appointment_date: datetime
    is_urgent: bool
    is_important: bool
    requires_preparation: bool
    is_online: bool
    duration_minutes: int | None = None

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


class SimpleOutputParser:
    """Parser simples que simula o comportamento do LangChain"""

    def __init__(self):
        self.tomorrow = datetime.now() + timedelta(days=1)
        self.friday = datetime.now() + timedelta(days=(4 - datetime.now().weekday()) % 7)

    def parse_event(self, text: str) -> EventInfo:
        """Simula parsing de evento com datetime"""
        # Simula extração de informações do LLM
        if "reunião de equipe" in text.lower():
            return EventInfo(
                event_name="Reunião de Equipe",
                event_date=self.tomorrow.replace(hour=14, minute=30),
                duration_hours=2.0,
                is_recurring=False
            )
        if "standup diário" in text.lower():
            return EventInfo(
                event_name="Standup Diário",
                event_date=self.tomorrow.replace(hour=9, minute=0),
                duration_hours=0.5,
                is_recurring=True
            )
        return EventInfo(
            event_name="Apresentação do Projeto",
            event_date=self.friday.replace(hour=16, minute=0),
            duration_hours=1.0,
            is_recurring=False
        )

    def parse_sentiment(self, text: str) -> SentimentAnalysis:
        """Simula parsing de sentimento com boolean"""
        # Simula análise de sentimento do LLM
        is_positive = any(word in text.lower() for word in ["adorei", "perfeito", "excelente", "ótimo"])
        is_negative = any(word in text.lower() for word in ["quebrado", "urgente", "problema", "ruim"])
        is_neutral = not (is_positive or is_negative)
        contains_urgency = any(word in text.lower() for word in ["urgente", "imediatamente", "agora"])

        # Calcula confiança baseada na clareza do sentimento
        positive_words = len([w for w in text.lower().split() if w in ["adorei", "perfeito", "excelente"]])
        negative_words = len([w for w in text.lower().split() if w in ["quebrado", "problema", "ruim"]])
        total_sentiment_words = positive_words + negative_words

        confidence = min(0.95, max(0.6, total_sentiment_words * 0.2))

        return SentimentAnalysis(
            text=text,
            is_positive=is_positive,
            is_negative=is_negative,
            is_neutral=is_neutral,
            contains_urgency=contains_urgency,
            confidence_score=confidence
        )

    def parse_appointment(self, text: str) -> AppointmentAnalysis:
        """Simula parsing de compromisso combinando datetime e boolean"""
        # Simula análise de compromisso do LLM
        is_urgent = "urgente" in text.lower()
        is_important = "importante" in text.lower() or is_urgent
        requires_preparation = "preparar" in text.lower() or "apresentação" in text.lower()
        is_online = "online" in text.lower()

        # Extrai duração se mencionada
        duration_match = re.search(r"(\d+)\s*hora", text.lower())
        duration_minutes = int(duration_match.group(1)) * 60 if duration_match else None

        return AppointmentAnalysis(
            appointment_date=self.tomorrow.replace(hour=10, minute=0),
            is_urgent=is_urgent,
            is_important=is_important,
            requires_preparation=requires_preparation,
            is_online=is_online,
            duration_minutes=duration_minutes
        )


def demo_datetime_parser():
    """Demonstra parser com datetime"""
    print("🎯 EXEMPLO 1: OutputParser com Datetime")
    print("=" * 60)

    parser = SimpleOutputParser()
    texts = [
        "Reunião de equipe amanhã às 14:30 por 2 horas",
        "Standup diário às 9h da manhã",
        "Apresentação do projeto na próxima sexta às 16h"
    ]

    for i, text in enumerate(texts, 1):
        event = parser.parse_event(text)
        print(f"\n📋 Exemplo {i}:")
        print(f"Texto: {text}")
        print(event.display_info())
        print("-" * 40)


def demo_boolean_parser():
    """Demonstra parser com boolean"""
    print("\n🎯 EXEMPLO 2: OutputParser com Boolean")
    print("=" * 60)

    parser = SimpleOutputParser()
    texts = [
        "Adorei o produto! Funciona perfeitamente e superou minhas expectativas.",
        "Preciso de ajuda URGENTE! O sistema está quebrado e não consigo trabalhar!",
        "O serviço é adequado, mas poderia ser melhor."
    ]

    for i, text in enumerate(texts, 1):
        sentiment = parser.parse_sentiment(text)
        print(f"\n📋 Exemplo {i}:")
        print(sentiment.display_analysis())
        print("-" * 40)


def demo_combined_parser():
    """Demonstra parser combinado (datetime + boolean)"""
    print("\n🎯 EXEMPLO 3: OutputParser Combinado (Datetime + Boolean)")
    print("=" * 60)

    parser = SimpleOutputParser()
    texts = [
        "Reunião URGENTE com o cliente amanhã às 10h. É muito importante e preciso preparar a apresentação. Será online por 1 hora.",
        "Café com João na sexta-feira às 15h"
    ]

    for i, text in enumerate(texts, 1):
        appointment = parser.parse_appointment(text)
        print(f"\n📋 Exemplo {i}:")
        print(f"Texto: {text}")
        print(appointment.display_appointment())
        print("-" * 40)


def demo_json_serialization():
    """Demonstra serialização JSON dos parsers"""
    print("\n🎯 EXEMPLO 4: Serialização JSON")
    print("=" * 60)

    parser = SimpleOutputParser()
    text = "Reunião de equipe amanhã às 14:30 por 2 horas"

    event = parser.parse_event(text)

    # Converte para dict (simula model_dump() do Pydantic)
    event_dict = {
        "event_name": event.event_name,
        "event_date": event.event_date.isoformat(),
        "duration_hours": event.duration_hours,
        "is_recurring": event.is_recurring
    }

    print("📋 Evento serializado em JSON:")
    print(json.dumps(event_dict, indent=2, ensure_ascii=False))
    print("-" * 40)


def main():
    """Função principal"""
    print("🚀 OUTPUTPARSERS - EXEMPLOS PRÁTICOS")
    print("=" * 60)

    demo_datetime_parser()
    demo_boolean_parser()
    demo_combined_parser()
    demo_json_serialization()

    print("\n📚 RESUMO DOS CONCEITOS")
    print("=" * 60)
    print("""
🎯 OutputParsers com Datetime:
- Extração de datas de textos naturais
- Validação temporal (futuro/passado)
- Formatação personalizada de datas

🎯 OutputParsers com Boolean:
- Análise de sentimento (positivo/negativo/neutro)
- Flags de status (urgência, importância)
- Validação lógica entre campos

🎯 OutputParsers Combinados:
- Datetime + Boolean no mesmo modelo
- Análise de compromissos com prioridade
- Gerenciamento de tarefas estruturado

🎯 Benefícios Demonstrados:
- Type Safety com dataclasses
- Estruturação consistente de dados
- Serialização JSON para APIs
- Código limpo e organizado
    """)


if __name__ == "__main__":
    main()
