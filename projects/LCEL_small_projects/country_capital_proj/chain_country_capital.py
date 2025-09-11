"""Script principal — CLI:
$ python chain_country_capital.py --pais Belgica
"""

import argparse

from country_capital_proj.chains.country_chain import build_pipeline
from country_capital_proj.models import ResultadoFinal
from country_capital_proj.utils.formatter import format_result


def main() -> None:
    """Ponto de entrada principal para a execução do script via CLI."""
    parser = argparse.ArgumentParser(
        description="Obter capital e curiosidade de um país"
    )
    parser.add_argument("--pais", type=str, required=True, help="Nome do país")
    args = parser.parse_args()

    pipeline = build_pipeline()
    try:
        # invoke() executa a pipeline: recebe {"pais": "..."} e retorna um objeto
        # do tipo ResultadoFinal.
        resultado: ResultadoFinal = pipeline.invoke({"pais": args.pais})  # type: ignore[assignment]
    except Exception as exc:
        # mensagem amigável no caso de erro de API/validação
        error_message = f"Erro ao executar pipeline: {exc}"
        raise SystemExit(error_message) from exc

    print(format_result(resultado))


if __name__ == "__main__":
    main()
