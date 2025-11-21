"""
Módulo para Pré-processamento de Dados
Autor: Sistema de Diagnóstico de Doenças
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, StandardScaler, OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from typing import Tuple, Dict, List, Optional
import joblib
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PreProcessadorDados:
    """Classe para pré-processamento completo dos dados"""
    
    def __init__(self, dados: pd.DataFrame):
        """
        Inicializa o pré-processador
        
        Args:
            dados (pd.DataFrame): DataFrame com os dados originais
        """
        self.dados_originais = dados.copy()
        self.dados_processados = None
        self.encoders = {}
        self.scaler = None
        # Ajuste para nomes em português
        self.colunas_sintomas = ['Febre', 'Tosse', 'Fadiga', 'Dificuldade para respirar']
        self.colunas_categoricas = ['Gênero', 'Pressão Arterial', 'Nível de Colesterol']
        self.target_column = 'Resultado'
        
    def limpar_dados(self) -> pd.DataFrame:
        """
        Limpa os dados removendo duplicatas e tratando valores inconsistentes
        
        Returns:
            pd.DataFrame: Dados limpos
        """
        logger.info("Iniciando limpeza dos dados...")
        
        dados_limpos = self.dados_originais.copy()
        
        # Remover duplicatas
        linhas_antes = len(dados_limpos)
        dados_limpos = dados_limpos.drop_duplicates()
        linhas_removidas = linhas_antes - len(dados_limpos)
        
        if linhas_removidas > 0:
            logger.info(f"Removidas {linhas_removidas} linhas duplicadas")
        
        # Tratar valores inconsistentes na idade
        if 'Idade' in dados_limpos.columns:
            # Remover idades inválidas (menores que 0 ou maiores que 120)
            dados_limpos = dados_limpos[(dados_limpos['Idade'] >= 0) & (dados_limpos['Idade'] <= 120)]
        
        # Padronizar valores categóricos
        for coluna in self.colunas_sintomas:
            if coluna in dados_limpos.columns:
                dados_limpos[coluna] = dados_limpos[coluna].str.strip().str.title()
        
        # Padronizar valores do alvo
        if self.target_column in dados_limpos.columns:
            dados_limpos[self.target_column] = dados_limpos[self.target_column].str.strip().str.title()
        
        logger.info(f"Dados limpos. Dimensões finais: {dados_limpos.shape}")
        return dados_limpos
    
    def tratar_valores_ausentes(self, dados: pd.DataFrame) -> pd.DataFrame:
        """
        Trata valores ausentes no conjunto de dados
        
        Args:
            dados (pd.DataFrame): Dados para tratar
            
        Returns:
            pd.DataFrame: Dados com valores ausentes tratados
        """
        logger.info("Tratando valores ausentes...")
        
        dados_tratados = dados.copy()
        
        # Para colunas numéricas - usar mediana
        colunas_numericas = dados_tratados.select_dtypes(include=[np.number]).columns
        for coluna in colunas_numericas:
            if dados_tratados[coluna].isnull().sum() > 0:
                mediana = dados_tratados[coluna].median()
                dados_tratados[coluna].fillna(mediana, inplace=True)
                logger.info(f"Preenchidos {dados_tratados[coluna].isnull().sum()} valores ausentes em {coluna} com mediana: {mediana}")
        
        # Para colunas categóricas - usar moda
        colunas_categoricas = dados_tratados.select_dtypes(include=['object']).columns
        for coluna in colunas_categoricas:
            if dados_tratados[coluna].isnull().sum() > 0:
                moda = dados_tratados[coluna].mode()[0] if len(dados_tratados[coluna].mode()) > 0 else 'Desconhecido'
                dados_tratados[coluna].fillna(moda, inplace=True)
                logger.info(f"Preenchidos valores ausentes em {coluna} com moda: {moda}")
        
        return dados_tratados
    
    def codificar_variaveis_categoricas(self, dados: pd.DataFrame) -> pd.DataFrame:
        """
        Codifica variáveis categóricas
        
        Args:
            dados (pd.DataFrame): Dados para codificar
            
        Returns:
            pd.DataFrame: Dados com variáveis codificadas
        """
        logger.info("Codificando variáveis categóricas...")
        
        dados_codificados = dados.copy()
        
        # Codificar sintomas (Sim/Não -> 1/0)
        for coluna in self.colunas_sintomas:
            if coluna in dados_codificados.columns:
                if coluna not in self.encoders:
                    self.encoders[coluna] = LabelEncoder()
                dados_codificados[coluna] = self.encoders[coluna].fit_transform(dados_codificados[coluna])
                logger.info(f"Codificada coluna {coluna}: {dict(zip(self.encoders[coluna].classes_, self.encoders[coluna].transform(self.encoders[coluna].classes_)))}")
        
        # Codificar outras variáveis categóricas (em português)
        for coluna in self.colunas_categoricas:
            if coluna in dados_codificados.columns:
                if coluna not in self.encoders:
                    self.encoders[coluna] = LabelEncoder()
                dados_codificados[coluna] = self.encoders[coluna].fit_transform(dados_codificados[coluna])
                logger.info(f"Codificada coluna {coluna}: {dict(zip(self.encoders[coluna].classes_, self.encoders[coluna].transform(self.encoders[coluna].classes_)))}")
        
        # Codificar alvo
        if self.target_column in dados_codificados.columns:
            if self.target_column not in self.encoders:
                self.encoders[self.target_column] = LabelEncoder()
            dados_codificados[self.target_column] = self.encoders[self.target_column].fit_transform(dados_codificados[self.target_column])
            logger.info(f"Codificada variável alvo {self.target_column}: {dict(zip(self.encoders[self.target_column].classes_, self.encoders[self.target_column].transform(self.encoders[self.target_column].classes_)))}")
        
        return dados_codificados
    
    def normalizar_dados(self, dados: pd.DataFrame, colunas_para_normalizar: List[str] = None) -> pd.DataFrame:
        """
        Normaliza dados numéricos
        
        Args:
            dados (pd.DataFrame): Dados para normalizar
            colunas_para_normalizar (List[str]): Colunas específicas para normalizar
            
        Returns:
            pd.DataFrame: Dados normalizados
        """
        logger.info("Normalizando dados...")
        
        dados_normalizados = dados.copy()
        
        if colunas_para_normalizar is None:
            # Normalizar apenas a coluna Idade (as outras já são binárias)
            colunas_para_normalizar = ['Idade'] if 'Idade' in dados_normalizados.columns else []
        
        if len(colunas_para_normalizar) > 0:
            if self.scaler is None:
                self.scaler = StandardScaler()
            
            dados_normalizados[colunas_para_normalizar] = self.scaler.fit_transform(dados_normalizados[colunas_para_normalizar])
            logger.info(f"Normalizadas colunas: {colunas_para_normalizar}")
        
        return dados_normalizados
    
    def preparar_features_target(self, dados: pd.DataFrame) -> Tuple[pd.DataFrame, pd.Series]:
        """
        Separa características e alvo
        
        Args:
            dados (pd.DataFrame): Conjunto de dados completo
            
        Returns:
            Tuple[pd.DataFrame, pd.Series]: Características e alvo
        """
        # Remover colunas que não são características
        colunas_para_remover = ['Doença']  # Doença não deve ser uma característica
        features = dados.drop(columns=[col for col in colunas_para_remover if col in dados.columns])
        if self.target_column in features.columns:
            target = features[self.target_column].copy()
            features = features.drop(columns=[self.target_column])
        else:
            raise ValueError(f"Coluna alvo '{self.target_column}' não encontrada")
        logger.info(f"Características preparadas: {list(features.columns)}")
        logger.info(f"Dimensões das características: {features.shape}")
        logger.info(f"Dimensões do alvo: {target.shape}")
        return features, target
    
    def dividir_dados(self, X: pd.DataFrame, y: pd.Series, 
                     test_size: float = 0.2, random_state: int = 42) -> Tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
        """
        Divide os dados em treino e teste
        
        Args:
            X (pd.DataFrame): Features
            y (pd.Series): Target
            test_size (float): Proporção do conjunto de teste
            random_state (int): Semente para reprodutibilidade
            
        Returns:
            Tuple: X_train, X_test, y_train, y_test
        """
        logger.info(f"Dividindo dados: {100-test_size*100:.0f}% treino, {test_size*100:.0f}% teste")
        
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state, stratify=y
        )
        
        logger.info(f"Treino: {X_train.shape[0]} amostras")
        logger.info(f"Teste: {X_test.shape[0]} amostras")
        
        return X_train, X_test, y_train, y_test
    
    def processar_dados_completo(self, test_size: float = 0.2, random_state: int = 42) -> Dict:
        """
        Executa todo o pipeline de pré-processamento
        
        Args:
            test_size (float): Proporção do conjunto de teste
            random_state (int): Semente para reprodutibilidade
            
        Returns:
            Dict: Dicionário com dados processados e informações
        """
        logger.info("🔧 Iniciando pré-processamento completo...")
        
        # 1. Limpeza
        dados_limpos = self.limpar_dados()
        
        # 2. Tratar valores ausentes
        dados_sem_na = self.tratar_valores_ausentes(dados_limpos)
        
        # 3. Codificar variáveis categóricas
        dados_codificados = self.codificar_variaveis_categoricas(dados_sem_na)
        
        # 4. Normalizar dados
        dados_normalizados = self.normalizar_dados(dados_codificados)
        
        # 5. Preparar features e target
        X, y = self.preparar_features_target(dados_normalizados)
        
        # 6. Dividir dados
        X_train, X_test, y_train, y_test = self.dividir_dados(X, y, test_size, random_state)
        
        # Salvar dados processados
        self.dados_processados = dados_normalizados
        
        resultado = {
            'X_train': X_train,
            'X_test': X_test,
            'y_train': y_train,
            'y_test': y_test,
            'feature_names': list(X.columns),
            'encoders': self.encoders,
            'scaler': self.scaler,
            'dados_processados': dados_normalizados,
            'info_preprocessamento': {
                'shape_original': self.dados_originais.shape,
                'shape_final': dados_normalizados.shape,
                'features_utilizadas': list(X.columns),
                'classes_target': dict(zip(self.encoders[self.target_column].classes_, 
                                         self.encoders[self.target_column].transform(self.encoders[self.target_column].classes_))) if self.target_column in self.encoders else {}
            }
        }
        
        logger.info("✅ Pré-processamento concluído com sucesso!")
        return resultado
    
    def salvar_preprocessadores(self, caminho: str):
        """
        Salva os objetos de pré-processamento
        
        Args:
            caminho (str): Caminho para salvar os objetos
        """
        os.makedirs(caminho, exist_ok=True)
        
        # Salvar encoders
        joblib.dump(self.encoders, os.path.join(caminho, 'encoders.pkl'))
        
        # Salvar scaler
        if self.scaler is not None:
            joblib.dump(self.scaler, os.path.join(caminho, 'scaler.pkl'))
        
        logger.info(f"Objetos de pré-processamento salvos em: {caminho}")
    
    def carregar_preprocessadores(self, caminho: str):
        """
        Carrega os objetos de pré-processamento
        
        Args:
            caminho (str): Caminho dos objetos salvos
        """
        try:
            self.encoders = joblib.load(os.path.join(caminho, 'encoders.pkl'))
            
            scaler_path = os.path.join(caminho, 'scaler.pkl')
            if os.path.exists(scaler_path):
                self.scaler = joblib.load(scaler_path)
            
            logger.info(f"Objetos de pré-processamento carregados de: {caminho}")
        except Exception as e:
            logger.error(f"Erro ao carregar objetos: {e}")
            raise
    
    def preprocessar_novos_dados(self, novos_dados: pd.DataFrame) -> pd.DataFrame:
        """
        Aplica o mesmo pré-processamento a novos dados
        
        Args:
            novos_dados (pd.DataFrame): Novos dados para processar
            
        Returns:
            pd.DataFrame: Dados processados
        """
        if not self.encoders:
            raise ValueError("Encoders não foram treinados. Execute processar_dados_completo() primeiro.")
        
        dados_processados = novos_dados.copy()
        
        # Aplicar encoders
        for coluna, encoder in self.encoders.items():
            if coluna in dados_processados.columns and coluna != self.target_column:
                # Tratar valores não vistos durante o treinamento
                valores_conhecidos = encoder.classes_
                mask_conhecidos = dados_processados[coluna].isin(valores_conhecidos)
                
                if not mask_conhecidos.all():
                    logger.warning(f"Valores desconhecidos encontrados em {coluna}. Usando valor mais comum.")
                    valor_mais_comum = valores_conhecidos[0]  # Primeira classe
                    dados_processados.loc[~mask_conhecidos, coluna] = valor_mais_comum
                
                dados_processados[coluna] = encoder.transform(dados_processados[coluna])
        
        # Aplicar normalização
        if self.scaler is not None and 'Idade' in dados_processados.columns:
            dados_processados[['Idade']] = self.scaler.transform(dados_processados[['Idade']])
        
        return dados_processados

def main():
    """Função para testar o módulo"""
    try:
        from carregador_dados import CarregadorDados
        
        caminho = "/home/felizado-manuel/Documentos/Faculdade/Terceiro/II Semestre/INAR/Projecto final 01/dataset/Disease_symptom_and_patient_profile_dataset.csv"
        
        # Carregar dados
        carregador = CarregadorDados(caminho)
        dados = carregador.carregar_dados()
        
        # Processar dados
        preprocessador = PreProcessadorDados(dados)
        resultado = preprocessador.processar_dados_completo()
        
        print("✅ Pré-processamento concluído!")
        print(f"Características: {resultado['feature_names']}")
        print(f"Dimensões treino: {resultado['X_train'].shape}")
        print(f"Dimensões teste: {resultado['X_test'].shape}")
        
    except ImportError:
        print("Execute este módulo a partir do arquivo principal")
    except Exception as e:
        print(f"Erro: {e}")

if __name__ == "__main__":
    main()