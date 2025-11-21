"""
Sistema de Diagnóstico de Doenças - Arquivo Principal
Projeto Final INAR - Terceiro Ano, II Semestre

Este sistema utiliza Machine Learning para auxiliar no diagnóstico de doenças
baseado em sintomas e características demográficas dos pacientes.

Autor: Sistema de Diagnóstico de Doenças
Data: Novembro 2025
"""

import os
import sys
import argparse
import logging
from datetime import datetime

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('sistema_diagnostico.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Adicionar paths dos módulos
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(BASE_DIR, 'src', 'utils'))
sys.path.append(os.path.join(BASE_DIR, 'src', 'models'))
sys.path.append(os.path.join(BASE_DIR, 'src', 'interface_grafica'))

def exibir_banner():
    """Exibe o banner do sistema"""
    banner = """
    ╔══════════════════════════════════════════════════════════════╗
    ║             🏥 SISTEMA DE DIAGNÓSTICO DE DOENÇAS             ║
    ║                                                              ║
    ║                    Projeto Final - INAR                     ║
    ║                Terceiro Ano, II Semestre                    ║
    ║                                                              ║
    ║  🤖 Machine Learning para Diagnóstico Médico Assistido      ║
    ║  📊 Análise de Sintomas e Características Demográficas      ║
    ║  🎯 Interface Gráfica Amigável                              ║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)

def verificar_dependencias():
    """Verifica se todas as dependências estão instaladas"""
    dependencias_obrigatorias = [
        'pandas', 'numpy', 'sklearn', 'matplotlib', 
        'seaborn', 'xgboost', 'joblib', 'tkinter'
    ]
    
    dependencias_faltantes = []
    
    for dep in dependencias_obrigatorias:
        try:
            if dep == 'tkinter':
                import tkinter
            else:
                __import__(dep)
        except ImportError:
            dependencias_faltantes.append(dep)
    
    if dependencias_faltantes:
        logger.error(f"❌ Dependências faltantes: {', '.join(dependencias_faltantes)}")
        logger.error("Execute: pip install -r requirements.txt")
        return False
    
    logger.info("✅ Todas as dependências estão instaladas")
    return True

def executar_pipeline_completo():
    """Executa o pipeline completo de análise"""
    logger.info("🚀 Iniciando pipeline completo...")
    
    try:
        # Importar módulos
        from carregador_dados import CarregadorDados
        from analise_exploratoria import AnalisadorExploratorio
        from preprocessador import PreProcessadorDados
        from treinador_modelos import TreinadorModelos
        from avaliador import AvaliadorModelos
        
        # Caminho do dataset
        caminho_dataset = os.path.join(BASE_DIR, 'dataset', 'Disease_symptom_and_patient_profile_dataset.csv')
        
        if not os.path.exists(caminho_dataset):
            logger.error(f"❌ Dataset não encontrado: {caminho_dataset}")
            return False
        
        # 1. Carregamento de dados
        logger.info("📂 Carregando dados...")
        carregador = CarregadorDados(caminho_dataset)
        dados = carregador.carregar_dados()
        
        if not carregador.validar_estrutura():
            logger.error("❌ Estrutura do dataset inválida")
            return False
        
        logger.info(f"✅ Dados carregados: {dados.shape}")
        
        # 2. Análise exploratória
        logger.info("🔍 Executando análise exploratória...")
        analisador = AnalisadorExploratorio(dados)
        
        # Criar pasta para salvar gráficos
        pasta_graficos = os.path.join(BASE_DIR, 'resultados', 'graficos')
        os.makedirs(pasta_graficos, exist_ok=True)
        
        relatorio_eda = analisador.executar_eda_completa(
            salvar_figuras=True, 
            caminho_salvar=pasta_graficos
        )
        
        # 3. Pré-processamento
        logger.info("🔧 Pré-processando dados...")
        preprocessador = PreProcessadorDados(dados)
        dados_processados = preprocessador.processar_dados_completo()
        
        # 4. Treinamento de modelos
        logger.info("🤖 Treinando modelos...")
        treinador = TreinadorModelos()
        
        # Usar grid search mais simples para execução mais rápida
        resultados_treino = treinador.treinar_todos_modelos(
            dados_processados['X_train'],
            dados_processados['y_train'],
            usar_grid_search=True,
            cv_folds=3  # Reduzir para acelerar
        )
        
        # 5. Avaliação
        logger.info("📊 Avaliando modelos...")
        avaliador = AvaliadorModelos()
        
        # Avaliar cada modelo
        resultados_avaliacao = {}
        for nome_modelo, modelo_treinado in treinador.modelos_treinados.items():
            resultado_avaliacao = avaliador.avaliar_modelo_completo(
                modelo_treinado,
                dados_processados['X_test'],
                dados_processados['y_test'],
                nome_modelo,
                salvar_figuras=True,
                caminho_salvar=pasta_graficos
            )
            resultados_avaliacao[nome_modelo] = resultado_avaliacao
        
        # 6. Relatório final
        logger.info("📋 Gerando relatório final...")
        relatorio_final = avaliador.gerar_relatorio_final(
            resultados_avaliacao,
            salvar_arquivo=True,
            caminho_salvar=os.path.join(BASE_DIR, 'resultados')
        )
        
        # 7. Salvar modelos
        logger.info("💾 Salvando modelos...")
        pasta_modelos = os.path.join(BASE_DIR, 'modelos_salvos')
        os.makedirs(pasta_modelos, exist_ok=True)
        
        treinador.salvar_modelos(pasta_modelos)
        preprocessador.salvar_preprocessadores(pasta_modelos)
        
        logger.info("✅ Pipeline completo executado com sucesso!")
        logger.info(f"📁 Resultados salvos em: {os.path.join(BASE_DIR, 'resultados')}")
        logger.info(f"🤖 Modelos salvos em: {pasta_modelos}")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Erro no pipeline: {e}")
        return False

def executar_interface_grafica():
    """Executa a interface gráfica do sistema em português"""
    logger.info("🖥️ Iniciando interface gráfica em português...")
    
    try:
        # Importar e executar nova interface em português
        from app_portugues import main as app_main
        app_main()
        
    except Exception as e:
        logger.error(f"❌ Erro na interface gráfica: {str(e)}")
        return False
    
    return True

def executar_analise_rapida():
    """Executa apenas análise exploratória rápida"""
    logger.info("⚡ Executando análise rápida...")
    
    try:
        from carregador_dados import CarregadorDados
        from analise_exploratoria import AnalisadorExploratorio
        
        # Carregar dados
        caminho_dataset = os.path.join(BASE_DIR, 'dataset', 'Disease_symptom_and_patient_profile_dataset.csv')
        carregador = CarregadorDados(caminho_dataset)
        dados = carregador.carregar_dados()
        
        # Análise básica
        info = carregador.obter_informacoes_basicas()
        print("\n📊 INFORMAÇÕES BÁSICAS:")
        print(f"• Registros: {info['numero_linhas']}")
        print(f"• Colunas: {info['numero_colunas']}")
        print(f"• Doenças únicas: {info['doencas_unicas']}")
        print(f"• Memória: {info['memoria_uso']:.2f} MB")
        
        # Estatísticas rápidas
        analisador = AnalisadorExploratorio(dados)
        stats = analisador.estatisticas_descritivas()
        
        print("\n🦠 DISTRIBUIÇÃO DE CLASSES:")
        if 'outcome' in stats:
            for classe, count in stats['outcome'].items():
                print(f"• {classe}: {count}")
        
        print("\n🏆 DOENÇAS MAIS COMUNS:")
        if 'doencas' in stats:
            for doenca, count in list(stats['doencas']['mais_comuns'].items())[:5]:
                print(f"• {doenca}: {count}")
        
        logger.info("✅ Análise rápida concluída!")
        return True
        
    except Exception as e:
        logger.error(f"❌ Erro na análise rápida: {e}")
        return False

def testar_predicao():
    """Testa o sistema de predição"""
    logger.info("🔮 Testando sistema de predição...")
    
    try:
        from sistema_predicao import SistemaPredicao
        
        # Criar sistema
        sistema = SistemaPredicao()
        
        # Verificar status
        status = sistema.status_sistema()
        if not status['modelo_carregado']:
            logger.warning("❌ Nenhum modelo carregado. Execute o treinamento primeiro.")
            return False
        
        # Dados de teste
        dados_teste = {
            'febre': True,
            'tosse': False,
            'fadiga': True,
            'dificuldade_respirar': False,
            'idade': 35,
            'genero': 'Male',
            'pressao': 'Normal',
            'colesterol': 'Normal'
        }
        
        # Fazer predição
        resultado = sistema.fazer_predicao(dados_teste)
        
        print("\n🔍 RESULTADO DO TESTE:")
        print(f"• Resultado: {resultado['resultado']} {resultado['resultado_interpretado']['emoji']}")
        print(f"• Confiança: {resultado['confianca']:.2%}")
        print(f"• Recomendação: {resultado['resultado_interpretado']['recomendacao']}")
        
        logger.info("✅ Teste de predição bem-sucedido!")
        return True
        
    except Exception as e:
        logger.error(f"❌ Erro no teste de predição: {e}")
        return False

def main():
    """Função principal"""
    parser = argparse.ArgumentParser(
        description="Sistema de Diagnóstico de Doenças - INAR",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos de uso:
  python main.py --gui                    # Interface gráfica
  python main.py --pipeline               # Pipeline completo
  python main.py --analise                # Análise rápida
  python main.py --testar                 # Testar predição
  python main.py --pipeline --gui         # Pipeline + Interface
        """
    )
    
    parser.add_argument('--gui', action='store_true', 
                       help='Executar interface gráfica')
    parser.add_argument('--pipeline', action='store_true',
                       help='Executar pipeline completo')
    parser.add_argument('--analise', action='store_true',
                       help='Executar apenas análise exploratória')
    parser.add_argument('--testar', action='store_true',
                       help='Testar sistema de predição')
    parser.add_argument('--verificar', action='store_true',
                       help='Verificar dependências')
    
    args = parser.parse_args()
    
    # Exibir banner
    exibir_banner()
    
    # Log inicial
    logger.info(f"🚀 Sistema iniciado em: {datetime.now()}")
    logger.info(f"📁 Diretório base: {BASE_DIR}")
    
    # Se nenhum argumento, mostrar help
    if not any(vars(args).values()):
        parser.print_help()
        return
    
    # Verificar dependências
    if not verificar_dependencias():
        return
    
    sucesso = True
    
    # Executar ações solicitadas
    if args.verificar:
        logger.info("✅ Verificação de dependências concluída")
    
    if args.analise:
        sucesso &= executar_analise_rapida()
    
    if args.pipeline:
        sucesso &= executar_pipeline_completo()
    
    if args.testar:
        sucesso &= testar_predicao()
    
    if args.gui:
        executar_interface_grafica()
    
    # Log final
    if sucesso:
        logger.info("🎉 Sistema executado com sucesso!")
    else:
        logger.error("❌ Sistema executado com erros")
        sys.exit(1)

if __name__ == "__main__":
    main()