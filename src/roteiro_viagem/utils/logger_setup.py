"""Configuração centralizada do Loguru para o projeto.

- Loga no console com cores
- Salva logs em arquivo rotacionado diariamente
- Mantém logs por 7 dias
"""

import os
import sys

from loguru import logger

# Criar pasta de logs se não existir
os.makedirs("logs", exist_ok=True)


def setup_logger() -> None:
    # Remove configuração padrão
    logger.remove()

    # Log no console (colorido)
    logger.add(
        sys.stdout,
        colorize=True,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
               "<level>{level: <8}</level> | "
               "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
               "<level>{message}</level>",
        level="DEBUG"
    )

    # Log em arquivo (rotaciona a cada dia, mantém 7 dias)
    logger.add(
        "logs/project.log",
        rotation="1 day",
        retention="7 days",
        encoding="utf-8",
        enqueue=True,
        level="DEBUG"
    )

    return logger


# Instância global
project_logger: "logger.__class__" = logger
