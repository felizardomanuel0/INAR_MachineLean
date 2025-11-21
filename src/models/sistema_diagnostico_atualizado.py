"""
Sistema de Diagnóstico Atualizado
Utiliza os novos datasets com pesos de sintomas, descrições e precauções
"""

import pandas as pd
import numpy as np
import logging
from typing import Dict, List, Tuple, Any, Optional
from collections import defaultdict, Counter
import os

from carregador_dados_atualizado import CarregadorDadosAtualizado
from sintomas_portugues import TRADUCAO_SINTOMAS, traduzir_sintoma_para_ingles
from traducao_doencas import traduzir_doenca_para_portugues

logger = logging.getLogger(__name__)

class SistemaDiagnosticoAtualizado:
    """
    Sistema de diagnóstico baseado nos novos datasets
    """
    
    def __init__(self, base_path: str = None):
        """
        Inicializa o sistema de diagnóstico
        
        Args:
            base_path: Caminho base para os datasets
        """
        self.carregador = CarregadorDadosAtualizado(base_path)
        self.sintomas_severidade = {}
        self.descricoes_doencas = {}
        self.precaucoes_doencas = {}
        self.dados_carregados = False
        
        logger.info("Sistema de diagnóstico atualizado inicializado")
    
    def carregar_dados(self) -> bool:
        """
        Carrega todos os dados necessários
        
        Returns:
            True se carregamento foi bem-sucedido
        """
        try:
            # Carrega todos os datasets
            dados = self.carregador.carregar_todos_dados()
            
            # Obtém dicionários organizados
            self.sintomas_severidade = self.carregador.obter_dicionario_severidade()
            self.descricoes_doencas = self.carregador.obter_dicionario_descricoes()
            self.precaucoes_doencas = self.carregador.obter_dicionario_precaucoes()
            
            self.dados_carregados = True
            
            logger.info(f"Dados carregados: {len(self.sintomas_severidade)} sintomas, "
                       f"{len(self.descricoes_doencas)} descrições de doenças")
            
            return True
            
        except Exception as e:
            logger.error(f"Erro ao carregar dados: {e}")
            return False
    
    def calcular_score_sintomas(self, sintomas_portugueses: List[str]) -> Dict[str, float]:
        """
        Calcula scores dos sintomas baseado nos pesos
        
        Args:
            sintomas_portugueses: Lista de sintomas em português
            
        Returns:
            Dicionário com sintomas e seus scores
        """
        if not self.dados_carregados:
            self.carregar_dados()
        
        scores = {}
        
        for sintoma_pt in sintomas_portugueses:
            # Traduz para inglês
            sintoma_en = traduzir_sintoma_para_ingles(sintoma_pt)
            
            # Busca peso no dataset
            peso = self.sintomas_severidade.get(sintoma_en, 1.0)  # Peso padrão se não encontrar
            
            scores[sintoma_pt] = peso
            
            if sintoma_en not in self.sintomas_severidade:
                logger.warning(f"Sintoma não encontrado no dataset: {sintoma_pt} -> {sintoma_en}")
        
        return scores
    
    def gerar_diagnosticos_baseados_em_pesos(
        self, 
        sintomas_portugueses: List[str],
        top_n: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Gera diagnósticos baseado nos pesos dos sintomas
        
        Args:
            sintomas_portugueses: Lista de sintomas reportados
            top_n: Número de diagnósticos a retornar
            
        Returns:
            Lista de diagnósticos com probabilidades
        """
        if not self.dados_carregados:
            self.carregar_dados()
        
        # Calcula scores dos sintomas
        scores_sintomas = self.calcular_score_sintomas(sintomas_portugueses)
        
        # Score total dos sintomas informados
        score_total_informado = sum(scores_sintomas.values())
        
        # Para cada doença, calcula compatibilidade baseada na experiência médica
        diagnosticos_ponderados = {}
        
        for doenca in self.descricoes_doencas.keys():
            # Algoritmo heurístico baseado no conhecimento médico comum
            score_doenca = self._calcular_compatibilidade_doenca(
                doenca, sintomas_portugueses, scores_sintomas
            )
            
            if score_doenca > 0:
                diagnosticos_ponderados[doenca] = score_doenca
        
        # Ordena por score e converte para percentuais
        diagnosticos_ordenados = sorted(
            diagnosticos_ponderados.items(), 
            key=lambda x: x[1], 
            reverse=True
        )[:top_n]
        
        # Normaliza scores para percentuais
        if diagnosticos_ordenados:
            max_score = diagnosticos_ordenados[0][1]
            total_scores = sum(score for _, score in diagnosticos_ordenados)
            
            resultados = []
            for i, (doenca, score) in enumerate(diagnosticos_ordenados):
                # Calcula probabilidade normalizada
                probabilidade = (score / total_scores * 100) if total_scores > 0 else 0
                
                # Ajusta para ter distribuição mais realista
                if i == 0:  # Diagnóstico principal
                    probabilidade = max(probabilidade, 40)
                elif i == 1:  # Segunda opção
                    probabilidade = max(probabilidade * 0.7, 20)
                else:  # Outras opções
                    probabilidade = max(probabilidade * 0.5, 10)
                
                # Traduz para português
                doenca_pt = traduzir_doenca_para_portugues(doenca)
                
                resultado = {
                    'doenca': doenca_pt,
                    'doenca_original': doenca,
                    'probabilidade': min(probabilidade, 95),  # Máximo 95%
                    'score_bruto': score,
                    'descricao': self.descricoes_doencas.get(doenca, ''),
                    'precaucoes': self.precaucoes_doencas.get(doenca, []),
                    'sintomas_considerados': list(scores_sintomas.keys()),
                    'score_sintomas': scores_sintomas
                }
                
                resultados.append(resultado)
            
            return resultados
        
        return []
    
    def _calcular_compatibilidade_doenca(
        self, 
        doenca: str, 
        sintomas_pt: List[str], 
        scores_sintomas: Dict[str, float]
    ) -> float:
        """
        Calcula compatibilidade entre sintomas e doença usando heurísticas médicas
        
        Args:
            doenca: Nome da doença em inglês
            sintomas_pt: Lista de sintomas em português
            scores_sintomas: Scores dos sintomas
            
        Returns:
            Score de compatibilidade
        """
        # Base score dos sintomas
        score_base = sum(scores_sintomas.values())
        
        # Aplicar heurísticas específicas por doença
        multiplicador = 1.0
        bonus = 0.0
        
        # Converte sintomas para inglês para análise
        sintomas_en = [traduzir_sintoma_para_ingles(s) for s in sintomas_pt]
        sintomas_en_lower = [s.lower() for s in sintomas_en]
        
        # Heurísticas específicas por doença
        doenca_lower = doenca.lower()
        
        if 'malaria' in doenca_lower:
            # Malária: febre + calafrios são muito indicativos
            if any('fever' in s or 'high_fever' in s for s in sintomas_en_lower):
                multiplicador *= 1.5
            if any('chill' in s or 'shiver' in s for s in sintomas_en_lower):
                multiplicador *= 1.3
            if any('sweat' in s for s in sintomas_en_lower):
                multiplicador *= 1.2
                
        elif 'diabetes' in doenca_lower:
            # Diabetes: micção frequente + fadiga + sede
            if any('urin' in s or 'polyuria' in s for s in sintomas_en_lower):
                multiplicador *= 1.4
            if any('fatigue' in s or 'lethargy' in s for s in sintomas_en_lower):
                multiplicador *= 1.2
            if any('weight_loss' in s for s in sintomas_en_lower):
                multiplicador *= 1.2
                
        elif 'tuberculosis' in doenca_lower:
            # Tuberculose: tosse persistente + perda de peso + suor noturno
            if any('cough' in s for s in sintomas_en_lower):
                multiplicador *= 1.6
            if any('weight_loss' in s for s in sintomas_en_lower):
                multiplicador *= 1.3
            if any('sweat' in s for s in sintomas_en_lower):
                multiplicador *= 1.3
                
        elif 'pneumonia' in doenca_lower:
            # Pneumonia: febre + dor no peito + dificuldade respirar
            if any('fever' in s or 'high_fever' in s for s in sintomas_en_lower):
                multiplicador *= 1.4
            if any('chest_pain' in s for s in sintomas_en_lower):
                multiplicador *= 1.5
            if any('breath' in s for s in sintomas_en_lower):
                multiplicador *= 1.4
                
        elif 'hypertension' in doenca_lower:
            # Hipertensão: pode ser assintomática, score moderado
            if any('headache' in s for s in sintomas_en_lower):
                multiplicador *= 1.2
            if any('dizziness' in s for s in sintomas_en_lower):
                multiplicador *= 1.2
            else:
                multiplicador *= 0.7  # Reduz se não há sintomas típicos
                
        elif 'asthma' in doenca_lower or 'bronchial' in doenca_lower:
            # Asma: falta de ar + chiado
            if any('breath' in s for s in sintomas_en_lower):
                multiplicador *= 1.6
            if any('chest' in s for s in sintomas_en_lower):
                multiplicador *= 1.2
                
        elif 'migraine' in doenca_lower:
            # Enxaqueca: dor de cabeça específica
            if any('headache' in s for s in sintomas_en_lower):
                multiplicador *= 1.8
            if any('nausea' in s or 'vomit' in s for s in sintomas_en_lower):
                multiplicador *= 1.3
                
        elif 'common cold' in doenca_lower or 'cold' in doenca_lower:
            # Resfriado: sintomas respiratórios leves
            if any('runny_nose' in s or 'congestion' in s for s in sintomas_en_lower):
                multiplicador *= 1.4
            if any('cough' in s for s in sintomas_en_lower):
                multiplicador *= 1.2
            if any('throat' in s for s in sintomas_en_lower):
                multiplicador *= 1.2
                
        elif 'gastroenteritis' in doenca_lower:
            # Gastroenterite: problemas digestivos
            if any('diarrhoea' in s or 'vomit' in s for s in sintomas_en_lower):
                multiplicador *= 1.5
            if any('abdominal_pain' in s or 'stomach_pain' in s for s in sintomas_en_lower):
                multiplicador *= 1.3
                
        # Penaliza diagnósticos pouco prováveis baseado no número de sintomas
        num_sintomas = len(sintomas_pt)
        if num_sintomas < 2:
            multiplicador *= 0.6  # Poucos sintomas = menos confiável
        elif num_sintomas > 8:
            multiplicador *= 0.8  # Muitos sintomas = pode ser inespecífico
        
        return score_base * multiplicador + bonus
    
    def obter_informacoes_doenca(self, nome_doenca: str) -> Dict[str, Any]:
        """
        Obtém informações completas sobre uma doença
        
        Args:
            nome_doenca: Nome da doença (português ou inglês)
            
        Returns:
            Informações da doença
        """
        if not self.dados_carregados:
            self.carregar_dados()
        
        return self.carregador.obter_informacoes_completas_doenca(nome_doenca)
    
    def diagnosticar_sintomas(
        self, 
        sintomas_portugueses: List[str],
        incluir_detalhes: bool = True
    ) -> Dict[str, Any]:
        """
        Função principal de diagnóstico
        
        Args:
            sintomas_portugueses: Lista de sintomas em português
            incluir_detalhes: Se deve incluir informações detalhadas
            
        Returns:
            Resultado completo do diagnóstico
        """
        try:
            if not sintomas_portugueses:
                return {
                    'sucesso': False,
                    'erro': 'Nenhum sintoma informado'
                }
            
            # Gera diagnósticos
            diagnosticos = self.gerar_diagnosticos_baseados_em_pesos(sintomas_portugueses)
            
            # Calcula scores dos sintomas
            scores_sintomas = self.calcular_score_sintomas(sintomas_portugueses)
            
            resultado = {
                'sucesso': True,
                'sintomas_informados': sintomas_portugueses,
                'sintomas_scores': scores_sintomas,
                'score_total': sum(scores_sintomas.values()),
                'num_diagnosticos': len(diagnosticos),
                'diagnosticos': diagnosticos,
                'timestamp': pd.Timestamp.now().isoformat()
            }
            
            if incluir_detalhes and diagnosticos:
                # Adiciona informações do diagnóstico principal
                principal = diagnosticos[0]
                resultado['diagnostico_principal'] = {
                    'doenca': principal['doenca'],
                    'probabilidade': principal['probabilidade'],
                    'descricao': principal['descricao'],
                    'precaucoes': principal['precaucoes']
                }
            
            logger.info(f"Diagnóstico realizado com {len(sintomas_portugueses)} sintomas, "
                       f"{len(diagnosticos)} possibilidades encontradas")
            
            return resultado
            
        except Exception as e:
            logger.error(f"Erro durante diagnóstico: {e}")
            return {
                'sucesso': False,
                'erro': str(e),
                'sintomas_informados': sintomas_portugueses
            }

# Função de conveniência
def criar_sistema_diagnostico(base_path: str = None) -> SistemaDiagnosticoAtualizado:
    """
    Cria instância do sistema de diagnóstico
    
    Args:
        base_path: Caminho para os datasets
        
    Returns:
        Sistema de diagnóstico configurado
    """
    return SistemaDiagnosticoAtualizado(base_path)

# Exemplo de uso
if __name__ == "__main__":
    # Configura logging
    logging.basicConfig(level=logging.INFO)
    
    try:
        # Cria sistema
        sistema = criar_sistema_diagnostico()
        
        # Teste com sintomas de malária
        sintomas_teste = [
            'Febre Alta',
            'Calafrios', 
            'Dor de Cabeça',
            'Náusea',
            'Fadiga'
        ]
        
        print(f"Testando diagnóstico com sintomas: {sintomas_teste}")
        
        resultado = sistema.diagnosticar_sintomas(sintomas_teste)
        
        if resultado['sucesso']:
            print(f"\nResultado do diagnóstico:")
            print(f"Score total dos sintomas: {resultado['score_total']}")
            print(f"Diagnósticos encontrados: {resultado['num_diagnosticos']}")
            
            for i, diag in enumerate(resultado['diagnosticos'], 1):
                print(f"\n{i}. {diag['doenca']} - {diag['probabilidade']:.1f}%")
                if diag['descricao']:
                    print(f"   Descrição: {diag['descricao'][:100]}...")
                if diag['precaucoes']:
                    print(f"   Precauções: {', '.join(diag['precaucoes'][:3])}")
        else:
            print(f"Erro no diagnóstico: {resultado['erro']}")
            
    except Exception as e:
        print(f"Erro no exemplo: {e}")