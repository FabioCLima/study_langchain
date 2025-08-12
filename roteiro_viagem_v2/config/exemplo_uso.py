#!/usr/bin/env python3
"""
Exemplo de uso da configuração.

Este módulo demonstra como usar as configurações do projeto
em diferentes cenários práticos.

Exemplo de uso:
    python3 exemplo_uso.py
    
    # Ou importar e usar programaticamente
    from exemplo_uso import main
    main()
"""
from typing import NoReturn

from config import settings


def main() -> None:
    """
    Exemplo de como usar as configurações do projeto.
    
    Esta função demonstra diferentes formas de acessar e usar
    as configurações carregadas do arquivo .env.
    
    Returns:
        None: Esta função não retorna valor.
    
    Example:
        # Executar o exemplo
        main()
        
        # Ou importar e usar
        from exemplo_uso import main
        main()
    
    Note:
        As chaves secretas são acessadas usando get_secret_value()
        para evitar vazamentos de segurança.
    """
    print("🔧 Configurações do Projeto:")
    print(f"   📁 Projeto: {settings.langchain_project}")
    print(f"   🤖 Modelo: {settings.model_name}")
    print(f"   🌡️  Temperatura: {settings.temperature}")
    print(f"   📝 Max Tokens: {settings.max_tokens}")

    # Para acessar as chaves secretas (sempre use get_secret_value())
    print("\n🔑 Chaves de API:")
    print(f"   OpenAI: {settings.openai_api_key.get_secret_value()[:10]}...")
    print(f"   LangChain: {settings.langchain_api_key.get_secret_value()[:10]}...")

    # Exemplo de uso em uma aplicação LangChain
    print("\n🚀 Exemplo de uso:")
    print("   from langchain_openai import ChatOpenAI")
    print("   llm = ChatOpenAI(")
    print("       api_key=settings.openai_api_key.get_secret_value(),")
    print("       model_name=settings.model_name,")
    print("       temperature=settings.temperature,")
    print("       max_tokens=settings.max_tokens")
    print("   )")


def run_example() -> NoReturn:
    """
    Executa o exemplo de uso da configuração.
    
    Esta função chama main() e encerra o programa com
    código de saída apropriado.
    
    Returns:
        NoReturn: Esta função nunca retorna, sempre encerra o programa.
    
    Note:
        Usa exit(0) para encerrar o programa após executar o exemplo.
    """
    main()
    exit(0)


if __name__ == "__main__":
    run_example()
