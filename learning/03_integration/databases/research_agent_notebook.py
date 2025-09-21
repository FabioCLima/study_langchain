# Agente Pesquisador Inteligente usando LangGraph
# Exemplo Didático com Tool Use e Reflection Patterns

"""
Este notebook demonstra a implementação de um agente de IA que combina:
1. Tool Use Pattern: Para buscar informações e fazer cálculos
2. Reflection Pattern: Para avaliar e melhorar suas respostas

O agente pode pesquisar informações, analisar dados e refinar suas conclusões.
"""

# =============================================================================
# SEÇÃO 1: INSTALAÇÃO E CONFIGURAÇÃO
# =============================================================================

# Execute no terminal ou primeira célula:
# !pip install langchain-openai langgraph langchain-core python-dotenv requests

import os
import json
import requests
from typing import List, Dict, Any, Optional, Literal, TypedDict
from datetime import datetime
import logging

# LangChain e LangGraph imports
from langchain_openai import ChatOpenAI
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage
from langchain_core.tools import tool
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuração da API Key (coloque sua chave da OpenAI)
# Recomenda-se usar um arquivo .env para isso
os.environ["OPENAI_API_KEY"] = "sua-chave-openai-aqui"

print("✅ Dependências carregadas com sucesso!")

# =============================================================================
# SEÇÃO 2: DEFINIÇÃO DO ESTADO DO AGENTE
# =============================================================================

class ResearchAgentState(TypedDict):
    """
    Estado do agente de pesquisa que mantém todas as informações necessárias
    durante o fluxo de execução.
    
    Attributes:
        messages: Lista de mensagens na conversa
        research_query: Consulta de pesquisa atual
        search_results: Resultados da busca
        draft_response: Rascunho da resposta
        reflection: Análise crítica da resposta
        final_response: Resposta final refinada
        iteration_count: Número de iterações de refinamento
        max_iterations: Máximo de iterações permitidas
        tools_used: Lista de ferramentas utilizadas
        confidence_score: Pontuação de confiança na resposta (0-10)
    """
    messages: List[BaseMessage]
    research_query: str
    search_results: List[Dict[str, Any]]
    draft_response: str
    reflection: str
    final_response: str
    iteration_count: int
    max_iterations: int
    tools_used: List[str]
    confidence_score: float

print("✅ Estado do agente definido!")

# =============================================================================
# SEÇÃO 3: DEFINIÇÃO DAS FERRAMENTAS (TOOL USE PATTERN)
# =============================================================================

@tool
def web_search_simulator(query: str) -> str:
    """
    Simula uma busca na web retornando resultados fictícios mas realistas.
    
    Em um ambiente real, você integraria com APIs como Google Search, Bing, etc.
    
    Args:
        query: Termo de busca
        
    Returns:
        Resultados da busca em formato JSON string
    """
    # Simulação de resultados baseados na query
    mock_results = {
        "inteligência artificial": [
            {
                "title": "IA na Educação: Transformando o Aprendizado",
                "snippet": "A inteligência artificial está revolucionando a educação com personalização de aprendizado e tutoria inteligente.",
                "source": "TechEducation.com"
            },
            {
                "title": "Benefícios e Desafios da IA",
                "snippet": "IA oferece automação e insights, mas levanta questões éticas e de emprego.",
                "source": "AIResearch.org"
            }
        ],
        "mudanças climáticas": [
            {
                "title": "Impactos Globais das Mudanças Climáticas",
                "snippet": "Temperatura global aumentou 1.1°C desde 1880, afetando ecossistemas mundialmente.",
                "source": "ClimateScience.gov"
            },
            {
                "title": "Soluções para o Clima",
                "snippet": "Energias renováveis e eficiência energética são chaves para mitigação climática.",
                "source": "GreenTech.net"
            }
        ],
        "default": [
            {
                "title": f"Informações sobre {query}",
                "snippet": f"Dados relevantes encontrados sobre {query} incluindo aspectos técnicos e práticos.",
                "source": "GeneralKnowledge.com"
            }
        ]
    }
    
    # Seleciona resultados baseados na query
    for key in mock_results:
        if key in query.lower():
            results = mock_results[key]
            break
    else:
        results = mock_results["default"]
    
    logger.info(f"🔍 Busca realizada para: {query}")
    return json.dumps(results, ensure_ascii=False, indent=2)

