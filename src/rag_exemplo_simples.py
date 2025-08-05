"""
RAG + Zero Prompting + Tools + Chain of Thought
Exemplo prático combinando todas as técnicas
"""

import math
import os

from langchain.agents import AgentType, initialize_agent
from langchain.chains import RetrievalQA
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.llms import OpenAI
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.tools import Tool
from langchain.vectorstores import FAISS

# * Carrega as variáveis de ambiente
_ = load_dotenv(find_dotenv())

# * Verifica se a API key está configurada
if not os.getenv("OPENAI_API_KEY"):
    raise ValueError("OPENAI_API_KEY não encontrada no arquivo .env")

print("=== RAG + Zero Prompting + Tools + Chain of Thought ===\n")

# 1. CRIANDO BASE DE CONHECIMENTO (RAG)
print("1. Criando base de conhecimento...")

documentos = [
    "A velocidade da luz no vácuo é 299.792.458 metros por segundo. É uma constante fundamental da física.",
    "A fórmula da energia cinética é E = (1/2) * m * v², onde m é a massa e v é a velocidade.",
    "A lei de Ohm estabelece que V = I * R, onde V é tensão, I é corrente e R é resistência.",
    "O teorema de Pitágoras diz que em um triângulo retângulo, a² + b² = c², onde c é a hipotenusa.",
    "A área de um círculo é π * r², onde r é o raio do círculo.",
    "A força gravitacional entre dois objetos é F = G * (m1 * m2) / r², onde G é a constante gravitacional.",
]

# Converter em Documents
docs = [Document(page_content=doc) for doc in documentos]

# Dividir em chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=20)
textos = text_splitter.split_documents(docs)
print(f"✓ Criados {len(textos)} chunks de texto")

# Criar vectorstore
try:
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_documents(textos, embeddings)
    print("✓ Vectorstore criado com sucesso!")
except Exception as e:
    print(f"❌ Erro ao criar vectorstore: {e}")
    print("   Configure sua OPENAI_API_KEY para continuar")
    exit()

# 2. CRIANDO TOOLS (FERRAMENTAS)
print("\n2. Criando ferramentas de cálculo...")


def calcular_energia_cinetica(massa: float, velocidade: float) -> float:
    """Calcula energia cinética usando E = (1/2) * m * v²"""
    return 0.5 * massa * (velocidade**2)


def calcular_area_circulo(raio: float) -> float:
    """Calcula área de um círculo usando π * r²"""
    return math.pi * (raio**2)


def teorema_pitagoras(a: float, b: float) -> float:
    """Calcula hipotenusa usando a² + b² = c²"""
    return math.sqrt(a**2 + b**2)


# Criar tools do LangChain
tool_energia = Tool(
    name="Calculadora_Energia_Cinetica",
    description="Calcula energia cinética. Use: 'massa,velocidade' (ex: '10,5' para 10kg e 5m/s)",
    func=lambda x: calcular_energia_cinetica(*[float(i) for i in x.split(",")]),
)

tool_area = Tool(
    name="Calculadora_Area_Circulo",
    description="Calcula área de círculo. Use apenas o raio (ex: '5' para raio=5)",
    func=lambda x: calcular_area_circulo(float(x)),
)

tool_pitagoras = Tool(
    name="Teorema_Pitagoras",
    description="Calcula hipotenusa. Use: 'cateto1,cateto2' (ex: '3,4')",
    func=lambda x: teorema_pitagoras(*[float(i) for i in x.split(",")]),
)

tools = [tool_energia, tool_area, tool_pitagoras]
print(f"✓ Criadas {len(tools)} ferramentas de cálculo")

# 3. CONFIGURANDO RAG CHAIN
print("\n3. Configurando RAG...")

llm = OpenAI(temperature=0.1)
retriever = vectorstore.as_retriever(search_kwargs={"k": 2})

