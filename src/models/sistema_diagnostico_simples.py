"""
Sistema de Diagnóstico Simplificado
Funciona apenas com o arquivo dados.csv
"""

import pandas as pd
import numpy as np
import logging
from typing import Dict, List, Tuple
from datetime import datetime
import sys
import os
sys.path.append(os.path.dirname(__file__))
from carregador_dados_simples import CarregadorDadosSimplificado

logger = logging.getLogger(__name__)

class SistemaDiagnosticoSimples:
    """
    Sistema de diagnóstico simplificado que funciona apenas com dados.csv
    """
    
    def __init__(self, caminho_dados: str = None):
        """
        Inicializa o sistema de diagnóstico
        
        Args:
            caminho_dados (str): Caminho para o diretório dos dados
        """
        self.carregador = CarregadorDadosSimplificado(caminho_dados)
        self.dados_carregados = False
        self.historico_diagnosticos = []
        
        # Carregar dados automaticamente
        self._carregar_dados()
        
        logger.info("Sistema de diagnóstico simplificado inicializado")
    
    def _carregar_dados(self):
        """Carrega os dados do sistema"""
        try:
            self.carregador.carregar_dados_principais()
            self.dados_carregados = True
            logger.info("✅ Dados carregados com sucesso")
            
        except Exception as e:
            logger.error(f"❌ Erro ao carregar dados: {e}")
            self.dados_carregados = False
    
    def obter_sintomas_disponiveis(self) -> List[str]:
        """
        Obtém lista de sintomas disponíveis para seleção
        
        Returns:
            List[str]: Lista de sintomas ordenados
        """
        if not self.dados_carregados:
            return []
        
        return self.carregador.obter_sintomas_ordenados()
    
    def obter_doencas_disponiveis(self) -> List[str]:
        """
        Obtém lista de doenças disponíveis no sistema
        
        Returns:
            List[str]: Lista de doenças ordenadas
        """
        if not self.dados_carregados:
            return []
        
        return self.carregador.obter_doencas_ordenadas()
    
    def realizar_diagnostico(self, sintomas_selecionados: List[str]) -> Dict:
        """
        Realiza diagnóstico baseado nos sintomas selecionados
        
        Args:
            sintomas_selecionados (List[str]): Lista de sintomas selecionados
            
        Returns:
            Dict: Resultado do diagnóstico
        """
        if not self.dados_carregados:
            return {
                'erro': 'Dados não carregados',
                'diagnosticos': [],
                'timestamp': datetime.now().isoformat()
            }
        
        if not sintomas_selecionados:
            return {
                'erro': 'Nenhum sintoma selecionado',
                'diagnosticos': [],
                'timestamp': datetime.now().isoformat()
            }
        
        try:
            # Calcular probabilidades
            resultados = self.carregador.calcular_probabilidades_doenca(sintomas_selecionados)
            
            # Processar resultados e limitar a 3 melhores
            diagnosticos_processados = []
            for resultado in resultados[:3]:  # Apenas os 3 melhores
                nivel_confianca = self._determinar_nivel_confianca(resultado['probabilidade'])
                
                diagnostico = {
                    'doenca': resultado['doenca'],
                    'probabilidade': resultado['probabilidade'],
                    'nivel_confianca': nivel_confianca,
                    'sintomas_comum': resultado['sintomas_comum'],
                    'sintomas_em_comum_count': resultado['sintomas_em_comum'],
                    'total_sintomas_doenca': resultado['total_sintomas_doenca']
                }
                diagnosticos_processados.append(diagnostico)
            
            # Criar resultado final
            resultado_final = {
                'sintomas_entrada': sintomas_selecionados,
                'total_sintomas_entrada': len(sintomas_selecionados),
                'diagnosticos': diagnosticos_processados,
                'total_diagnosticos': len(diagnosticos_processados),
                'timestamp': datetime.now().isoformat(),
                'confiabilidade_geral': self._calcular_confiabilidade_geral(diagnosticos_processados)
            }
            
            # Adicionar ao histórico
            self.historico_diagnosticos.append(resultado_final)
            
            logger.info(f"Diagnóstico realizado: {len(diagnosticos_processados)} possibilidades encontradas")
            
            return resultado_final
            
        except Exception as e:
            logger.error(f"Erro ao realizar diagnóstico: {e}")
            return {
                'erro': str(e),
                'diagnosticos': [],
                'timestamp': datetime.now().isoformat()
            }
    
    def _determinar_nivel_confianca(self, probabilidade: float) -> str:
        """
        Determina o nível de confiança baseado na probabilidade
        
        Args:
            probabilidade (float): Probabilidade calculada
            
        Returns:
            str: Nível de confiança
        """
        if probabilidade >= 70:
            return "Alta"
        elif probabilidade >= 40:
            return "Média"
        elif probabilidade >= 20:
            return "Baixa"
        else:
            return "Muito Baixa"
    
    def _calcular_confiabilidade_geral(self, diagnosticos: List[Dict]) -> str:
        """
        Calcula confiabilidade geral do diagnóstico
        
        Args:
            diagnosticos (List[Dict]): Lista de diagnósticos
            
        Returns:
            str: Confiabilidade geral
        """
        if not diagnosticos:
            return "Sem diagnósticos"
        
        probabilidade_maxima = max(d['probabilidade'] for d in diagnosticos)
        
        if probabilidade_maxima >= 70:
            return "Alta confiabilidade"
        elif probabilidade_maxima >= 50:
            return "Confiabilidade moderada"
        elif probabilidade_maxima >= 30:
            return "Baixa confiabilidade"
        else:
            return "Confiabilidade muito baixa"
    
    def buscar_por_sintoma(self, sintoma: str) -> List[str]:
        """
        Busca doenças que contêm um sintoma específico
        
        Args:
            sintoma (str): Sintoma para buscar
            
        Returns:
            List[str]: Lista de doenças
        """
        if not self.dados_carregados:
            return []
        
        return self.carregador.buscar_doencas_por_sintoma(sintoma)
    
    def obter_sintomas_por_doenca(self, doenca: str) -> List[str]:
        """
        Obtém sintomas associados a uma doença
        
        Args:
            doenca (str): Nome da doença
            
        Returns:
            List[str]: Lista de sintomas
        """
        if not self.dados_carregados:
            return []
        
        return self.carregador.obter_sintomas_por_doenca(doenca)
    
    def obter_estatisticas_sistema(self) -> Dict:
        """
        Obtém estatísticas do sistema
        
        Returns:
            Dict: Estatísticas do sistema
        """
        stats_carregador = self.carregador.obter_estatisticas()
        
        stats_sistema = {
            'sistema_ativo': self.dados_carregados,
            'total_diagnosticos_realizados': len(self.historico_diagnosticos),
            'data_inicializacao': datetime.now().isoformat()
        }
        
        return {**stats_carregador, **stats_sistema}
    
    def obter_historico_diagnosticos(self, ultimos: int = None) -> List[Dict]:
        """
        Obtém histórico de diagnósticos
        
        Args:
            ultimos (int): Número de diagnósticos recentes
            
        Returns:
            List[Dict]: Histórico de diagnósticos
        """
        if ultimos:
            return self.historico_diagnosticos[-ultimos:]
        return self.historico_diagnosticos.copy()
    
    def limpar_historico(self):
        """Limpa o histórico de diagnósticos"""
        self.historico_diagnosticos.clear()
        logger.info("Histórico de diagnósticos limpo")