@tool
def calculate_metrics(numbers: List[float], operation: str) -> str:
    """
    Realiza cálculos estatísticos básicos em uma lista de números.
    
    Args:
        numbers: Lista de números para calcular
        operation: Tipo de operação ('mean', 'sum', 'max', 'min', 'median')
        
    Returns:
        Resultado do cálculo
    """
    if not numbers:
        return "Erro: Lista de números vazia"
    
    try:
        if operation == "mean":
            result = sum(numbers) / len(numbers)
        elif operation == "sum":
            result = sum(numbers)
        elif operation == "max":
            result = max(numbers)
        elif operation == "min":
            result = min(numbers)
        elif operation == "median":
            sorted_nums = sorted(numbers)
            n = len(sorted_nums)
            if n % 2 == 0:
                result = (sorted_nums[n//2 - 1] + sorted_nums[n//2]) / 2
            else:
                result = sorted_nums[n//2]
        else:
            return f"Erro: Operação '{operation}' não suportada"
        
        logger.info(f"🧮 Calculado {operation} de {numbers}: {result}")
        return f"Resultado da operação '{operation}': {result}"
    
    except Exception as e:
        return f"Erro no cálculo: {str(e)}"

@tool
def fact_checker(claim: str) -> str:
    """
    Simula verificação de fatos para uma afirmação.
    
    Args:
        claim: Afirmação a ser verificada
        
    Returns:
        Status de verificação da afirmação
    """
    # Simulação simples de fact-checking
    fact_database = {
        "terra é redonda": "VERDADEIRO - Confirmado por evidências científicas",
        "temperatura global": "VERDADEIRO - Dados confirmados por organizações climáticas",
        "ia substitui humanos": "PARCIALMENTE VERDADEIRO - IA automatiza tarefas específicas, não substitui completamente",
        "vacinas": "VERDADEIRO - Eficácia comprovada cientificamente"
    }
    
    claim_lower = claim.lower()
    for key, value in fact_database.items():
        if key in claim_lower:
            logger.info(f"✅ Verificação realizada para: {claim}")
            return f"Verificação: {value}"
    
    return "NECESSITA VERIFICAÇÃO - Não há dados suficientes na base de conhecimento"

# Lista de todas as ferramentas disponíveis
AVAILABLE_TOOLS = [web_search_simulator, calculate_metrics, fact_checker]

print("✅ Ferramentas definidas!")

# =============================================================================
# SEÇÃO 4: CONFIGURAÇÃO DO MODELO E FERRAMENTAS
# =============================================================================

def setup_llm_with_tools() -> ChatOpenAI:
    """
    Configura o modelo de linguagem com as ferramentas disponíveis.
    
    Returns:
        Modelo ChatOpenAI configurado com ferramentas
    """
    llm = ChatOpenAI(
        model="gpt-4",
        temperature=0.1,  # Baixa temperatura para maior consistência
        timeout=60
    )
    
    # Vincula as ferramentas ao modelo
    llm_with_tools = llm.bind_tools(AVAILABLE_TOOLS)
    
    logger.info("🤖 Modelo configurado com ferramentas")
    return llm_with_tools

# Instancia o modelo
llm_with_tools = setup_llm_with_tools()

print("✅ Modelo configurado!")

# =============================================================================
# SEÇÃO 5: FUNÇÕES DOS NÓS DO GRAFO
# =============================================================================

def query_analyzer_node(state: ResearchAgentState) -> Dict[str, Any]:
    """
    Analisa a consulta do usuário e determina a estratégia de pesquisa.
    
    Args:
        state: Estado atual do agente
        
    Returns:
        Estado atualizado com análise da consulta
    """
    user_message = state["messages"][-1].content if state["messages"] else ""
    
    analysis_prompt = f"""
    Analise a seguinte consulta do usuário e determine:
    1. Qual é a intenção principal da pergunta?
    2. Que tipo de informações precisamos buscar?
    3. Quais ferramentas seriam mais úteis?
    
    Consulta: {user_message}
    
    Forneça uma análise estruturada.
    """
    
    system_message = SystemMessage(content="Você é um analisador de consultas especializado.")
    analysis_message = HumanMessage(content=analysis_prompt)
    
    response = llm_with_tools.invoke([system_message, analysis_message])
    
    # Extrai a consulta principal para pesquisa
    research_query = user_message  # Simplificado para este exemplo
    
    logger.info(f"🔍 Consulta analisada: {research_query}")
    
    return {
        **state,
        "research_query": research_query,
        "tools_used": ["query_analysis"]
    }

def research_node(state: ResearchAgentState) -> Dict[str, Any]:
    """
    Executa a pesquisa usando as ferramentas disponíveis (Tool Use Pattern).
    
    Args:
        state: Estado atual do agente
        
    Returns:
        Estado atualizado com resultados da pesquisa
    """
    query = state["research_query"]
    
    # Prompt para o agente decidir quais ferramentas usar
    research_prompt = f"""
    Você precisa pesquisar informações sobre: {query}
    
    Use as ferramentas disponíveis para coletar dados relevantes:
    - web_search_simulator: para buscar informações gerais
    - calculate_metrics: para cálculos se necessário
    - fact_checker: para verificar informações
    
    Comece com uma busca web sobre o tópico.
    """
    
    system_message = SystemMessage(content="Você é um pesquisador que usa ferramentas para coletar informações.")
    research_message = HumanMessage(content=research_prompt)
    
    response = llm_with_tools.invoke([system_message, research_message])
    
    # Se há tool calls, executa as ferramentas
    if hasattr(response, 'tool_calls') and response.tool_calls:
        tool_node = ToolNode(AVAILABLE_TOOLS)
        tool_results = tool_node.invoke({"messages": [response]})
        
        # Processa os resultados das ferramentas
        search_results = []
        for message in tool_results["messages"]:
            if hasattr(message, 'content'):
                try:
                    # Tenta fazer parse se for JSON
                    result = json.loads(message.content)
                    if isinstance(result, list):
                        search_results.extend(result)
                    else:
                        search_results.append(result)
                except json.JSONDecodeError:
                    # Se não for JSON, adiciona como texto
                    search_results.append({"content": message.content})
    else:
        search_results = [{"content": "Nenhuma ferramenta foi utilizada"}]
    
    logger.info(f"📊 Pesquisa concluída com {len(search_results)} resultados")
    
    return {
        **state,
        "search_results": search_results,
        "tools_used": state["tools_used"] + ["web_search"]
    }

def draft_generator_node(state: ResearchAgentState) -> Dict[str, Any]:
    """
    Gera um rascunho de resposta baseado nos resultados da pesquisa.
    
    Args:
        state: Estado atual do agente
        
    Returns:
        Estado atualizado com rascunho da resposta
    """
    query = state["research_query"]
    search_results = state["search_results"]
    
    # Formata os resultados da pesquisa
    formatted_results = "\n".join([
        f"- {result.get('title', 'Info')}: {result.get('snippet', result.get('content', 'N/A'))}"
        for result in search_results
    ])
    
    draft_prompt = f"""
    Com base na pesquisa realizada, elabore uma resposta completa e informativa para a pergunta: {query}
    
    Dados coletados:
    {formatted_results}
    
    Sua resposta deve ser:
    - Precisa e baseada nos dados coletados
    - Bem estruturada e fácil de entender
    - Incluir fontes quando relevante
    - Abordar diferentes aspectos do tópico
    """
    
    system_message = SystemMessage(content="Você é um especialista em sintetizar informações de pesquisa.")
    draft_message = HumanMessage(content=draft_prompt)
    
    draft_response = llm_with_tools.invoke([system_message, draft_message])
    
    logger.info("📝 Rascunho da resposta gerado")
    
    return {
        **state,
        "draft_response": draft_response.content,
        "iteration_count": 1
    }

def reflection_node(state: ResearchAgentState) -> Dict[str, Any]:
    """
    Aplica o Reflection Pattern para avaliar e melhorar a resposta.
    
    Args:
        state: Estado atual do agente
        
    Returns:
        Estado atualizado com reflexão sobre a resposta
    """
    draft = state["draft_response"]
    query = state["research_query"]
    
    reflection_prompt = f"""
    Analise criticamente a seguinte resposta para a pergunta: "{query}"
    
    RESPOSTA A SER ANALISADA:
    {draft}
    
    Avalie os seguintes aspectos e dê uma nota de 0 a 10:
    1. PRECISÃO: As informações estão corretas e bem fundamentadas?
    2. COMPLETUDE: A resposta aborda todos os aspectos importantes?
    3. CLAREZA: A explicação é fácil de entender?
    4. ESTRUTURA: A organização do texto é lógica?
    5. RELEVÂNCIA: O conteúdo responde diretamente à pergunta?
    
    Forneça:
    - Uma nota geral de 0 a 10
    - Pontos fortes identificados
    - Áreas específicas que precisam de melhoria
    - Sugestões concretas de como melhorar
    """
    
    system_message = SystemMessage(content="Você é um crítico especializado em avaliar qualidade de respostas.")
    reflection_message = HumanMessage(content=reflection_prompt)
    
    reflection_response = llm_with_tools.invoke([system_message, reflection_message])
    
    # Extrai a pontuação de confiança (simplificado)
    confidence_score = 7.0  # Por padrão, assumimos uma confiança média
    content = reflection_response.content.lower()
    
    # Busca por padrões de pontuação no texto
    import re
    scores = re.findall(r'(?:nota|score|pontuação)[:\s]*([0-9]+(?:\.[0-9]+)?)', content)
    if scores:
        try:
            confidence_score = float(scores[0])
        except ValueError:
            pass
    
    logger.info(f"🤔 Reflexão realizada - Confiança: {confidence_score}")
    
    return {
        **state,
        "reflection": reflection_response.content,
        "confidence_score": confidence_score
    }

def revision_node(state: ResearchAgentState) -> Dict[str, Any]:
    """
    Revisa e melhora a resposta com base na reflexão.
    
    Args:
        state: Estado atual do agente
        
    Returns:
        Estado atualizado com resposta revisada
    """
    draft = state["draft_response"]
    reflection = state["reflection"]
    query = state["research_query"]
    
    revision_prompt = f"""
    Melhore a seguinte resposta incorporando as críticas e sugestões fornecidas:
    
    PERGUNTA ORIGINAL: {query}
    
    RESPOSTA ATUAL:
    {draft}
    
    ANÁLISE CRÍTICA:
    {reflection}
    
    Reescreva a resposta implementando as melhorias sugeridas. Mantenha o que está bom e melhore o que foi criticado.
    """
    
    system_message = SystemMessage(content="Você é um editor especializado em melhorar textos baseado em feedback.")
    revision_message = HumanMessage(content=revision_prompt)
    
    revised_response = llm_with_tools.invoke([system_message, revision_message])
    
    logger.info("✏️ Resposta revisada")
    
    return {
        **state,
        "draft_response": revised_response.content,
        "iteration_count": state["iteration_count"] + 1
    }

def finalization_node(state: ResearchAgentState) -> Dict[str, Any]:
    """
    Finaliza a resposta e prepara o resultado final.
    
    Args:
        state: Estado atual do agente
        
    Returns:
        Estado final com resposta completa
    """
    final_response = state["draft_response"]
    tools_used = state["tools_used"]
    confidence = state["confidence_score"]
    iterations = state["iteration_count"]
    
    # Adiciona metadados à resposta final
    metadata = f"""
    
    ---
    📊 Metadados da Pesquisa:
    • Ferramentas utilizadas: {', '.join(tools_used)}
    • Iterações de refinamento: {iterations}
    • Confiança na resposta: {confidence}/10
    • Processado em: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    """
    
    final_with_metadata = final_response + metadata
    
    logger.info("🎯 Resposta finalizada")
    
    return {
        **state,
        "final_response": final_with_metadata
    }

print("✅ Funções dos nós definidas!")

# =============================================================================
# SEÇÃO 6: FUNÇÕES DE DECISÃO DO FLUXO
# =============================================================================

def should_continue_research(state: ResearchAgentState) -> Literal["draft", "research"]:
    """
    Decide se deve continuar pesquisando ou gerar rascunho.
    
    Args:
        state: Estado atual do agente
        
    Returns:
        Próximo nó do fluxo
    """
    search_results = state.get("search_results", [])
    
    # Se temos resultados, prosseguir para o rascunho
    if search_results:
        return "draft"
    else:
        return "research"

def should_revise(state: ResearchAgentState) -> Literal["revision", "finalize"]:
    """
    Decide se a resposta precisa ser revisada ou pode ser finalizada.
    
    Args:
        state: Estado atual do agente
        
    Returns:
        Próximo nó do fluxo
    """
    confidence = state.get("confidence_score", 0)
    iterations = state.get("iteration_count", 0)
    max_iterations = state.get("max_iterations", 2)
    
    # Se confiança é baixa e não excedeu max iterações, revisar
    if confidence < 7.0 and iterations < max_iterations:
        return "revision"
    else:
        return "finalize"

print("✅ Funções de decisão definidas!")

# =============================================================================
# SEÇÃO 7: CONSTRUÇÃO DO GRAFO DO AGENTE
# =============================================================================

def create_research_agent() -> StateGraph:
    """
    Cria e configura o grafo do agente de pesquisa.
    
    Returns:
        Grafo compilado do agente
    """
    # Cria o grafo
    workflow = StateGraph(ResearchAgentState)
    
    # Adiciona todos os nós
    workflow.add_node("analyze_query", query_analyzer_node)
    workflow.add_node("research", research_node)
    workflow.add_node("draft", draft_generator_node)
    workflow.add_node("reflect", reflection_node)
    workflow.add_node("revision", revision_node)
    workflow.add_node("finalize", finalization_node)
    
    # Define o ponto de entrada
    workflow.set_entry_point("analyze_query")
    
    # Define as conexões entre os nós
    workflow.add_edge("analyze_query", "research")
    workflow.add_conditional_edges("research", should_continue_research)
    workflow.add_edge("draft", "reflect")
    workflow.add_conditional_edges("reflect", should_revise)
    workflow.add_edge("revision", "reflect")  # Volta para reflexão após revisão
    workflow.add_edge("finalize", END)
    
    # Compila o grafo
    agent = workflow.compile()
    
    logger.info("🏗️ Agente de pesquisa construído com sucesso!")
    return agent

# Cria o agente
research_agent = create_research_agent()

print("✅ Agente de pesquisa criado!")

# =============================================================================
# SEÇÃO 8: FUNÇÃO DE EXECUÇÃO E TESTE
# =============================================================================

def run_research_agent(question: str, max_iterations: int = 2) -> Dict[str, Any]:
    """
    Executa o agente de pesquisa com uma pergunta.
    
    Args:
        question: Pergunta para pesquisar
        max_iterations: Máximo de iterações de refinamento
        
    Returns:
        Resultado completo da execução
    """
    print(f"\n🚀 Iniciando pesquisa: {question}")
    print("=" * 60)
    
    # Estado inicial
    initial_state = ResearchAgentState(
        messages=[HumanMessage(content=question)],
        research_query="",
        search_results=[],
        draft_response="",
        reflection="",
        final_response="",
        iteration_count=0,
        max_iterations=max_iterations,
        tools_used=[],
        confidence_score=0.0
    )
    
    # Executa o agente
    try:
        result = research_agent.invoke(initial_state)
        
        print("\n✅ PESQUISA CONCLUÍDA!")
        print("=" * 60)
        print(result["final_response"])
        
        return result
        
    except Exception as e:
        print(f"\n❌ Erro durante a execução: {str(e)}")
        return {"error": str(e)}

print("✅ Sistema completo configurado!")

# =============================================================================
# SEÇÃO 9: EXEMPLOS DE TESTE
# =============================================================================

# Exemplo 1: Teste básico
print("\n" + "="*80)
print("🧪 EXEMPLO 1: Teste sobre Inteligência Artificial")
print("="*80)

exemplo_1 = run_research_agent(
    "Quais são os principais benefícios da inteligência artificial na educação?",
    max_iterations=2
)

# Exemplo 2: Teste sobre tema científico
print("\n" + "="*80)
print("🧪 EXEMPLO 2: Teste sobre Mudanças Climáticas")
print("="*80)

exemplo_2 = run_research_agent(
    "Como as mudanças climáticas estão afetando os oceanos?",
    max_iterations=1
)

# =============================================================================
# SEÇÃO 10: ANÁLISE DOS RESULTADOS E PRÓXIMOS PASSOS
# =============================================================================

print("\n" + "="*80)
print("📊 ANÁLISE DOS RESULTADOS")
print("="*80)

def analyze_results(result: Dict[str, Any], example_name: str) -> None:
    """
    Analisa e apresenta os resultados de uma execução do agente.
    
    Args:
        result: Resultado da execução
        example_name: Nome do exemplo para identificação
    """
    if "error" in result:
        print(f"❌ {example_name}: Erro encontrado - {result['error']}")
        return
    
    print(f"\n📋 {example_name}:")
    print(f"   • Ferramentas usadas: {result.get('tools_used', [])}")
    print(f"   • Iterações: {result.get('iteration_count', 0)}")
    print(f"   • Confiança: {result.get('confidence_score', 0)}/10")
    print(f"   • Resultados de pesquisa: {len(result.get('search_results', []))}")

analyze_results(exemplo_1, "Exemplo IA na Educação")
analyze_results(exemplo_2, "Exemplo Mudanças Climáticas")

print("\n" + "="*80)
print("🎯 PRÓXIMOS PASSOS E MELHORIAS")
print("="*80)

print("""
Este agente demonstra os conceitos fundamentais, mas pode ser melhorado:

🔧 MELHORIAS TÉCNICAS:
   • Integrar APIs reais (Google Search, Wikipedia, etc.)
   • Adicionar mais ferramentas especializadas
   • Implementar cache de resultados
   • Melhorar análise de confiança
   • Adicionar tratamento de erros mais robusto

🎨 MELHORIAS DE UX:
   • Interface gráfica interativa
   • Streaming de respostas em tempo real
   • Visualização do grafo de execução
   • Histórico de conversas
   • Exportação de resultados

📊 MELHORIAS DE PERFORMANCE:
   • Execução paralela de ferramentas
   • Otimização de prompts
   • Modelo de linguagem fine-tuned
   • Métricas detalhadas de performance

🔒 MELHORIAS DE SEGURANÇA:
   • Validação de entrada
   • Sanitização de dados
   • Rate limiting
   • Auditoria de execuções
""")

print("\n✨ Agente de Pesquisa Inteligente executado com sucesso!")
print("📚 Este exemplo demonstra como combinar Tool Use e Reflection patterns")
print("🚀 Pronto para ser estendido com suas próprias ferramentas e casos de uso!")
