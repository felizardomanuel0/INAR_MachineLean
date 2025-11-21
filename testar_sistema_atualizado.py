#!/usr/bin/env python3
"""
Teste do Sistema Atualizado com Novos Datasets
Verifica se todos os componentes funcionam corretamente
"""

import os
import sys
import logging

# Configurar paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(BASE_DIR, 'src', 'utils'))
sys.path.append(os.path.join(BASE_DIR, 'src', 'models'))

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def testar_carregador_dados():
    """Testa o carregador de dados atualizado"""
    print("\n🔄 Testando Carregador de Dados...")
    
    try:
        from carregador_dados_atualizado import CarregadorDadosAtualizado
        
        carregador = CarregadorDadosAtualizado()
        dados = carregador.carregar_todos_dados()
        
        print(f"✅ Sintomas carregados: {len(carregador.obter_lista_sintomas())}")
        print(f"✅ Doenças carregadas: {len(carregador.obter_lista_doencas())}")
        
        # Teste de informações de doença
        info_malaria = carregador.obter_informacoes_completas_doenca("Malaria")
        print(f"✅ Informações sobre Malária encontradas: {info_malaria['encontrada']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro no carregador: {e}")
        return False

def testar_sintomas_portugues():
    """Testa traduções de sintomas"""
    print("\n🔄 Testando Sintomas em Português...")
    
    try:
        from sintomas_portugues import SINTOMAS_DISPONIVEIS, TRADUCAO_SINTOMAS, traduzir_sintoma_para_ingles
        
        print(f"✅ Sintomas disponíveis: {len(SINTOMAS_DISPONIVEIS)}")
        print(f"✅ Traduções disponíveis: {len(TRADUCAO_SINTOMAS)}")
        
        # Teste algumas traduções
        teste_sintomas = ['Febre', 'Tosse', 'Fadiga', 'Dor de Cabeça']
        for sintoma in teste_sintomas:
            traducao = traduzir_sintoma_para_ingles(sintoma)
            print(f"   {sintoma} -> {traducao}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro nos sintomas: {e}")
        return False

def testar_sistema_diagnostico():
    """Testa o sistema de diagnóstico atualizado"""
    print("\n🔄 Testando Sistema de Diagnóstico...")
    
    try:
        from sistema_diagnostico_atualizado import SistemaDiagnosticoAtualizado
        
        sistema = SistemaDiagnosticoAtualizado()
        
        # Teste com sintomas de malária
        sintomas_teste = ['Febre Alta', 'Calafrios', 'Dor de Cabeça', 'Náusea']
        
        print(f"   Testando com sintomas: {sintomas_teste}")
        
        resultado = sistema.diagnosticar_sintomas(sintomas_teste)
        
        if resultado['sucesso']:
            print(f"✅ Diagnóstico realizado com sucesso")
            print(f"   Score total: {resultado['score_total']}")
            print(f"   Diagnósticos encontrados: {resultado['num_diagnosticos']}")
            
            if resultado['diagnosticos']:
                principal = resultado['diagnosticos'][0]
                print(f"   Diagnóstico principal: {principal['doenca']} ({principal['probabilidade']:.1f}%)")
                
                if principal.get('precaucoes'):
                    print(f"   Precauções: {len(principal['precaucoes'])} itens")
        else:
            print(f"❌ Erro no diagnóstico: {resultado['erro']}")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Erro no sistema: {e}")
        import traceback
        traceback.print_exc()
        return False

def testar_interface_grafica():
    """Testa a interface gráfica (sem abrir janela)"""
    print("\n🔄 Testando Interface Gráfica (importação)...")
    
    try:
        sys.path.append(os.path.join(BASE_DIR, 'src', 'interface_grafica'))
        from app_portugues import SistemaDiagnosticoPortugues
        
        print("✅ Interface gráfica importada com sucesso")
        # Nota: Não instanciamos para evitar abrir janela
        
        return True
        
    except Exception as e:
        print(f"❌ Erro na interface: {e}")
        return False

def verificar_arquivos_dataset():
    """Verifica se os arquivos de dataset existem"""
    print("\n🔄 Verificando Arquivos de Dataset...")
    
    dataset_dir = os.path.join(BASE_DIR, 'dataset')
    arquivos_necessarios = [
        'Symptom-severity.csv',
        'symptom_Description.csv', 
        'symptom_precaution.csv'
    ]
    
    todos_existem = True
    
    for arquivo in arquivos_necessarios:
        caminho = os.path.join(dataset_dir, arquivo)
        if os.path.exists(caminho):
            print(f"✅ {arquivo} encontrado")
        else:
            print(f"❌ {arquivo} NÃO encontrado")
            todos_existem = False
    
    return todos_existem

def main():
    """Função principal de teste"""
    print("🧪 TESTE COMPLETO DO SISTEMA ATUALIZADO")
    print("=" * 50)
    
    testes = [
        ("Arquivos Dataset", verificar_arquivos_dataset),
        ("Carregador Dados", testar_carregador_dados),
        ("Sintomas Português", testar_sintomas_portugues),
        ("Sistema Diagnóstico", testar_sistema_diagnostico),
        ("Interface Gráfica", testar_interface_grafica)
    ]
    
    resultados = {}
    
    for nome_teste, funcao_teste in testes:
        try:
            resultado = funcao_teste()
            resultados[nome_teste] = resultado
        except Exception as e:
            print(f"❌ Erro crítico em {nome_teste}: {e}")
            resultados[nome_teste] = False
    
    # Sumário dos resultados
    print("\n" + "=" * 50)
    print("📊 SUMÁRIO DOS TESTES:")
    print("=" * 50)
    
    sucessos = 0
    total = len(resultados)
    
    for teste, sucesso in resultados.items():
        status = "✅ PASSOU" if sucesso else "❌ FALHOU"
        print(f"{teste:20} : {status}")
        if sucesso:
            sucessos += 1
    
    print(f"\n🎯 RESULTADO GERAL: {sucessos}/{total} testes passaram")
    
    if sucessos == total:
        print("🎉 TODOS OS TESTES PASSARAM! Sistema pronto para uso.")
        return 0
    else:
        print("⚠️  Alguns testes falharam. Verifique os erros acima.")
        return 1

if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\n⏸️  Teste interrompido pelo usuário.")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n💥 Erro crítico durante teste: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)