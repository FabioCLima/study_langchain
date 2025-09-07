# Comparação: RunnableParallel vs Chain Encadeada
# Vamos ver a diferença prática entre as duas abordagens

import time

# Simulando logs (como no notebook)
logs: list[str] = []


def processar_texto(texto: str) -> str:
    """Simula o processamento de texto"""
    time.sleep(0.1)  # Simula processamento
    return f"Processado: {texto}"


def salvar_log(texto: str) -> None:
    """Simula salvar nos logs"""
    time.sleep(0.05)  # Simula operação de log
    logs.append(texto)


# ===== ABORDAGEM 1: CHAIN ENCADEADA (Sequencial) =====
def chain_encadeada(texto: str):
    """Faz uma operação após a outra"""
    print("🔄 Chain Encadeada (Sequencial):")
    inicio = time.time()

    # Passo 1: Processar
    resultado = processar_texto(texto)
    print(f"  1. Processamento: {resultado}")

    # Passo 2: Salvar log
    salvar_log(resultado)
    print(f"  2. Log salvo: {resultado}")

    tempo = time.time() - inicio
    print(f"  ⏱️ Tempo total: {tempo:.3f}s")
    print()


# ===== ABORDAGEM 2: RUNNABLEPARALLEL (Paralelo) =====
def runnable_paralelo(texto: str):
    """Faz as operações ao mesmo tempo"""
    print("⚡ RunnableParallel (Paralelo):")
    inicio = time.time()

    # Simulando RunnableParallel
    from concurrent.futures import ThreadPoolExecutor

    with ThreadPoolExecutor(max_workers=2) as executor:
        # Executa AMBAS as operações simultaneamente
        future_processamento = executor.submit(processar_texto, texto)
        future_log = executor.submit(salvar_log, texto)

        # Coleta resultados
        resultado = future_processamento.result()
        future_log.result()  # Aguarda o log terminar

        print(f"  1. Processamento: {resultado}")
        print(f"  2. Log salvo: {texto}")

        tempo = time.time() - inicio
        print(f"  ⏱️ Tempo total: {tempo:.3f}s")
        print()


# ===== TESTE PRÁTICO =====
if __name__ == "__main__":
    texto_teste = "Olá mundo!"

    print("=== COMPARAÇÃO: ENCADEADA vs PARALELA ===")
    print(f"Texto: '{texto_teste}'")
    print()

    # Limpa logs
    logs.clear()

    # Testa chain encadeada
    chain_encadeada(texto_teste)

    # Limpa logs novamente
    logs.clear()

    # Testa RunnableParallel
    runnable_paralelo(texto_teste)

    print("💡 CONCLUSÃO:")
    print("- Chain Encadeada: Uma operação ESPERA a outra terminar")
    print("- RunnableParallel: Ambas as operações RODAM SIMULTANEAMENTE")
    print("- Resultado final: O MESMO")
    print("- Performance: Paralelo é MAIS RÁPIDO!")
    print()

    print("🎯 NO SEU NOTEBOOK:")
    print("parse_and_log_output_chain = RunnableParallel(")
    print("    output=parser,           # Processa o texto")
    print("    log=RunnableLambda(...)  # Salva nos logs")
    print(")")
    print()
    print("✅ Ambas as operações acontecem AO MESMO TEMPO!")
    print("✅ Resultado: {'output': 'texto processado', 'log': None}")
    print("✅ Performance: Mais rápido que fazer sequencialmente")
