#!/usr/bin/env python3
"""
Script de Teste - Sistema de Diagnóstico de Doenças
Este script testa rapidamente se todos os módulos estão funcionando corretamente.
"""

import os
import sys
import traceback

# Adicionar paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(BASE_DIR, 'src', 'utils'))
sys.path.append(os.path.join(BASE_DIR, 'src', 'models'))

def teste_importacoes():
    """Testa se todas as importações funcionam"""
    print("🧪 Testando importações...")
    
    try:
        # Teste básico de bibliotecas
        import pandas as pd
        import numpy as np
        import matplotlib.pyplot as plt
        import seaborn as sns
        import sklearn
        print("✅ Bibliotecas básicas: OK")
        
        # Teste dos nossos módulos
        from carregador_dados import CarregadorDados  
        print("✅ CarregadorDados: OK")
        
        from analise_exploratoria import AnalisadorExploratorio
        print("✅ AnalisadorExploratorio: OK")
        
        from preprocessador import PreProcessadorDados
        print("✅ PreProcessadorDados: OK")
        
        from treinador_modelos import TreinadorModelos
        print("✅ TreinadorModelos: OK")
        
        from avaliador import AvaliadorModelos
        print("✅ AvaliadorModelos: OK")
        
        from sistema_predicao import SistemaPredicao
        print("✅ SistemaPredicao: OK")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro na importação: {e}")
        traceback.print_exc()
        return False

def teste_carregamento_dados():
    """Testa o carregamento de dados"""
    print("\n🧪 Testando carregamento de dados...")
    
    try:
        from carregador_dados import CarregadorDados
        
        caminho_dataset = os.path.join(BASE_DIR, 'dataset', 'Disease_symptom_and_patient_profile_dataset.csv')
        
        if not os.path.exists(caminho_dataset):
            print(f"❌ Dataset não encontrado: {caminho_dataset}")
            return False
        
        carregador = CarregadorDados(caminho_dataset)
        dados = carregador.carregar_dados()
        
        if carregador.validar_estrutura():
            print(f"✅ Dados carregados: {dados.shape}")
            
            info = carregador.obter_informacoes_basicas()
            print(f"   • Registros: {info['numero_linhas']:,}")
            print(f"   • Colunas: {info['numero_colunas']}")
            print(f"   • Doenças: {info['doencas_unicas']}")
            
            return True
        else:
            print("❌ Estrutura do dataset inválida")
            return False
            
    except Exception as e:
        print(f"❌ Erro no carregamento: {e}")
        return False

def teste_preprocessamento():
    """Testa o pré-processamento básico"""
    print("\n🧪 Testando pré-processamento...")
    
    try:
        from carregador_dados import CarregadorDados
        from preprocessador import PreProcessadorDados
        
        # Carregar dados
        caminho_dataset = os.path.join(BASE_DIR, 'dataset', 'Disease_symptom_and_patient_profile_dataset.csv')
        carregador = CarregadorDados(caminho_dataset)
        dados = carregador.carregar_dados()
        
        # Pré-processar uma amostra pequena
        dados_pequenos = dados.head(100)  # Apenas 100 registros para teste rápido
        
        preprocessador = PreProcessadorDados(dados_pequenos)
        resultado = preprocessador.processar_dados_completo(test_size=0.3)
        
        print(f"✅ Pré-processamento OK")
        print(f"   • Treino: {resultado['X_train'].shape}")
        print(f"   • Teste: {resultado['X_test'].shape}")
        print(f"   • Features: {len(resultado['feature_names'])}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro no pré-processamento: {e}")
        return False

def teste_modelo_simples():
    """Testa treinamento de um modelo simples"""
    print("\n🧪 Testando treinamento de modelo...")
    
    try:
        from carregador_dados import CarregadorDados
        from preprocessador import PreProcessadorDados
        from treinador_modelos import TreinadorModelos
        
        # Carregar e processar dados
        caminho_dataset = os.path.join(BASE_DIR, 'dataset', 'Disease_symptom_and_patient_profile_dataset.csv')
        carregador = CarregadorDados(caminho_dataset)
        dados = carregador.carregar_dados()
        
        # Usar amostra ainda menor para teste rápido
        dados_teste = dados.head(50)
        
        preprocessador = PreProcessadorDados(dados_teste)
        resultado = preprocessador.processar_dados_completo(test_size=0.3)
        
        # Treinar apenas um modelo simples
        treinador = TreinadorModelos()
        modelo_resultado = treinador.treinar_modelo_individual(
            'Logistic Regression',
            resultado['X_train'],
            resultado['y_train'],
            usar_grid_search=False
        )
        
        print(f"✅ Treinamento OK")
        print(f"   • Modelo: Logistic Regression")
        print(f"   • CV Score: {modelo_resultado['cv_score']:.3f}")
        print(f"   • Tempo: {modelo_resultado['tempo_treinamento']:.2f}s")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro no treinamento: {e}")
        return False

def teste_interface_grafica():
    """Testa se a interface gráfica pode ser importada"""
    print("\n🧪 Testando interface gráfica...")
    
    try:
        import tkinter as tk
        print("✅ Tkinter disponível")
        
        # Teste básico da interface (sem executar)
        sys.path.append(os.path.join(BASE_DIR, 'src', 'interface_grafica'))
        from app_principal import SistemaDiagnostico
        print("✅ Interface importada com sucesso")
        
        return True
        
    except ImportError as e:
        print(f"❌ Tkinter não disponível: {e}")
        print("   💡 No Linux, instale: sudo apt-get install python3-tk")
        return False
    except Exception as e:
        print(f"❌ Erro na interface: {e}")
        return False

def teste_completo():
    """Executa todos os testes"""
    print("🚀 INICIANDO TESTES DO SISTEMA")
    print("=" * 50)
    
    testes = [
        ("Importações", teste_importacoes),
        ("Carregamento de Dados", teste_carregamento_dados),
        ("Pré-processamento", teste_preprocessamento),
        ("Modelo Simples", teste_modelo_simples),
        ("Interface Gráfica", teste_interface_grafica)
    ]
    
    resultados = {}
    
    for nome, teste_func in testes:
        try:
            resultado = teste_func()
            resultados[nome] = resultado
        except Exception as e:
            print(f"❌ Erro crítico em {nome}: {e}")
            resultados[nome] = False
    
    # Resumo final
    print("\n" + "=" * 50)
    print("📋 RESUMO DOS TESTES:")
    print("=" * 50)
    
    sucessos = 0
    for nome, resultado in resultados.items():
        status = "✅ PASSOU" if resultado else "❌ FALHOU"
        print(f"{nome:<20} {status}")
        if resultado:
            sucessos += 1
    
    print(f"\n🎯 RESULTADO FINAL: {sucessos}/{len(testes)} testes passaram")
    
    if sucessos == len(testes):
        print("🎉 TODOS OS TESTES PASSARAM! Sistema pronto para uso.")
        print("\n💡 Próximos passos:")
        print("   • python main.py --gui (Interface gráfica)")
        print("   • python main.py --pipeline (Pipeline completo)")
        print("   • python main.py --analise (Análise rápida)")
    else:
        print("⚠️  Alguns testes falharam. Verifique as dependências.")
        print("   • pip install -r requirements.txt")
        print("   • Verifique se o dataset está na pasta 'dataset/'")
    
    return sucessos == len(testes)

if __name__ == "__main__":
    teste_completo()