# Criar RAG chain
rag_chain = RetrievalQA.from_chain_type(
    llm=llm, chain_type="stuff", retriever=retriever, return_source_documents=True
)

# Tool para RAG
rag_tool = Tool(
    name="Consulta_Base_Conhecimento",
    description="Busca informações na base de conhecimento sobre física e matemática",
    func=lambda x: rag_chain.run(x),
)

all_tools = tools + [rag_tool]
print(f"✓ RAG configurado com {len(all_tools)} ferramentas totais")

# 4. CRIANDO AGENT COM CHAIN OF THOUGHT
print("\n4. Criando agent com Chain of Thought...")

# Prompt que incentiva Chain of Thought (Zero Prompting)
system_prompt = """
Você é um assistente de física e matemática que sempre:
1. Primeiro busca informações relevantes na base de conhecimento
2. Explica seu raciocínio passo a passo
3. Usa ferramentas de cálculo quando necessário
4. Mostra os cálculos e resultados claramente

SEMPRE siga este processo de pensamento:
- Passo 1: Identificar o que precisa ser resolvido
- Passo 2: Buscar fórmulas ou conceitos relevantes
- Passo 3: Aplicar cálculos se necessário
- Passo 4: Verificar e explicar o resultado
"""

# Criar agent
agent = initialize_agent(
    tools=all_tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    handle_parsing_errors=True,
)

print("✓ Agent configurado com sucesso!")

# 5. EXEMPLOS PRÁTICOS
print("\n" + "=" * 60)
print("EXEMPLOS PRÁTICOS")
print("=" * 60)

# Exemplo 1: RAG + CoT + Tool
print("\n🔬 EXEMPLO 1: Energia Cinética")
print("-" * 40)

pergunta1 = """
Explique a fórmula da energia cinética e calcule a energia cinética 
de um objeto de 5kg movendo-se a 10 m/s.
"""

try:
    resultado1 = agent.run(system_prompt + pergunta1)
    print(f"\n✅ Resultado: {resultado1}")
except Exception as e:
    print(f"❌ Erro: {e}")

# Exemplo 2: Teorema de Pitágoras
print("\n📐 EXEMPLO 2: Teorema de Pitágoras")
print("-" * 40)

pergunta2 = """
Preciso calcular a hipotenusa de um triângulo retângulo com catetos 
de 6 e 8 metros. Primeiro me explique o teorema envolvido.
"""

try:
    resultado2 = agent.run(system_prompt + pergunta2)
    print(f"\n✅ Resultado: {resultado2}")
except Exception as e:
    print(f"❌ Erro: {e}")

# Exemplo 3: Área do círculo
print("\n⭕ EXEMPLO 3: Área do Círculo")
print("-" * 40)

pergunta3 = """
Qual é a fórmula para calcular a área de um círculo e qual seria 
a área de um círculo com raio de 3 metros?
"""

try:
    resultado3 = agent.run(system_prompt + pergunta3)
    print(f"\n✅ Resultado: {resultado3}")
except Exception as e:
    print(f"❌ Erro: {e}")

print("\n" + "=" * 60)
print("ANÁLISE DOS COMPONENTES")
print("=" * 60)

print("""
🔍 RAG (Retrieval-Augmented Generation):
   - Busca informações relevantes nos documentos indexados
   - Fornece contexto atualizado para o LLM
   - Reduz alucinações ao basear respostas em dados reais

💭 Zero Prompting:
   - Não usa exemplos específicos no prompt
   - Confia na capacidade natural do LLM de seguir instruções
   - Mais flexível que few-shot prompting

🛠️ Tools:
   - Permitem cálculos precisos
   - Estendem capacidades do LLM
   - Fornecem resultados determinísticos

🧠 Chain of Thought:
   - Força o modelo a explicar seu raciocínio
   - Melhora a qualidade das respostas
   - Torna o processo transparente e auditável
""")

print("\n✨ Exemplo criado com sucesso!")
print("Para executar: python rag_exemplo_simples.py")
