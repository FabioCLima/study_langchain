# study_langchain/langchain_ex1.py

from contextlib import redirect_stdout
from io import StringIO

from openai_client import create_analytical_model

# * Sem logs de debug ou prints
with redirect_stdout(StringIO()):
    model = create_analytical_model()

if model:
    resposta = model.invoke("Qual é a maior cidade do mundo?")
    print(str(resposta.content))  # type: ignore
