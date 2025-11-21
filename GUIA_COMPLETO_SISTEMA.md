# 🏥 GUIA COMPLETO: Como Funciona o Sistema de Diagnóstico Médico

## 📋 ÍNDICE
1. [Visão Geral do Sistema](#visao-geral)
2. [Como Usar o Sistema (Guia Prático)](#como-usar)
3. [Como Funciona por Trás (Técnico)](#como-funciona-tecnico)
4. [Machine Learning Explicado](#machine-learning)
5. [Estrutura do Projeto](#estrutura-projeto)
6. [Fluxo Completo de Diagnóstico](#fluxo-diagnostico)
7. [Perguntas Frequentes](#faq)

---

## 🎯 VISÃO GERAL DO SISTEMA {#visao-geral}

### **O Que É**
Sistema inteligente de diagnóstico médico que usa **Inteligência Artificial** para analisar sintomas e sugerir possíveis doenças. Foi desenvolvido como projeto acadêmico para o curso INAR.

### **Objetivo Principal**
- ✅ **Auxiliar** profissionais de saúde e estudantes
- ✅ **Demonstrar** aplicação prática de Machine Learning
- ✅ **Facilitar** análise inicial de sintomas
- ⚠️ **NÃO substitui** consulta médica real

### **Capacidades do Sistema**
- 🩺 Analisa **70+ sintomas diferentes**
- 🏥 Diagnostica **116 doenças** específicas
- 🤖 Usa **8 algoritmos** de Machine Learning
- 🇵🇹 Interface **100% em português**
- 📊 Gera **relatórios profissionais**
- 💾 **Salva histórico** de consultas

---

## 🚀 COMO USAR O SISTEMA (GUIA PRÁTICO) {#como-usar}

### **Passo 1: Iniciar o Sistema**
```bash
# No terminal Linux:
cd "Projecto final 01"
source venv/bin/activate
python main.py --gui
```

### **Passo 2: Preencher Dados do Paciente**
1. **Nome do Paciente**: Digite o nome completo
2. **Idade**: Insira a idade em anos
3. **Gênero**: Selecione Masculino ou Feminino
4. **Pressão Arterial**: Escolha Baixa/Normal/Alta
5. **Colesterol**: Selecione Baixo/Normal/Alto

### **Passo 3: Selecionar Sintomas**

#### **Sintomas Principais (Checkboxes)**
- ✅ Febre
- ✅ Tosse  
- ✅ Fadiga
- ✅ Dificuldade para Respirar
- ✅ Dor de Cabeça
- ✅ Dor no Corpo
- ✅ Náusea
- ✅ Diarreia
- ✅ Dor no Peito
- ✅ Dor de Garganta

#### **Sintomas Adicionais**
- **Lista Completa**: Escolha da lista de 70+ sintomas
- **Entrada Manual**: Digite sintomas personalizados
- **Exemplos**: "Dor no estômago", "Coceira nas pernas"

### **Passo 4: Informações Temporais**
- **Duração**: Há quanto tempo sente os sintomas
  - Menos de 1 dia → Mais de 1 ano
- **Intensidade**: Nível de gravidade (1-10)
  - Leve → Moderada → Grave → Muito Grave

### **Passo 5: Realizar Diagnóstico**
- **Botão**: "🔍 Realizar Diagnóstico"
- **Atalho**: Tecla `F5`
- **Aguardar**: Processamento da IA

### **Passo 6: Ver Resultado**
- **Dados do Paciente**: Resumo completo
- **Sintomas**: Lista organizada
- **Diagnóstico**: Doença sugerida
- **Confiança**: Probabilidade do modelo
- **Recomendações**: Orientações específicas

### **Passo 7: Salvar Consulta**
- **Rápido**: `Ctrl + S` (salva automaticamente)
- **Completo**: Botão "💾 Salvar Consulta"
- **Histórico**: Botão "📊 Ver Histórico"

---

## 🔬 COMO FUNCIONA POR TRÁS (TÉCNICO) {#como-funciona-tecnico}

### **Arquitetura do Sistema**

```
📁 Sistema de Diagnóstico
├── 🎯 Interface Gráfica (Frontend)
│   └── Tkinter + Python
├── 🧠 Motor de IA (Backend)  
│   └── 8 Algoritmos de ML
├── 📊 Base de Dados
│   └── CSV com 350+ casos reais
└── 💾 Sistema de Arquivos
    └── Consultas + Histórico
```

### **Fluxo de Processamento**

#### **1. Coleta de Dados**
```python
dados_paciente = {
    'Fever': 'Yes/No',
    'Cough': 'Yes/No', 
    'Age': numero,
    'Gender': 'Male/Female',
    # ... outros campos
}
```

#### **2. Pré-processamento**
```python
# Conversão para formato numérico
'Yes' → 1, 'No' → 0
'Male' → 1, 'Female' → 0  
'Normal' → 1, 'High' → 2, 'Low' → 0
```

#### **3. Predição com IA**
```python
# Modelo treinado faz a predição
predicao = modelo.predict(dados_processados)
probabilidade = modelo.predict_proba(dados_processados)
```

#### **4. Interpretação Inteligente**
```python
# Algoritmo de diagnóstico diferencial
if 'Febre' + 'Tosse' + 'Dificuldade Respirar':
    return 'Pneumonia'
elif 'Febre' + 'Dor de Cabeça' + 'Calafrios':
    return 'Malária'
# ... outras regras
```

### **Componentes Principais**

#### **Interface Gráfica** (`app_portugues.py`)
- **Tkinter**: Biblioteca gráfica nativa Python
- **4 Abas**: Diagnóstico, Treinamento, Resultados, Sobre
- **Widgets**: Botões, campos, listas, áreas de texto
- **Eventos**: Cliques, atalhos, scroll, redimensionamento

#### **Carregador de Dados** (`carregador_dados.py`)
- **Função**: Lê arquivo CSV com dados médicos
- **Validação**: Verifica integridade dos dados
- **Limpeza**: Remove dados inválidos ou incompletos

#### **Pré-processador** (`preprocessador.py`)
- **Codificação**: Converte texto em números
- **Normalização**: Padroniza escalas de valores
- **Divisão**: Separa dados treino/teste
- **Salvamento**: Guarda configurações para uso futuro

#### **Treinador de Modelos** (`treinador_modelos.py`)
- **8 Algoritmos**: RF, SVM, LR, KNN, NB, DT, GB, XGB
- **Grid Search**: Otimização automática de parâmetros
- **Validação Cruzada**: Teste de robustez do modelo
- **Ranking**: Comparação de performance

#### **Avaliador** (`avaliador.py`)
- **Métricas**: Accuracy, Precision, Recall, F1-Score
- **Gráficos**: ROC Curves, Confusion Matrix
- **Relatórios**: Análise detalhada de performance

#### **Sistema de Predição** (`sistema_predicao.py`)
- **Carregamento**: Recupera modelo treinado
- **Validação**: Verifica entrada do usuário
- **Predição**: Executa diagnóstico
- **Interpretação**: Gera explicação em português

---

## 🤖 MACHINE LEARNING EXPLICADO {#machine-learning}

### **O Que É Machine Learning**
Técnica de **Inteligência Artificial** onde o computador **aprende padrões** a partir de dados históricos para fazer **predições** sobre novos casos.

### **Como o Sistema Aprende**

#### **Fase 1: Treinamento**
```
📊 Dados Históricos (350 casos)
↓
🔄 Algoritmos analisam padrões
↓  
🧠 Modelo treinado é criado
```

**Exemplo Simplificado**:
```
Caso 1: Febre=Sim, Tosse=Sim, Idade=25 → Gripe
Caso 2: Febre=Sim, Tosse=Não, Idade=35 → Malária  
Caso 3: Febre=Não, Tosse=Sim, Idade=45 → Bronquite
...
IA aprende: "Febre + Tosse = provavelmente Gripe"
```

#### **Fase 2: Predição**
```
🩺 Novo paciente com sintomas
↓
🧠 Modelo analisa padrões aprendidos
↓
🎯 Predição: "85% chance de ser Gripe"
```

### **Os 8 Algoritmos Usados**

#### **1. Random Forest (Floresta Aleatória)**
- **Como funciona**: Combina centenas de "árvores de decisão"
- **Vantagem**: Muito preciso e robusto
- **Analogia**: Como consultar vários médicos e usar a opinião da maioria

#### **2. Support Vector Machine (SVM)**
- **Como funciona**: Encontra a melhor "linha" que separa doenças
- **Vantagem**: Funciona bem com dados complexos
- **Analogia**: Como traçar uma linha para separar sintomas de diferentes doenças

#### **3. Logistic Regression (Regressão Logística)**
- **Como funciona**: Calcula probabilidade matemática
- **Vantagem**: Rápido e interpretável
- **Analogia**: Como uma fórmula matemática que considera peso de cada sintoma

#### **4. K-Nearest Neighbors (KNN)**
- **Como funciona**: Compara com casos mais similares
- **Vantagem**: Simples e intuitivo
- **Analogia**: "Seus sintomas são parecidos com estes 5 casos que eram gripe"

#### **5. Naive Bayes**
- **Como funciona**: Usa probabilidade estatística
- **Vantagem**: Funciona bem com poucos dados
- **Analogia**: "Estatisticamente, esses sintomas indicam 70% chance de gripe"

#### **6. Decision Tree (Árvore de Decisão)**
- **Como funciona**: Cria uma árvore de perguntas
- **Vantagem**: Fácil de entender o raciocínio
- **Analogia**: "Tem febre? Sim. Tem tosse? Sim. Então é gripe."

#### **7. Gradient Boosting**
- **Como funciona**: Combina vários modelos simples
- **Vantagem**: Muito preciso para casos complexos
- **Analogia**: Como vários especialistas corrigindo uns aos outros

#### **8. XGBoost (Extreme Gradient Boosting)**
- **Como funciona**: Versão otimizada do Gradient Boosting
- **Vantagem**: Estado da arte em competições de ML
- **Analogia**: A versão "turbinada" do algoritmo anterior

### **Como Escolhemos o Melhor**
1. **Treinamento**: Todos os 8 algoritmos são treinados
2. **Teste**: Cada um faz predições em casos não vistos
3. **Avaliação**: Medimos precisão, recall, F1-score
4. **Ranking**: Ordenamos do melhor para o pior
5. **Seleção**: O melhor é usado para diagnósticos

---

## 🏗️ ESTRUTURA DO PROJETO {#estrutura-projeto}

### **Organização de Pastas**
```
📁 Projecto final 01/
├── 📄 main.py                    # Arquivo principal
├── 📄 requirements.txt           # Dependências Python
├── 📄 README.md                 # Documentação geral
├── 📄 testar_sistema.py         # Testes automáticos
├── 📄 config.py                 # Configurações
│
├── 📁 src/                      # Código fonte
│   ├── 📁 utils/                # Utilitários
│   │   ├── carregador_dados.py
│   │   ├── analise_exploratoria.py
│   │   ├── preprocessador.py
│   │   ├── sistema_predicao.py
│   │   ├── traducao_doencas.py
│   │   └── sintomas_portugues.py
│   ├── 📁 models/               # Modelos ML
│   │   ├── treinador_modelos.py
│   │   └── avaliador.py
│   └── 📁 interface_grafica/    # Interface
│       ├── app_principal.py
│       └── app_portugues.py
│
├── 📁 dataset/                  # Base de dados
│   └── Disease_symptom_and_patient_profile_dataset.csv
│
├── 📁 modelos_salvos/           # Modelos treinados
│   ├── melhor_modelo.pkl
│   ├── encoders.pkl
│   └── scaler.pkl
│
├── 📁 consultas_salvas/         # Consultas realizadas
│   ├── 📁 relatorios/
│   ├── 📁 historico/
│   └── 📁 backup/
│
├── 📁 notebooks/                # Jupyter Notebooks
│   └── analise_exploratoria.ipynb
│
├── 📁 resultados/               # Gráficos e análises
│
└── 📁 venv/                     # Ambiente virtual Python
```

### **Fluxo de Dados**
```
CSV Dataset → Carregador → Pré-processador → Treinador → Modelo Salvo
                                                            ↓
Novo Paciente → Interface → Predição ← Sistema Predicao ← Modelo
                    ↓
              Resultado → Relatório → Arquivo Salvo
```

---

## 🔄 FLUXO COMPLETO DE DIAGNÓSTICO {#fluxo-diagnostico}

### **1. Inicialização do Sistema**
```python
# Quando você abre o programa
✅ Carrega bibliotecas necessárias
✅ Verifica dependências instaladas  
✅ Cria estrutura de pastas
✅ Carrega modelo pré-treinado
✅ Inicializa interface gráfica
```

### **2. Entrada de Dados**
```python
# Quando você preenche o formulário
✅ Valida campos obrigatórios
✅ Organiza sintomas selecionados
✅ Converte dados para formato padrão
✅ Aplica regras de validação
```

### **3. Processamento Inteligente**
```python
# Quando clica "Realizar Diagnóstico"
✅ Cria DataFrame com dados do paciente
✅ Aplica pré-processamento (codificação)
✅ Executa predição com modelo treinado
✅ Calcula probabilidades de confiança
✅ Aplica algoritmo de diagnóstico diferencial
```

### **4. Geração do Resultado**
```python
# Sistema gera relatório completo
✅ Formata dados do paciente
✅ Lista sintomas organizadamente
✅ Apresenta diagnóstico sugerido
✅ Mostra confiança do modelo
✅ Gera recomendações específicas
✅ Adiciona avisos médicos
```

### **5. Salvamento e Histórico**
```python
# Quando salva a consulta
✅ Cria arquivo .txt com relatório
✅ Registra no histórico CSV
✅ Organiza em pastas por data
✅ Atualiza estatísticas de uso
```

### **Exemplo Prático Completo**

#### **Entrada**:
```
Paciente: João Silva, 35 anos, Masculino
Sintomas: Febre, Tosse, Dor de Cabeça  
Duração: 3-7 dias
Intensidade: Moderada (4-6)
```

#### **Processamento**:
```python
dados = {
    'Fever': 1, 'Cough': 1, 'Fatigue': 0, 
    'Difficulty_Breathing': 0, 'Age': 35, 
    'Gender': 1, 'Blood_Pressure': 1, 'Cholesterol': 1
}

# Modelo analisa padrões e decide:
probabilidade_gripe = 0.87  # 87%
probabilidade_outras = 0.13 # 13%
```

#### **Diagnóstico Diferencial**:
```python
if febre + tosse + dor_cabeca:
    if duracao_curta:
        return "Gripe" 
    elif calafrios:
        return "Malária"
    else:
        return "Resfriado"
```

#### **Resultado**:
```
🎯 DIAGNÓSTICO: Gripe (87% confiança)
💡 RECOMENDAÇÕES: Repouso, hidratação, procurar médico se piorar
⚠️ AVISO: Não substitui consulta médica real
```

---

## ❓ PERGUNTAS FREQUENTES {#faq}

### **Sobre Funcionamento**

**P: Como o sistema sabe qual doença é?**
R: O sistema usa 8 algoritmos de IA treinados com 350+ casos médicos reais. Ele identifica padrões entre sintomas e doenças, calculando probabilidades baseadas em casos similares já vistos.

**P: Por que às vezes o diagnóstico muda com sintomas parecidos?**  
R: Pequenas diferenças (idade, gênero, duração) podem alterar significativamente as probabilidades. É como um médico considerando todo o contexto, não apenas sintomas isolados.

**P: O sistema pode errar?**
R: Sim, como qualquer ferramenta diagnóstica. Por isso sempre mostramos o nível de confiança e recomendamos consulta médica real.

### **Sobre Uso Prático**

**P: Posso confiar 100% no diagnóstico?**
R: NÃO. O sistema é educacional e deve ser usado apenas como ferramenta de apoio. Sempre procure um médico qualificado.

**P: Funciona para crianças?** 
R: O sistema foi treinado com dados de adultos. Para crianças, sempre consulte um pediatra.

**P: E se eu não souber alguns dados (pressão, colesterol)?**
R: O sistema funciona, mas pode ser menos preciso. Preencha o máximo de informações possível.

### **Sobre Aspectos Técnicos**

**P: Por que 8 algoritmos diferentes?**
R: Cada algoritmo tem pontos fortes diferentes. Comparando todos, escolhemos o mais preciso para cada caso.

**P: Como vocês validaram o sistema?**
R: Usamos validação cruzada, dividindo dados em treino/teste, e métricas padrão da área médica (sensibilidade, especificidade, etc.).

**P: O sistema aprende com novos casos?**
R: Atualmente não, mas pode ser retreinado periodicamente com novos dados.

### **Sobre Dados e Privacidade**

**P: Meus dados ficam seguros?**
R: Sim, todos os dados são salvos apenas no seu computador local. Nada é enviado pela internet.

**P: Posso deletar consultas antigas?**
R: Sim, você tem controle total sobre os arquivos na pasta `consultas_salvas`.

**P: O sistema funciona offline?**
R: Sim, completamente offline após instalação.

---

## 🎓 COMO EXPLICAR PARA OUTROS

### **Para Leigos (Versão Simples)**
> "É como um médico robô que aprendeu analisando milhares de casos. Você conta os sintomas, ele compara com casos parecidos e sugere qual doença pode ser. Mas é só uma opinião inicial - sempre precisa de médico de verdade."

### **Para Estudantes (Versão Educacional)**
> "Sistema de machine learning que implementa classificação multiclasse usando ensemble de algoritmos. Treina com dataset médico real, aplica pré-processamento de features categóricas e numéricas, e usa voting classifier para predição final com interpretação por regras heurísticas."

### **Para Profissionais (Versão Técnica)**
> "Pipeline completo de ML médico em Python: carregamento/validação de dados, feature engineering com encoders personalizados, treinamento de 8 algoritmos (RF, SVM, LR, KNN, NB, DT, GB, XGB) com grid search, avaliação cruzada, seleção do melhor modelo por métricas médicas, deploy em interface Tkinter com sistema de persistence e logging estruturado."

### **Demonstração Prática (5 minutos)**
1. **Abrir sistema** (30s)
2. **Preencher caso exemplo** - paciente com gripe (1min)
3. **Mostrar diagnóstico** e explicar confiança (2min)  
4. **Salvar consulta** e mostrar histórico (1min)
5. **Explicar limitações** e uso educacional (30s)

---

## 🏆 CONCLUSÃO

Este sistema representa uma **aplicação prática completa** de Machine Learning na área médica, demonstrando:

✅ **Coleta e processamento** de dados médicos reais
✅ **Implementação de múltiplos algoritmos** de IA  
✅ **Interface profissional** em português
✅ **Sistema completo** de persistence e logging
✅ **Boas práticas** de desenvolvimento de software
✅ **Aplicação responsável** com avisos éticos claros

É uma ferramenta **educacional valiosa** que mostra como a tecnologia pode auxiliar (mas não substituir) profissionais de saúde, sempre respeitando os limites éticos e a necessidade de supervisão médica humana.

---

*Sistema desenvolvido para Projeto Final INAR - 2025*  
*Terceiro Ano, II Semestre*