"""Ferramentas customizadas e externas utilizadas pelo agente de pesquisa."""

from datetime import datetime

from langchain.tools import tool
from langchain_community.tools import DuckDuckGoSearchRun, WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper


# ---------------------------------------------------------------------------- #
# Função customizada para salvar resultados em arquivo
# ---------------------------------------------------------------------------- #
@tool("save_text_to_file", return_direct=False)
def save_to_txt(data: str, filename: str | None = "research_output.txt") -> str:
    """Salva dados estruturados em um arquivo .txt com timestamp.

    Args:
        data (str): Texto a ser salvo.
        filename (str, opcional): Nome do arquivo destino. Padrão: "research_output.txt".

    Returns:
        str: Mensagem de confirmação.

    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted_text = f"--- Research Output ---\nTimestamp: {timestamp}\n\n{data}\n\n"

    with open(filename, "a", encoding="utf-8") as f:
        f.write(formatted_text)

    return f"✅ Data successfully saved to {filename}"


# ---------------------------------------------------------------------------- #
# Ferramenta de busca na web (DuckDuckGo)
# ---------------------------------------------------------------------------- #
search_tool = DuckDuckGoSearchRun(name="search")


# ---------------------------------------------------------------------------- #
# Ferramenta de consulta ao Wikipedia
# ---------------------------------------------------------------------------- #
wiki_api = WikipediaAPIWrapper(top_k_results=1, doc_content_chars_max=1000)
wiki_tool = WikipediaQueryRun(api_wrapper=wiki_api, name="wikipedia")
