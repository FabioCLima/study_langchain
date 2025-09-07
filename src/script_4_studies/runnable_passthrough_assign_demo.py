#!/usr/bin/env python3
"""Demonstração do RunnablePassthrough().assign()
==============================================

Este código complementa o exercício da célula 15 do notebook, demonstrando como
o RunnablePassthrough().assign() executa uma chain e adiciona seu resultado
como uma nova chave no dicionário de entrada, preservando os dados originais.

Este é o padrão-ouro para passar informações entre etapas de um workflow.
"""

import json

from langchain.schema.runnable import (  # type: ignore
    RunnableLambda,
    RunnablePassthrough,
)


def demonstrar_runnable_passthrough_assign():
    """Demonstra o uso do RunnablePassthrough().assign() para preservar dados
    originais enquanto adiciona novos resultados.
    """
    # Frase de exemplo
    frase: str = "A vida que se leva é a vida que se vive !"

    print("=== Demonstração do RunnablePassthrough().assign() ===\n")
    print(f"Frase de entrada: '{frase}'\n")

    # 1. Pipeline básico com RunnablePassthrough().assign()
    print("1. Pipeline básico com .assign():")
    print("-" * 40)

    pipeline_basico = RunnablePassthrough().assign(
        # Adiciona o número de palavras como nova chave
        num_palavras=RunnableLambda(lambda input_str: len(input_str.split())),
        # Adiciona a frase em maiúsculas como nova chave
        frase_maiuscula=RunnableLambda(lambda input_str: input_str.upper()),
        # Adiciona o número de caracteres como nova chave
        num_caracteres=RunnableLambda(lambda input_str: len(input_str))
    )

    # Execute o pipeline básico
    resultado_basico = pipeline_basico.invoke(frase)  # type: ignore

    print(f"Frase original: {resultado_basico['input']}")
    print(f"Número de palavras: {resultado_basico['num_palavras']}")
    print(f"Frase em maiúsculas: {resultado_basico['frase_maiuscula']}")
    print(f"Número de caracteres: {resultado_basico['num_caracteres']}")

    # 2. Demonstração de como os dados originais são preservados
    print("\n2. Dados preservados:")
    print("-" * 40)
    print(f"Tipo do resultado: {type(resultado_basico)}")
    print(f"Chaves disponíveis: {list(resultado_basico.keys())}")
    print(f"Estrutura completa: {json.dumps(resultado_basico, indent=2, ensure_ascii=False)}")

    # 3. Pipeline avançado que usa os dados preservados
    print("\n3. Pipeline avançado usando dados preservados:")
    print("-" * 40)

    pipeline_avancado = pipeline_basico.assign(
        # Adiciona uma análise baseada nos dados preservados
        analise=RunnableLambda(lambda dados: {
            "palavras_por_caractere": round(dados["num_palavras"] / dados["num_caracteres"], 3),
            "tem_exclamacao": "!" in dados["input"],
            "palavras_unicas": len(set(dados["input"].lower().split())),
            "palavra_mais_longa": max(dados["input"].split(), key=len),
            "comprimento_palavra_mais_longa": len(max(dados["input"].split(), key=len))
        })
    )

    # Execute o pipeline avançado
    resultado_avancado = pipeline_avancado.invoke(frase)  # type: ignore

    print("Análise detalhada:")
    for chave, valor in resultado_avancado["analise"].items():
        print(f"  {chave}: {valor}")

    # 4. Demonstração de pipeline em cascata
    print("\n4. Pipeline em cascata com múltiplos .assign():")
    print("-" * 40)

    pipeline_cascata = (
        RunnablePassthrough()
        .assign(
            # Primeira camada de análise
            estatisticas_basicas=RunnableLambda(lambda texto: {
                "comprimento": len(texto),
                "palavras": len(texto.split()),
                "caracteres_sem_espaco": len(texto.replace(" ", ""))
            })
        )
        .assign(
            # Segunda camada de análise
            analise_semantica=RunnableLambda(lambda dados: {
                "tem_pontuacao": any(c in dados["input"] for c in "!?.,;:"),
                "palavras_por_caractere": round(dados["estatisticas_basicas"]["palavras"] / dados["estatisticas_basicas"]["comprimento"], 3),
                "densidade_texto": round(dados["estatisticas_basicas"]["caracteres_sem_espaco"] / dados["estatisticas_basicas"]["comprimento"], 3)
            })
        )
        .assign(
            # Terceira camada - resumo executivo
            resumo=RunnableLambda(lambda dados: {
                "texto_curto": dados["estatisticas_basicas"]["comprimento"] < 50,
                "denso": dados["analise_semantica"]["densidade_texto"] > 0.7,
                "complexidade": "alta" if dados["estatisticas_basicas"]["palavras"] > 10 else "baixa"
            })
        )
    )

    resultado_cascata = pipeline_cascata.invoke(frase)  # type: ignore

    print("Resultado do pipeline em cascata:")
    print(f"  Estatísticas básicas: {resultado_cascata['estatisticas_basicas']}")
    print(f"  Análise semântica: {resultado_cascata['analise_semantica']}")
    print(f"  Resumo: {resultado_cascata['resumo']}")

    # 5. Demonstração de como usar os dados preservados em um prompt
    print("\n5. Simulação de uso em um prompt:")
    print("-" * 40)

    # Simula um prompt que usa todos os dados preservados
    prompt_simulado = f"""
    Análise da frase: "{resultado_cascata['input']}"
    
    Estatísticas:
    - Comprimento: {resultado_cascata['estatisticas_basicas']['comprimento']} caracteres
    - Palavras: {resultado_cascata['estatisticas_basicas']['palavras']}
    - Caracteres sem espaço: {resultado_cascata['estatisticas_basicas']['caracteres_sem_espaco']}
    
    Análise semântica:
    - Tem pontuação: {resultado_cascata['analise_semantica']['tem_pontuacao']}
    - Palavras por caractere: {resultado_cascata['analise_semantica']['palavras_por_caractere']}
    - Densidade do texto: {resultado_cascata['analise_semantica']['densidade_texto']}
    
    Resumo:
    - Texto curto: {resultado_cascata['resumo']['texto_curto']}
    - Denso: {resultado_cascata['resumo']['denso']}
    - Complexidade: {resultado_cascata['resumo']['complexidade']}
    """

    print(prompt_simulado)

    return resultado_cascata


