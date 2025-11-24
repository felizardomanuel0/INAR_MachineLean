"""
Interface Gráfica Simplificada para Diagnóstico Médico
Funciona apenas com dados.csv
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import logging
from datetime import datetime
from typing import List, Dict
import pandas as pd
import os

# Importações dos módulos locais
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from models.sistema_diagnostico_simples import SistemaDiagnosticoSimples
try:
    from utils.traducoes import obter_texto_interface
except ImportError:
    def obter_texto_interface(chave):
        return chave

logger = logging.getLogger(__name__)

class InterfaceDiagnosticoSimples:
    """
    Interface gráfica simplificada para diagnóstico médico
    """
    
    def __init__(self):
        """Inicializa a interface"""
        self.root = tk.Tk()
        self.setup_window()
        
        # Sistema de diagnóstico
        self.sistema = None
        self.sintomas_selecionados = []
        
        # Elementos da interface
        self.widgets = {}
        
        self.setup_ui()
        self.inicializar_sistema()
        
    def setup_window(self):
        """Configura a janela principal"""
        self.root.title(f"{obter_texto_interface('titulo_principal')} - {obter_texto_interface('subtitulo')}")
        self.root.geometry("1000x700")
        self.root.configure(bg='#f0f0f0')
        
        # Centralizar janela
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def setup_ui(self):
        """Configura a interface do usuário"""
        # Notebook para abas
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Aba principal - Diagnóstico
        self.create_diagnostico_tab()
        
        # Aba de estatísticas
        self.create_estatisticas_tab()
        
        # Aba de histórico
        self.create_historico_tab()
        
        # Status bar
        self.create_status_bar()
    
    def create_diagnostico_tab(self):
        """Cria aba de diagnóstico"""
        tab_diagnostico = ttk.Frame(self.notebook)
        self.notebook.add(tab_diagnostico, text=obter_texto_interface('aba_diagnostico'))
        
        # Frame principal
        main_frame = ttk.Frame(tab_diagnostico)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Título
        title_label = tk.Label(main_frame, 
                              text=obter_texto_interface('titulo_principal'), 
                              font=("Arial", 16, "bold"),
                              fg="#2c3e50")
        title_label.pack(pady=(0, 20))
        
        # Frame esquerdo - Seleção de sintomas
        left_frame = ttk.LabelFrame(main_frame, text=obter_texto_interface('selecionar_sintomas'), padding=10)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Campo de busca
        search_frame = ttk.Frame(left_frame)
        search_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(search_frame, text="Buscar sintoma:").pack(anchor=tk.W)
        self.widgets['search_entry'] = ttk.Entry(search_frame)
        self.widgets['search_entry'].pack(fill=tk.X, pady=(5, 0))
        self.widgets['search_entry'].bind('<KeyRelease>', self.on_search_change)
        
        # Lista de sintomas
        list_frame = ttk.Frame(left_frame)
        list_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Scrollbar para lista
        scrollbar_sintomas = ttk.Scrollbar(list_frame)
        scrollbar_sintomas.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.widgets['sintomas_listbox'] = tk.Listbox(list_frame, 
                                                     yscrollcommand=scrollbar_sintomas.set,
                                                     selectmode=tk.MULTIPLE)
        self.widgets['sintomas_listbox'].pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar_sintomas.config(command=self.widgets['sintomas_listbox'].yview)
        
        # Botões de ação
        buttons_frame = ttk.Frame(left_frame)
        buttons_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(buttons_frame, 
                  text="Adicionar Selecionados", 
                  command=self.adicionar_sintomas_selecionados).pack(side=tk.LEFT, padx=(0, 5))
        
        ttk.Button(buttons_frame, 
                  text="Limpar Seleção", 
                  command=self.limpar_selecao_sintomas).pack(side=tk.LEFT)
        
        # Frame direito - Sintomas selecionados e resultados
        right_frame = ttk.Frame(main_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Sintomas selecionados
        selected_frame = ttk.LabelFrame(right_frame, text="Sintomas Selecionados", padding=10)
        selected_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.widgets['sintomas_selecionados_text'] = scrolledtext.ScrolledText(selected_frame, 
                                                                              height=6, 
                                                                              wrap=tk.WORD)
        self.widgets['sintomas_selecionados_text'].pack(fill=tk.BOTH, expand=True)
        
        # Botão de diagnóstico
        diagnostico_btn = ttk.Button(selected_frame, 
                                   text="🔍 Realizar Diagnóstico", 
                                   command=self.realizar_diagnostico,
                                   style="Accent.TButton")
        diagnostico_btn.pack(pady=10)
        
        # Resultados
        resultados_frame = ttk.LabelFrame(right_frame, text="Resultados do Diagnóstico", padding=10)
        resultados_frame.pack(fill=tk.BOTH, expand=True)
        
        self.widgets['resultados_text'] = scrolledtext.ScrolledText(resultados_frame, 
                                                                   wrap=tk.WORD,
                                                                   font=("Consolas", 10))
        self.widgets['resultados_text'].pack(fill=tk.BOTH, expand=True)
    
    def create_estatisticas_tab(self):
        """Cria aba de estatísticas"""
        tab_stats = ttk.Frame(self.notebook)
        self.notebook.add(tab_stats, text="📊 Estatísticas")
        
        main_frame = ttk.Frame(tab_stats)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Título
        title_label = tk.Label(main_frame, 
                              text="Estatísticas do Sistema", 
                              font=("Arial", 16, "bold"),
                              fg="#2c3e50")
        title_label.pack(pady=(0, 20))
        
        # Frame para estatísticas
        stats_frame = ttk.LabelFrame(main_frame, text="Informações do Sistema", padding=15)
        stats_frame.pack(fill=tk.BOTH, expand=True)
        
        self.widgets['stats_text'] = scrolledtext.ScrolledText(stats_frame, 
                                                              wrap=tk.WORD,
                                                              font=("Consolas", 11))
        self.widgets['stats_text'].pack(fill=tk.BOTH, expand=True)
        
        # Botão de atualizar
        ttk.Button(stats_frame, 
                  text="🔄 Atualizar Estatísticas", 
                  command=self.atualizar_estatisticas).pack(pady=10)
    
    def create_historico_tab(self):
        """Cria aba de histórico"""
        tab_historico = ttk.Frame(self.notebook)
        self.notebook.add(tab_historico, text="📋 Histórico")
        
        main_frame = ttk.Frame(tab_historico)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Título
        title_label = tk.Label(main_frame, 
                              text="Histórico de Diagnósticos", 
                              font=("Arial", 16, "bold"),
                              fg="#2c3e50")
        title_label.pack(pady=(0, 20))
        
        # Frame para histórico
        historico_frame = ttk.LabelFrame(main_frame, text="Diagnósticos Realizados", padding=15)
        historico_frame.pack(fill=tk.BOTH, expand=True)
        
        self.widgets['historico_text'] = scrolledtext.ScrolledText(historico_frame, 
                                                                  wrap=tk.WORD,
                                                                  font=("Consolas", 10))
        self.widgets['historico_text'].pack(fill=tk.BOTH, expand=True)
        
        # Botões
        buttons_frame = ttk.Frame(historico_frame)
        buttons_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(buttons_frame, 
                  text="🔄 Atualizar Histórico", 
                  command=self.atualizar_historico).pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(buttons_frame, 
                  text="🗑️ Limpar Histórico", 
                  command=self.limpar_historico).pack(side=tk.LEFT)
    
    def create_status_bar(self):
        """Cria barra de status"""
        self.widgets['status_bar'] = tk.Label(self.root, 
                                             text="Inicializando sistema...", 
                                             relief=tk.SUNKEN, 
                                             anchor=tk.W,
                                             bg="#ecf0f1",
                                             fg="#2c3e50")
        self.widgets['status_bar'].pack(side=tk.BOTTOM, fill=tk.X)
    
    def inicializar_sistema(self):
        """Inicializa o sistema de diagnóstico"""
        try:
            self.update_status("Carregando sistema de diagnóstico...")
            self.sistema = SistemaDiagnosticoSimples()
            
            if self.sistema.dados_carregados:
                self.carregar_sintomas()
                self.atualizar_estatisticas()
                self.update_status("Sistema carregado com sucesso!")
            else:
                self.update_status("❌ Erro ao carregar dados do sistema")
                messagebox.showerror("Erro", "Não foi possível carregar os dados do sistema.")
                
        except Exception as e:
            logger.error(f"Erro ao inicializar sistema: {e}")
            self.update_status(f"❌ Erro: {e}")
            messagebox.showerror("Erro", f"Erro ao inicializar sistema: {e}")
    
    def carregar_sintomas(self):
        """Carrega sintomas na listbox"""
        try:
            sintomas = self.sistema.obter_sintomas_disponiveis()
            
            self.widgets['sintomas_listbox'].delete(0, tk.END)
            for sintoma in sintomas:
                self.widgets['sintomas_listbox'].insert(tk.END, sintoma)
                
            self.update_status(f"✅ {len(sintomas)} sintomas carregados")
            
        except Exception as e:
            logger.error(f"Erro ao carregar sintomas: {e}")
            self.update_status(f"❌ Erro ao carregar sintomas: {e}")
    
    def on_search_change(self, event):
        """Filtra sintomas baseado na busca"""
        search_term = self.widgets['search_entry'].get().lower()
        
        if not self.sistema or not self.sistema.dados_carregados:
            return
        
        sintomas = self.sistema.obter_sintomas_disponiveis()
        
        # Filtrar sintomas
        if search_term:
            sintomas_filtrados = [s for s in sintomas if search_term in s.lower()]
        else:
            sintomas_filtrados = sintomas
        
        # Atualizar listbox
        self.widgets['sintomas_listbox'].delete(0, tk.END)
        for sintoma in sintomas_filtrados:
            self.widgets['sintomas_listbox'].insert(tk.END, sintoma)
    
    def adicionar_sintomas_selecionados(self):
        """Adiciona sintomas selecionados à lista"""
        try:
            selected_indices = self.widgets['sintomas_listbox'].curselection()
            
            for index in selected_indices:
                sintoma = self.widgets['sintomas_listbox'].get(index)
                if sintoma not in self.sintomas_selecionados:
                    self.sintomas_selecionados.append(sintoma)
            
            self.atualizar_sintomas_selecionados_display()
            self.update_status(f"✅ {len(selected_indices)} sintoma(s) adicionado(s)")
            
        except Exception as e:
            logger.error(f"Erro ao adicionar sintomas: {e}")
            messagebox.showerror("Erro", f"Erro ao adicionar sintomas: {e}")
    
    def limpar_selecao_sintomas(self):
        """Limpa seleção de sintomas"""
        self.sintomas_selecionados.clear()
        self.atualizar_sintomas_selecionados_display()
        self.update_status("Seleção de sintomas limpa")
    
    def atualizar_sintomas_selecionados_display(self):
        """Atualiza display de sintomas selecionados"""
        text_widget = self.widgets['sintomas_selecionados_text']
        text_widget.delete(1.0, tk.END)
        
        if self.sintomas_selecionados:
            for i, sintoma in enumerate(self.sintomas_selecionados, 1):
                text_widget.insert(tk.END, f"{i}. {sintoma}\n")
        else:
            text_widget.insert(tk.END, "Nenhum sintoma selecionado.")
    
    def realizar_diagnostico(self):
        """Realiza diagnóstico baseado nos sintomas selecionados"""
        if not self.sintomas_selecionados:
            messagebox.showwarning("Aviso", "Selecione pelo menos um sintoma para realizar o diagnóstico.")
            return
        
        try:
            self.update_status("Realizando diagnóstico...")
            
            resultado = self.sistema.realizar_diagnostico(self.sintomas_selecionados)
            
            # Mostrar resultado
            self.mostrar_resultado_diagnostico(resultado)
            
            # Atualizar histórico
            self.atualizar_historico()
            
            self.update_status("✅ Diagnóstico realizado com sucesso")
            
        except Exception as e:
            logger.error(f"Erro ao realizar diagnóstico: {e}")
            messagebox.showerror("Erro", f"Erro ao realizar diagnóstico: {e}")
            self.update_status(f"❌ Erro no diagnóstico: {e}")
    
    def mostrar_resultado_diagnostico(self, resultado):
        """Mostra resultado do diagnóstico"""
        text_widget = self.widgets['resultados_text']
        text_widget.delete(1.0, tk.END)
        
        if 'erro' in resultado:
            text_widget.insert(tk.END, f"❌ Erro: {resultado['erro']}\n")
            return
        
        # Cabeçalho
        text_widget.insert(tk.END, "🩺 RESULTADO DO DIAGNÓSTICO\n")
        text_widget.insert(tk.END, "=" * 50 + "\n\n")
        
        # Informações gerais
        text_widget.insert(tk.END, f"📊 Sintomas informados: {resultado['total_sintomas_entrada']}\n")
        text_widget.insert(tk.END, f"🔍 Possibilidades encontradas: {resultado['total_diagnosticos']}\n")
        text_widget.insert(tk.END, f"🎯 Confiabilidade geral: {resultado['confiabilidade_geral']}\n")
        text_widget.insert(tk.END, f"⏰ Data/Hora: {resultado['timestamp'][:19]}\n\n")
        
        # Sintomas informados
        text_widget.insert(tk.END, "📋 SINTOMAS INFORMADOS:\n")
        for i, sintoma in enumerate(resultado['sintomas_entrada'], 1):
            text_widget.insert(tk.END, f"  {i}. {sintoma}\n")
        
        text_widget.insert(tk.END, "\n")
        
        # Diagnósticos
        if resultado['diagnosticos']:
            text_widget.insert(tk.END, "🏥 TOP 3 DIAGNÓSTICOS MAIS PROVÁVEIS:\n")
            text_widget.insert(tk.END, "-" * 50 + "\n")
            
            for i, diag in enumerate(resultado['diagnosticos'], 1):
                # Emoji baseado na probabilidade
                if diag['probabilidade'] >= 70:
                    emoji = "🔴"  # Alta probabilidade
                elif diag['probabilidade'] >= 40:
                    emoji = "🟡"  # Média probabilidade
                else:
                    emoji = "🟢"  # Baixa probabilidade
                
                text_widget.insert(tk.END, f"\n{i}. {emoji} {diag['doenca']}\n")
                text_widget.insert(tk.END, f"   Probabilidade: {diag['probabilidade']:.1f}%\n")
                text_widget.insert(tk.END, f"   Nível de confiança: {diag['nivel_confianca']}\n")
                text_widget.insert(tk.END, f"   Sintomas em comum: {diag['sintomas_em_comum_count']}/{diag['total_sintomas_doenca']}\n")
                
                if diag['sintomas_comum']:
                    text_widget.insert(tk.END, f"   Sintomas coincidentes: {', '.join(diag['sintomas_comum'])}\n")
        else:
            text_widget.insert(tk.END, "⚠️ Nenhum diagnóstico encontrado com os sintomas informados.\n")
        
        # Disclaimer
        text_widget.insert(tk.END, "\n" + "⚠️" * 50 + "\n")
        text_widget.insert(tk.END, "IMPORTANTE: Este é um sistema de apoio ao diagnóstico.\n")
        text_widget.insert(tk.END, "Sempre consulte um médico profissional para\n")
        text_widget.insert(tk.END, "confirmação e tratamento adequado.\n")
        text_widget.insert(tk.END, "⚠️" * 50 + "\n")
    
    def atualizar_estatisticas(self):
        """Atualiza estatísticas do sistema"""
        if not self.sistema:
            return
        
        try:
            stats = self.sistema.obter_estatisticas_sistema()
            
            text_widget = self.widgets['stats_text']
            text_widget.delete(1.0, tk.END)
            
            text_widget.insert(tk.END, "📊 ESTATÍSTICAS DO SISTEMA\n")
            text_widget.insert(tk.END, "=" * 50 + "\n\n")
            
            for chave, valor in stats.items():
                # Formatação especial para algumas chaves
                if 'data' in chave.lower() or 'timestamp' in chave.lower():
                    if isinstance(valor, str) and 'T' in valor:
                        valor = valor[:19].replace('T', ' ')
                
                text_widget.insert(tk.END, f"• {chave.replace('_', ' ').title()}: {valor}\n")
            
            text_widget.insert(tk.END, f"\n⏰ Atualizado em: {datetime.now().strftime('%H:%M:%S')}\n")
            
        except Exception as e:
            logger.error(f"Erro ao atualizar estatísticas: {e}")
    
    def atualizar_historico(self):
        """Atualiza histórico de diagnósticos"""
        if not self.sistema:
            return
        
        try:
            historico = self.sistema.obter_historico_diagnosticos()
            
            text_widget = self.widgets['historico_text']
            text_widget.delete(1.0, tk.END)
            
            if not historico:
                text_widget.insert(tk.END, "📋 Nenhum diagnóstico realizado ainda.\n")
                return
            
            text_widget.insert(tk.END, f"📋 HISTÓRICO DE DIAGNÓSTICOS ({len(historico)} registros)\n")
            text_widget.insert(tk.END, "=" * 60 + "\n\n")
            
            for i, diag in enumerate(reversed(historico), 1):
                timestamp = diag['timestamp'][:19].replace('T', ' ')
                
                text_widget.insert(tk.END, f"{i}. Diagnóstico realizado em {timestamp}\n")
                text_widget.insert(tk.END, f"   Sintomas: {len(diag['sintomas_entrada'])}\n")
                text_widget.insert(tk.END, f"   Resultados: {diag['total_diagnosticos']}\n")
                text_widget.insert(tk.END, f"   Confiabilidade: {diag['confiabilidade_geral']}\n")
                
                if diag['diagnosticos']:
                    melhor = diag['diagnosticos'][0]
                    text_widget.insert(tk.END, f"   Melhor resultado: {melhor['doenca']} ({melhor['probabilidade']:.1f}%)\n")
                
                text_widget.insert(tk.END, "\n")
            
        except Exception as e:
            logger.error(f"Erro ao atualizar histórico: {e}")
    
    def limpar_historico(self):
        """Limpa histórico de diagnósticos"""
        if messagebox.askyesno("Confirmar", "Deseja realmente limpar todo o histórico?"):
            if self.sistema:
                self.sistema.limpar_historico()
                self.atualizar_historico()
                self.update_status("✅ Histórico limpo")
    
    def update_status(self, message):
        """Atualiza barra de status"""
        self.widgets['status_bar'].config(text=message)
        self.root.update_idletasks()
    
    def run(self):
        """Executa a aplicação"""
        try:
            logger.info("Iniciando interface gráfica")
            self.root.mainloop()
        except Exception as e:
            logger.error(f"Erro na interface: {e}")
            messagebox.showerror("Erro Fatal", f"Erro na interface: {e}")

def main():
    """Função principal"""
    # Configurar logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    try:
        app = InterfaceDiagnosticoSimples()
        app.run()
    except Exception as e:
        print(f"Erro ao iniciar aplicação: {e}")

if __name__ == "__main__":
    main()