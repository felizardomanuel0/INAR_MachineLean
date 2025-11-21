"""
Configurações do Sistema de Diagnóstico de Doenças
"""

import os

# Informações do projeto
PROJECT_NAME = "Sistema de Diagnóstico de Doenças"
PROJECT_VERSION = "2.0.0"  # Atualizado para usar novos datasets
PROJECT_AUTHOR = "INAR - Terceiro Ano, II Semestre"

# Caminhos do projeto
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_DIR = os.path.join(BASE_DIR, 'dataset')
MODELS_DIR = os.path.join(BASE_DIR, 'modelos_salvos')
RESULTS_DIR = os.path.join(BASE_DIR, 'resultados')
GRAPHICS_DIR = os.path.join(RESULTS_DIR, 'graficos')

# Configurações de dados - NOVOS DATASETS
SYMPTOM_SEVERITY_FILE = 'Symptom-severity.csv'
DISEASE_DESCRIPTION_FILE = 'symptom_Description.csv'
DISEASE_PRECAUTION_FILE = 'symptom_precaution.csv'

# Caminhos dos novos datasets
SYMPTOM_SEVERITY_PATH = os.path.join(DATASET_DIR, SYMPTOM_SEVERITY_FILE)
DISEASE_DESCRIPTION_PATH = os.path.join(DATASET_DIR, DISEASE_DESCRIPTION_FILE)
DISEASE_PRECAUTION_PATH = os.path.join(DATASET_DIR, DISEASE_PRECAUTION_FILE)

# Compatibilidade com sistema antigo (deprecated)
DATASET_FILE = 'Disease_symptom_and_patient_profile_dataset.csv'
DATASET_PATH = os.path.join(DATASET_DIR, DATASET_FILE)

# Configurações de modelos
DEFAULT_TEST_SIZE = 0.2
DEFAULT_RANDOM_STATE = 42
DEFAULT_CV_FOLDS = 5

# Configurações da interface
WINDOW_TITLE = f"{PROJECT_NAME} - {PROJECT_VERSION}"
WINDOW_SIZE = "1200x800"

# Colunas esperadas no dataset
EXPECTED_COLUMNS = [
    'Disease', 'Fever', 'Cough', 'Fatigue', 'Difficulty Breathing',
    'Age', 'Gender', 'Blood Pressure', 'Cholesterol Level', 'Outcome Variable'
]

# Sintomas suportados
SYMPTOM_COLUMNS = ['Fever', 'Cough', 'Fatigue', 'Difficulty Breathing']

# Colunas demográficas
DEMOGRAPHIC_COLUMNS = ['Age', 'Gender']

# Colunas clínicas
CLINICAL_COLUMNS = ['Blood Pressure', 'Cholesterol Level']

# Target column
TARGET_COLUMN = 'Outcome Variable'

# Mapeamentos de valores
VALUE_MAPPINGS = {
    'symptoms': {'Yes': 1, 'No': 0},
    'gender': {'Male': 1, 'Female': 0},
    'blood_pressure': {'Low': 0, 'Normal': 1, 'High': 2},
    'cholesterol': {'Low': 0, 'Normal': 1, 'High': 2},
    'outcome': {'Positive': 1, 'Negative': 0}
}

# Configurações de logging
LOG_FILE = 'sistema_diagnostico.log'
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

# Cores da interface
COLORS = {
    'primary': '#2c3e50',
    'secondary': '#3498db',
    'success': '#27ae60',
    'danger': '#e74c3c',
    'warning': '#f39c12',
    'background': '#ecf0f1',
    'white': '#ffffff'
}

# Configurações de visualização
FIGURE_SIZE = (12, 8)
DPI = 300
PLOT_STYLE = 'seaborn-v0_8'

# Avisos e mensagens
MEDICAL_DISCLAIMER = """
⚠️ AVISO IMPORTANTE:
Este sistema é apenas para fins educacionais e de pesquisa.
Não deve ser usado para diagnósticos médicos reais.
Sempre consulte um profissional de saúde qualificado para questões médicas.
"""

# Algoritmos suportados
SUPPORTED_ALGORITHMS = [
    'Random Forest',
    'Logistic Regression', 
    'SVM',
    'K-Nearest Neighbors',
    'Naive Bayes',
    'Decision Tree',
    'Gradient Boosting',
    'XGBoost'
]