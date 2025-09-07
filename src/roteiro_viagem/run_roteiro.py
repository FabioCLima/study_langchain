#!/usr/bin/env python3
"""
Script de execução para o projeto Roteiro de Viagem
Execute este script a partir do diretório raiz do projeto
"""

import sys
import os

# Adiciona o diretório roteiro_viagem ao path
roteiro_path = os.path.join(os.path.dirname(__file__), 'roteiro_viagem')
sys.path.insert(0, roteiro_path)

# Também adiciona o diretório pai para permitir importações absolutas
sys.path.insert(0, os.path.dirname(__file__))

# Agora executa o main
from roteiro_viagem.main import main

if __name__ == "__main__":
    main()
