"""
Sistema de Diagnóstico de Doenças - Módulos Utils
Projeto Final INAR - Terceiro Ano, II Semestre

Este package contém utilitários para processamento de dados,
análise exploratória, pré-processamento e avaliação de modelos.
"""

__version__ = "1.0.0"
__author__ = "Sistema de Diagnóstico de Doenças"

# Importações principais
try:
    from .carregador_dados import CarregadorDados
    from .analise_exploratoria import AnalisadorExploratorio
    from .preprocessador import PreProcessadorDados
    from .avaliador import AvaliadorModelos
    from .sistema_predicao import SistemaPredicao
    
    __all__ = [
        'CarregadorDados',
        'AnalisadorExploratorio', 
        'PreProcessadorDados',
        'AvaliadorModelos',
        'SistemaPredicao'
    ]
    
except ImportError as e:
    print(f"Aviso: Alguns módulos não puderam ser importados: {e}")
    __all__ = []