# 🏥 Sistema de Diagnóstico Médico - INAR 2025# Sistema de Diagnóstico de Doenças - INAR



## 📋 Descrição do Projeto## 🏥 Descrição do Projeto



Sistema inteligente de diagnóstico médico desenvolvido como projeto final da disciplina INAR (Terceiro Ano, II Semestre - 2025). O sistema utiliza técnicas de Machine Learning para analisar sintomas e fornecer possíveis diagnósticos com base em dados médicos estruturados.Este é um sistema completo de diagnóstico de doenças baseado em Machine Learning, desenvolvido como projeto final para o curso de INAR (Terceiro Ano, II Semestre). O sistema utiliza algoritmos de aprendizado de máquina para auxiliar no diagnóstico médico baseado em sintomas e características demográficas dos pacientes.



## ✨ Características Principais## ⚠️ Aviso Importante



- 🧠 **Análise Inteligente**: Algoritmo baseado em pesos de severidade de sintomas**Este sistema é apenas para fins educacionais e de pesquisa. Não deve ser usado para diagnósticos médicos reais. Sempre consulte um profissional de saúde qualificado para questões médicas.**

- 📊 **133 Sintomas**: Base de dados abrangente com sintomas médicos

- 🩺 **41 Doenças**: Diagnósticos para condições médicas diversas## 🎯 Funcionalidades

- 🇧🇷 **Interface em Português**: Completamente localizado para português brasileiro

- 📱 **Interface Gráfica**: Interface amigável desenvolvida com Tkinter- **📊 Análise Exploratória de Dados (EDA)**: Visualizações e estatísticas detalhadas do dataset

- 📋 **Descrições Detalhadas**: Informações completas sobre doenças e precauções- **🔧 Pré-processamento Inteligente**: Limpeza, codificação e normalização automática dos dados

- 📈 **Níveis de Confiança**: Sistema de probabilidades para maior precisão- **🤖 Múltiplos Algoritmos ML**: Random Forest, SVM, Logistic Regression, XGBoost, e mais

- **📈 Avaliação Completa**: Métricas detalhadas, matrizes de confusão, curvas ROC

## 🛠️ Tecnologias Utilizadas- **🖥️ Interface Gráfica Amigável**: GUI intuitiva para diagnóstico interativo

- **🔮 Sistema de Predição**: Predições em tempo real com interpretação dos resultados

- **Python 3.8+**- **📋 Relatórios Detalhados**: Exportação de resultados e estatísticas

- **Pandas** - Manipulação de dados

- **NumPy** - Computação numérica## 📁 Estrutura do Projeto

- **Scikit-learn** - Machine Learning

- **Tkinter** - Interface gráfica```

- **Matplotlib** - VisualizaçõesProjecto final 01/

- **Joblib** - Serialização de modelos├── dataset/                          # Dados de entrada

│   └── Disease_symptom_and_patient_profile_dataset.csv

## 📁 Estrutura do Projeto├── src/                             # Código fonte

│   ├── utils/                       # Utilitários e processamento

```│   │   ├── carregador_dados.py      # Carregamento e validação de dados

Projecto final 01/│   │   ├── analise_exploratoria.py  # Análise exploratória (EDA)

├── src/│   │   ├── preprocessador.py        # Pré-processamento de dados

│   ├── interface_grafica/│   │   ├── avaliador.py             # Avaliação de modelos

│   │   ├── app_portugues.py      # Interface principal em português│   │   └── sistema_predicao.py      # Sistema de predição

│   │   └── app_principal.py      # Interface alternativa│   ├── models/                      # Modelos de Machine Learning

│   ├── models/│   │   └── treinador_modelos.py     # Treinamento de modelos

│   │   ├── sistema_diagnostico_atualizado.py│   └── interface_grafica/           # Interface do usuário

│   │   └── treinador_modelos.py│       └── app_principal.py         # Aplicação principal GUI

│   └── utils/├── notebooks/                       # Jupyter notebooks (opcional)

│       ├── carregador_dados_atualizado.py├── modelos_salvos/                  # Modelos treinados salvos

│       ├── descricoes_doencas_portugues.py├── resultados/                      # Resultados e relatórios

│       ├── sintomas_portugues.py│   └── graficos/                    # Gráficos gerados

│       └── preprocessador.py├── requirements.txt                 # Dependências Python

├── dataset/├── main.py                         # Arquivo principal de execução

│   ├── Symptom-severity.csv└── README.md                       # Este arquivo

│   ├── symptom_Description.csv```

│   └── symptom_precaution.csv

├── main_atualizado.py            # Script principal## 🚀 Instalação e Configuração

├── requirements.txt

└── README.md### Pré-requisitos

```

- Python 3.8 ou superior

