#!/bin/bash

# Script de Instalação Rápida - Sistema de Diagnóstico Simplificado
# Para Ubuntu/Debian

echo "🏥 Instalando Sistema de Diagnóstico Médico Simplificado"
echo "=========================================================="

# Verificar se está no diretório correto
if [ ! -f "main_simples.py" ]; then
    echo "❌ Erro: Execute este script no diretório do projeto"
    echo "   (onde está localizado o arquivo main_simples.py)"
    exit 1
fi

# Verificar se dados.csv existe
if [ ! -f "dataset/dados.csv" ]; then
    echo "❌ Erro: Arquivo dataset/dados.csv não encontrado"
    echo "   Certifique-se de que o arquivo dados.csv está na pasta dataset/"
    exit 1
fi

echo "✅ Arquivos do projeto encontrados"

# Atualizar sistema
echo "🔄 Atualizando lista de pacotes..."
sudo apt update

# Instalar dependências
echo "📦 Instalando dependências Python..."
sudo apt install -y python3-pandas python3-numpy python3-sklearn python3-tk

# Verificar instalação
echo "🧪 Testando instalação..."
python3 -c "import pandas, numpy, sklearn, tkinter; print('✅ Todas as dependências instaladas com sucesso')" 2>/dev/null

if [ $? -eq 0 ]; then
    echo "✅ Instalação concluída com sucesso!"
    echo ""
    echo "🚀 Para executar o sistema:"
    echo "   python3 main_simples.py"
    echo ""
    echo "📋 Opções disponíveis:"
    echo "   1. Interface gráfica (recomendado)"
    echo "   2. Teste no terminal"
    echo ""
    echo "📖 Leia README_SISTEMA_SIMPLES.md para mais informações"
else
    echo "❌ Erro na instalação das dependências"
    echo "   Verifique as mensagens de erro acima"
    exit 1
fi