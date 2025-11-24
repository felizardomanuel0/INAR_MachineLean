"""
Sistema de Diagnóstico Simplificado
Funciona apenas com o arquivo dados.csv
"""

import pandas as pd
import numpy as np
import logging
import json
import os
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
        self.sintomas_personalizados = []  # Lista de sintomas adicionados manualmente
        
        # Configurar caminhos para armazenamento
        self.diretorio_dados = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        self.arquivo_consultas = os.path.join(self.diretorio_dados, 'consultas_realizadas.json')
        self.arquivo_sintomas_custom = os.path.join(self.diretorio_dados, 'sintomas_personalizados.json')
        
        # Carregar dados salvos
        self._carregar_consultas_salvas()
        self._carregar_sintomas_personalizados()
        
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
    
    def realizar_diagnostico(self, sintomas_selecionados: List[str], dados_paciente: Dict = None) -> Dict:
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
                'confiabilidade_geral': self._calcular_confiabilidade_geral(diagnosticos_processados),
                'dados_paciente': dados_paciente if dados_paciente else {}
            }
            
            # Adicionar ao histórico
            self.historico_diagnosticos.append(resultado_final)
            
            # Salvar consulta permanentemente
            self._salvar_consulta(resultado_final)
            
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
    
    def _carregar_consultas_salvas(self):
        """Carrega consultas salvas de arquivo JSON"""
        try:
            if os.path.exists(self.arquivo_consultas):
                with open(self.arquivo_consultas, 'r', encoding='utf-8') as f:
                    consultas_salvas = json.load(f)
                    # Carregar apenas as últimas 50 consultas para o histórico
                    self.historico_diagnosticos = consultas_salvas[-50:] if len(consultas_salvas) > 50 else consultas_salvas
                logger.info(f"Carregadas {len(self.historico_diagnosticos)} consultas do histórico")
        except Exception as e:
            logger.warning(f"Erro ao carregar consultas salvas: {e}")
            self.historico_diagnosticos = []
    
    def _carregar_sintomas_personalizados(self):
        """Carrega sintomas personalizados de arquivo JSON"""
        try:
            if os.path.exists(self.arquivo_sintomas_custom):
                with open(self.arquivo_sintomas_custom, 'r', encoding='utf-8') as f:
                    self.sintomas_personalizados = json.load(f)
                logger.info(f"Carregados {len(self.sintomas_personalizados)} sintomas personalizados")
        except Exception as e:
            logger.warning(f"Erro ao carregar sintomas personalizados: {e}")
            self.sintomas_personalizados = []
    
    def _salvar_consulta(self, consulta: Dict):
        """Salva consulta em arquivo JSON"""
        try:
            # Carregar consultas existentes
            consultas_existentes = []
            if os.path.exists(self.arquivo_consultas):
                with open(self.arquivo_consultas, 'r', encoding='utf-8') as f:
                    consultas_existentes = json.load(f)
            
            # Adicionar nova consulta
            consultas_existentes.append(consulta)
            
            # Manter apenas últimas 1000 consultas
            if len(consultas_existentes) > 1000:
                consultas_existentes = consultas_existentes[-1000:]
            
            # Salvar arquivo
            with open(self.arquivo_consultas, 'w', encoding='utf-8') as f:
                json.dump(consultas_existentes, f, ensure_ascii=False, indent=2)
                
        except Exception as e:
            logger.error(f"Erro ao salvar consulta: {e}")
    
    def adicionar_sintoma_personalizado(self, sintoma: str) -> bool:
        """
        Adiciona um sintoma personalizado à lista
        
        Args:
            sintoma (str): Sintoma a ser adicionado
            
        Returns:
            bool: True se adicionado com sucesso
        """
        try:
            sintoma_limpo = sintoma.strip().title()
            
            if not sintoma_limpo:
                return False
            
            # Verificar se já existe
            if sintoma_limpo not in self.sintomas_personalizados:
                self.sintomas_personalizados.append(sintoma_limpo)
                self._salvar_sintomas_personalizados()
                logger.info(f"Sintoma personalizado adicionado: {sintoma_limpo}")
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"Erro ao adicionar sintoma personalizado: {e}")
            return False
    
    def _salvar_sintomas_personalizados(self):
        """Salva sintomas personalizados em arquivo JSON"""
        try:
            with open(self.arquivo_sintomas_custom, 'w', encoding='utf-8') as f:
                json.dump(self.sintomas_personalizados, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"Erro ao salvar sintomas personalizados: {e}")
    
    def obter_todos_sintomas(self) -> List[str]:
        """
        Retorna todos os sintomas disponíveis (originais + personalizados)
        
        Returns:
            List[str]: Lista completa de sintomas
        """
        sintomas_originais = self.obter_sintomas_disponiveis() if self.dados_carregados else []
        todos_sintomas = list(set(sintomas_originais + self.sintomas_personalizados))
        return sorted(todos_sintomas)
    
    def obter_consultas_por_paciente(self, nome_paciente: str) -> List[Dict]:
        """
        Obtém consultas de um paciente específico
        
        Args:
            nome_paciente (str): Nome do paciente
            
        Returns:
            List[Dict]: Lista de consultas do paciente
        """
        try:
            consultas_paciente = []
            
            # Buscar no histórico atual
            for consulta in self.historico_diagnosticos:
                dados_paciente = consulta.get('dados_paciente', {})
                if dados_paciente.get('nome', '').lower() == nome_paciente.lower():
                    consultas_paciente.append(consulta)
            
            # Buscar no arquivo completo se necessário
            if os.path.exists(self.arquivo_consultas):
                with open(self.arquivo_consultas, 'r', encoding='utf-8') as f:
                    todas_consultas = json.load(f)
                    for consulta in todas_consultas:
                        dados_paciente = consulta.get('dados_paciente', {})
                        if dados_paciente.get('nome', '').lower() == nome_paciente.lower():
                            # Evitar duplicatas
                            if consulta not in consultas_paciente:
                                consultas_paciente.append(consulta)
            
            # Ordenar por timestamp (mais recente primeiro)
            consultas_paciente.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
            
            return consultas_paciente
            
        except Exception as e:
            logger.error(f"Erro ao buscar consultas do paciente: {e}")
            return []
    
    def obter_estatisticas_consultas(self) -> Dict:
        """
        Obtém estatísticas das consultas realizadas
        
        Returns:
            Dict: Estatísticas das consultas
        """
        try:
            total_consultas = 0
            pacientes_unicos = set()
            sintomas_mais_comuns = {}
            doencas_mais_diagnosticadas = {}
            
            # Contar consultas no arquivo
            if os.path.exists(self.arquivo_consultas):
                with open(self.arquivo_consultas, 'r', encoding='utf-8') as f:
                    todas_consultas = json.load(f)
                    total_consultas = len(todas_consultas)
                    
                    for consulta in todas_consultas:
                        # Pacientes únicos
                        dados_paciente = consulta.get('dados_paciente', {})
                        nome = dados_paciente.get('nome', '').strip()
                        if nome:
                            pacientes_unicos.add(nome.lower())
                        
                        # Sintomas mais comuns
                        for sintoma in consulta.get('sintomas_entrada', []):
                            sintomas_mais_comuns[sintoma] = sintomas_mais_comuns.get(sintoma, 0) + 1
                        
                        # Doenças mais diagnosticadas
                        diagnosticos = consulta.get('diagnosticos', [])
                        if diagnosticos:
                            doenca = diagnosticos[0].get('doenca', '')
                            if doenca:
                                doencas_mais_diagnosticadas[doenca] = doencas_mais_diagnosticadas.get(doenca, 0) + 1
            
            # Top 5 sintomas e doenças
            top_sintomas = sorted(sintomas_mais_comuns.items(), key=lambda x: x[1], reverse=True)[:5]
            top_doencas = sorted(doencas_mais_diagnosticadas.items(), key=lambda x: x[1], reverse=True)[:5]
            
            return {
                'total_consultas': total_consultas,
                'pacientes_unicos': len(pacientes_unicos),
                'sintomas_personalizados': len(self.sintomas_personalizados),
                'top_sintomas': top_sintomas,
                'top_doencas': top_doencas
            }
            
        except Exception as e:
            logger.error(f"Erro ao calcular estatísticas: {e}")
            return {}
    
    def remover_sintoma_personalizado(self, sintoma: str) -> bool:
        """
        Remove um sintoma personalizado
        
        Args:
            sintoma (str): Sintoma a ser removido
            
        Returns:
            bool: True se removido com sucesso
        """
        try:
            if sintoma in self.sintomas_personalizados:
                self.sintomas_personalizados.remove(sintoma)
                self._salvar_sintomas_personalizados()
                logger.info(f"Sintoma personalizado removido: {sintoma}")
                return True
            return False
        except Exception as e:
            logger.error(f"Erro ao remover sintoma personalizado: {e}")
            return False

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