"""
Módulo para carregamento e validação de dados
Autor: Sistema de Diagnóstico de Doenças
"""

import pandas as pd
import numpy as np
import os
from typing import Tuple, Optional
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CarregadorDados:
    """Classe responsável pelo carregamento e validação inicial dos dados"""
    
    def __init__(self, caminho_dataset: str):
        """
        Inicializa o carregador de dados
        
        Args:
            caminho_dataset (str): Caminho para o arquivo CSV
        """
        self.caminho_dataset = caminho_dataset
        self.dados = None
        self.colunas_esperadas = [
            'Disease', 'Fever', 'Cough', 'Fatigue', 'Difficulty Breathing',
            'Age', 'Gender', 'Blood Pressure', 'Cholesterol Level', 'Outcome Variable'
        ]
        
    def carregar_dados(self) -> pd.DataFrame:
        """
        Carrega os dados do arquivo CSV
        
        Returns:
            pd.DataFrame: DataFrame com os dados carregados
            
        Raises:
            FileNotFoundError: Se o arquivo não existir
            ValueError: Se o arquivo estiver vazio ou corrompido
        """
        try:
            # Verificar se o arquivo existe
            if not os.path.exists(self.caminho_dataset):
                raise FileNotFoundError(f"Arquivo não encontrado: {self.caminho_dataset}")
            
            # Carregar dados
            logger.info(f"Carregando dados de: {self.caminho_dataset}")
            self.dados = pd.read_csv(self.caminho_dataset)
            
            # Verificar se o dataset não está vazio
            if self.dados.empty:
                raise ValueError("O dataset está vazio")
            
            logger.info(f"Dados carregados com sucesso. Dimensões: {self.dados.shape}")
            return self.dados
            
        except Exception as e:
            logger.error(f"Erro ao carregar dados: {str(e)}")
            raise
    
    def validar_estrutura(self) -> bool:
        """
        Valida se o dataset possui a estrutura esperada
        
        Returns:
            bool: True se a estrutura estiver correta
        """
        if self.dados is None:
            logger.error("Dados não foram carregados")
            return False
        
        # Verificar colunas
        colunas_faltantes = set(self.colunas_esperadas) - set(self.dados.columns)
        if colunas_faltantes:
            logger.error(f"Colunas faltantes: {colunas_faltantes}")
            return False
        
        logger.info("Estrutura do dataset validada com sucesso")
        return True
    
    def obter_informacoes_basicas(self) -> dict:
        """
        Retorna informações básicas sobre o dataset
        
        Returns:
            dict: Dicionário com informações básicas
        """
        if self.dados is None:
            return {}
        
        info = {
            'numero_linhas': self.dados.shape[0],
            'numero_colunas': self.dados.shape[1],
            'colunas': list(self.dados.columns),
            'tipos_dados': self.dados.dtypes.to_dict(),
            'valores_nulos': self.dados.isnull().sum().to_dict(),
            'doencas_unicas': self.dados['Disease'].nunique() if 'Disease' in self.dados.columns else 0,
            'memoria_uso': self.dados.memory_usage(deep=True).sum() / 1024**2  # MB
        }
        
        return info
    
    def obter_amostra_dados(self, n: int = 5) -> pd.DataFrame:
        """
        Retorna uma amostra dos dados
        
        Args:
            n (int): Número de linhas para mostrar
            
        Returns:
            pd.DataFrame: Amostra dos dados
        """
        if self.dados is None:
            return pd.DataFrame()
        
        return self.dados.head(n)
    
    def verificar_qualidade_dados(self) -> dict:
        """
        Verifica a qualidade dos dados
        
        Returns:
            dict: Relatório de qualidade dos dados
        """
        if self.dados is None:
            return {}
        
        relatorio = {
            'valores_nulos_total': self.dados.isnull().sum().sum(),
            'porcentagem_valores_nulos': (self.dados.isnull().sum().sum() / (self.dados.shape[0] * self.dados.shape[1])) * 100,
            'linhas_duplicadas': self.dados.duplicated().sum(),
            'distribuicao_classes': self.dados['Outcome Variable'].value_counts().to_dict() if 'Outcome Variable' in self.dados.columns else {},
            'dados_inconsistentes': {}
        }
        
        # Verificar inconsistências específicas
        if 'Age' in self.dados.columns:
            relatorio['dados_inconsistentes']['idade_invalida'] = (self.dados['Age'] < 0).sum() + (self.dados['Age'] > 120).sum()
        
        return relatorio

def main():
    """Função principal para testar o módulo"""
    # Exemplo de uso
    caminho = "/home/felizado-manuel/Documentos/Faculdade/Terceiro/II Semestre/INAR/Projecto final 01/dataset/Disease_symptom_and_patient_profile_dataset.csv"
    
    carregador = CarregadorDados(caminho)
    
    try:
        # Carregar dados
        dados = carregador.carregar_dados()
        
        # Validar estrutura
        if carregador.validar_estrutura():
            print("✓ Estrutura do dataset validada")
        
        # Mostrar informações básicas
        info = carregador.obter_informacoes_basicas()
        print(f"\nInformações básicas:")
        print(f"- Linhas: {info['numero_linhas']}")
        print(f"- Colunas: {info['numero_colunas']}")
        print(f"- Doenças únicas: {info['doencas_unicas']}")
        print(f"- Uso de memória: {info['memoria_uso']:.2f} MB")
        
        # Verificar qualidade
        qualidade = carregador.verificar_qualidade_dados()
        print(f"\nQualidade dos dados:")
        print(f"- Valores nulos: {qualidade['valores_nulos_total']}")
        print(f"- Linhas duplicadas: {qualidade['linhas_duplicadas']}")
        
    except Exception as e:
        print(f"Erro: {e}")

if __name__ == "__main__":
    main()