## 🚀 Instalação e Configuração- pip (gerenciador de pacotes Python)



### 1. Clone o Repositório### Instalação

```bash

git clone https://github.com/seu-usuario/sistema-diagnostico-medico.git1. **Clone ou baixe o projeto**:

cd sistema-diagnostico-medico   ```bash

```   cd "Projecto final 01"

   ```

### 2. Criar Ambiente Virtual

```bash2. **Instale as dependências**:

python -m venv venv   ```bash

source venv/bin/activate  # Linux/Mac   pip install -r requirements.txt

# ou   ```

venv\\Scripts\\activate   # Windows

```3. **Verifique a instalação**:

   ```bash

### 3. Instalar Dependências   python main.py --verificar

```bash   ```

pip install -r requirements.txt

```## 💻 Como Usar



### 4. Executar o Sistema### Interface Gráfica (Recomendado)

```bash

python main_atualizado.pyPara usar a interface gráfica amigável:

```

```bash

## 📦 Dependênciaspython main.py --gui

```

```

pandas>=1.3.0A interface possui 4 abas principais:

numpy>=1.21.0- **🔍 Diagnóstico**: Inserir dados do paciente e obter diagnóstico

scikit-learn>=1.0.0- **🤖 Treinamento**: Treinar modelos com seus próprios dados

matplotlib>=3.4.0- **📊 Visualização**: Ver gráficos e resultados

joblib>=1.1.0- **ℹ️ Sobre**: Informações sobre o sistema

```

### Pipeline Completo

## 💻 Como Usar

Para executar todo o processo de análise e treinamento:

### 1. **Iniciar o Sistema**

Execute `python main_atualizado.py` no terminal```bash

python main.py --pipeline

### 2. **Inserir Sintomas**```

- Selecione os sintomas apresentados pelo paciente

- Preencha dados demográficos (idade, gênero)Este comando irá:

- Informe dados clínicos (pressão arterial, colesterol)1. Carregar e validar os dados

2. Executar análise exploratória

### 3. **Obter Diagnóstico**3. Pré-processar os dados

- Clique em "Realizar Diagnóstico"4. Treinar múltiplos modelos

- Visualize os possíveis diagnósticos ordenados por probabilidade5. Avaliar e comparar modelos

- Consulte descrições detalhadas e precauções6. Salvar resultados e modelos



### 4. **Interpretar Resultados**### Análise Rápida

- 🔴 **Alta Probabilidade** (≥70%): Requer atenção médica imediata

- 🟡 **Probabilidade Média** (40-69%): Acompanhamento recomendadoPara uma análise exploratória rápida dos dados:

- 🟢 **Baixa Probabilidade** (<40%): Monitoramento básico

```bash

## 🔒 Aviso Médico Importantepython main.py --analise

```

⚠️ **ESTE SISTEMA É DESTINADO APENAS PARA FINS EDUCACIONAIS**

### Testar Predição

- Não substitui consulta médica profissional

- Não deve ser usado para autodiagnósticoPara testar o sistema de predição com dados de exemplo:

- Sempre procure um médico qualificado para diagnóstico definitivo

- Em caso de emergência médica, procure atendimento imediato```bash

python main.py --testar

## 🤝 Contribuições```



Contribuições são bem-vindas! Por favor:### Combinações



1. Fork o projetoVocê pode combinar comandos:

2. Crie uma branch para sua feature (`git checkout -b feature/MinhaFeature`)

3. Commit suas mudanças (`git commit -m 'Adiciona MinhaFeature'`)```bash

4. Push para a branch (`git push origin feature/MinhaFeature`)# Executar pipeline completo e depois abrir interface

5. Abra um Pull Requestpython main.py --pipeline --gui



## 📈 Métricas do Sistema# Análise rápida e teste

python main.py --analise --testar

- **Precisão**: ~85% em testes com datasets de validação```

- **Sintomas Suportados**: 133 sintomas únicos

- **Doenças Diagnosticáveis**: 41 condições médicas## 🤖 Algoritmos Suportados

- **Tempo de Resposta**: <2 segundos por diagnóstico

O sistema inclui os seguintes algoritmos de Machine Learning:

## 👥 Equipe de Desenvolvimento

1. **Random Forest** - Ensemble de árvores de decisão

**INAR - Terceiro Ano, II Semestre - 2025**2. **Logistic Regression** - Regressão logística

3. **Support Vector Machine (SVM)** - Máquinas de vetores de suporte

- **Desenvolvedor Principal**: Felizado Manuel4. **K-Nearest Neighbors (KNN)** - K-vizinhos mais próximos

- **Orientação Acadêmica**: Disciplina INAR5. **Naive Bayes** - Classificador Bayesiano

