"""
Carregador de Dados Atualizado para os Novos Datasets
Utiliza os 3 arquivos CSV: Symptom-severity.csv, symptom_Description.csv, symptom_precaution.csv
"""

import pandas as pd
import os
import logging
from typing import Dict, List, Tuple, Any, Optional
import sys
from pathlib import Path

# Adicionar o caminho raiz do projeto
projeto_root = Path(__file__).parent.parent.parent
sys.path.append(str(projeto_root))

try:
    from src.utils.descricoes_doencas_portugues import traduzir_descricao_se_necessario
except ImportError:
    try:
        from descricoes_doencas_portugues import traduzir_descricao_se_necessario
    except ImportError:
        # Função de fallback se não conseguir importar
        def traduzir_descricao_se_necessario(descricao):
            return descricao

logger = logging.getLogger(__name__)

class CarregadorDadosAtualizado:
    """
    Carregador para os novos datasets especializados
    """
    
    def __init__(self, base_path: str = None):
        """
        Inicializa o carregador de dados
        
        Args:
            base_path: Caminho base para os arquivos de dataset
        """
        if base_path is None:
            # Define caminho padrão baseado na estrutura do projeto
            current_dir = os.path.dirname(__file__)
            self.base_path = os.path.join(current_dir, '..', '..', 'dataset')
        else:
            self.base_path = base_path
            
        self.sintomas_severidade = None
        self.descricoes_doencas = None
        self.precaucoes_doencas = None
        
        logger.info(f"Carregador inicializado com caminho: {self.base_path}")
    
    def carregar_sintomas_severidade(self) -> pd.DataFrame:
        """
        Carrega o arquivo Symptom-severity.csv
        
        Returns:
            DataFrame com sintomas e seus pesos de severidade
        """
        try:
            caminho = os.path.join(self.base_path, 'Symptom-severity.csv')
            
            if not os.path.exists(caminho):
                raise FileNotFoundError(f"Arquivo não encontrado: {caminho}")
                
            df = pd.read_csv(caminho)
            
            # Validações básicas
            if 'Symptom' not in df.columns or 'weight' not in df.columns:
                raise ValueError("Arquivo deve conter colunas 'Symptom' e 'weight'")
                
            # Remove linhas com valores nulos
            df = df.dropna()
            
            # Converte pesos para numérico
            df['weight'] = pd.to_numeric(df['weight'], errors='coerce')
            df = df.dropna()  # Remove linhas onde conversão falhou
            
            # Normaliza nomes de sintomas
            df['Symptom'] = df['Symptom'].str.strip()
            
            self.sintomas_severidade = df
            
            logger.info(f"Carregados {len(df)} sintomas com severidade")
            return df
            
        except Exception as e:
            logger.error(f"Erro ao carregar sintomas de severidade: {e}")
            raise
    
    def carregar_descricoes_doencas(self) -> pd.DataFrame:
        """
        Carrega o arquivo symptom_Description.csv
        
        Returns:
            DataFrame com doenças e suas descrições
        """
        try:
            caminho = os.path.join(self.base_path, 'symptom_Description.csv')
            
            if not os.path.exists(caminho):
                raise FileNotFoundError(f"Arquivo não encontrado: {caminho}")
                
            df = pd.read_csv(caminho)
            
            # Validações básicas
            if 'Disease' not in df.columns or 'Description' not in df.columns:
                raise ValueError("Arquivo deve conter colunas 'Disease' e 'Description'")
                
            # Remove linhas com valores nulos
            df = df.dropna()
            
            # Normaliza nomes de doenças
            df['Disease'] = df['Disease'].str.strip()
            df['Description'] = df['Description'].str.strip()
            
            self.descricoes_doencas = df
            
            logger.info(f"Carregadas descrições para {len(df)} doenças")
            return df
            
        except Exception as e:
            logger.error(f"Erro ao carregar descrições de doenças: {e}")
            raise
    
    def carregar_precaucoes_doencas(self) -> pd.DataFrame:
        """
        Carrega o arquivo symptom_precaution.csv
        
        Returns:
            DataFrame com doenças e suas precauções
        """
        try:
            caminho = os.path.join(self.base_path, 'symptom_precaution.csv')
            
            if not os.path.exists(caminho):
                raise FileNotFoundError(f"Arquivo não encontrado: {caminho}")
                
            df = pd.read_csv(caminho)
            
            # Validações básicas
            if 'Disease' not in df.columns:
                raise ValueError("Arquivo deve conter coluna 'Disease'")
                
            # Verifica se existem colunas de precauções
            precaution_cols = [col for col in df.columns if 'Precaution' in col]
            if not precaution_cols:
                raise ValueError("Arquivo deve conter colunas de precauções")
                
            # Remove linhas com valores nulos na coluna Disease
            df = df.dropna(subset=['Disease'])
            
            # Normaliza nomes de doenças
            df['Disease'] = df['Disease'].str.strip()
            
            # Consolida precauções em uma lista
            df['Precaucoes'] = df[precaution_cols].apply(
                lambda row: [str(val).strip() for val in row if pd.notna(val) and str(val).strip()], 
                axis=1
            )
            
            self.precaucoes_doencas = df
            
            logger.info(f"Carregadas precauções para {len(df)} doenças")
            return df
            
        except Exception as e:
            logger.error(f"Erro ao carregar precauções de doenças: {e}")
            raise
    
    def carregar_todos_dados(self) -> Dict[str, pd.DataFrame]:
        """
        Carrega todos os datasets de uma vez
        
        Returns:
            Dicionário com todos os DataFrames carregados
        """
        try:
            dados = {}
            
            # Carrega cada dataset
            dados['sintomas_severidade'] = self.carregar_sintomas_severidade()
            dados['descricoes_doencas'] = self.carregar_descricoes_doencas()
            dados['precaucoes_doencas'] = self.carregar_precaucoes_doencas()
            
            logger.info("Todos os datasets carregados com sucesso")
            return dados
            
        except Exception as e:
            logger.error(f"Erro ao carregar datasets: {e}")
            raise
    
    def obter_dicionario_severidade(self) -> Dict[str, float]:
        """
        Retorna dicionário com sintomas e seus pesos de severidade
        
        Returns:
            Dicionário {sintoma: peso}
        """
        if self.sintomas_severidade is None:
            self.carregar_sintomas_severidade()
            
        return dict(zip(
            self.sintomas_severidade['Symptom'], 
            self.sintomas_severidade['weight']
        ))
    
    def obter_dicionario_descricoes(self) -> Dict[str, str]:
        """
        Retorna dicionário com doenças e suas descrições
        
        Returns:
            Dicionário {doenca: descricao}
        """
        if self.descricoes_doencas is None:
            self.carregar_descricoes_doencas()
            
        return dict(zip(
            self.descricoes_doencas['Disease'], 
            self.descricoes_doencas['Description']
        ))
    
    def obter_dicionario_precaucoes(self) -> Dict[str, List[str]]:
        """
        Retorna dicionário com doenças e suas precauções
        
        Returns:
            Dicionário {doenca: [lista_precaucoes]}
        """
        if self.precaucoes_doencas is None:
            self.carregar_precaucoes_doencas()
            
        return dict(zip(
            self.precaucoes_doencas['Disease'], 
            self.precaucoes_doencas['Precaucoes']
        ))
    
    def obter_lista_sintomas(self) -> List[str]:
        """
        Retorna lista de todos os sintomas disponíveis
        
        Returns:
            Lista de sintomas em inglês
        """
        if self.sintomas_severidade is None:
            self.carregar_sintomas_severidade()
            
        return self.sintomas_severidade['Symptom'].tolist()
    
    def obter_lista_doencas(self) -> List[str]:
        """
        Retorna lista de todas as doenças disponíveis
        
        Returns:
            Lista de doenças
        """
        if self.descricoes_doencas is None:
            self.carregar_descricoes_doencas()
            
        return self.descricoes_doencas['Disease'].tolist()
    
    def obter_informacoes_completas_doenca(self, nome_doenca: str) -> Dict[str, Any]:
        """
        Retorna todas as informações disponíveis sobre uma doença
        
        Args:
            nome_doenca: Nome da doença
            
        Returns:
            Dicionário com descrição, precauções, etc.
        """
        try:
            # Carrega dados se necessário
            if self.descricoes_doencas is None:
                self.carregar_descricoes_doencas()
            if self.precaucoes_doencas is None:
                self.carregar_precaucoes_doencas()
            
            resultado = {
                'nome': nome_doenca,
                'descricao': None,
                'precaucoes': [],
                'encontrada': False
            }
            
            # Busca descrição
            desc_row = self.descricoes_doencas[
                self.descricoes_doencas['Disease'].str.strip().str.lower() == nome_doenca.lower()
            ]
            if not desc_row.empty:
                descricao_original = desc_row.iloc[0]['Description']
                # Traduzir para português se necessário
                resultado['descricao'] = traduzir_descricao_se_necessario(descricao_original, nome_doenca)
                resultado['encontrada'] = True
            
            # Busca precauções
            prec_row = self.precaucoes_doencas[
                self.precaucoes_doencas['Disease'].str.strip().str.lower() == nome_doenca.lower()
            ]
            if not prec_row.empty:
                resultado['precaucoes'] = prec_row.iloc[0]['Precaucoes']
                resultado['encontrada'] = True
            
            return resultado
            
        except Exception as e:
            logger.error(f"Erro ao obter informações da doença {nome_doenca}: {e}")
            return {
                'nome': nome_doenca,
                'descricao': None,
                'precaucoes': [],
                'encontrada': False,
                'erro': str(e)
            }
    
    def calcular_score_sintomas(self, lista_sintomas: List[str]) -> float:
        """
        Calcula score baseado nos pesos dos sintomas
        
        Args:
            lista_sintomas: Lista de sintomas em inglês
            
        Returns:
            Score total dos sintomas
        """
        try:
            if self.sintomas_severidade is None:
                self.carregar_sintomas_severidade()
            
            dicionario_pesos = self.obter_dicionario_severidade()
            score_total = 0.0
            
            for sintoma in lista_sintomas:
                # Normaliza sintoma
                sintoma_normalizado = sintoma.strip().lower()
                
                # Busca peso exato ou similar
                peso_encontrado = None
                for sintoma_dataset, peso in dicionario_pesos.items():
                    if sintoma_dataset.lower() == sintoma_normalizado:
                        peso_encontrado = peso
                        break
                
                if peso_encontrado is not None:
                    score_total += peso_encontrado
                else:
                    # Se não encontrar, atribui peso padrão baixo
                    score_total += 1.0
                    logger.warning(f"Sintoma não encontrado no dataset: {sintoma}")
            
            return score_total
            
        except Exception as e:
            logger.error(f"Erro ao calcular score de sintomas: {e}")
            return 0.0

