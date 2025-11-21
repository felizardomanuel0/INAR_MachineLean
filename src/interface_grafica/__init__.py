"""
Sistema de Diagnóstico de Doenças - Interface Gráfica
Projeto Final INAR - Terceiro Ano, II Semestre

Este package contém a interface gráfica do usuário
para interação com o sistema de diagnóstico.
"""

__version__ = "1.0.0"
__author__ = "Sistema de Diagnóstico de Doenças"

try:
    from .app_principal import SistemaDiagnostico
    
    __all__ = ['SistemaDiagnostico']
    
except ImportError as e:
    print(f"Aviso: Interface gráfica não pôde ser importada: {e}")
    __all__ = []