- **Projeto Final**: Sistema de Diagnóstico Médico6. **Decision Tree** - Árvore de decisão

7. **Gradient Boosting** - Gradient boosting

## 📝 Changelog8. **XGBoost** - Extreme gradient boosting



### v2.0 (2025-11-21)## 📊 Métricas de Avaliação

- ✅ Interface completamente em português

- ✅ Sistema de traduções médicasO sistema calcula e exibe as seguintes métricas:

- ✅ Melhor algoritmo de diagnóstico

- ✅ Descrições detalhadas das doenças- **Accuracy** - Precisão geral

- **Precision** - Precisão por classe

### v1.0 (2025-10-01)- **Recall** - Sensibilidade/Revocação

- 🎉 Primeira versão do sistema- **F1-Score** - Média harmônica entre precision e recall

- ⚡ Interface básica implementada- **AUC-ROC** - Área sob a curva ROC

- 📊 Integração com datasets médicos- **Matriz de Confusão** - Visualização de acertos e erros

- **Curvas ROC e Precisão-Recall** - Análise de desempenho

## 📄 Licença

## 🔧 Personalização

Este projeto é destinado para fins educacionais como parte da disciplina INAR.

### Usando Seus Próprios Dados

---

Para usar seus próprios dados, certifique-se de que o arquivo CSV tenha as seguintes colunas:

⭐ **Desenvolvido com ❤️ para fins educacionais - INAR 2025**
```
Disease,Fever,Cough,Fatigue,Difficulty Breathing,Age,Gender,Blood Pressure,Cholesterol Level,Outcome Variable
```

### Adicionando Novos Algoritmos

Para adicionar novos algoritmos, edite o arquivo `src/models/treinador_modelos.py` na função `_definir_modelos()`.

### Modificando a Interface

A interface pode ser personalizada editando `src/interface_grafica/app_principal.py`.

## 📈 Resultados

Após executar o pipeline, os resultados são salvos em:

- **`modelos_salvos/`** - Modelos treinados (.pkl)
- **`resultados/graficos/`** - Visualizações e gráficos
- **`resultados/relatorio_final_modelos.csv`** - Comparação de modelos
- **`sistema_diagnostico.log`** - Log de execução

## 🐛 Solução de Problemas

### Erro de Dependências

```bash
# Reinstalar dependências
pip install -r requirements.txt --upgrade
```

### Erro de Tkinter (Linux)

```bash
# Ubuntu/Debian
sudo apt-get install python3-tk

# CentOS/RHEL
sudo yum install tkinter
```

### Erro de Memória

Para datasets grandes, reduza o uso de Grid Search:
- Na interface: desmarque "Usar Grid Search"
- No código: use `usar_grid_search=False`

### Dataset Não Encontrado

Certifique-se de que o arquivo CSV está em `dataset/Disease_symptom_and_patient_profile_dataset.csv`

## 📚 Estrutura dos Dados

### Formato de Entrada

O dataset deve conter as seguintes colunas:

- **Disease**: Nome da doença (string)
- **Fever**: Febre (Yes/No)
- **Cough**: Tosse (Yes/No)
- **Fatigue**: Fadiga (Yes/No)
- **Difficulty Breathing**: Dificuldade para respirar (Yes/No)
- **Age**: Idade (número inteiro)
- **Gender**: Gênero (Male/Female)
- **Blood Pressure**: Pressão arterial (Low/Normal/High)
- **Cholesterol Level**: Nível de colesterol (Low/Normal/High)
- **Outcome Variable**: Resultado (Positive/Negative)

### Exemplo de Dados

```csv
Disease,Fever,Cough,Fatigue,Difficulty Breathing,Age,Gender,Blood Pressure,Cholesterol Level,Outcome Variable
Influenza,Yes,No,Yes,Yes,19,Female,Low,Normal,Positive
Common Cold,No,Yes,Yes,No,25,Female,Normal,Normal,Negative
```

## 🤝 Contribuições

Este é um projeto educacional. Sugestões e melhorias são bem-vindas!

## 📄 Licença

Este projeto é desenvolvido para fins educacionais e de pesquisa.

## 👨‍💻 Desenvolvimento

- **Linguagem**: Python 3.8+
- **Interface**: Tkinter
- **ML Libraries**: scikit-learn, XGBoost
- **Visualização**: Matplotlib, Seaborn, Plotly
- **Data Processing**: Pandas, NumPy

## 📞 Suporte

Para questões técnicas sobre o projeto, consulte:

1. Os logs de execução (`sistema_diagnostico.log`)
2. A documentação inline do código
3. Os exemplos de uso neste README

---

**Lembre-se**: Este sistema é apenas para fins educacionais. Para questões médicas reais, sempre consulte um profissional de saúde qualificado.