def demonstrar_caso_uso_real():
    """Demonstra um caso de uso real onde RunnablePassthrough().assign() é útil.
    """
    print("\n" + "=" * 60)
    print("CASO DE USO REAL: Análise de Texto para Classificação")
    print("=" * 60)

    # Simula um sistema de classificação de textos
    textos_exemplo = [
        "Python é uma linguagem de programação incrível!",
        "A inteligência artificial está revolucionando o mundo.",
        "Olá, como você está hoje?",
        "Este é um texto muito longo que contém muitas palavras e informações detalhadas sobre diversos tópicos interessantes."
    ]

    # Pipeline de análise para classificação
    pipeline_classificacao = (
        RunnablePassthrough()
        .assign(
            # Extrai características do texto
            caracteristicas=RunnableLambda(lambda texto: {
                "comprimento": len(texto),
                "palavras": len(texto.split()),
                "tem_exclamacao": "!" in texto,
                "tem_interrogacao": "?" in texto,
                "palavra_mais_longa": max(texto.split(), key=len),
                "comprimento_medio_palavras": round(sum(len(p) for p in texto.split()) / len(texto.split()), 2)
            })
        )
        .assign(
            # Classifica o texto baseado nas características
            classificacao=RunnableLambda(lambda dados: {
                "tipo": "exclamativo" if dados["caracteristicas"]["tem_exclamacao"] else
                        "interrogativo" if dados["caracteristicas"]["tem_interrogacao"] else
                        "declarativo",
                "complexidade": "alta" if dados["caracteristicas"]["palavras"] > 15 else
                               "média" if dados["caracteristicas"]["palavras"] > 8 else "baixa",
                "sentimento": "positivo" if any(palavra in dados["input"].lower() for palavra in ["incrível", "revolucionando", "interessantes"]) else "neutro"
            })
        )
    )

    print("Análise e classificação dos textos:\n")

    for i, texto in enumerate(textos_exemplo, 1):
        resultado = pipeline_classificacao.invoke(texto)  # type: ignore

        print(f"Texto {i}: '{texto}'")
        print(f"  Características: {resultado['caracteristicas']}")
        print(f"  Classificação: {resultado['classificacao']}")
        print()


if __name__ == "__main__":
    # Executa as demonstrações
    resultado_principal = demonstrar_runnable_passthrough_assign()
    demonstrar_caso_uso_real()

    print("\n" + "=" * 60)
    print("RESUMO: Vantagens do RunnablePassthrough().assign()")
    print("=" * 60)
    print("✅ Preserva dados originais intactos")
    print("✅ Permite adicionar novos resultados incrementalmente")
    print("✅ Facilita a criação de pipelines complexos")
    print("✅ Mantém rastreabilidade dos dados")
    print("✅ Ideal para workflows de múltiplas etapas")
    print("✅ Permite reutilização de dados em diferentes pontos")
    print("✅ Facilita debugging e manutenção")
