from country_capital_proj.models import ResultadoFinal


def format_result(result: ResultadoFinal) -> str:
    """Formata ResultadoFinal para exibição amigável no console.

    Args:
        result: ResultadoFinal (Pydantic).

    Returns:
        str: Texto formatado pronto para print.
    """
    return (
        "\n📌 Resultado Final:\n"
        f"País       : {result.pais}\n"
        f"Capital    : {result.capital}\n"
        f"Curiosidade: {result.curiosidade}\n"
    )
