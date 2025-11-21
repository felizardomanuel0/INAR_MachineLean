#!/usr/bin/env python3
"""
Teste simples para verificar se as traduções estão funcionando
"""

import sys
import os
from pathlib import Path

# Adicionar paths necessários
base_dir = Path(__file__).parent
sys.path.append(str(base_dir))
sys.path.append(str(base_dir / 'src' / 'utils'))

def testar_traducao():
    """Testa a funcionalidade de tradução"""
    try:
        print("🔍 Testando importação da tradução...")
        from src.utils.descricoes_doencas_portugues import obter_descricao_portugues, traduzir_descricao_se_necessario
        
        # Testar algumas traduções
        print("\n✅ Importação bem-sucedida!")
        
        teste_doencas = ["Malaria", "Diabetes ", "Common Cold"]
        
        for doenca in teste_doencas:
            descricao = obter_descricao_portugues(doenca)
            if descricao:
                print(f"\n🏥 {doenca}:")
                print(f"   {descricao[:100]}...")
            else:
                print(f"\n❌ Não encontrada tradução para: {doenca}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao testar tradução: {e}")
        import traceback
        traceback.print_exc()
        return False

def testar_carregador():
    """Testa o carregador de dados"""
    try:
        print("\n🔍 Testando carregador de dados...")
        from src.utils.carregador_dados_atualizado import CarregadorDadosAtualizado
        
        carregador = CarregadorDadosAtualizado()
        
        print("✅ Carregador iniciado com sucesso!")
        
        # Testar carregamento básico
        sintomas_pesos = carregador.carregar_sintomas_pesos()
        print(f"📊 Sintomas carregados: {len(sintomas_pesos)} itens")
        
        descricoes = carregador.carregar_descricoes_doencas() 
        print(f"📋 Descrições carregadas: {len(descricoes)} itens")
        
        # Testar uma descrição específica
        if 'Malaria' in descricoes:
            descricao_malaria = descricoes['Malaria']
            print(f"\n🦠 Malaria (primeiros 150 chars):")
            print(f"   {descricao_malaria[:150]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao testar carregador: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Função principal de teste"""
    print("🧪 TESTE SIMPLES DO SISTEMA DE TRADUÇÕES")
    print("=" * 50)
    
    # Verificar estrutura de arquivos
    dataset_dir = base_dir / 'dataset'
    if not dataset_dir.exists():
        print("❌ Diretório dataset não encontrado!")
        return False
    
    arquivos_necessarios = [
        'Symptom-severity.csv',
        'symptom_Description.csv', 
        'symptom_precaution.csv'
    ]
    
    for arquivo in arquivos_necessarios:
        caminho = dataset_dir / arquivo
        if not caminho.exists():
            print(f"❌ Arquivo não encontrado: {arquivo}")
            return False
        else:
            print(f"✅ {arquivo} encontrado")
    
    # Testar tradução
    if not testar_traducao():
        return False
    
    # Testar carregador
    if not testar_carregador():
        return False
    
    print("\n🎉 TODOS OS TESTES PASSARAM!")
    return True

if __name__ == "__main__":
    sucesso = main()
    sys.exit(0 if sucesso else 1)