# 🗺️ Roteiro de Viagem - Projeto LangChain

## 📖 Sobre o Projeto

Este projeto demonstra como usar o LangChain para criar um sistema inteligente de recomendação de viagens. Ele recebe um interesse de atividade do usuário e gera automaticamente um roteiro completo com destino, restaurantes e passeios culturais.

## 🚀 Como Usar

### 1. Configuração
```bash
# Criar arquivo .env
OPENAI_API_KEY=sua_chave_aqui
LANGCHAIN_API_KEY=sua_chave_langsmith
```

### 2. Execução
```bash
python main.py "trekking na montanha"
```

## 🏗️ Arquitetura

- **Models**: Estruturas Pydantic para validação de dados
- **Chains**: Componentes LangChain para cada funcionalidade
- **Orchestrator**: Coordena todas as chains
- **Utils**: Configuração, logging e setup do LLM

## 🎓 Conceitos LangChain Aprendidos

1. **Chain Composition**: Como conectar prompts, modelos e parsers
2. **Output Parsing**: Conversão de respostas para estruturas Pydantic
3. **Error Handling**: Tratamento de falhas com fallbacks
4. **Logging**: Observabilidade e debugging
5. **Configuration**: Gerenciamento centralizado de configurações

## 📚 Documentação Completa

Veja `DOCUMENTACAO_DIDATICA.md` para explicações detalhadas e `EXERCICIOS_PRATICOS.md` para exercícios práticos.
