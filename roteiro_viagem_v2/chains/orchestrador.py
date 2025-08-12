'''
Orquestrador de chains
'''

from langchain_core.runnables import RunnablePassthrough, RunnableParallel
from chains.chain_destino import create_chain_destino
from chains.chain_restaurante import create_chain_restaurantes
from chains.chain_passeios import create_chain_passeios_culturais


def create_main_chain(model):
    # As chains individuais são criadas aqui
    chain_destino = create_chain_destino(model)
    chain_restaurantes = create_chain_restaurantes(model)
    chain_passeios_culturais = create_chain_passeios_culturais(model)

    # A lógica de orquestração é a mesma
    roteiro_viagem = (
        RunnablePassthrough.assign(destino_info=chain_destino)
        | RunnablePassthrough.assign(
            sugestoes=RunnableParallel(
                restaurantes=(
                    {"cidade": lambda x: x["destino_info"]["cidade"]}
                    | chain_restaurantes
                ),
                passeios_culturais=(
                    {"cidade": lambda x: x["destino_info"]["cidade"]}
                    | chain_passeios_culturais
                ),
            )
        )
    )
    return roteiro_viagem
