# Correção do erro na Célula 5 do langchain_review_exercises.ipynb

logs = []

def log_and_pass(text: str) -> str:
    """Log simples que passa o texto adiante"""
    print(f"[LOG] Tradução gerada: {text}")
    return text  # Importante: retornar o texto para continuar a cadeia
    
# Cadeia com log simples
model = ChatOpenAI(model="gpt-4.1", temperature=0.0)
translator_template = ChatPromptTemplate.from_messages(
    [
        ("system", "Você é um tradutor especializado. Traduza o texto para {idioma}."),
        ("human", "{texto}")
    ]
)
parser_output = StrOutputParser()

# Adicionando log após o parse
translator_chain_with_log = (
    translator_template
    | model
    | parser_output 
    | RunnableLambda(log_and_pass)
)

# ❌ ERRO ORIGINAL:
# response = translator_chain.invoke({"texto": "Hello, how are you today?", "idioma": "português"})

# ✅ CORREÇÃO:
response = translator_chain_with_log.invoke({"texto": "Hello, how are you today?", "idioma": "português"})
print(response)

print("\n=== LOGS ===")
print(f"Logs salvos: {logs}") 