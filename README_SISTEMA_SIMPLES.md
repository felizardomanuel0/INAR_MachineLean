# Sistema de Diagnóstico Médico Simplificado

Sistema de diagnóstico médico que funciona exclusivamente com o dataset `dados.csv`, eliminando a dependência de múltiplos arquivos CSV.

## ✨ Características

- **🔧 Simplificado**: Funciona apenas com `dados.csv`
- **🎯 Eficiente**: Carregamento rápido de dados
- **💻 Interface Dupla**: Terminal e interface gráfica
- **📊 Estatísticas**: Informações detalhadas do sistema
- **📋 Histórico**: Registro de diagnósticos realizados
- **🔍 Busca**: Filtragem de sintomas em tempo real

## 📁 Estrutura do Projeto

```
Projecto final 01/
├── dataset/
│   └── dados.csv                    # Dataset principal (único necessário)
├── src/
│   ├── models/
│   │   ├── carregador_dados_simples.py      # Carregador de dados
│   │   └── sistema_diagnostico_simples.py   # Sistema de diagnóstico
│   └── ui/
│       └── interface_diagnostico_simples.py # Interface gráfica
├── main_simples.py                  # Arquivo principal de execução
└── README_SISTEMA_SIMPLES.md        # Este arquivo
```

## 🚀 Como Usar

### Executar o Sistema

```bash
cd "Projecto final 01"
python3 main_simples.py
```

### Opções Disponíveis

1. **Interface Gráfica** (Recomendado)
   - Interface amigável com abas
   - Seleção múltipla de sintomas
   - Visualização de resultados
   - Estatísticas em tempo real

2. **Teste no Terminal**
   - Execução rápida via linha de comando
   - Ideal para testes e desenvolvimento

## 📊 Dataset: dados.csv

### Formato Esperado
```csv
Disease,Symptom_1,Symptom_2,Symptom_3,...,Symptom_17
Fungal infection,itching,skin_rash,nodal_skin_eruptions,dischromic_patches
...
```

### Características
- **Colunas**: 1 coluna Disease + 17 colunas de sintomas
- **Registros**: ~4920 entradas
- **Doenças**: 41 doenças únicas
- **Sintomas**: 131 sintomas únicos

## 🔧 Componentes Principais

### 1. CarregadorDadosSimplificado
```python
# Carrega e processa dados do dados.csv
carregador = CarregadorDadosSimplificado()
carregador.carregar_dados_principais()
```

### 2. SistemaDiagnosticoSimples
```python
# Sistema de diagnóstico principal
sistema = SistemaDiagnosticoSimples()
resultado = sistema.realizar_diagnostico(['itching', 'skin_rash'])
```

### 3. InterfaceDiagnosticoSimples
```python
# Interface gráfica
app = InterfaceDiagnosticoSimples()
app.run()
```

## 📋 Funcionalidades

### 🩺 Diagnóstico
- Seleção múltipla de sintomas
- Cálculo de probabilidades
- Níveis de confiança (Alta/Média/Baixa)
- Ranking de diagnósticos

### 📊 Estatísticas
- Total de registros carregados
- Número de doenças e sintomas
- Estatísticas de uso do sistema
- Diagnósticos realizados

### 🔍 Busca e Filtros
- Busca de sintomas por texto
- Filtros em tempo real
- Lista ordenada alfabeticamente

### 📋 Histórico
- Registro de todos os diagnósticos
- Timestamp de cada consulta
- Estatísticas de confiabilidade
- Opção de limpar histórico

## 🎯 Como Funciona o Diagnóstico

1. **Entrada**: Usuário seleciona sintomas
2. **Processamento**: Sistema calcula correspondências
3. **Cálculo**: Probabilidade = (sintomas_em_comum / total_sintomas_doenca) × 100
4. **Resultado**: Lista ordenada por probabilidade

### Níveis de Confiança
- **Alta** (≥70%): 🔴 Forte correspondência
- **Média** (40-69%): 🟡 Correspondência moderada
- **Baixa** (20-39%): 🟢 Correspondência fraca
- **Muito Baixa** (<20%): 🟢 Correspondência muito fraca

## 🛠️ Dependências

### Pacotes Python
```bash
sudo apt install python3-pandas python3-numpy python3-sklearn python3-tk
```

### Bibliotecas Utilizadas
- `pandas`: Manipulação de dados
- `numpy`: Cálculos numéricos
- `tkinter`: Interface gráfica
- `logging`: Sistema de logs

## 📝 Exemplo de Uso

### Via Terminal
```python
from src.models.sistema_diagnostico_simples import SistemaDiagnosticoSimples

# Inicializar sistema
sistema = SistemaDiagnosticoSimples()

# Realizar diagnóstico
sintomas = ['itching', 'skin_rash', 'nodal_skin_eruptions']
resultado = sistema.realizar_diagnostico(sintomas)

# Ver resultado
print(f"Diagnósticos: {resultado['total_diagnosticos']}")
for diag in resultado['diagnosticos'][:3]:
    print(f"- {diag['doenca']}: {diag['probabilidade']:.1f}%")
```

### Via Interface Gráfica
1. Execute `python3 main_simples.py`
2. Escolha opção "1" (Interface gráfica)
3. Selecione sintomas na lista à esquerda
4. Clique "Adicionar Selecionados"
5. Clique "🔍 Realizar Diagnóstico"
6. Veja os resultados na área de resultados

## 🔍 Logs e Debugging

### Arquivo de Log
- **Localização**: `sistema_diagnostico_simples.log`
- **Conteúdo**: Operações do sistema, erros, estatísticas
- **Rotação**: Manual (limpar quando necessário)

### Níveis de Log
- `INFO`: Operações normais
- `ERROR`: Erros do sistema
- `DEBUG`: Informações detalhadas (se habilitado)

## ⚠️ Importante

### Disclaimer Médico
Este sistema é apenas para fins educacionais e de apoio ao diagnóstico. **NUNCA** substitui a consulta com um profissional de saúde qualificado.

### Uso Responsável
- Use apenas como ferramenta de apoio
- Sempre consulte um médico
- Não tome decisões médicas baseadas apenas neste sistema

## 🚀 Performance

### Tempos Típicos
- **Carregamento**: ~3-5 segundos
- **Diagnóstico**: <1 segundo
- **Interface**: Responsiva em tempo real

### Recursos do Sistema
- **RAM**: ~50-100MB durante execução
- **CPU**: Baixo uso (principalmente I/O)
- **Armazenamento**: ~2MB para dataset

## 🔄 Diferenças da Versão Original

### Simplificações
- ✅ **Único arquivo**: Apenas `dados.csv`
- ✅ **Imports simples**: Estrutura de módulos simplificada
- ✅ **Menos dependências**: Sem XGBoost e outros modelos complexos
- ✅ **Setup rápido**: Instalação mais fácil

### Funcionalidades Mantidas
- ✅ Interface gráfica completa
- ✅ Sistema de diagnóstico
- ✅ Estatísticas e histórico
- ✅ Busca e filtros
- ✅ Logs detalhados

## 📞 Suporte

Para problemas ou dúvidas:
1. Verifique se o arquivo `dados.csv` está na pasta `dataset/`
2. Confirme que as dependências estão instaladas
3. Execute o teste no terminal primeiro
4. Verifique o arquivo de log para detalhes de erros

---
**Desenvolvido para o curso INAR - Machine Learning**  
*Versão Simplificada - Novembro 2025*