def main():
    """Função para testar o sistema"""
    print("🏥 Testando Sistema de Diagnóstico Simplificado")
    print("=" * 60)
    
    sistema = SistemaDiagnosticoSimples()
    
    if not sistema.dados_carregados:
        print("❌ Erro: Não foi possível carregar os dados")
        return
    
    # Estatísticas
    stats = sistema.obter_estatisticas_sistema()
    print(f"📊 Estatísticas do Sistema:")
    for chave, valor in stats.items():
        print(f"  • {chave}: {valor}")
    
    print(f"\n🔍 Sintomas disponíveis (primeiros 10):")
    sintomas = sistema.obter_sintomas_disponiveis()[:10]
    for i, sintoma in enumerate(sintomas, 1):
        print(f"  {i}. {sintoma}")
    
    # Teste de diagnóstico
    print(f"\n🩺 Teste de Diagnóstico:")
    sintomas_teste = ['itching', 'skin rash', 'nodal skin eruptions']
    resultado = sistema.realizar_diagnostico(sintomas_teste)
    
    if 'erro' in resultado:
        print(f"❌ Erro: {resultado['erro']}")
    else:
        print(f"Sintomas: {resultado['sintomas_entrada']}")
        print(f"Confiabilidade: {resultado['confiabilidade_geral']}")
        print(f"Possíveis diagnósticos:")
        
        for i, diag in enumerate(resultado['diagnosticos'][:5], 1):
            emoji = "🔴" if diag['probabilidade'] >= 70 else "🟡" if diag['probabilidade'] >= 40 else "🟢"
            print(f"  {i}. {emoji} {diag['doenca']} - {diag['probabilidade']:.1f}% ({diag['nivel_confianca']})")

if __name__ == "__main__":
    main()