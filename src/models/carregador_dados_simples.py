"""
Carregador de Dados Simplificado para dados.csv
Sistema de diagnóstico médico usando apenas o arquivo dados.csv
"""

import pandas as pd
import numpy as np
import os
import sys
import logging
from typing import Dict, List, Tuple, Set
from collections import Counter

# Adicionar caminho para importar traduções
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
try:
    from utils.traducoes import traduzir_sintoma, traduzir_doenca, traduzir_lista_sintomas
except ImportError:
    # Funções de fallback caso não encontre as traduções
    def traduzir_sintoma(sintoma):
        return sintoma.replace('_', ' ').title()
    def traduzir_doenca(doenca):
        return doenca
    def traduzir_lista_sintomas(lista):
        return [traduzir_sintoma(s) for s in lista]

logger = logging.getLogger(__name__)

class CarregadorDadosSimplificado:
    """
    Carregador simplificado que trabalha apenas com dados.csv
    """
    
    def __init__(self, base_path: str = None):
        """
        Inicializa o carregador de dados
        
        Args:
            base_path (str): Caminho base para os datasets
        """
        if base_path is None:
            self.base_path = os.path.join(os.path.dirname(__file__), '..', '..', 'dataset')
        else:
            self.base_path = base_path
            
        self.dados_principais = None
        self.sintomas_unicos = set()
        self.doencas_unicas = set()
        self.mapa_doenca_sintomas = {}
        
        logger.info(f"Carregador inicializado com caminho: {self.base_path}")
    
    def carregar_dados_principais(self) -> pd.DataFrame:
        """
        Carrega e processa o arquivo dados.csv
        
        Returns:
            pd.DataFrame: Dados processados
        """
        try:
            caminho = os.path.join(self.base_path, 'dados.csv')
            
            if not os.path.exists(caminho):
                raise FileNotFoundError(f"Arquivo não encontrado: {caminho}")
            
            # Carregar dados
            df = pd.read_csv(caminho)
            
            logger.info(f"Carregados {len(df)} registros do arquivo dados.csv")
            
            # Processar dados
            self._processar_dados(df)
            
            self.dados_principais = df
            return df
            
        except Exception as e:
            logger.error(f"Erro ao carregar dados principais: {e}")
            raise
    
    def _processar_dados(self, df: pd.DataFrame):
        """
        Processa os dados para extrair sintomas e doenças únicos
        
        Args:
            df (pd.DataFrame): DataFrame com os dados
        """
        # Extrair doenças únicas
        self.doencas_unicas = set(df['Disease'].unique())
        
        # Extrair sintomas únicos
        sintomas_colunas = [col for col in df.columns if col.startswith('Symptom_')]
        
        # Criar mapeamentos para tradução
        self.mapa_sintomas_pt_en = {}  # português -> inglês
        self.mapa_doencas_pt_en = {}   # português -> inglês
        
        for _, row in df.iterrows():
            doenca = row['Disease']
            doenca_pt = traduzir_doenca(doenca)
            self.mapa_doencas_pt_en[doenca_pt] = doenca
            
            sintomas_doenca = []
            sintomas_doenca_pt = []
            
            for col in sintomas_colunas:
                sintoma = row[col]
                if pd.notna(sintoma) and sintoma.strip():
                    # Limpar sintoma original
                    sintoma_limpo = sintoma.strip()
                    # Traduzir para português
                    sintoma_pt = traduzir_sintoma(sintoma_limpo)
                    
                    self.sintomas_unicos.add(sintoma_pt)
                    self.mapa_sintomas_pt_en[sintoma_pt] = sintoma_limpo
                    
                    sintomas_doenca.append(sintoma_limpo)
                    sintomas_doenca_pt.append(sintoma_pt)
            
            # Mapear doença em português -> sintomas em português
            if doenca_pt not in self.mapa_doenca_sintomas:
                self.mapa_doenca_sintomas[doenca_pt] = []
            self.mapa_doenca_sintomas[doenca_pt].extend(sintomas_doenca_pt)
        
        # Traduzir doenças únicas
        self.doencas_unicas = {traduzir_doenca(d) for d in self.doencas_unicas}
        
        logger.info(f"Encontradas {len(self.doencas_unicas)} doenças únicas")
        logger.info(f"Encontrados {len(self.sintomas_unicos)} sintomas únicos")
    
    def obter_sintomas_ordenados(self) -> List[str]:
        """
        Retorna lista de sintomas ordenados alfabeticamente
        
        Returns:
            List[str]: Sintomas ordenados
        """
        return sorted(list(self.sintomas_unicos))
    
    def obter_doencas_ordenadas(self) -> List[str]:
        """
        Retorna lista de doenças ordenadas alfabeticamente
        
        Returns:
            List[str]: Doenças ordenadas
        """
        return sorted(list(self.doencas_unicas))
    
    def obter_sintomas_por_doenca(self, doenca: str) -> List[str]:
        """
        Retorna sintomas associados a uma doença específica
        
        Args:
            doenca (str): Nome da doença
            
        Returns:
            List[str]: Lista de sintomas
        """
        return self.mapa_doenca_sintomas.get(doenca, [])
    
    def calcular_probabilidades_doenca(self, sintomas_selecionados: List[str]) -> List[Dict]:
        """
        Calcula probabilidades de doenças baseado nos sintomas selecionados
        
        Args:
            sintomas_selecionados (List[str]): Sintomas selecionados pelo usuário
            
        Returns:
            List[Dict]: Lista de doenças com probabilidades
        """
        if not sintomas_selecionados:
            return []
        
        # Os sintomas já estão em português
        sintomas_selecionados_set = set(sintomas_selecionados)
        
        resultados = []
        
        for doenca, sintomas_doenca in self.mapa_doenca_sintomas.items():
            # Contar sintomas em comum (já em português)
            sintomas_doenca_set = set(sintomas_doenca)
            sintomas_selecionados_set_normalizado = sintomas_selecionados_set
            
            # Interseção (sintomas em comum)
            sintomas_comum = sintomas_doenca_set.intersection(sintomas_selecionados_set_normalizado)
            
            if sintomas_comum:
                # Calcular probabilidade baseada na proporção de sintomas em comum
                total_sintomas_doenca = len(sintomas_doenca_set)
                total_sintomas_selecionados = len(sintomas_selecionados_set_normalizado)
                sintomas_em_comum = len(sintomas_comum)
                
                # Fórmula: (sintomas em comum / total sintomas da doença) * 100
                # Com boost se muitos sintomas selecionados batem
                probabilidade_base = (sintomas_em_comum / total_sintomas_doenca) * 100
                
                # Boost baseado na cobertura dos sintomas selecionados
                cobertura_selecionados = sintomas_em_comum / total_sintomas_selecionados
                probabilidade_final = min(95, probabilidade_base * (1 + cobertura_selecionados * 0.5))
                
                resultados.append({
                    'doenca': doenca,
                    'probabilidade': probabilidade_final,
                    'sintomas_comum': list(sintomas_comum),
                    'total_sintomas_doenca': total_sintomas_doenca,
                    'sintomas_em_comum': sintomas_em_comum
                })
        
        # Ordenar por probabilidade (maior para menor)
        resultados.sort(key=lambda x: x['probabilidade'], reverse=True)
        
        return resultados[:10]  # Top 10 diagnósticos
    
    def obter_estatisticas(self) -> Dict:
        """
        Retorna estatísticas dos dados carregados
        
        Returns:
            Dict: Estatísticas dos dados
        """
        if self.dados_principais is None:
            return {'erro': 'Dados não carregados'}
        
        # Contar sintomas por doença
        sintomas_por_doenca = {}
        for doenca, sintomas in self.mapa_doenca_sintomas.items():
            sintomas_por_doenca[doenca] = len(set(sintomas))
        
        return {
            'total_registros': len(self.dados_principais),
            'total_doencas': len(self.doencas_unicas),
            'total_sintomas': len(self.sintomas_unicos),
            'media_sintomas_por_doenca': np.mean(list(sintomas_por_doenca.values())),
            'doenca_mais_sintomas': max(sintomas_por_doenca.items(), key=lambda x: x[1]),
            'doenca_menos_sintomas': min(sintomas_por_doenca.items(), key=lambda x: x[1])
        }
    
    def buscar_doencas_por_sintoma(self, sintoma: str) -> List[str]:
        """
        Busca doenças que contêm um sintoma específico
        
        Args:
            sintoma (str): Sintoma a buscar
            
        Returns:
            List[str]: Lista de doenças que contêm o sintoma
        """
        sintoma_normalizado = sintoma.lower().strip()
        doencas_encontradas = []
        
        for doenca, sintomas in self.mapa_doenca_sintomas.items():
            if sintoma_normalizado in [s.lower() for s in sintomas]:
                doencas_encontradas.append(doenca)
        
        return doencas_encontradas

def main():
    """Função para testar o carregador"""
    print("🔬 Testando Carregador de Dados Simplificado")
    print("=" * 50)
    
    carregador = CarregadorDadosSimplificado()
    
    try:
        # Carregar dados
        df = carregador.carregar_dados_principais()
        print(f"✅ Dados carregados: {len(df)} registros")
        
        # Estatísticas
        stats = carregador.obter_estatisticas()
        print(f"\n📊 Estatísticas:")
        for chave, valor in stats.items():
            print(f"  • {chave}: {valor}")
        
        # Teste de diagnóstico
        print(f"\n🩺 Teste de Diagnóstico:")
        sintomas_teste = ['itching', 'skin rash', 'nodal skin eruptions']
        resultados = carregador.calcular_probabilidades_doenca(sintomas_teste)
        
        print(f"Sintomas testados: {sintomas_teste}")
        print("Possíveis diagnósticos:")
        for i, resultado in enumerate(resultados[:5], 1):
            print(f"  {i}. {resultado['doenca']} - {resultado['probabilidade']:.1f}%")
        
    except Exception as e:
        print(f"❌ Erro: {e}")

if __name__ == "__main__":
    main()