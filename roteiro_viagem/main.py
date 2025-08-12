"""
Entrega de um roteiro de viagem completo
Executa o fluxo principal do projeto:
- Recebe interesse de atividade do usuário
- Gera destino sugerido
- Lista restaurantes e passeios culturais
"""

import argparse
from config import settings
from utils.llm_setup import load_environment_variables, create_model
from chains.orchestrador import create_main_chain
from utils.logger_setup import project_logger


def format_and_print_roteiro(resultado: dict) -> None:
    """
    Formata e apresenta o resultado final no terminal.
    Aceita tanto objetos Pydantic quanto dicionários.
    """
    print("\n" + "=" * 50)
    print("✨ ROTEIRO DE VIAGEM GERADO COM SUCESSO! ✨")
    print("=" * 50)

    destino_info = resultado.get('destino_info', {})
    sugestoes = resultado.get('sugestoes', {})

    # Tratamento seguro para Pydantic ou dict
    cidade = getattr(destino_info, "cidade", destino_info.get("cidade", "N/A"))
    motivo = getattr(destino_info, "motivo", destino_info.get("motivo", "N/A"))

    print(f"\n📍 Destino Recomendado: {cidade}")
    print(f"   Motivo: {motivo}")

    restaurantes = sugestoes.get('restaurantes')
    if restaurantes:
        print("\n🍴 Restaurantes Recomendados:")
        lista_restaurantes = getattr(restaurantes, "restaurantes", restaurantes.get("restaurantes", []))
        for r in lista_restaurantes:
            nome = getattr(r, "nome", r.get("nome"))
            tipo = getattr(r, "tipo", r.get("tipo"))
            descricao = getattr(r, "descricao", r.get("descricao"))
            print(f"   - {nome} ({tipo}): {descricao}")

    passeios = sugestoes.get('passeios_culturais')
    if passeios:
        print("\n🏛️ Passeios Culturais:")
        lista_passeios = getattr(passeios, "atracoes", passeios.get("atracoes", []))
        for p in lista_passeios:
            nome = getattr(p, "nome", p.get("nome"))
            descricao = getattr(p, "descricao", p.get("descricao"))
            print(f"   - {nome}: {descricao}")

    print("\n" + "=" * 50)


def main() -> None:
    """Função principal que executa o fluxo."""
    parser = argparse.ArgumentParser(description="Gerador de Roteiro de Viagem com LangChain.")
    parser.add_argument("interesse", type=str, help="Descreva o seu interesse de viagem. Ex: 'praias históricas no nordeste'")
    args = parser.parse_args()

    try:
        project_logger.info("🚀 Iniciando geração de roteiro...")
        project_logger.debug(f"Interesse informado pelo usuário: {args.interesse}")

        api_key = load_environment_variables()
        model = create_model(api_key)

        roteiro_completo_chain = create_main_chain(model)

        project_logger.info("🔍 Executando cadeia principal...")
        resultado_final = roteiro_completo_chain({"interesse": args.interesse})

        project_logger.info("📄 Roteiro gerado com sucesso. Exibindo resultado...")
        format_and_print_roteiro(resultado_final)

    except Exception as e:
        project_logger.exception(f"❌ Erro durante a execução: {e}")


if __name__ == "__main__":
    main()
