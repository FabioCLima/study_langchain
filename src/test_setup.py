#!/usr/bin/env python3
"""
Script de teste para verificar a configuração do OpenAI
"""

import os
from pathlib import Path

def test_env_setup():
    """Testa se o arquivo .env existe e tem a chave da API"""
    
    # Verifica se existe arquivo .env
    env_path = Path(__file__).parent / ".env"
    
    print("🔍 Verificando configuração...")
    print(f"📁 Procurando arquivo .env em: {env_path}")
    
    if not env_path.exists():
        print("❌ Arquivo .env não encontrado!")
        print("💡 Crie o arquivo .env com:")
        print("   OPENAI_API_KEY=sua_chave_aqui")
        return False
    
    print("✅ Arquivo .env encontrado!")
    
    # Carrega variáveis de ambiente
    from dotenv import load_dotenv
    load_dotenv(env_path)
    
    api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        print("❌ OPENAI_API_KEY não encontrada no arquivo .env")
        return False
    
    if not api_key.startswith("sk-"):
        print("❌ Chave da API parece inválida (deve começar com 'sk-')")
        return False
    
    print(f"✅ Chave da API encontrada: ***{api_key[-4:]}")
    return True

def test_model_creation():
    """Testa se consegue criar o modelo"""
    
    print("\n🧪 Testando criação do modelo...")
    
    try:
        from openai_client import create_analytical_model
        
        model = create_analytical_model()
        
        if model is None:
            print("❌ Falha ao criar modelo")
            return False
        
        print(f"✅ Modelo criado com sucesso: {model.model_name}")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao criar modelo: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Teste de Configuração do OpenAI\n")
    
    env_ok = test_env_setup()
    
    if env_ok:
        model_ok = test_model_creation()
        
        if model_ok:
            print("\n🎉 Tudo configurado corretamente!")
            print("✅ Você pode executar: python3 src/exercise_chain1.py")
        else:
            print("\n❌ Problema na criação do modelo")
    else:
        print("\n❌ Configure o arquivo .env primeiro")