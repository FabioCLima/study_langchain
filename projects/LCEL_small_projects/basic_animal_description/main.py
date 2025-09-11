# main.py
"""Ponto de entrada principal para a aplicação de descrição de animais.

Este script utiliza 'argparse' para criar uma interface de linha de comando (CLI)
amigável, permitindo que o usuário peça a descrição de um animal específico.

Como usar:
$ python main.py --animal "Leão"
"""

import argparse

from chains.chain_animal_description import pipeline_completa


def main():
    """Função principal que configura o CLI, executa a pipeline e imprime o resultado."""
    # 1. Configuração do Parser de Argumentos
    # Isso cria a ajuda e os argumentos que seu script aceita no terminal.
    parser = argparse.ArgumentParser(
        description="Gera uma descrição detalhada sobre um animal usando LangChain."
    )
    parser.add_argument(
        "--animal",
        type=str,
        required=True,
        help="O nome do animal para o qual a descrição será gerada.",
    )
    args = parser.parse_args()

    # 2. Execução da Pipeline
    # Tenta executar a pipeline importada e trata possíveis erros.
    try:
        print(f"🐾 Gerando descrição para: {args.animal}...")

        # O dicionário {"animal": args.animal} corresponde à entrada que a pipeline espera.
        resultado_final = pipeline_completa.invoke({"animal": args.animal})

        print("\n✅ Descrição gerada com sucesso!")
        print(resultado_final)

    except Exception as e:
        print(f"\n❌ Ocorreu um erro ao executar a pipeline: {e}")


# 3. Ponto de Entrada Padrão do Python
# Este bloco garante que a função main() só será executada quando
# o script for chamado diretamente (ex: python main.py).
if __name__ == "__main__":
    main()
