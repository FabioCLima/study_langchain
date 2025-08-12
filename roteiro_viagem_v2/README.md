# Roteiro Viagem v2 - Configuração

## Configuração do Projeto

Este módulo gerencia as configurações do projeto usando Pydantic para validação de tipos e variáveis de ambiente.

### Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:

```bash
# Configurações da API OpenAI
OPENAI_API_KEY=your_openai_api_key_here

# Configurações da LangChain
LANGCHAIN_API_KEY=your_langchain_api_key_here
LANGCHAIN_PROJECT=roteiro_viagem_v2

# Configurações do modelo (opcionais)
MODEL_NAME=gpt-4.1
TEMPERATURE=0.3
MAX_TOKENS=1024
```

### Uso

```python
from roteiro_viagem_v2.config import settings

# Acessar configurações
api_key = settings.openai_api_key.get_secret_value()
model = settings.model_name
temp = settings.temperature
```

### Instalação

```bash
pip install -r requirements.txt
```

### Estrutura

- `Settings`: Classe principal com validação de tipos
- `Config`: Classe aninhada para configurações de arquivo de ambiente
- `settings`: Instância global das configurações
