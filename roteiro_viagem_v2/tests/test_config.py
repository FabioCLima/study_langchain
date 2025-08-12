#!/usr/bin/env python3
"""
Teste simples para verificar se a configuração está funcionando.

Este módulo contém testes básicos para validar se a configuração
pode ser importada e acessada corretamente.

Exemplo de uso:
    python3 test_config.py
    
    # Ou importar e usar programaticamente
    from test_config import test_config
    success = test_config()
"""
import os
import sys
from typing import NoReturn

# Adicionar o diretório atual ao path para importar o módulo
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def test_config() -> bool:
    """
    Testa se a configuração pode ser importada sem erros.
    
    Esta função tenta importar o módulo de configuração e acessar
    suas propriedades básicas para verificar se está funcionando.
    
    Returns:
        bool: True se a configuração foi carregada com sucesso, False caso contrário.
    
    Example:
        success = test_config()
        if success:
            print("✅ Configuração funcionando!")
        else:
            print("❌ Problema na configuração")
    
    Note:
        Esta função requer que as dependências estejam instaladas:
        pip install -r requirements.txt
    """
    try:
        from config import settings
        print("✅ Configuração importada com sucesso!")
        print(f"📁 Projeto: {settings.langchain_project}")
        print(f"🤖 Modelo: {settings.model_name}")
        print(f"🌡️  Temperatura: {settings.temperature}")
        print(f"📝 Max Tokens: {settings.max_tokens}")
        return True
    except Exception as e:
        print(f"❌ Erro ao importar configuração: {e}")
        return False


def main() -> NoReturn:
    """
    Função principal que executa o teste de configuração.
    
    Esta função chama test_config() e encerra o programa com
    código de saída apropriado.
    
    Returns:
        NoReturn: Esta função nunca retorna, sempre encerra o programa.
    
    Note:
        Usa sys.exit(0) para encerrar o programa após o teste.
    """
    test_config()
    sys.exit(0)


if __name__ == "__main__":
    main()
