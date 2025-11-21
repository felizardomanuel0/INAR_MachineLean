#!/usr/bin/env python3
"""
Sistema de Diagnóstico Médico - Versão 2.0 (ATUALIZADA)
Launcher Principal com Novos Datasets

Executa a interface gráfica em português com:
- Análise baseada em pesos de sintomas
- Descrições completas das doenças 
- Precauções e recomendações médicas
- 133 sintomas e 41 doenças no dataset atualizado

Uso:
    python main_atualizado.py          # Interface gráfica
    python main_atualizado.py --test   # Executar testes
    python main_atualizado.py --help   # Ajuda
"""

import os
import sys
import argparse
import logging
from pathlib import Path

# Configurar paths do projeto
BASE_DIR = Path(__file__).parent.absolute()
sys.path.append(str(BASE_DIR / 'src' / 'utils'))
sys.path.append(str(BASE_DIR / 'src' / 'models'))
sys.path.append(str(BASE_DIR / 'src' / 'interface_grafica'))

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(BASE_DIR / 'sistema_diagnostico.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def verificar_ambiente():
    """Verifica se o ambiente está configurado corretamente"""
    logger.info("Verificando ambiente do sistema...")
    
    # Verificar arquivos de dataset
    dataset_dir = BASE_DIR / 'dataset'
    arquivos_necessarios = [
        'Symptom-severity.csv',
        'symptom_Description.csv', 
        'symptom_precaution.csv'
    ]
    
    for arquivo in arquivos_necessarios:
        caminho = dataset_dir / arquivo
        if not caminho.exists():
            raise FileNotFoundError(f"Arquivo de dataset necessário não encontrado: {arquivo}")
    
    logger.info("✅ Todos os arquivos de dataset encontrados")
    
    # Verificar dependências Python essenciais
    try:
        import pandas
        import numpy
        import tkinter
        logger.info("✅ Dependências Python verificadas")
    except ImportError as e:
        raise ImportError(f"Dependência não encontrada: {e}")
    
    return True

def executar_testes():
    """Executa testes do sistema"""
    logger.info("Executando testes do sistema...")
    
    try:
        # Importar e executar testes
        from testar_sistema_atualizado import main as executar_teste
        return executar_teste()
    except Exception as e:
        logger.error(f"Erro durante execução de testes: {e}")
        return 1

def iniciar_interface_grafica():
    """Inicia a interface gráfica do sistema"""
    logger.info("Iniciando interface gráfica...")
    
    try:
        from app_portugues import SistemaDiagnosticoPortugues
        
        # Criar e iniciar aplicação
        app = SistemaDiagnosticoPortugues()
        
        logger.info("🏥 Sistema de Diagnóstico Médico v2.0 iniciado")
        logger.info("   - Dataset atualizado com 133 sintomas e 41 doenças")
        logger.info("   - Análise baseada em pesos de severidade")
        logger.info("   - Descrições e precauções médicas incluídas")
        
        # Executar loop principal
        app.executar()
        
        logger.info("Aplicação encerrada pelo usuário")
        return 0
        
    except Exception as e:
        logger.error(f"Erro ao iniciar interface gráfica: {e}")
        import traceback
        traceback.print_exc()
        return 1

def exibir_informacoes_sistema():
    """Exibe informações sobre o sistema"""
    print("""
🏥 Sistema de Diagnóstico Médico - Versão 2.0
═══════════════════════════════════════════════

📊 CARACTERÍSTICAS DO SISTEMA ATUALIZADO:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• 133 sintomas com pesos de severidade
• 41 doenças com descrições completas
• Precauções e cuidados médicos
• Interface totalmente em português
• Algoritmo baseado em análise de sintomas ponderada
• Diagnósticos múltiplos com probabilidades

🗂️  NOVOS DATASETS:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• Symptom-severity.csv    - Pesos dos sintomas
• symptom_Description.csv - Descrições das doenças  
• symptom_precaution.csv  - Precauções médicas

🚀 MELHORIAS DA VERSÃO 2.0:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• Sistema mais preciso com pesos de sintomas
• Informações médicas detalhadas
• Múltiplos diagnósticos com probabilidades
• Precauções específicas por doença
• Interface aprimorada com scroll otimizado
• Sistema de salvamento expandido

⚕️  NOTA MÉDICA IMPORTANTE:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Este sistema é desenvolvido para fins educacionais.
NÃO substitui consulta médica profissional.
Sempre procure um médico para diagnóstico definitivo.

🎓 Desenvolvido por: INAR - Terceiro Ano, II Semestre - 2025
""")

def main():
    """Função principal do launcher"""
    parser = argparse.ArgumentParser(
        description="Sistema de Diagnóstico Médico v2.0 - INAR",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos de uso:
  python main_atualizado.py              # Inicia interface gráfica
  python main_atualizado.py --test       # Executa testes do sistema  
  python main_atualizado.py --info       # Mostra informações detalhadas
        """
    )
    
    parser.add_argument(
        '--test', 
        action='store_true',
        help='Executa testes completos do sistema'
    )
    
    parser.add_argument(
        '--info',
        action='store_true', 
        help='Exibe informações detalhadas sobre o sistema'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Ativa logs detalhados'
    )
    
    args = parser.parse_args()
    
    # Configurar nível de log
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    try:
        # Verificar ambiente
        verificar_ambiente()
        
        # Executar ação solicitada
        if args.info:
            exibir_informacoes_sistema()
            return 0
            
        elif args.test:
            return executar_testes()
            
        else:
            # Modo padrão: interface gráfica
            return iniciar_interface_grafica()
            
    except FileNotFoundError as e:
        logger.error(f"❌ Arquivo não encontrado: {e}")
        logger.error("Certifique-se de que todos os arquivos de dataset estão presentes")
        return 1
        
    except ImportError as e:
        logger.error(f"❌ Dependência não encontrada: {e}")
        logger.error("Execute: pip install -r requirements.txt")
        return 1
        
    except KeyboardInterrupt:
        logger.info("⏸️  Execução interrompida pelo usuário")
        return 1
        
    except Exception as e:
        logger.error(f"💥 Erro crítico: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except Exception as e:
        print(f"\n💥 Erro fatal: {e}")
        sys.exit(1)