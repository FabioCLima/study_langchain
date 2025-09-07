"""
Orquestrador de chains (versão procedural, com logging, validação e fallback).

Este orquestrador executa as chains em sequência (destino -> restaurantes & passeios),
normaliza os modelos Pydantic para `dict`, valida valores essenciais (ex.: cidade)
e aplica fallbacks em caso de erro nas subchains.
"""

from typing import Any, Callable, Dict

from chains.chain_destino import create_chain_destino
from chains.chain_restaurante import create_chain_restaurantes
from chains.chain_passeios import create_chain_passeios_culturais
from models.pydantic_models import ListaRestaurantes, ListaAtracoes
from utils.logger_setup import project_logger  # Loguru


def create_main_chain(model) -> Callable[[Dict[str, Any]], Dict[str, Any]]:
    """
    Cria a função principal que orquestra a geração do roteiro.

    Retorna um callable que recebe um dicionário de inputs (ex.: {"interesse": "trekking"})
    e devolve um dicionário com a estrutura:
    {
        "destino_info": { "cidade": "...", "motivo": "..." },
        "sugestoes": {
            "restaurantes": ListaRestaurantes(...),
            "passeios_culturais": ListaAtracoes(...)
        }
    }
    """
    # Cria as chains (cada uma é um callable que envolve prompt|model|parser + logging)
    chain_destino = create_chain_destino(model)
    chain_restaurantes = create_chain_restaurantes(model)
    chain_passeios_culturais = create_chain_passeios_culturais(model)

    def run_main(inputs: Dict[str, Any]) -> Dict[str, Any]:
        project_logger.info("[Orquestrador] Iniciando execução do roteiro")
        project_logger.debug(f"[Orquestrador] Inputs iniciais: {inputs!r}")

        # 1) Executa chain_destino e normaliza o resultado
        try:
            destino = chain_destino(inputs)
            project_logger.debug(f"[Orquestrador] Resultado raw destino: {destino!r}")
        except Exception as e:
            project_logger.exception("[Orquestrador] Falha ao executar chain_destino")
            raise RuntimeError("Erro ao determinar destino a partir do interesse do usuário") from e

        # Normalizar destino para dict (suporta Pydantic BaseModel ou dicts)
        if hasattr(destino, "dict"):
            destino_dict = destino.model_dump()
        elif isinstance(destino, dict):
            destino_dict = destino
        else:
            # objeto inesperado: tenta extrair atributos básicos
            destino_dict = {
                "cidade": getattr(destino, "cidade", None),
                "motivo": getattr(destino, "motivo", None),
            }

        project_logger.debug(f"[Orquestrador] Destino normalizado: {destino_dict!r}")

        # 2) Validar presença de 'cidade' (campo essencial)
        cidade = destino_dict.get("cidade")
        if not cidade:
            msg = f"chain_destino não retornou 'cidade' válida. Resultado: {destino_dict!r}"
            project_logger.error(f"[Orquestrador] {msg}")
            raise ValueError(msg)

        # 3) Executar subchains (restaurantes e passeios) com tratamento de erro.
        #    Executamos sequencialmente aqui para ter logs claros e controle de fallback.
        try:
            restaurantes = chain_restaurantes({"cidade": cidade})
            project_logger.debug(f"[Orquestrador] Restaurantes raw: {restaurantes!r}")
        except Exception:
            project_logger.exception("[Orquestrador] Erro em chain_restaurantes — aplicando fallback vazio")
            restaurantes = ListaRestaurantes(restaurantes=[])

        try:
            passeios = chain_passeios_culturais({"cidade": cidade})
            project_logger.debug(f"[Orquestrador] Passeios raw: {passeios!r}")
        except Exception:
            project_logger.exception("[Orquestrador] Erro em chain_passeios — aplicando fallback vazio")
            passeios = ListaAtracoes(atracoes=[])

        resultado = {
            "destino_info": destino_dict,
            "sugestoes": {
                "restaurantes": restaurantes,
                "passeios_culturais": passeios,
            },
        }

        project_logger.info("[Orquestrador] Execução finalizada com sucesso")
        project_logger.debug(f"[Orquestrador] Resultado final: {resultado!r}")

        return resultado

    return run_main
