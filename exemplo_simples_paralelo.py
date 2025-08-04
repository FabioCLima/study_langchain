# Exemplo Simples: Conceito de Execução Paralela
# Vamos entender o conceito do RunnableParallel sem depender do LangChain

import time
from concurrent.futures import ThreadPoolExecutor
from typing import Dict, Any

# 1. Funções que simulam operações (como no LangChain)
def contar_palavras(texto: str) -> int:
    """Simula uma operação de contagem de palavras"""
    time.sleep(0.1)  # Simula processamento
    return len(texto.split())

def contar_caracteres(texto: str) -> int:
    """Simula uma operação de contagem de caracteres"""
    time.sleep(0.1)  # Simula processamento
    return len(texto)

def converter_maiusculo(texto: str) -> str:
    """Simula uma operação de conversão"""
    time.sleep(0.1)  # Simula processamento
    return texto.upper()

# 2. Simulando o RunnableParallel (execução paralela)
def executar_paralelo(texto: str) -> Dict[str, Any]:
    """Simula o comportamento do RunnableParallel"""
    with ThreadPoolExecutor(max_workers=3) as executor:
        # Executa as três operações em paralelo
        future_palavras = executor.submit(contar_palavras, texto)
        future_caracteres = executor.submit(contar_caracteres, texto)
        future_maiusculo = executor.submit(converter_maiusculo, texto)
        
        # Coleta os resultados
        return {
            "palavras": future_palavras.result(),
            "caracteres": future_caracteres.result(),
            "maiusculo": future_maiusculo.result()
        }

# 3. Simulando execução sequencial (uma após a outra)
def executar_sequencial(texto: str) -> Dict[str, Any]:
    """Executa as operações uma após a outra"""
    return {
        "palavras": contar_palavras(texto),
        "caracteres": contar_caracteres(texto),
        "maiusculo": converter_maiusculo(texto)
    }

# 4. Testando e comparando
if __name__ == "__main__":
    texto_teste = "Olá mundo! Como você está?"
    
    print("=== CONCEITO DO RUNNABLEPARALLEL ===")
    print(f"Texto de entrada: '{texto_teste}'")
    print()
    
    # Teste com execução paralela
    print("🔄 Executando em PARALELO (como RunnableParallel):")
    inicio_paralelo = time.time()
    resultado_paralelo = executar_paralelo(texto_teste)
    tempo_paralelo = time.time() - inicio_paralelo
    
    print(f"Resultado: {resultado_paralelo}")
    print(f"Tempo: {tempo_paralelo:.3f} segundos")
    print()
    
    # Teste com execução sequencial
    print("⏳ Executando SEQUENCIAL (uma após a outra):")
    inicio_sequencial = time.time()
    resultado_sequencial = executar_sequencial(texto_teste)
    tempo_sequencial = time.time() - inicio_sequencial
    
    print(f"Resultado: {resultado_sequencial}")
    print(f"Tempo: {tempo_sequencial:.3f} segundos")
    print()
    
    # Comparação
    print("📊 COMPARAÇÃO:")
    print(f"Paralelo: {tempo_paralelo:.3f}s")
    print(f"Sequencial: {tempo_sequencial:.3f}s")
    print(f"Melhoria: {tempo_sequencial/tempo_paralelo:.1f}x mais rápido!")
    print()
    
    print("💡 CONCEITO CHAVE:")
    print("- RunnableParallel executa múltiplas operações SIMULTANEAMENTE")
    print("- Cada operação recebe a mesma entrada")
    print("- O resultado é um dicionário com chaves nomeadas")
    print("- Ideal para operações independentes que podem rodar em paralelo") 