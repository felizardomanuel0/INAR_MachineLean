"""
Sistema de Diagnóstico Médico Simplificado
Executar apenas com dados.csv

Versão simplificada que funciona apenas com o dataset dados.csv
sem dependência de múltiplos arquivos CSV.
"""

import sys
import os
import logging
from pathlib import Path

# Adicionar diretório src ao path
current_dir = Path(__file__).parent
src_dir = current_dir / "src"
sys.path.insert(0, str(src_dir))

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('sistema_diagnostico_simples.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def verificar_dataset():
    """
    Verifica se o dataset dados.csv existe
    
    Returns:
        str: Caminho para o dataset ou None se não encontrado
    """
    possiveis_caminhos = [
        current_dir / "dataset" / "dados.csv",
        current_dir / "dados.csv",
        current_dir / "data" / "dados.csv"
    ]
    
    for caminho in possiveis_caminhos:
        if caminho.exists():
            logger.info(f"✅ Dataset encontrado: {caminho}")
            return str(caminho.parent)
    
    logger.error("❌ Dataset 'dados.csv' não encontrado!")
    return None

def executar_interface_grafica():
    """Executa a interface gráfica"""
    try:
        from ui.interface_diagnostico_simples import InterfaceDiagnosticoSimples
        
        logger.info("🚀 Iniciando Sistema de Diagnóstico Simplificado")
        app = InterfaceDiagnosticoSimples()
        app.run()
        
    except ImportError as e:
        logger.error(f"Erro de importação: {e}")
        print("❌ Erro: Não foi possível importar os módulos necessários.")
        print("Verifique se todos os arquivos estão no local correto.")
        
    except Exception as e:
        logger.error(f"Erro ao executar interface: {e}")
        print(f"❌ Erro ao executar o sistema: {e}")

def executar_teste_terminal():
    """Executa teste no terminal"""
    try:
        from models.sistema_diagnostico_simples import SistemaDiagnosticoSimples
        
        print("🏥 Sistema de Diagnóstico Médico - Teste Terminal")
        print("=" * 60)
        
        # Verificar dataset
        caminho_dataset = verificar_dataset()
        if not caminho_dataset:
            print("❌ Dataset não encontrado. Coloque o arquivo 'dados.csv' na pasta 'dataset'")
            return
        
        # Inicializar sistema
        sistema = SistemaDiagnosticoSimples(caminho_dataset)
        
        if not sistema.dados_carregados:
            print("❌ Erro ao carregar dados do sistema")
            return
        
        # Mostrar estatísticas
        stats = sistema.obter_estatisticas_sistema()
        print("📊 Estatísticas do Sistema:")
        for chave, valor in stats.items():
            print(f"  • {chave}: {valor}")
        
        # Teste básico
        print(f"\n🔍 Teste de Diagnóstico:")
        sintomas_teste = ['Coceira', 'Erupção Cutânea', 'Erupções Cutâneas Nodulares']
        
        print(f"Sintomas de teste: {sintomas_teste}")
        resultado = sistema.realizar_diagnostico(sintomas_teste)
        
        if 'erro' in resultado:
            print(f"❌ Erro: {resultado['erro']}")
        else:
            print(f"✅ {resultado['total_diagnosticos']} diagnósticos encontrados")
            print(f"Confiabilidade: {resultado['confiabilidade_geral']}")
            
            if resultado['diagnosticos']:
                print("\nTop 3 diagnósticos mais prováveis:")
                for i, diag in enumerate(resultado['diagnosticos'], 1):
                    emoji = "🔴" if diag['probabilidade'] >= 70 else "🟡" if diag['probabilidade'] >= 40 else "🟢"
                    print(f"  {i}. {emoji} {diag['doenca']} - {diag['probabilidade']:.1f}%")
        
        print(f"\n✅ Teste concluído com sucesso!")
        
    except ImportError as e:
        logger.error(f"Erro de importação: {e}")
        print("❌ Erro: Não foi possível importar os módulos necessários.")
        
    except Exception as e:
        logger.error(f"Erro no teste: {e}")
        print(f"❌ Erro no teste: {e}")

def main():
    """Função principal"""
    print("🏥 Sistema de Diagnóstico Médico - Versão Simplificada")
    print("=" * 60)
    
    # Verificar dataset
    if not verificar_dataset():
        print("\n📁 Estrutura de pastas esperada:")
        print("  projeto/")
        print("  ├── dataset/")
        print("  │   └── dados.csv")
        print("  ├── src/")
        print("  └── main_simples.py")
        print("\n💡 Coloque o arquivo 'dados.csv' na pasta 'dataset'")
        return
    
    print("\n📋 Opções disponíveis:")
    print("1. Executar interface gráfica (recomendado)")
    print("2. Executar teste no terminal")
    print("3. Sair")
    
    while True:
        try:
            escolha = input("\nEscolha uma opção (1-3): ").strip()
            
            if escolha == "1":
                executar_interface_grafica()
                break
                
            elif escolha == "2":
                executar_teste_terminal()
                break
                
            elif escolha == "3":
                print("👋 Até logo!")
                break
                
            else:
                print("❌ Opção inválida. Digite 1, 2 ou 3.")
                
        except KeyboardInterrupt:
            print("\n\n👋 Programa interrompido pelo usuário.")
            break
            
        except Exception as e:
            print(f"❌ Erro: {e}")
            break

if __name__ == "__main__":
    main()