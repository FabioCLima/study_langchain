"""Módulo que define as estruturas de dados Pydantic para o projeto"""

from pydantic import BaseModel, Field


# * Modelo de dados Pydantic
class AnimalNome(BaseModel):
    """Representa apenas o nome de um animal."""

    nome: str = Field(description="O nome do animal.")


class AnimalDescricao(BaseModel):
    """Representa a descrição de um animal."""

    nome: str = Field(description="O nome do animal.")
    descricao: str = Field(description="Uma descrição curta sobre o animal.")
