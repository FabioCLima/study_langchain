# core/logger.py

import sys

from loguru import logger  #! <-- A LINHA QUE FALTAVA

from core.settings import settings

# 1. Agora que 'logger' foi importado, esta linha funciona.
logger.remove()

# 2. Quebra a string de formato em partes legíveis para evitar linha longa (E501)
log_format = (
    "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
    "<level>{level: <8}</level> | "
    "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
    "<level>{message}</level>"
)

# 3. Adiciona um novo handler (para o console) com o formato definido acima.
logger.add(
    sys.stderr,
    level=settings.log_level.upper(),
    format=log_format,
    colorize=True,
)

# O logger está pronto e configurado para ser importado em outros módulos
