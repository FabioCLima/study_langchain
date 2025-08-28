"""Define os modelos de dados Pydantic para a aplicação."""

from pydantic import BaseModel, Field


class Pais(BaseModel):
    """Representa os dados estruturados de um país."""
    nome: str = Field(..., description="Nome do país")
    capital: str = Field(..., description="Capital do país")

class Curiosidade(BaseModel):
    """Representa uma curiosidade sobre uma cidade."""
    curiosidade: str = Field(..., description="Curiosidade sobre a cidade")

class ResultadoFinal(BaseModel):
    """Modelo de saída final da pipeline."""
    pais: str = Field(..., description="Nome do país")
    capital: str = Field(..., description="Capital do país")
    curiosidade: str = Field(..., description="Curiosidade sobre a capital")
