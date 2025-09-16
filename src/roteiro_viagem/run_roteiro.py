#!/usr/bin/env python3
"""Script de execução para o projeto Roteiro de Viagem
Execute este script a partir do diretório raiz do projeto
"""

import os
import pathlib
import sys

# Adiciona o diretório roteiro_viagem ao path
roteiro_path = os.path.join(pathlib.Path(__file__).parent, "roteiro_viagem")
sys.path.insert(0, roteiro_path)

# Também adiciona o diretório pai para permitir importações absolutas
sys.path.insert(0, pathlib.Path(__file__).parent)

# Agora executa o main
from roteiro_viagem.main import main

if __name__ == "__main__":
    main()
