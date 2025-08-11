'''Entrega de um roteiro de viagem completo'''
import argparse # para lidar com argumentos de linha de comando
from utils.llm_setup import load_environment_variables, create_model
from chains.orchestrador import create_main_chain


def format_and_print_roteiro(resultado: dict):
    """Função dedicada a apresentar o resultado final de forma elegante."""
    print("\n" + "="*50)
    print("✨ ROTEIRO DE VIAGEM GERADO COM SUCESSO! ✨")
    print("="*50)

    destino_info = resultado.get('destino_info', {})
    sugestoes = resultado.get('sugestoes', {})
    
    print(f"\n📍 Destino Recomendado: {destino_info.get('cidade', 'N/A')}")
    print(f"   Motivo: {destino_info.get('motivo', 'N/A')}")
    
    restaurantes = sugestoes.get('restaurantes')
    if restaurantes:
        print("\n🍴 Restaurantes Recomendados:")
        for r in restaurantes.restaurantes:
            print(f"   - {r.nome} ({r.tipo}): {r.descricao}")

    passeios = sugestoes.get('passeios_culturais')
    if passeios:
        print("\n🏛️ Passeios Culturais:")
        # O print direto aqui é aceitável, pois a formatação foi definida no prompt.
        # Para mais controle, você também poderia parsear essa string.
        print(passeios)
    
    print("\n" + "="*50)

def main() -> None:
    """Função principal que executa o fluxo."""
    # Configura o parser de argumentos
    parser = argparse.ArgumentParser(description="Gerador de Roteiro de Viagem com LangChain.")
    parser.add_argument("interesse", type=str, help="Descreva o seu interesse de viagem. Ex: 'praias históricas no nordeste'")
    args = parser.parse_args()

    try:
        api_key = load_environment_variables()
        model = create_model(api_key)

        roteiro_completo_chain = create_main_chain(model)

        print(f"Buscando roteiro para interesse: '{args.interesse}'...")

        # Usa o interesse passado como argumento
        resultado_final = roteiro_completo_chain.invoke({"interesse": args.interesse})

        format_and_print_roteiro(resultado_final)

    except Exception as e:
        print(f"Ocorreu um erro: {e}")


if __name__ == "__main__":
    main()