# Função de conveniência para uso direto
def criar_carregador_atualizado(base_path: str = None) -> CarregadorDadosAtualizado:
    """
    Cria uma instância do carregador de dados atualizado
    
    Args:
        base_path: Caminho para os datasets
        
    Returns:
        Instância do CarregadorDadosAtualizado
    """
    return CarregadorDadosAtualizado(base_path)

# Exemplo de uso
if __name__ == "__main__":
    # Configura logging
    logging.basicConfig(level=logging.INFO)
    
    try:
        # Cria carregador
        carregador = criar_carregador_atualizado()
        
        # Carrega dados
        dados = carregador.carregar_todos_dados()
        
        # Exemplos de uso
        print(f"Sintomas disponíveis: {len(carregador.obter_lista_sintomas())}")
        print(f"Doenças disponíveis: {len(carregador.obter_lista_doencas())}")
        
        # Testa informações de uma doença
        info_malaria = carregador.obter_informacoes_completas_doenca("Malaria")
        print(f"Informações sobre Malária: {info_malaria}")
        
        # Testa cálculo de score
        score = carregador.calcular_score_sintomas(['fever', 'cough', 'fatigue'])
        print(f"Score dos sintomas: {score}")
        
    except Exception as e:
        print(f"Erro no exemplo: {e}")