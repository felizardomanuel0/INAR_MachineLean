"""
Módulo para Avaliação e Métricas de Modelos
Autor: Sistema de Diagnóstico de Doenças
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, classification_report, roc_curve, auc,
    precision_recall_curve, average_precision_score
)
from sklearn.model_selection import learning_curve, validation_curve
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from typing import Dict, List, Tuple, Any
import warnings
warnings.filterwarnings('ignore')

class AvaliadorModelos:
    """Classe para avaliação completa de modelos de Machine Learning"""
    
    def __init__(self):
        """Inicializa o avaliador"""
        self.resultados_avaliacao = {}
        self.nomes_classes = ['Negative', 'Positive']
    
    def calcular_metricas_basicas(self, y_true: np.ndarray, y_pred: np.ndarray, 
                                 y_pred_proba: np.ndarray = None) -> Dict[str, float]:
        """
        Calcula métricas básicas de classificação
        
        Args:
            y_true (np.ndarray): Valores verdadeiros
            y_pred (np.ndarray): Predições
            y_pred_proba (np.ndarray): Probabilidades preditas
            
        Returns:
            Dict[str, float]: Dicionário com métricas
        """
        metricas = {
            'accuracy': accuracy_score(y_true, y_pred),
            'precision_macro': precision_score(y_true, y_pred, average='macro'),
            'precision_weighted': precision_score(y_true, y_pred, average='weighted'),
            'recall_macro': recall_score(y_true, y_pred, average='macro'),
            'recall_weighted': recall_score(y_true, y_pred, average='weighted'),
            'f1_macro': f1_score(y_true, y_pred, average='macro'),
            'f1_weighted': f1_score(y_true, y_pred, average='weighted')
        }
        
        # Adicionar AUC-ROC se probabilidades estiverem disponíveis
        if y_pred_proba is not None:
            try:
                metricas['auc_roc'] = auc(*roc_curve(y_true, y_pred_proba)[:2])
                metricas['average_precision'] = average_precision_score(y_true, y_pred_proba)
            except:
                pass
        
        return metricas
    
    def matriz_confusao(self, y_true: np.ndarray, y_pred: np.ndarray, 
                       titulo: str = "Matriz de Confusão", salvar_fig: bool = False, 
                       caminho_salvar: str = None) -> np.ndarray:
        """
        Gera e visualiza matriz de confusão
        
        Args:
            y_true (np.ndarray): Valores verdadeiros
            y_pred (np.ndarray): Predições
            titulo (str): Título do gráfico
            salvar_fig (bool): Se deve salvar a figura
            caminho_salvar (str): Caminho para salvar
            
        Returns:
            np.ndarray: Matriz de confusão
        """
        cm = confusion_matrix(y_true, y_pred)
        
        plt.figure(figsize=(8, 6))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                   xticklabels=self.nomes_classes, 
                   yticklabels=self.nomes_classes)
        plt.title(titulo, fontsize=16, fontweight='bold')
        plt.xlabel('Predição', fontsize=12)
        plt.ylabel('Valor Real', fontsize=12)
        
        # Adicionar estatísticas
        total = cm.sum()
        accuracy = (cm[0,0] + cm[1,1]) / total
        plt.figtext(0.15, 0.02, f'Accuracy: {accuracy:.3f}', fontsize=12, fontweight='bold')
        
        if salvar_fig and caminho_salvar:
            plt.savefig(f"{caminho_salvar}/matriz_confusao.png", dpi=300, bbox_inches='tight')
        
        plt.tight_layout()
        plt.show()
        
        return cm
    
    def curva_roc(self, y_true: np.ndarray, y_pred_proba: np.ndarray, 
                  titulo: str = "Curva ROC", salvar_fig: bool = False, 
                  caminho_salvar: str = None) -> Tuple[np.ndarray, np.ndarray, float]:
        """
        Gera curva ROC
        
        Args:
            y_true (np.ndarray): Valores verdadeiros
            y_pred_proba (np.ndarray): Probabilidades preditas
            titulo (str): Título do gráfico
            salvar_fig (bool): Se deve salvar a figura
            caminho_salvar (str): Caminho para salvar
            
        Returns:
            Tuple[np.ndarray, np.ndarray, float]: FPR, TPR, AUC
        """
        fpr, tpr, thresholds = roc_curve(y_true, y_pred_proba)
        roc_auc = auc(fpr, tpr)
        
        plt.figure(figsize=(8, 6))
        plt.plot(fpr, tpr, color='darkorange', lw=2, 
                label=f'Curva ROC (AUC = {roc_auc:.2f})')
        plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--', 
                label='Classificador Aleatório')
        
        plt.xlim([0.0, 1.0])
        plt.ylim([0.0, 1.05])
        plt.xlabel('Taxa de Falsos Positivos (1 - Especificidade)')
        plt.ylabel('Taxa de Verdadeiros Positivos (Sensibilidade)')
        plt.title(titulo, fontweight='bold')
        plt.legend(loc="lower right")
        plt.grid(alpha=0.3)
        
        if salvar_fig and caminho_salvar:
            plt.savefig(f"{caminho_salvar}/curva_roc.png", dpi=300, bbox_inches='tight')
        
        plt.tight_layout()
        plt.show()
        
        return fpr, tpr, roc_auc
    
    def curva_precisao_recall(self, y_true: np.ndarray, y_pred_proba: np.ndarray,
                             titulo: str = "Curva Precisão-Recall", salvar_fig: bool = False,
                             caminho_salvar: str = None) -> Tuple[np.ndarray, np.ndarray, float]:
        """
        Gera curva Precisão-Recall
        
        Args:
            y_true (np.ndarray): Valores verdadeiros
            y_pred_proba (np.ndarray): Probabilidades preditas
            titulo (str): Título do gráfico
            salvar_fig (bool): Se deve salvar a figura
            caminho_salvar (str): Caminho para salvar
            
        Returns:
            Tuple[np.ndarray, np.ndarray, float]: Precision, Recall, Average Precision
        """
        precision, recall, thresholds = precision_recall_curve(y_true, y_pred_proba)
        avg_precision = average_precision_score(y_true, y_pred_proba)
        
        plt.figure(figsize=(8, 6))
        plt.plot(recall, precision, color='blue', lw=2,
                label=f'Curva PR (AP = {avg_precision:.2f})')
        
        # Linha de referência (proporção de positivos)
        baseline = np.sum(y_true) / len(y_true)
        plt.axhline(y=baseline, color='red', linestyle='--', 
                   label=f'Baseline (AP = {baseline:.2f})')
        
        plt.xlim([0.0, 1.0])
        plt.ylim([0.0, 1.05])
        plt.xlabel('Recall (Sensibilidade)')
        plt.ylabel('Precisão')
        plt.title(titulo, fontweight='bold')
        plt.legend(loc="lower left")
        plt.grid(alpha=0.3)
        
        if salvar_fig and caminho_salvar:
            plt.savefig(f"{caminho_salvar}/curva_precisao_recall.png", dpi=300, bbox_inches='tight')
        
        plt.tight_layout()
        plt.show()
        
        return precision, recall, avg_precision
    
    def comparar_modelos(self, resultados_modelos: Dict[str, Dict], salvar_fig: bool = False,
                        caminho_salvar: str = None):
        """
        Compara múltiplos modelos visualmente
        
        Args:
            resultados_modelos (Dict): Resultados de avaliação dos modelos
            salvar_fig (bool): Se deve salvar a figura
            caminho_salvar (str): Caminho para salvar
        """
        # Preparar dados para comparação
        nomes_modelos = list(resultados_modelos.keys())
        metricas = ['accuracy', 'precision_weighted', 'recall_weighted', 'f1_weighted']
        
        dados_comparacao = []
        for modelo in nomes_modelos:
            if 'metricas' in resultados_modelos[modelo]:
                for metrica in metricas:
                    if metrica in resultados_modelos[modelo]['metricas']:
                        dados_comparacao.append({
                            'Modelo': modelo,
                            'Métrica': metrica.replace('_weighted', '').title(),
                            'Valor': resultados_modelos[modelo]['metricas'][metrica]
                        })
        
        df_comparacao = pd.DataFrame(dados_comparacao)
        
        # Gráfico de barras comparativo
        plt.figure(figsize=(12, 8))
        sns.barplot(data=df_comparacao, x='Métrica', y='Valor', hue='Modelo')
        plt.title('Comparação de Desempenho dos Modelos', fontsize=16, fontweight='bold')
        plt.ylabel('Score')
        plt.ylim(0, 1)
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.grid(axis='y', alpha=0.3)
        
        if salvar_fig and caminho_salvar:
            plt.savefig(f"{caminho_salvar}/comparacao_modelos.png", dpi=300, bbox_inches='tight')
        
        plt.tight_layout()
        plt.show()
    
    def curvas_aprendizado(self, modelo, X: pd.DataFrame, y: pd.Series, 
                          titulo: str = "Curvas de Aprendizado", cv: int = 5,
                          salvar_fig: bool = False, caminho_salvar: str = None):
        """
        Gera curvas de aprendizado para análise de bias/variance
        
        Args:
            modelo: Modelo treinado
            X (pd.DataFrame): Features
            y (pd.Series): Target
            titulo (str): Título do gráfico
            cv (int): Número de folds para cross-validation
            salvar_fig (bool): Se deve salvar a figura
            caminho_salvar (str): Caminho para salvar
        """
        train_sizes, train_scores, val_scores = learning_curve(
            modelo, X, y, cv=cv, n_jobs=-1, 
            train_sizes=np.linspace(0.1, 1.0, 10),
            scoring='accuracy'
        )
        
        # Calcular médias e desvios padrão
        train_mean = np.mean(train_scores, axis=1)
        train_std = np.std(train_scores, axis=1)
        val_mean = np.mean(val_scores, axis=1)
        val_std = np.std(val_scores, axis=1)
        
        plt.figure(figsize=(10, 6))
        
        # Plotar curvas
        plt.plot(train_sizes, train_mean, 'o-', color='blue', label='Score de Treino')
        plt.fill_between(train_sizes, train_mean - train_std, train_mean + train_std, 
                        alpha=0.1, color='blue')
        
        plt.plot(train_sizes, val_mean, 'o-', color='red', label='Score de Validação')
        plt.fill_between(train_sizes, val_mean - val_std, val_mean + val_std, 
                        alpha=0.1, color='red')
        
        plt.xlabel('Tamanho do Conjunto de Treino')
        plt.ylabel('Accuracy Score')
        plt.title(titulo, fontweight='bold')
        plt.legend(loc='best')
        plt.grid(alpha=0.3)
        
        if salvar_fig and caminho_salvar:
            plt.savefig(f"{caminho_salvar}/curvas_aprendizado.png", dpi=300, bbox_inches='tight')
        
        plt.tight_layout()
        plt.show()
    
    def relatorio_classificacao_detalhado(self, y_true: np.ndarray, y_pred: np.ndarray,
                                        nome_modelo: str = "Modelo") -> pd.DataFrame:
        """
        Gera relatório detalhado de classificação
        
        Args:
            y_true (np.ndarray): Valores verdadeiros
            y_pred (np.ndarray): Predições
            nome_modelo (str): Nome do modelo
            
        Returns:
            pd.DataFrame: Relatório detalhado
        """
        report = classification_report(y_true, y_pred, target_names=self.nomes_classes, 
                                     output_dict=True)
        
        # Converter para DataFrame para melhor visualização
        df_report = pd.DataFrame(report).transpose()
        
        print(f"\n{'='*50}")
        print(f"RELATÓRIO DETALHADO - {nome_modelo.upper()}")
        print(f"{'='*50}")
        print(df_report.round(3))
        
        return df_report
    
    def avaliar_modelo_completo(self, modelo, X_test: pd.DataFrame, y_test: pd.Series,
                               nome_modelo: str = "Modelo", salvar_figuras: bool = False,
                               caminho_salvar: str = None) -> Dict:
        """
        Avaliação completa de um modelo
        
        Args:
            modelo: Modelo treinado
            X_test (pd.DataFrame): Dados de teste
            y_test (pd.Series): Target de teste
            nome_modelo (str): Nome do modelo
            salvar_figuras (bool): Se deve salvar as figuras
            caminho_salvar (str): Caminho para salvar
            
        Returns:
            Dict: Resultados completos da avaliação
        """
        print(f"\n🔍 Avaliando modelo: {nome_modelo}")
        print("=" * 50)
        
        # Fazer predições
        y_pred = modelo.predict(X_test)
        y_pred_proba = None
        
        if hasattr(modelo, 'predict_proba'):
            y_pred_proba = modelo.predict_proba(X_test)[:, 1]
        
        # Calcular métricas básicas
        metricas = self.calcular_metricas_basicas(y_test, y_pred, y_pred_proba)
        
        # Exibir métricas principais
        print(f"📊 MÉTRICAS PRINCIPAIS:")
        print(f"  • Precisão: {metricas['accuracy']:.4f}")
        print(f"  • Precisão (Ponderada): {metricas['precision_weighted']:.4f}")
        print(f"  • Recall (Ponderado): {metricas['recall_weighted']:.4f}")
        print(f"  • F1-Score (Ponderado): {metricas['f1_weighted']:.4f}")
        
        if 'auc_roc' in metricas:
            print(f"  • AUC-ROC: {metricas['auc_roc']:.4f}")
        
        # Visualizações
        print(f"\n📈 Gerando visualizações...")
        
        # Matriz de confusão
        cm = self.matriz_confusao(y_test, y_pred, 
                                 f"Matriz de Confusão - {nome_modelo}",
                                 salvar_figuras, caminho_salvar)
        
        # Curvas ROC e Precisão-Recall (se probabilidades disponíveis)
        if y_pred_proba is not None:
            fpr, tpr, roc_auc = self.curva_roc(y_test, y_pred_proba,
                                              f"Curva ROC - {nome_modelo}",
                                              salvar_figuras, caminho_salvar)
            
            precision, recall, avg_precision = self.curva_precisao_recall(
                y_test, y_pred_proba, f"Curva Precisão-Recall - {nome_modelo}",
                salvar_figuras, caminho_salvar)
        
        # Relatório detalhado
        df_report = self.relatorio_classificacao_detalhado(y_test, y_pred, nome_modelo)
        
        # Compilar resultados
        resultado_completo = {
            'metricas': metricas,
            'matriz_confusao': cm.tolist(),
            'relatorio_classificacao': df_report.to_dict(),
            'predicoes': y_pred.tolist(),
            'probabilidades': y_pred_proba.tolist() if y_pred_proba is not None else None
        }
        
        print(f"\n✅ Avaliação de {nome_modelo} concluída!")
        
        return resultado_completo
    
    def gerar_relatorio_final(self, resultados_todos_modelos: Dict, 
                             salvar_arquivo: bool = False, caminho_salvar: str = None) -> pd.DataFrame:
        """
        Gera relatório final comparativo de todos os modelos
        
        Args:
            resultados_todos_modelos (Dict): Resultados de todos os modelos
            salvar_arquivo (bool): Se deve salvar o arquivo
            caminho_salvar (str): Caminho para salvar
            
        Returns:
            pd.DataFrame: Relatório final
        """
        print(f"\n📋 RELATÓRIO FINAL - COMPARAÇÃO DE MODELOS")
        print("=" * 80)
        
        relatorio_final = []
        
        for nome_modelo, resultado in resultados_todos_modelos.items():
            if 'metricas' in resultado:
                metricas = resultado['metricas']
                relatorio_final.append({
                    'Modelo': nome_modelo,
                    'Accuracy': f"{metricas['accuracy']:.4f}",
                    'Precision': f"{metricas['precision_weighted']:.4f}",
                    'Recall': f"{metricas['recall_weighted']:.4f}",
                    'F1-Score': f"{metricas['f1_weighted']:.4f}",
                    'AUC-ROC': f"{metricas.get('auc_roc', 0):.4f}" if metricas.get('auc_roc') else 'N/A'
                })
        
        df_relatorio = pd.DataFrame(relatorio_final)
        
        # Ordenar por F1-Score
        if len(df_relatorio) > 0:
            df_relatorio['F1_num'] = df_relatorio['F1-Score'].astype(float)
            df_relatorio = df_relatorio.sort_values('F1_num', ascending=False).drop('F1_num', axis=1)
            df_relatorio.index = range(1, len(df_relatorio) + 1)
        
        print(df_relatorio.to_string())
        
        if salvar_arquivo and caminho_salvar:
            df_relatorio.to_csv(f"{caminho_salvar}/relatorio_final_modelos.csv", index=True)
            print(f"\n💾 Relatório salvo em: {caminho_salvar}/relatorio_final_modelos.csv")
        
        return df_relatorio

def main():
    """Função para testar o módulo"""
    print("Módulo de Avaliação de Modelos - Teste")
    
    # Dados sintéticos para teste
    np.random.seed(42)
    y_true = np.random.randint(0, 2, 100)
    y_pred = np.random.randint(0, 2, 100)
    y_pred_proba = np.random.random(100)
    
    avaliador = AvaliadorModelos()
    
    # Teste das métricas básicas
    metricas = avaliador.calcular_metricas_basicas(y_true, y_pred, y_pred_proba)
    print("Métricas calculadas:", metricas)
    
    # Teste da matriz de confusão
    cm = avaliador.matriz_confusao(y_true, y_pred, "Teste")
    print("Matriz de confusão:", cm)

if __name__ == "__main__":
    main()