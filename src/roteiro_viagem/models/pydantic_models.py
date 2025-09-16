"""Pydantic models for the Roteiro de Viagem - estruturas de dados
"""

from pydantic import BaseModel, Field


# !============================================================================
# ! Estruturas de Dados
# ! =============================================================================
# * Chain 1 - Destino
class Destino(BaseModel):
    cidade: str = Field(description="Nome da cidade recomendada.")
    motivo: str = Field(description="Motivo da recomendação da cidade.")


# * Chain 2 - Lista de Restaurantes
class Restaurante(BaseModel):
    nome: str = Field(description="Nome do restaurante.")
    tipo: str = Field(description="Tipo de culinária do restaurante.")
    descricao: str = Field(description="Descrição do restaurante.")


class ListaRestaurantes(BaseModel):
    restaurantes: list[Restaurante]


# * Chain 3 - Atrações
class Atracao(BaseModel):
    nome: str
    descricao: str


class ListaAtracoes(BaseModel):
    atracoes: list[Atracao]
