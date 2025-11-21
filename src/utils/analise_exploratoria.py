"""
Módulo para Análise Exploratória de Dados (EDA)
Autor: Sistema de Diagnóstico de Doenças
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from typing import Dict, List, Tuple, Optional
import warnings
warnings.filterwarnings('ignore')

# Configurar estilo dos gráficos
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

class AnalisadorExploratorio:
    """Classe para realizar análise exploratória completa dos dados"""
    
    def __init__(self, dados: pd.DataFrame):
        """
        Inicializa o analisador
        
        Args:
            dados (pd.DataFrame): DataFrame com os dados para análise
        """
        self.dados = dados.copy()
        self.colunas_sintomas = ['Fever', 'Cough', 'Fatigue', 'Difficulty Breathing']
        self.colunas_demograficas = ['Age', 'Gender']
        self.colunas_clinicas = ['Blood Pressure', 'Cholesterol Level']
        
    def estatisticas_descritivas(self) -> Dict:
        """
        Gera estatísticas descritivas completas
        
        Returns:
            Dict: Dicionário com estatísticas descritivas
        """
        stats = {}
        
        # Estatísticas gerais
        stats['geral'] = {
            'total_registros': len(self.dados),
            'total_colunas': len(self.dados.columns),
            'memoria_mb': self.dados.memory_usage(deep=True).sum() / 1024**2
        }
        
        # Estatísticas da variável alvo
        if 'Outcome Variable' in self.dados.columns:
            stats['outcome'] = self.dados['Outcome Variable'].value_counts().to_dict()
            stats['outcome_percentual'] = (self.dados['Outcome Variable'].value_counts(normalize=True) * 100).to_dict()
        
        # Estatísticas de doenças
        if 'Disease' in self.dados.columns:
            stats['doencas'] = {
                'total_unicas': self.dados['Disease'].nunique(),
                'mais_comuns': self.dados['Disease'].value_counts().head(10).to_dict(),
                'distribuicao': self.dados['Disease'].value_counts().to_dict()
            }
        
        # Estatísticas demográficas
        if 'Age' in self.dados.columns:
            stats['idade'] = {
                'media': self.dados['Age'].mean(),
                'mediana': self.dados['Age'].median(),
                'desvio_padrao': self.dados['Age'].std(),
                'min': self.dados['Age'].min(),
                'max': self.dados['Age'].max(),
                'quartis': self.dados['Age'].quantile([0.25, 0.5, 0.75]).to_dict()
            }
        
        if 'Gender' in self.dados.columns:
            stats['genero'] = self.dados['Gender'].value_counts().to_dict()
        
        # Estatísticas de sintomas
        stats['sintomas'] = {}
        for sintoma in self.colunas_sintomas:
            if sintoma in self.dados.columns:
                stats['sintomas'][sintoma] = self.dados[sintoma].value_counts().to_dict()
        
        return stats
    
    def visualizar_distribuicao_classes(self, salvar_fig: bool = False, caminho_salvar: str = None):
        """
        Visualiza a distribuição das classes (Outcome Variable)
        """
        if 'Outcome Variable' not in self.dados.columns:
            print("Coluna 'Outcome Variable' não encontrada")
            return
        
        fig, axes = plt.subplots(1, 2, figsize=(15, 6))
        
        # Gráfico de barras
        contagem = self.dados['Outcome Variable'].value_counts()
        axes[0].bar(contagem.index, contagem.values, color=['#FF6B6B', '#4ECDC4'])
        axes[0].set_title('Distribuição das Classes (Contagem)', fontsize=14, fontweight='bold')
        axes[0].set_xlabel('Resultado')
        axes[0].set_ylabel('Quantidade')
        
        # Adicionar valores nas barras
        for i, v in enumerate(contagem.values):
            axes[0].text(i, v + 1, str(v), ha='center', va='bottom', fontweight='bold')
        
        # Gráfico de pizza
        percentual = self.dados['Outcome Variable'].value_counts(normalize=True) * 100
        cores = ['#FF6B6B', '#4ECDC4']
        wedges, texts, autotexts = axes[1].pie(percentual.values, labels=percentual.index, 
                                               autopct='%1.1f%%', colors=cores, startangle=90)
        axes[1].set_title('Distribuição das Classes (Percentual)', fontsize=14, fontweight='bold')
        
        plt.tight_layout()
        
        if salvar_fig and caminho_salvar:
            plt.savefig(f"{caminho_salvar}/distribuicao_classes.png", dpi=300, bbox_inches='tight')
        
        plt.show()
    
    def visualizar_distribuicao_doencas(self, top_n: int = 15, salvar_fig: bool = False, caminho_salvar: str = None):
        """
        Visualiza a distribuição das doenças mais comuns
        """
        if 'Disease' not in self.dados.columns:
            print("Coluna 'Disease' não encontrada")
            return
        
        # Top N doenças mais comuns
        top_doencas = self.dados['Disease'].value_counts().head(top_n)
        
        plt.figure(figsize=(12, 8))
        bars = plt.barh(range(len(top_doencas)), top_doencas.values, color=plt.cm.viridis(np.linspace(0, 1, len(top_doencas))))
        plt.yticks(range(len(top_doencas)), top_doencas.index)
        plt.xlabel('Quantidade de Casos')
        plt.title(f'Top {top_n} Doenças Mais Comuns no Dataset', fontsize=16, fontweight='bold')
        plt.grid(axis='x', alpha=0.3)
        
        # Adicionar valores nas barras
        for i, v in enumerate(top_doencas.values):
            plt.text(v + 0.5, i, str(v), va='center', fontweight='bold')
        
        plt.tight_layout()
        
        if salvar_fig and caminho_salvar:
            plt.savefig(f"{caminho_salvar}/distribuicao_doencas.png", dpi=300, bbox_inches='tight')
        
        plt.show()
    
    def visualizar_sintomas(self, salvar_fig: bool = False, caminho_salvar: str = None):
        """
        Visualiza a distribuição dos sintomas
        """
        sintomas_presentes = [col for col in self.colunas_sintomas if col in self.dados.columns]
        
        if not sintomas_presentes:
            print("Nenhuma coluna de sintoma encontrada")
            return
        
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        axes = axes.ravel()
        
        for i, sintoma in enumerate(sintomas_presentes):
            if i < len(axes):
                contagem = self.dados[sintoma].value_counts()
                cores = ['#FF6B6B' if val == 'Yes' else '#95A5A6' for val in contagem.index]
                
                bars = axes[i].bar(contagem.index, contagem.values, color=cores)
                axes[i].set_title(f'Distribuição: {sintoma}', fontsize=12, fontweight='bold')
                axes[i].set_ylabel('Quantidade')
                
                # Adicionar valores nas barras
                for bar, val in zip(bars, contagem.values):
                    axes[i].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1, 
                               str(val), ha='center', va='bottom', fontweight='bold')
        
        # Remover eixos vazios
        for j in range(len(sintomas_presentes), len(axes)):
            fig.delaxes(axes[j])
        
        plt.tight_layout()
        
        if salvar_fig and caminho_salvar:
            plt.savefig(f"{caminho_salvar}/distribuicao_sintomas.png", dpi=300, bbox_inches='tight')
        
        plt.show()
    
    def visualizar_correlacao_sintomas(self, salvar_fig: bool = False, caminho_salvar: str = None):
        """
        Visualiza a correlação entre sintomas
        """
        # Criar dados numéricos para correlação
        dados_numericos = self.dados.copy()
        
        # Converter sintomas para numérico
        for col in self.colunas_sintomas:
            if col in dados_numericos.columns:
                dados_numericos[col] = dados_numericos[col].map({'Yes': 1, 'No': 0})
        
        # Converter outcome para numérico
        if 'Outcome Variable' in dados_numericos.columns:
            dados_numericos['Outcome Variable'] = dados_numericos['Outcome Variable'].map({'Positive': 1, 'Negative': 0})
        
        # Selecionar apenas colunas numéricas para correlação
        colunas_para_correlacao = self.colunas_sintomas + ['Outcome Variable', 'Age']
        colunas_para_correlacao = [col for col in colunas_para_correlacao if col in dados_numericos.columns]
        
        correlacao = dados_numericos[colunas_para_correlacao].corr()
        
        plt.figure(figsize=(12, 10))
        mask = np.triu(np.ones_like(correlacao, dtype=bool))
        sns.heatmap(correlacao, mask=mask, annot=True, cmap='RdYlBu_r', center=0,
                   square=True, linewidths=0.5, cbar_kws={"shrink": .8})
        plt.title('Matriz de Correlação entre Sintomas e Outcome', fontsize=16, fontweight='bold')
        plt.tight_layout()
        
        if salvar_fig and caminho_salvar:
            plt.savefig(f"{caminho_salvar}/correlacao_sintomas.png", dpi=300, bbox_inches='tight')
        
        plt.show()
    
    def analise_demografica(self, salvar_fig: bool = False, caminho_salvar: str = None):
        """
        Análise demográfica dos dados
        """
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        
        # Distribuição por idade
        if 'Age' in self.dados.columns:
            axes[0, 0].hist(self.dados['Age'], bins=20, color='skyblue', alpha=0.7, edgecolor='black')
            axes[0, 0].set_title('Distribuição por Idade', fontweight='bold')
            axes[0, 0].set_xlabel('Idade')
            axes[0, 0].set_ylabel('Frequência')
            axes[0, 0].grid(alpha=0.3)
        
        # Distribuição por gênero
        if 'Gender' in self.dados.columns:
            contagem_genero = self.dados['Gender'].value_counts()
            cores = ['#FF6B6B', '#4ECDC4']
            bars = axes[0, 1].bar(contagem_genero.index, contagem_genero.values, color=cores)
            axes[0, 1].set_title('Distribuição por Gênero', fontweight='bold')
            axes[0, 1].set_ylabel('Quantidade')
            
            for bar, val in zip(bars, contagem_genero.values):
                axes[0, 1].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1, 
                               str(val), ha='center', va='bottom', fontweight='bold')
        
        # Boxplot idade por outcome
        if 'Age' in self.dados.columns and 'Outcome Variable' in self.dados.columns:
            sns.boxplot(data=self.dados, x='Outcome Variable', y='Age', ax=axes[1, 0])
            axes[1, 0].set_title('Distribuição de Idade por Outcome', fontweight='bold')
        
        # Distribuição de gênero por outcome
        if 'Gender' in self.dados.columns and 'Outcome Variable' in self.dados.columns:
            crosstab = pd.crosstab(self.dados['Gender'], self.dados['Outcome Variable'])
            crosstab.plot(kind='bar', ax=axes[1, 1], color=['#FF6B6B', '#4ECDC4'])
            axes[1, 1].set_title('Distribuição de Gênero por Outcome', fontweight='bold')
            axes[1, 1].set_xlabel('Gênero')
            axes[1, 1].set_ylabel('Quantidade')
            axes[1, 1].legend(title='Outcome')
            axes[1, 1].tick_params(axis='x', rotation=0)
        
        plt.tight_layout()
        
        if salvar_fig and caminho_salvar:
            plt.savefig(f"{caminho_salvar}/analise_demografica.png", dpi=300, bbox_inches='tight')
        
        plt.show()
    
    def gerar_relatorio_completo(self) -> Dict:
        """
        Gera um relatório completo da análise exploratória
        
        Returns:
            Dict: Relatório completo
        """
        relatorio = {}
        
        # Estatísticas básicas
        relatorio['estatisticas'] = self.estatisticas_descritivas()
        
        # Análise de qualidade
        relatorio['qualidade'] = {
            'valores_nulos': self.dados.isnull().sum().to_dict(),
            'duplicatas': self.dados.duplicated().sum(),
            'tipos_dados': self.dados.dtypes.to_dict()
        }
        
        # Insights principais
        insights = []
        
        if 'Outcome Variable' in self.dados.columns:
            outcome_dist = self.dados['Outcome Variable'].value_counts(normalize=True)
            insights.append(f"Distribuição de classes: {outcome_dist.to_dict()}")
        
        if 'Disease' in self.dados.columns:
            doenca_mais_comum = self.dados['Disease'].value_counts().index[0]
            insights.append(f"Doença mais comum: {doenca_mais_comum}")
        
        if 'Age' in self.dados.columns:
            idade_media = self.dados['Age'].mean()
            insights.append(f"Idade média dos pacientes: {idade_media:.1f} anos")
        
        relatorio['insights'] = insights
        
        return relatorio
    
    def executar_eda_completa(self, salvar_figuras: bool = False, caminho_salvar: str = None):
        """
        Executa toda a análise exploratória
        """
        print("🔍 Iniciando Análise Exploratória de Dados...")
        print("=" * 50)
        
        # Estatísticas descritivas
        stats = self.estatisticas_descritivas()
        print(f"📊 Total de registros: {stats['geral']['total_registros']}")
        print(f"📊 Total de colunas: {stats['geral']['total_colunas']}")
        
        if 'doencas' in stats:
            print(f"🦠 Doenças únicas: {stats['doencas']['total_unicas']}")
        
        print("\n" + "=" * 50)
        
        # Gerar visualizações
        print("📈 Gerando visualizações...")
        
        self.visualizar_distribuicao_classes(salvar_figuras, caminho_salvar)
        self.visualizar_distribuicao_doencas(salvar_fig=salvar_figuras, caminho_salvar=caminho_salvar)
        self.visualizar_sintomas(salvar_figuras, caminho_salvar)
        self.visualizar_correlacao_sintomas(salvar_figuras, caminho_salvar)
        self.analise_demografica(salvar_figuras, caminho_salvar)
        
        # Relatório final
        relatorio = self.gerar_relatorio_completo()
        
        print("\n" + "=" * 50)
        print("📋 INSIGHTS PRINCIPAIS:")
        for insight in relatorio['insights']:
            print(f"• {insight}")
        
        print("\n✅ Análise Exploratória Concluída!")
        
        return relatorio

def main():
    """Função para testar o módulo"""
    # Exemplo de uso (substituir pelo caminho real)
    try:
        from carregador_dados import CarregadorDados
        
        caminho = "/home/felizado-manuel/Documentos/Faculdade/Terceiro/II Semestre/INAR/Projecto final 01/dataset/Disease_symptom_and_patient_profile_dataset.csv"
        
        # Carregar dados
        carregador = CarregadorDados(caminho)
        dados = carregador.carregar_dados()
        
        # Executar EDA
        analisador = AnalisadorExploratorio(dados)
        relatorio = analisador.executar_eda_completa()
        
    except ImportError:
        print("Execute este módulo a partir do arquivo principal")
    except Exception as e:
        print(f"Erro: {e}")

if __name__ == "__main__":
    main()