"""
Sistema de Diagnóstico de Doenças - Módulos Models
Projeto Final INAR - Terceiro Ano, II Semestre

Este package contém os modelos de Machine Learning
para treinamento e predição.
"""

__version__ = "1.0.0"
__author__ = "Sistema de Diagnóstico de Doenças"

try:
    from .treinador_modelos import TreinadorModelos
    
    __all__ = ['TreinadorModelos']
    
except ImportError as e:
    print(f"Aviso: Módulo de modelos não pôde ser importado: {e}")
    __all__ = []