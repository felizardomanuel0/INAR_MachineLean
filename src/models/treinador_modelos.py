"""
Módulo para Modelos de Machine Learning
Autor: Sistema de Diagnóstico de Doenças
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from xgboost import XGBClassifier
from sklearn.model_selection import GridSearchCV, cross_val_score
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, classification_report
import joblib
import os
from typing import Dict, List, Tuple, Any
import logging
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TreinadorModelos:
    """Classe para treinar e avaliar múltiplos modelos de Machine Learning"""
    
    def __init__(self):
        """Inicializa o treinador de modelos"""
        self.modelos = {}
        self.modelos_treinados = {}
        self.resultados = {}
        self.melhor_modelo = None
        self.melhor_score = 0
        
        # Definir modelos e seus hiperparâmetros
        self._definir_modelos()
    
    def _definir_modelos(self):
        """Define os modelos e seus hiperparâmetros para grid search"""
        
        self.modelos = {
            'Random Forest': {
                'modelo': RandomForestClassifier(random_state=42),
                'parametros': {
                    'n_estimators': [50, 100, 200],
                    'max_depth': [None, 10, 20],
                    'min_samples_split': [2, 5],
                    'min_samples_leaf': [1, 2]
                }
            },
            
            'Logistic Regression': {
                'modelo': LogisticRegression(random_state=42, max_iter=1000),
                'parametros': {
                    'C': [0.1, 1, 10],
                    'penalty': ['l1', 'l2'],
                    'solver': ['liblinear']
                }
            },
            
            'SVM': {
                'modelo': SVC(random_state=42, probability=True),
                'parametros': {
                    'C': [0.1, 1, 10],
                    'kernel': ['linear', 'rbf'],
                    'gamma': ['scale', 'auto']
                }
            },
            
            'K-Nearest Neighbors': {
                'modelo': KNeighborsClassifier(),
                'parametros': {
                    'n_neighbors': [3, 5, 7, 9],
                    'weights': ['uniform', 'distance'],
                    'metric': ['euclidean', 'manhattan']
                }
            },
            
            'Naive Bayes': {
                'modelo': GaussianNB(),
                'parametros': {
                    'var_smoothing': [1e-9, 1e-8, 1e-7]
                }
            },
            
            'Decision Tree': {
                'modelo': DecisionTreeClassifier(random_state=42),
                'parametros': {
                    'max_depth': [None, 5, 10, 15],
                    'min_samples_split': [2, 5, 10],
                    'min_samples_leaf': [1, 2, 4]
                }
            },
            
            'Gradient Boosting': {
                'modelo': GradientBoostingClassifier(random_state=42),
                'parametros': {
                    'n_estimators': [50, 100],
                    'learning_rate': [0.1, 0.01],
                    'max_depth': [3, 5]
                }
            },
            
            'XGBoost': {
                'modelo': XGBClassifier(random_state=42, eval_metric='logloss'),
                'parametros': {
                    'n_estimators': [50, 100],
                    'learning_rate': [0.1, 0.01],
                    'max_depth': [3, 6]
                }
            }
        }
    
    def treinar_modelo_individual(self, nome_modelo: str, X_train: pd.DataFrame, y_train: pd.Series,
                                 usar_grid_search: bool = True, cv_folds: int = 5) -> Dict:
        """
        Treina um modelo individual
        
        Args:
            nome_modelo (str): Nome do modelo
            X_train (pd.DataFrame): Dados de treino
            y_train (pd.Series): Target de treino
            usar_grid_search (bool): Se deve usar grid search
            cv_folds (int): Número de folds para cross-validation
            
        Returns:
            Dict: Resultados do treinamento
        """
        if nome_modelo not in self.modelos:
            raise ValueError(f"Modelo '{nome_modelo}' não está disponível")
        
        logger.info(f"🤖 Treinando {nome_modelo}...")
        inicio = time.time()
        
        modelo_config = self.modelos[nome_modelo]
        
        if usar_grid_search and modelo_config['parametros']:
            # Grid Search com Cross-Validation
            grid_search = GridSearchCV(
                modelo_config['modelo'],
                modelo_config['parametros'],
                cv=cv_folds,
                scoring='accuracy',
                n_jobs=-1,
                verbose=0
            )
            
            grid_search.fit(X_train, y_train)
            melhor_modelo = grid_search.best_estimator_
            melhores_params = grid_search.best_params_
            melhor_cv_score = grid_search.best_score_
            
        else:
            # Treinamento simples
            melhor_modelo = modelo_config['modelo']
            melhor_modelo.fit(X_train, y_train)
            melhores_params = melhor_modelo.get_params()
            
            # Cross-validation score
            cv_scores = cross_val_score(melhor_modelo, X_train, y_train, cv=cv_folds, scoring='accuracy')
            melhor_cv_score = cv_scores.mean()
        
        tempo_treinamento = time.time() - inicio
        
        # Salvar modelo treinado
        self.modelos_treinados[nome_modelo] = melhor_modelo
        
        resultado = {
            'modelo': melhor_modelo,
            'melhores_parametros': melhores_params,
            'cv_score': melhor_cv_score,
            'tempo_treinamento': tempo_treinamento
        }
        
        logger.info(f"✅ {nome_modelo} treinado! CV Score: {melhor_cv_score:.4f} | Tempo: {tempo_treinamento:.2f}s")
        
        return resultado
    
    def treinar_todos_modelos(self, X_train: pd.DataFrame, y_train: pd.Series,
                             usar_grid_search: bool = True, cv_folds: int = 5) -> Dict:
        """
        Treina todos os modelos
        
        Args:
            X_train (pd.DataFrame): Dados de treino
            y_train (pd.Series): Target de treino
            usar_grid_search (bool): Se deve usar grid search
            cv_folds (int): Número de folds para cross-validation
            
        Returns:
            Dict: Resultados de todos os modelos
        """
        logger.info("🚀 Iniciando treinamento de todos os modelos...")
        
        resultados_completos = {}
        
        for nome_modelo in self.modelos.keys():
            try:
                resultado = self.treinar_modelo_individual(
                    nome_modelo, X_train, y_train, usar_grid_search, cv_folds
                )
                resultados_completos[nome_modelo] = resultado
                
                # Verificar se é o melhor modelo
                if resultado['cv_score'] > self.melhor_score:
                    self.melhor_score = resultado['cv_score']
                    self.melhor_modelo = resultado['modelo']
                    
            except Exception as e:
                logger.error(f"Erro ao treinar {nome_modelo}: {str(e)}")
                resultados_completos[nome_modelo] = {'erro': str(e)}
        
        self.resultados = resultados_completos
        
        logger.info(f"🏆 Melhor modelo: {self._obter_nome_melhor_modelo()} com score: {self.melhor_score:.4f}")
        
        return resultados_completos
    
    def avaliar_modelos(self, X_test: pd.DataFrame, y_test: pd.Series) -> Dict:
        """
        Avalia todos os modelos treinados no conjunto de teste
        
        Args:
            X_test (pd.DataFrame): Dados de teste
            y_test (pd.Series): Target de teste
            
        Returns:
            Dict: Métricas de avaliação para todos os modelos
        """
        logger.info("📊 Avaliando modelos no conjunto de teste...")
        
        avaliacoes = {}
        
        for nome_modelo, modelo in self.modelos_treinados.items():
            try:
                # Fazer predições
                y_pred = modelo.predict(X_test)
                y_pred_proba = modelo.predict_proba(X_test)[:, 1] if hasattr(modelo, 'predict_proba') else None
                
                # Calcular métricas
                metricas = {
                    'accuracy': accuracy_score(y_test, y_pred),
                    'precision': precision_score(y_test, y_pred, average='weighted'),
                    'recall': recall_score(y_test, y_pred, average='weighted'),
                    'f1_score': f1_score(y_test, y_pred, average='weighted'),
                    'confusion_matrix': confusion_matrix(y_test, y_pred).tolist(),
                    'classification_report': classification_report(y_test, y_pred, output_dict=True)
                }
                
                if y_pred_proba is not None:
                    from sklearn.metrics import roc_auc_score
                    metricas['auc_roc'] = roc_auc_score(y_test, y_pred_proba)
                
                avaliacoes[nome_modelo] = metricas
                
                logger.info(f"✅ {nome_modelo} - Accuracy: {metricas['accuracy']:.4f} | F1: {metricas['f1_score']:.4f}")
                
            except Exception as e:
                logger.error(f"Erro ao avaliar {nome_modelo}: {str(e)}")
                avaliacoes[nome_modelo] = {'erro': str(e)}
        
        return avaliacoes
    
    def _obter_nome_melhor_modelo(self) -> str:
        """Retorna o nome do melhor modelo"""
        for nome, resultado in self.resultados.items():
            if 'modelo' in resultado and resultado['modelo'] == self.melhor_modelo:
                return nome
        return "Desconhecido"
    
    def obter_ranking_modelos(self, X_test: pd.DataFrame, y_test: pd.Series) -> pd.DataFrame:
        """
        Cria um ranking dos modelos baseado nas métricas de teste
        
        Args:
            X_test (pd.DataFrame): Dados de teste
            y_test (pd.Series): Target de teste
            
        Returns:
            pd.DataFrame: Ranking dos modelos
        """
        avaliacoes = self.avaliar_modelos(X_test, y_test)
        
        ranking_data = []
        
        for nome_modelo, metricas in avaliacoes.items():
            if 'erro' not in metricas:
                ranking_data.append({
                    'Modelo': nome_modelo,
                    'Accuracy': metricas['accuracy'],
                    'Precision': metricas['precision'],
                    'Recall': metricas['recall'],
                    'F1-Score': metricas['f1_score'],
                    'AUC-ROC': metricas.get('auc_roc', 'N/A'),
                    'CV Score': self.resultados[nome_modelo]['cv_score'],
                    'Tempo (s)': self.resultados[nome_modelo]['tempo_treinamento']
                })
        
        ranking_df = pd.DataFrame(ranking_data)
        ranking_df = ranking_df.sort_values('F1-Score', ascending=False).reset_index(drop=True)
        ranking_df.index = ranking_df.index + 1  # Começar ranking do 1
        
        return ranking_df
    
    def salvar_modelos(self, caminho: str, salvar_todos: bool = True):
        """
        Salva os modelos treinados
        
        Args:
            caminho (str): Caminho para salvar
            salvar_todos (bool): Se deve salvar todos os modelos ou apenas o melhor
        """
        os.makedirs(caminho, exist_ok=True)
        
        if salvar_todos:
            for nome_modelo, modelo in self.modelos_treinados.items():
                nome_arquivo = nome_modelo.lower().replace(' ', '_').replace('-', '_')
                caminho_modelo = os.path.join(caminho, f"{nome_arquivo}.pkl")
                joblib.dump(modelo, caminho_modelo)
                logger.info(f"Modelo {nome_modelo} salvo em: {caminho_modelo}")
        
        # Sempre salvar o melhor modelo
        if self.melhor_modelo is not None:
            caminho_melhor = os.path.join(caminho, "melhor_modelo.pkl")
            joblib.dump(self.melhor_modelo, caminho_melhor)
            
            # Salvar informações do melhor modelo
            info_melhor = {
                'nome': self._obter_nome_melhor_modelo(),
                'score': self.melhor_score
            }
            joblib.dump(info_melhor, os.path.join(caminho, "info_melhor_modelo.pkl"))
            
            logger.info(f"Melhor modelo salvo em: {caminho_melhor}")
    
    def carregar_modelo(self, caminho_modelo: str):
        """
        Carrega um modelo salvo
        
        Args:
            caminho_modelo (str): Caminho do modelo
            
        Returns:
            Modelo carregado
        """
        try:
            modelo = joblib.load(caminho_modelo)
            logger.info(f"Modelo carregado de: {caminho_modelo}")
            return modelo
        except Exception as e:
            logger.error(f"Erro ao carregar modelo: {e}")
            raise
    
    def fazer_predicao(self, modelo, X_novos: pd.DataFrame) -> Tuple[np.ndarray, np.ndarray]:
        """
        Faz predições com um modelo
        
        Args:
            modelo: Modelo treinado
            X_novos (pd.DataFrame): Dados para predição
            
        Returns:
            Tuple: Predições e probabilidades
        """
        predicoes = modelo.predict(X_novos)
        probabilidades = modelo.predict_proba(X_novos) if hasattr(modelo, 'predict_proba') else None
        
        return predicoes, probabilidades

def main():
    """Função para testar o módulo"""
    try:
        # Importar outros módulos necessários
        import sys
        sys.path.append('/home/felizado-manuel/Documentos/Faculdade/Terceiro/II Semestre/INAR/Projecto final 01/src/utils')
        
        from carregador_dados import CarregadorDados
        from preprocessador import PreProcessadorDados
        
        # Caminho do dataset
        caminho = "/home/felizado-manuel/Documentos/Faculdade/Terceiro/II Semestre/INAR/Projecto final 01/dataset/Disease_symptom_and_patient_profile_dataset.csv"
        
        # Carregar e processar dados
        carregador = CarregadorDados(caminho)
        dados = carregador.carregar_dados()
        
        preprocessador = PreProcessadorDados(dados)
        dados_processados = preprocessador.processar_dados_completo()
        
        # Treinar modelos
        treinador = TreinadorModelos()
        resultados = treinador.treinar_todos_modelos(
            dados_processados['X_train'], 
            dados_processados['y_train'],
            usar_grid_search=False  # Para teste rápido
        )
        
        # Avaliar modelos
        ranking = treinador.obter_ranking_modelos(
            dados_processados['X_test'], 
            dados_processados['y_test']
        )
        
        print("🏆 Ranking dos modelos:")
        print(ranking)
        
    except ImportError as e:
        print(f"Erro de importação: {e}")
        print("Execute este módulo a partir do arquivo principal")
    except Exception as e:
        print(f"Erro: {e}")

if __name__ == "__main__":
    main()