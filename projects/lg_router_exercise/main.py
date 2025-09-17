# main.py (Versão Melhorada com Rich)
"""Ponto de entrada principal para a aplicação de processamento de strings."""

from loguru import logger
from pydantic import ValidationError
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

from .graph_builder import build_graph
from .settings import get_settings
from .state import State

# Cria uma instância do console do Rich para imprimir saídas formatadas
console = Console()


def setup_logger() -> None:
    """Configura o logger para uma saída simples no console."""
    logger.remove()
    logger.add(lambda msg: print(msg, end=""), format="{message}")


def main() -> None:
    """Função principal que constrói e executa o grafo."""
    setup_logger()
    logger.info("🚀 Iniciando a aplicação e carregando configurações...")
    settings = get_settings()
    logger.info(
        f"✅ Configurações carregadas para o projeto: '{settings.langsmith_project}'"
    )

    console.print("\n[bold cyan]🛠️  Construindo o grafo...[/bold cyan]")
    app = build_graph()
    console.print(
        "[bold green]✅ Grafo construído e compilado com sucesso![/bold green]"
    )

    console.print("\n[bold]--- ESTRUTURA DO GRAFO ---[/bold]")
    app.get_graph().print_ascii()
    console.print("[bold]--------------------------[/bold]\n")

    test_cases = [
        {"user_string": "Hello LangGraph!", "action_type": "reverse"},
        {"user_string": "Python is Fun", "action_type": "upper"},
        {"user_string": "Test Error", "action_type": "invalid_action"},
    ]

    success_count = 0
    fail_count = 0

    for i, inputs in enumerate(test_cases):
        console.print(f"[bold]--- ▶️  EXECUTANDO CASO DE TESTE #{i + 1} ---[/bold]")
        try:
            State.model_validate(inputs)
            final_state = app.invoke(inputs)

            # Cria um painel visualmente agradável para o resultado
            result_text = Text()
            result_text.append("Entrada....: ", style="bold")
            result_text.append(f"'{final_state['user_string']}'\n")
            result_text.append("Ação......: ", style="bold")
            result_text.append(f"'{final_state['action_type']}'\n")
            result_text.append("Resultado..: ", style="bold green")
            result_text.append(
                f"'{final_state['processed_string']}'", style="bold green"
            )

            console.print(
                Panel(
                    result_text,
                    title="[bold green]✅ RESULTADO FINAL[/bold green]",
                    expand=False,
                )
            )
            print()  # Adiciona uma linha em branco
            success_count += 1

        except ValidationError:
            fail_count += 1
            error_text = Text()
            error_text.append(f"Input inválido: {inputs}\n", style="bold yellow")
            error_text.append(
                "A ação solicitada não é permitida. Opções válidas são 'reverse' ou\
            'upper'.",
                style="yellow",
            )

            console.print(
                Panel(
                    error_text,
                    title="[bold red]❌ ERRO DE VALIDAÇÃO[/bold red]",
                    expand=False,
                )
            )
            print()

    console.print(
        f"[bold]Execução Concluída:[/bold] {success_count} com sucesso, {fail_count}\
 com falha de validação."
    )


if __name__ == "__main__":
    main()
