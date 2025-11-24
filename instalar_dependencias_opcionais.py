#!/usr/bin/env python3
"""
Script para instalar dependências opcionais do sistema
Autor: Sistema de Diagnóstico de Doenças
"""

import subprocess
import sys
import os

def executar_comando(comando):
    """Executa um comando e retorna se foi bem-sucedido"""
    try:
        print(f"🔄 Executando: {comando}")
        resultado = subprocess.run(comando, shell=True, check=True, 
                                 capture_output=True, text=True)
        print(f"✅ Sucesso: {comando}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao executar '{comando}': {e}")
        if e.stdout:
            print(f"Stdout: {e.stdout}")
        if e.stderr:
            print(f"Stderr: {e.stderr}")
        return False

def verificar_instalacao(modulo, comando_teste):
    """Verifica se um módulo foi instalado corretamente"""
    try:
        resultado = subprocess.run(comando_teste, shell=True, 
                                 capture_output=True, text=True)
        if resultado.returncode == 0:
            print(f"✅ {modulo} instalado corretamente!")
            if resultado.stdout.strip():
                print(f"   Versão: {resultado.stdout.strip()}")
            return True
        else:
            print(f"❌ {modulo} não foi instalado corretamente")
            return False
    except Exception as e:
        print(f"❌ Erro ao verificar {modulo}: {e}")
        return False

def main():
    """Função principal para instalar dependências opcionais"""
    
    print("🏥 INSTALADOR DE DEPENDÊNCIAS OPCIONAIS")
    print("=" * 50)
    print()
    print("Este script irá instalar as dependências opcionais:")
    print("• XGBoost - Algoritmo avançado de machine learning")
    print("• Seaborn - Biblioteca para visualizações avançadas")
    print()
    
    resposta = input("Deseja continuar? (s/n): ").lower().strip()
    if resposta not in ['s', 'sim', 'y', 'yes']:
        print("❌ Instalação cancelada pelo usuário")
        return
    
    print("\n🚀 INICIANDO INSTALAÇÃO...")
    print("=" * 30)
    
    # Lista de pacotes para instalar
    pacotes = [
        {
            'nome': 'XGBoost',
            'comando_install': 'pip3 install xgboost',
            'comando_teste': 'python3 -c "import xgboost; print(xgboost.__version__)"'
        },
        {
            'nome': 'Seaborn',
            'comando_install': 'pip3 install seaborn',
            'comando_teste': 'python3 -c "import seaborn; print(seaborn.__version__)"'
        }
    ]
    
    sucessos = []
    falhas = []
    
    for pacote in pacotes:
        print(f"\n📦 Instalando {pacote['nome']}...")
        
        # Tentar instalar
        if executar_comando(pacote['comando_install']):
            # Verificar se foi instalado corretamente
            if verificar_instalacao(pacote['nome'], pacote['comando_teste']):
                sucessos.append(pacote['nome'])
            else:
                falhas.append(pacote['nome'])
        else:
            falhas.append(pacote['nome'])
    
    # Relatório final
    print("\n" + "=" * 50)
    print("📋 RELATÓRIO DE INSTALAÇÃO")
    print("=" * 50)
    
    if sucessos:
        print("\n✅ PACOTES INSTALADOS COM SUCESSO:")
        for pacote in sucessos:
            print(f"   • {pacote}")
    
    if falhas:
        print("\n❌ PACOTES COM FALHA NA INSTALAÇÃO:")
        for pacote in falhas:
            print(f"   • {pacote}")
        
        print("\n🔧 SOLUÇÕES ALTERNATIVAS:")
        print("   1. Tente instalar manualmente:")
        for pacote_info in pacotes:
            if pacote_info['nome'] in falhas:
                print(f"      {pacote_info['comando_install']}")
        
        print("\n   2. Verifique se tem pip atualizado:")
        print("      python3 -m pip install --upgrade pip")
        
        print("\n   3. Em sistemas Ubuntu/Debian, tente:")
        print("      sudo apt update && sudo apt install python3-pip")
    else:
        print("\n🎉 TODAS as dependências foram instaladas com sucesso!")
        print("   O sistema agora tem funcionalidades completas disponíveis.")
    
    print("\n💡 NOTA IMPORTANTE:")
    print("   • XGBoost é opcional - o sistema funciona sem ele")
    print("   • Seaborn é opcional - gráficos usarão matplotlib nativo")
    print("   • O sistema detecta automaticamente a disponibilidade")
    
    print(f"\n🏥 Sistema pronto para uso!")
    print("   Execute: python3 main_simples.py")

if __name__ == "__main__":
    main()