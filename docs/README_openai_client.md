# OpenAI Client Utility Module

Este módulo fornece utilitários para carregar a chave da API OpenAI de um arquivo `.env` e criar um cliente OpenAI de forma segura, didática e reutilizável.

## Objetivos Didáticos

- Demonstrar boas práticas de engenharia de software para prototipagem.
- Ensinar separação de responsabilidades (SRP) usando classes.
- Mostrar uso de tipagem, docstrings e tratamento de erros.
- Facilitar a reutilização do código em outros módulos/projetos.

## Estrutura do Módulo

- `ApiKeyLoader`: Classe responsável por carregar a chave da API do arquivo `.env`.
- `OpenAIClient`: Classe que encapsula a criação e acesso ao cliente OpenAI.

## Boas Práticas Demonstradas

- **SRP (Single Responsibility Principle):** Cada classe tem uma única responsabilidade.
- **Tipagem explícita:** Uso de tipos para maior clareza e segurança.
- **Docstrings:** Documentação clara para métodos e classes.
- **Uso de `@property`:** Permite acesso controlado ao cliente OpenAI.
- **Singleton leve:** O cliente OpenAI é criado apenas uma vez por instância.
- **Exemplo de uso separado em função:** Facilita testes e reutilização.
- **Sugestão de exceção customizada:** Para tratamento de erros mais claro.
- **Facilidade de importação:** Uso de `__all__` para expor as classes principais.

## Exemplo de Uso

```python
from openai_client import ApiKeyLoader, OpenAIClient
from pathlib import Path

loader = ApiKeyLoader(Path(".env"))
api_key = loader.get_openai_key()
client = OpenAIClient(api_key)
openai_client = client.client  # Cliente OpenAI pronto para uso
```

## Execução do Exemplo

O módulo inclui uma função `example_usage()` que demonstra o uso típico. Basta rodar:

```bash
python openai_client.py
```

## Dicas de Engenharia de Software

- Separe responsabilidades em classes e funções pequenas.
- Use tipagem e docstrings para facilitar manutenção.
- Prefira exemplos de uso em funções, não no bloco principal.
- Considere criar exceções customizadas para erros específicos.
- Organize utilitários em módulos/diretórios para facilitar prototipagem.

## Possível Exceção Customizada (Sugestão)

```python
class ApiKeyNotFoundError(Exception):
    pass
```

## Requisitos

- Python 3.10+
- `python-dotenv`
- `openai`

Instale as dependências com:

```bash
pip install python-dotenv openai
```
