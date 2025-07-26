"""
Few-Shot Prompting com LangChain - Exemplo Didático
Demonstra como usar exemplos para treinar o modelo a seguir um padrão específico
"""

from langchain.prompts import FewShotPromptTemplate, PromptTemplate

# Exemplo 1: Few-Shot básico para classificação de sentimentos
def exemplo_classificacao_sentimentos():
    """
    Ensina o modelo a classificar sentimentos usando exemplos
    """
    
    # Exemplos que "ensinam" o modelo
    examples = [
        {
            "texto": "Eu amo este produto! É incrível!",
            "sentimento": "Positivo"
        },
        {
            "texto": "Este produto é terrível, não recomendo.",
            "sentimento": "Negativo"
        },
        {
            "texto": "O produto é ok, nada especial.",
            "sentimento": "Neutro"
        }
    ]
    
    # Template para cada exemplo
    example_prompt = PromptTemplate(
        input_variables=["texto", "sentimento"],
        template="Texto: {texto}\nSentimento: {sentimento}"
    )
    
    # Template Few-Shot completo
    few_shot_prompt = FewShotPromptTemplate(
        examples=examples,
        example_prompt=example_prompt,
        prefix="Classifique o sentimento dos seguintes textos:\n\n",
        suffix="Texto: {input}\nSentimento:",
        input_variables=["input"],
        example_separator="\n\n"
    )
    
    # Teste
    prompt = few_shot_prompt.format(input="Estou muito feliz com minha compra!")
    print("=== EXEMPLO 1: Classificação de Sentimentos ===")
    print(prompt)
    print("\n")
