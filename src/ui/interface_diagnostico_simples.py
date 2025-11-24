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
        self.root.geometry("1200x800")  # Janela maior para melhor visualização
        self.root.minsize(900, 600)     # Tamanho mínimo
        self.root.configure(bg='#f0f0f0')
        
        # Maximizar a janela no início (opcional)
        # self.root.state('zoomed')  # Windows
        # self.root.attributes('-zoomed', True)  # Linux
        
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
        
        # Aba de consultas por paciente
        self.create_consultas_paciente_tab()
        
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
        
        # Frame esquerdo - Dados do paciente e sintomas com scroll
        left_canvas = tk.Canvas(main_frame, highlightthickness=0)
        left_scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=left_canvas.yview)
        left_scrollable_frame = ttk.Frame(left_canvas)
        
        left_scrollable_frame.bind(
            "<Configure>",
            lambda e: left_canvas.configure(scrollregion=left_canvas.bbox("all"))
        )
        
        left_canvas.create_window((0, 0), window=left_scrollable_frame, anchor="nw")
        left_canvas.configure(yscrollcommand=left_scrollbar.set)
        
        left_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        left_scrollbar.pack(side=tk.LEFT, fill=tk.Y)
        
        # Adicionar scroll com mouse
        def _on_mouse_wheel_left(event):
            left_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        left_canvas.bind("<MouseWheel>", _on_mouse_wheel_left)
        left_scrollable_frame.bind("<MouseWheel>", _on_mouse_wheel_left)
        
        # Usar left_scrollable_frame em vez de left_frame
        left_frame = left_scrollable_frame
        
        # Dados do Paciente - Layout melhorado
        dados_frame = ttk.LabelFrame(left_frame, text="👤 Dados do Paciente", padding=15)
        dados_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Configurar grid
        dados_frame.grid_columnconfigure(1, weight=1)
        dados_frame.grid_columnconfigure(3, weight=1)
        
        # Nome (linha completa)
        ttk.Label(dados_frame, text="Nome Completo:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.widgets['entry_nome'] = ttk.Entry(dados_frame, width=40)
        self.widgets['entry_nome'].grid(row=0, column=1, columnspan=3, sticky=tk.W+tk.E, padx=5, pady=2)
        
        # Linha 2: Idade e Bairro
        ttk.Label(dados_frame, text="Idade:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.widgets['entry_idade'] = ttk.Entry(dados_frame, width=10)
        self.widgets['entry_idade'].grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)
        
        ttk.Label(dados_frame, text="Bairro:").grid(row=1, column=2, sticky=tk.W, pady=5, padx=(15,5))
        self.widgets['entry_bairro'] = ttk.Entry(dados_frame, width=25)
        self.widgets['entry_bairro'].grid(row=1, column=3, sticky=tk.W+tk.E, padx=5, pady=5)
        
        # Linha 3: Tempo dos sintomas
        ttk.Label(dados_frame, text="🕐 Tempo dos sintomas:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.widgets['combo_tempo'] = ttk.Combobox(dados_frame, 
                                                   values=["Menos de 1 dia", "1-3 dias", "4-7 dias", 
                                                          "1-2 semanas", "2-4 semanas", "Mais de 1 mês"],
                                                   state="readonly", width=20)
        self.widgets['combo_tempo'].grid(row=2, column=1, columnspan=3, sticky=tk.W+tk.E, padx=5, pady=5)
        
        # Separador visual
        separator = ttk.Separator(dados_frame, orient='horizontal')
        separator.grid(row=3, column=0, columnspan=4, sticky=tk.W+tk.E, pady=10)
        
        # Botão de limpar dados
        limpar_frame = ttk.Frame(dados_frame)
        limpar_frame.grid(row=4, column=0, columnspan=4, pady=5)
        
        ttk.Button(limpar_frame, text="🗑️ Limpar Dados", 
                  command=self.limpar_dados_paciente).pack(side=tk.LEFT, padx=5)
        
        dados_frame.columnconfigure(1, weight=1)
        dados_frame.columnconfigure(3, weight=2)
        
        # Frame de Seleção de sintomas
        sintomas_frame = ttk.LabelFrame(left_frame, text=obter_texto_interface('selecionar_sintomas'), padding=10)
        sintomas_frame.pack(fill=tk.BOTH, expand=True)
        
        # Campo de busca e adição de sintomas
        search_frame = ttk.Frame(sintomas_frame)
        search_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(search_frame, text="Buscar sintoma:").pack(anchor=tk.W)
        
        search_input_frame = ttk.Frame(search_frame)
        search_input_frame.pack(fill=tk.X, pady=(5, 0))
        
        self.widgets['search_entry'] = ttk.Entry(search_input_frame)
        self.widgets['search_entry'].pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        self.widgets['search_entry'].bind('<KeyRelease>', self.on_search_change)
        
        ttk.Button(search_input_frame, text="+ Adicionar", 
                  command=self.adicionar_sintoma_personalizado).pack(side=tk.RIGHT)
        
        # Botão para gerenciar sintomas personalizados
        ttk.Button(search_frame, text="Gerenciar Sintomas Personalizados", 
                  command=self.abrir_gerenciador_sintomas).pack(pady=(5, 0))
        
        # Lista de sintomas
        list_frame = ttk.Frame(sintomas_frame)
        list_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Scrollbar para lista
        scrollbar_sintomas = ttk.Scrollbar(list_frame)
        scrollbar_sintomas.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.widgets['sintomas_listbox'] = tk.Listbox(list_frame, 
                                                     yscrollcommand=scrollbar_sintomas.set,
                                                     selectmode=tk.MULTIPLE)
        self.widgets['sintomas_listbox'].pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar_sintomas.config(command=self.widgets['sintomas_listbox'].yview)
        
        # Botões de ação - Melhor layout
        buttons_frame = ttk.Frame(sintomas_frame)
        buttons_frame.pack(fill=tk.X, pady=10)
        
        # Primeira linha
        buttons_row1 = ttk.Frame(buttons_frame)
        buttons_row1.pack(fill=tk.X, pady=(0, 5))
        
        ttk.Button(buttons_row1, 
                  text="✅ Adicionar Selecionados", 
                  command=self.adicionar_sintomas_selecionados).pack(side=tk.LEFT, padx=(0, 5))
        
        ttk.Button(buttons_row1, 
                  text="🗑️ Limpar Seleção", 
                  command=self.limpar_selecao_sintomas).pack(side=tk.LEFT)
        
        # Segunda linha
        buttons_row2 = ttk.Frame(buttons_frame)
        buttons_row2.pack(fill=tk.X)
        
        ttk.Button(buttons_row2, 
                  text="🔄 Atualizar Lista", 
                  command=self.carregar_sintomas).pack(side=tk.LEFT, padx=(0, 5))
        
        ttk.Button(buttons_row2, 
                  text="📋 Ver Personalizados", 
                  command=self.abrir_gerenciador_sintomas).pack(side=tk.LEFT)
        
        # Frame direito - Sintomas selecionados e resultados com scroll
        right_canvas = tk.Canvas(main_frame, highlightthickness=0)
        right_scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=right_canvas.yview)
        right_scrollable_frame = ttk.Frame(right_canvas)
        
        right_scrollable_frame.bind(
            "<Configure>",
            lambda e: right_canvas.configure(scrollregion=right_canvas.bbox("all"))
        )
        
        right_canvas.create_window((0, 0), window=right_scrollable_frame, anchor="nw")
        right_canvas.configure(yscrollcommand=right_scrollbar.set)
        
        right_canvas.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        right_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Adicionar scroll com mouse
        def _on_mouse_wheel_right(event):
            right_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        right_canvas.bind("<MouseWheel>", _on_mouse_wheel_right)
        right_scrollable_frame.bind("<MouseWheel>", _on_mouse_wheel_right)
        
        # Usar right_scrollable_frame em vez de right_frame
        right_frame = right_scrollable_frame
        
        # Armazenar canvas para uso posterior
        self.left_canvas = left_canvas
        self.right_canvas = right_canvas
        
        # Vincular scroll a todos os widgets após criação completa
        self.root.after(100, self._bind_scroll_to_widgets)
        
        # Sintomas selecionados
        selected_frame = ttk.LabelFrame(right_frame, text="Sintomas Selecionados", padding=10)
        selected_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.widgets['sintomas_selecionados_text'] = scrolledtext.ScrolledText(selected_frame, 
                                                                              height=4,  # Reduzido para economizar espaço
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
        self.widgets['resultados_text'].pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Botões para ações com consultas
        actions_frame = ttk.Frame(resultados_frame)
        actions_frame.pack(fill=tk.X)
        
        self.widgets['salvar_consulta_btn'] = ttk.Button(actions_frame, 
                                                        text="💾 Salvar Consulta", 
                                                        command=self.salvar_consulta_atual,
                                                        state=tk.DISABLED)
        self.widgets['salvar_consulta_btn'].pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(actions_frame, 
                  text="📄 Gerar Relatório", 
                  command=self.gerar_relatorio_consulta).pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(actions_frame, 
                  text="📧 Enviar por Email", 
                  command=self.enviar_consulta_email).pack(side=tk.LEFT)
    
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
    
    def create_consultas_paciente_tab(self):
        """Cria aba de consultas por paciente"""
        tab_consultas = ttk.Frame(self.notebook)
        self.notebook.add(tab_consultas, text="👤 Consultas por Paciente")
        
        main_frame = ttk.Frame(tab_consultas)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Título
        title_label = tk.Label(main_frame, 
                              text="Consultas por Paciente", 
                              font=("Arial", 16, "bold"),
                              fg="#2c3e50")
        title_label.pack(pady=(0, 20))
        
        # Frame para busca
        search_frame = ttk.LabelFrame(main_frame, text="Buscar Paciente", padding=15)
        search_frame.pack(fill=tk.X, pady=(0, 10))
        
        search_input_frame = ttk.Frame(search_frame)
        search_input_frame.pack(fill=tk.X)
        
        ttk.Label(search_input_frame, text="Nome do paciente:").pack(side=tk.LEFT, padx=(0, 10))
        self.widgets['entry_busca_paciente'] = ttk.Entry(search_input_frame, width=30)
        self.widgets['entry_busca_paciente'].pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(search_input_frame, 
                  text="🔍 Buscar", 
                  command=self.buscar_consultas_paciente).pack(side=tk.LEFT)
        
        # Frame para resultados
        resultados_frame = ttk.LabelFrame(main_frame, text="Consultas Encontradas", padding=15)
        resultados_frame.pack(fill=tk.BOTH, expand=True)
        
        self.widgets['consultas_paciente_text'] = scrolledtext.ScrolledText(resultados_frame, 
                                                                           wrap=tk.WORD,
                                                                           font=("Consolas", 10))
        self.widgets['consultas_paciente_text'].pack(fill=tk.BOTH, expand=True)
    
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
            sintomas = self.sistema.obter_todos_sintomas()
            
            self.widgets['sintomas_listbox'].delete(0, tk.END)
            for sintoma in sintomas:
                # Marcar sintomas personalizados com um asterisco
                if sintoma in self.sistema.sintomas_personalizados:
                    sintoma_display = f"{sintoma} *"
                else:
                    sintoma_display = sintoma
                self.widgets['sintomas_listbox'].insert(tk.END, sintoma_display)
                
            self.update_status(f"✅ {len(sintomas)} sintomas carregados ({len(self.sistema.sintomas_personalizados)} personalizados)")
            
        except Exception as e:
            logger.error(f"Erro ao carregar sintomas: {e}")
            self.update_status(f"❌ Erro ao carregar sintomas: {e}")
    
    def on_search_change(self, event):
        """Filtra sintomas baseado na busca"""
        search_term = self.widgets['search_entry'].get().lower()
        
        if not self.sistema:
            return
        
        sintomas = self.sistema.obter_todos_sintomas()
        
        # Filtrar sintomas
        if search_term:
            sintomas_filtrados = [s for s in sintomas if search_term in s.lower()]
        else:
            sintomas_filtrados = sintomas
        
        # Atualizar listbox
        self.widgets['sintomas_listbox'].delete(0, tk.END)
        for sintoma in sintomas_filtrados:
            # Marcar sintomas personalizados
            if sintoma in self.sistema.sintomas_personalizados:
                sintoma_display = f"{sintoma} *"
            else:
                sintoma_display = sintoma
            self.widgets['sintomas_listbox'].insert(tk.END, sintoma_display)
    
    def adicionar_sintomas_selecionados(self):
        """Adiciona sintomas selecionados à lista"""
        try:
            selected_indices = self.widgets['sintomas_listbox'].curselection()
            
            for index in selected_indices:
                sintoma = self.widgets['sintomas_listbox'].get(index)
                # Remover asterisco se for sintoma personalizado
                sintoma_limpo = sintoma.replace(' *', '')
                if sintoma_limpo not in self.sintomas_selecionados:
                    self.sintomas_selecionados.append(sintoma_limpo)
            
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
            
            # Realizar diagnóstico
            resultado = self.sistema.realizar_diagnostico(self.sintomas_selecionados)
            
            # Adicionar dados do paciente ao resultado
            # Adicionar dados do paciente ao resultado
            resultado['nome_paciente'] = self.widgets['entry_nome'].get()
            resultado['idade_paciente'] = self.widgets['entry_idade'].get()
            resultado['bairro_paciente'] = self.widgets['entry_bairro'].get()
            resultado['tempo_sintomas'] = self.widgets['combo_tempo'].get()
            
            # Armazenar consulta atual
            self.ultima_consulta = resultado
            
            # Mostrar resultado
            self.mostrar_resultado_diagnostico(resultado)
            
            # Habilitar botão de salvar
            self.widgets['salvar_consulta_btn'].configure(state=tk.NORMAL)
            
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
        
        # Dados do paciente
        if (resultado.get('nome_paciente') or resultado.get('idade_paciente') or 
            resultado.get('bairro_paciente') or resultado.get('tempo_sintomas')):
            text_widget.insert(tk.END, "👤 DADOS DO PACIENTE:\n")
            if resultado.get('nome_paciente'):
                text_widget.insert(tk.END, f"   • Nome: {resultado['nome_paciente']}\n")
            if resultado.get('idade_paciente'):
                text_widget.insert(tk.END, f"   • Idade: {resultado['idade_paciente']} anos\n")
            if resultado.get('bairro_paciente'):
                text_widget.insert(tk.END, f"   • Bairro: {resultado['bairro_paciente']}\n")
            if resultado.get('tempo_sintomas'):
                text_widget.insert(tk.END, f"   • Tempo dos sintomas: {resultado['tempo_sintomas']}\n")
            text_widget.insert(tk.END, "\n")
        
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
            stats_sistema = self.sistema.obter_estatisticas_sistema()
            stats_consultas = self.sistema.obter_estatisticas_consultas()
            
            text_widget = self.widgets['stats_text']
            text_widget.delete(1.0, tk.END)
            
            text_widget.insert(tk.END, "📊 ESTATÍSTICAS DO SISTEMA\n")
            text_widget.insert(tk.END, "=" * 50 + "\n\n")
            
            # Estatísticas do sistema
            text_widget.insert(tk.END, "🏥 DADOS DO SISTEMA:\n")
            for chave, valor in stats_sistema.items():
                if 'data' in chave.lower() or 'timestamp' in chave.lower():
                    if isinstance(valor, str) and 'T' in valor:
                        valor = valor[:19].replace('T', ' ')
                
                text_widget.insert(tk.END, f"• {chave.replace('_', ' ').title()}: {valor}\n")
            
            # Estatísticas de consultas
            text_widget.insert(tk.END, "\n👥 CONSULTAS REALIZADAS:\n")
            text_widget.insert(tk.END, f"• Total de consultas: {stats_consultas.get('total_consultas', 0)}\n")
            text_widget.insert(tk.END, f"• Pacientes únicos: {stats_consultas.get('pacientes_unicos', 0)}\n")
            text_widget.insert(tk.END, f"• Sintomas personalizados: {stats_consultas.get('sintomas_personalizados', 0)}\n")
            
            # Top sintomas
            top_sintomas = stats_consultas.get('top_sintomas', [])
            if top_sintomas:
                text_widget.insert(tk.END, "\n🔝 TOP 5 SINTOMAS MAIS COMUNS:\n")
                for i, (sintoma, count) in enumerate(top_sintomas, 1):
                    text_widget.insert(tk.END, f"  {i}. {sintoma}: {count} vezes\n")
            
            # Top doenças
            top_doencas = stats_consultas.get('top_doencas', [])
            if top_doencas:
                text_widget.insert(tk.END, "\n🏆 TOP 5 DIAGNÓSTICOS MAIS FREQUENTES:\n")
                for i, (doenca, count) in enumerate(top_doencas, 1):
                    text_widget.insert(tk.END, f"  {i}. {doenca}: {count} vezes\n")
            
            text_widget.insert(tk.END, f"\n⏰ Atualizado em: {datetime.now().strftime('%H:%M:%S')}\n")
            
        except Exception as e:
            logger.error(f"Erro ao atualizar estatísticas: {e}")
            messagebox.showerror("Erro", f"Erro ao atualizar estatísticas: {e}")
    
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

    
    def limpar_dados_paciente(self):
        """Limpa todos os dados do paciente"""
        self.widgets['entry_nome'].delete(0, tk.END)
        self.widgets['entry_idade'].delete(0, tk.END)
        self.widgets['entry_bairro'].delete(0, tk.END)
        self.widgets['combo_tempo'].set("")
        
        self.update_status("🗑️ Dados do paciente limpos")
    
    def salvar_consulta_atual(self):
        """Salva a consulta atual"""
        if not hasattr(self, 'ultima_consulta') or not self.ultima_consulta:
            messagebox.showwarning("Aviso", "Nenhuma consulta para salvar. Realize um diagnóstico primeiro.")
            return
        
        try:
            if self.sistema:
                # A consulta já foi salva automaticamente no sistema
                messagebox.showinfo("Sucesso", "Consulta salva com sucesso!\nPode ser consultada no histórico.")
                self.widgets['salvar_consulta_btn'].configure(state=tk.DISABLED)
                self.update_status("💾 Consulta salva")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar consulta: {e}")
    
    def gerar_relatorio_consulta(self):
        """Gera relatório da consulta atual"""
        if not hasattr(self, 'ultima_consulta') or not self.ultima_consulta:
            messagebox.showwarning("Aviso", "Nenhuma consulta para gerar relatório.")
            return
        
        try:
            # Criar janela de relatório
            relatorio_window = tk.Toplevel(self.root)
            relatorio_window.title("📄 Relatório da Consulta")
            relatorio_window.geometry("600x500")
            
            # Texto do relatório
            relatorio_text = scrolledtext.ScrolledText(relatorio_window, wrap=tk.WORD)
            relatorio_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            
            # Conteúdo do relatório
            conteudo = self._gerar_conteudo_relatorio()
            relatorio_text.insert(1.0, conteudo)
            relatorio_text.configure(state=tk.DISABLED)
            
            # Botões
            btn_frame = ttk.Frame(relatorio_window)
            btn_frame.pack(fill=tk.X, padx=10, pady=5)
            
            ttk.Button(btn_frame, text="💾 Salvar em Arquivo", 
                      command=lambda: self._salvar_relatorio_arquivo(conteudo)).pack(side=tk.LEFT, padx=5)
            
            ttk.Button(btn_frame, text="🖨️ Imprimir", 
                      command=lambda: self._imprimir_relatorio(conteudo)).pack(side=tk.LEFT, padx=5)
            
            ttk.Button(btn_frame, text="✖️ Fechar", 
                      command=relatorio_window.destroy).pack(side=tk.RIGHT, padx=5)
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao gerar relatório: {e}")
    
    def enviar_consulta_email(self):
        """Simula envio da consulta por email"""
        if not hasattr(self, 'ultima_consulta') or not self.ultima_consulta:
            messagebox.showwarning("Aviso", "Nenhuma consulta para enviar.")
            return
        
        # Janela para email
        email_window = tk.Toplevel(self.root)
        email_window.title("📧 Enviar Consulta por Email")
        email_window.geometry("400x250")
        
        # Campos de email
        ttk.Label(email_window, text="Email do destinatário:").pack(anchor=tk.W, padx=10, pady=5)
        entry_email = ttk.Entry(email_window, width=50)
        entry_email.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(email_window, text="Assunto:").pack(anchor=tk.W, padx=10, pady=5)
        entry_assunto = ttk.Entry(email_window, width=50)
        entry_assunto.insert(0, f"Consulta Médica - {self.widgets['entry_nome'].get()}")
        entry_assunto.pack(fill=tk.X, padx=10, pady=5)
        
        # Botões
        btn_frame = ttk.Frame(email_window)
        btn_frame.pack(fill=tk.X, padx=10, pady=20)
        
        def simular_envio():
            email = entry_email.get()
            if email:
                messagebox.showinfo("Simulação", f"Email simulado enviado para: {email}")
                email_window.destroy()
            else:
                messagebox.showwarning("Aviso", "Digite um email válido")
        
        ttk.Button(btn_frame, text="📧 Enviar", command=simular_envio).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="❌ Cancelar", command=email_window.destroy).pack(side=tk.RIGHT, padx=5)
    
    def _gerar_conteudo_relatorio(self):
        """Gera o conteúdo do relatório"""
        if not hasattr(self, 'ultima_consulta'):
            return "Nenhuma consulta disponível."
        
        consulta = self.ultima_consulta
        
        relatorio = f"""
RELATÓRIO DE CONSULTA MÉDICA
{'='*50}

DADOS DO PACIENTE:
• Nome: {consulta.get('nome_paciente', 'Não informado')}
• Idade: {consulta.get('idade_paciente', 'Não informada')}
• Bairro: {consulta.get('bairro_paciente', 'Não informado')}
• Tempo dos sintomas: {consulta.get('tempo_sintomas', 'Não informado')}

SINTOMAS REPORTADOS:
{chr(10).join([f'• {sintoma}' for sintoma in consulta.get('sintomas_entrada', [])])}

RESULTADOS DO DIAGNÓSTICO:
Total de possibilidades analisadas: {consulta.get('total_diagnosticos', 0)}
Confiabilidade geral: {consulta.get('confiabilidade_geral', 'Não calculada')}

TOP 3 DIAGNÓSTICOS:
"""
        
        for i, diag in enumerate(consulta.get('diagnosticos', []), 1):
            relatorio += f"""
{i}. {diag['doenca']}
   Probabilidade: {diag['probabilidade']:.1f}%
   Nível de confiança: {diag['nivel_confianca']}
   Sintomas em comum: {diag['sintomas_em_comum_count']}/{diag['total_sintomas_doenca']}
"""
        
        relatorio += f"""

OBSERVAÇÕES:
• Data da consulta: {consulta.get('timestamp', '')[:19].replace('T', ' ')}
• Este relatório é gerado automaticamente pelo sistema
• Sempre consulte um médico profissional para confirmação

AVISO IMPORTANTE:
Este sistema é apenas para fins educacionais e de apoio.
Não substitui a consulta médica profissional.
"""
        
        return relatorio
    
    def _salvar_relatorio_arquivo(self, conteudo):
        """Salva o relatório em arquivo"""
        try:
            from tkinter import filedialog
            nome_arquivo = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Arquivo de texto", "*.txt"), ("Todos os arquivos", "*.*")]
            )
            
            if nome_arquivo:
                with open(nome_arquivo, 'w', encoding='utf-8') as f:
                    f.write(conteudo)
                messagebox.showinfo("Sucesso", f"Relatório salvo em: {nome_arquivo}")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar arquivo: {e}")
    
    def _imprimir_relatorio(self, conteudo):
        """Simula impressão do relatório"""
        messagebox.showinfo("Simulação", "Função de impressão simulada.\nEm um sistema real, isso enviaria para a impressora.")
    
    def adicionar_sintoma_personalizado(self):
        """Adiciona sintoma digitado no campo de busca"""
        sintoma = self.widgets['search_entry'].get().strip()
        if sintoma and sintoma not in self.sintomas_selecionados:
            self.sintomas_selecionados.append(sintoma)
            self.atualizar_sintomas_selecionados_display()
            self.widgets['search_entry'].delete(0, tk.END)
            self.update_status(f"➕ Sintoma '{sintoma}' adicionado")
        elif sintoma in self.sintomas_selecionados:
            self.update_status(f"⚠️ Sintoma '{sintoma}' já foi selecionado")
        else:
            messagebox.showwarning("Aviso", "Digite um sintoma para adicionar")
    
    def adicionar_sintoma_personalizado(self):
        """Adiciona um sintoma personalizado"""
        sintoma = self.widgets['search_entry'].get().strip()
        
        if not sintoma:
            messagebox.showwarning("Aviso", "Digite um sintoma para adicionar.")
            return
        
        if self.sistema.adicionar_sintoma_personalizado(sintoma):
            messagebox.showinfo("Sucesso", f"Sintoma '{sintoma}' adicionado com sucesso!")
            self.widgets['search_entry'].delete(0, tk.END)
            self.carregar_sintomas()
        else:
            messagebox.showwarning("Aviso", f"Sintoma '{sintoma}' já existe na lista.")
    
    def abrir_gerenciador_sintomas(self):
        """Abre janela para gerenciar sintomas personalizados"""
        if not self.sistema.sintomas_personalizados:
            messagebox.showinfo("Informação", "Não há sintomas personalizados para gerenciar.")
            return
        
        # Criar janela de gerenciamento
        janela = tk.Toplevel(self.root)
        janela.title("Gerenciar Sintomas Personalizados")
        janela.geometry("400x300")
        janela.transient(self.root)
        janela.grab_set()
        
        # Lista de sintomas personalizados
        frame_lista = ttk.Frame(janela)
        frame_lista.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        ttk.Label(frame_lista, text="Sintomas Personalizados:", font=("Arial", 12, "bold")).pack(anchor=tk.W)
        
        # Listbox com scrollbar
        list_frame = ttk.Frame(frame_lista)
        list_frame.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
        
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        listbox_sintomas = tk.Listbox(list_frame, yscrollcommand=scrollbar.set)
        listbox_sintomas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=listbox_sintomas.yview)
        
        # Carregar sintomas personalizados
        for sintoma in self.sistema.sintomas_personalizados:
            listbox_sintomas.insert(tk.END, sintoma)
        
        # Botões
        buttons_frame = ttk.Frame(janela)
        buttons_frame.pack(fill=tk.X, padx=10, pady=10)
        
        def remover_sintoma():
            selection = listbox_sintomas.curselection()
            if not selection:
                messagebox.showwarning("Aviso", "Selecione um sintoma para remover.")
                return
            
            sintoma = listbox_sintomas.get(selection[0])
            if messagebox.askyesno("Confirmar", f"Remover sintoma '{sintoma}'?"):
                if self.sistema.remover_sintoma_personalizado(sintoma):
                    listbox_sintomas.delete(selection[0])
                    messagebox.showinfo("Sucesso", f"Sintoma '{sintoma}' removido!")
                    self.carregar_sintomas()
        
        ttk.Button(buttons_frame, text="Remover Selecionado", command=remover_sintoma).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(buttons_frame, text="Fechar", command=janela.destroy).pack(side=tk.RIGHT)
    
    def buscar_consultas_paciente(self):
        """Busca consultas de um paciente específico"""
        nome_paciente = self.widgets['entry_busca_paciente'].get().strip()
        
        if not nome_paciente:
            messagebox.showwarning("Aviso", "Digite o nome do paciente para buscar.")
            return
        
        try:
            consultas = self.sistema.obter_consultas_por_paciente(nome_paciente)
            
            text_widget = self.widgets['consultas_paciente_text']
            text_widget.delete(1.0, tk.END)
            
            if not consultas:
                text_widget.insert(tk.END, f"📋 Nenhuma consulta encontrada para '{nome_paciente}'.\n")
                return
            
            text_widget.insert(tk.END, f"👤 CONSULTAS DE {nome_paciente.upper()}\n")
            text_widget.insert(tk.END, f"Total de consultas: {len(consultas)}\n")
            text_widget.insert(tk.END, "=" * 60 + "\n\n")
            
            for i, consulta in enumerate(consultas, 1):
                timestamp = consulta['timestamp'][:19].replace('T', ' ')
                dados_paciente = consulta.get('dados_paciente', {})
                
                text_widget.insert(tk.END, f"{i}. Consulta realizada em {timestamp}\n")
                text_widget.insert(tk.END, f"   Idade: {dados_paciente.get('idade', 'N/A')}\n")
                text_widget.insert(tk.END, f"   Bairro: {dados_paciente.get('bairro', 'N/A')}\n")
                text_widget.insert(tk.END, f"   Tempo dos sintomas: {dados_paciente.get('tempo_sintomas', 'N/A')}\n")
                text_widget.insert(tk.END, f"   Sintomas: {', '.join(consulta.get('sintomas_entrada', []))}\n")
                text_widget.insert(tk.END, f"   Confiabilidade: {consulta.get('confiabilidade_geral', 'N/A')}\n")
                
                diagnosticos = consulta.get('diagnosticos', [])
                if diagnosticos:
                    text_widget.insert(tk.END, f"   Diagnósticos:\n")
                    for j, diag in enumerate(diagnosticos, 1):
                        emoji = "🔴" if diag['probabilidade'] >= 70 else "🟡" if diag['probabilidade'] >= 40 else "🟢"
                        text_widget.insert(tk.END, f"      {j}. {emoji} {diag['doenca']} - {diag['probabilidade']:.1f}%\n")
                
                text_widget.insert(tk.END, "\n" + "-" * 40 + "\n\n")
            
        except Exception as e:
            logger.error(f"Erro ao buscar consultas: {e}")
            messagebox.showerror("Erro", f"Erro ao buscar consultas: {e}")
    
    def update_status(self, message):
        """Atualiza barra de status"""
        self.widgets['status_bar'].config(text=message)
        self.root.update_idletasks()
    
    def _bind_scroll_to_widgets(self):
        """Vincula scroll do mouse a todos os widgets"""
        def bind_to_mousewheel(widget, canvas):
            def _on_mousewheel(event):
                try:
                    canvas.yview_scroll(int(-1*(event.delta/120)), "units")
                except:
                    # Para sistemas Linux
                    if event.num == 4:
                        canvas.yview_scroll(-1, "units")
                    elif event.num == 5:
                        canvas.yview_scroll(1, "units")
            
            widget.bind("<MouseWheel>", _on_mousewheel)  # Windows
            widget.bind("<Button-4>", _on_mousewheel)    # Linux
            widget.bind("<Button-5>", _on_mousewheel)    # Linux
        
        # Vincular todos os widgets do frame esquerdo
        def bind_all_children_left(widget):
            bind_to_mousewheel(widget, self.left_canvas)
            for child in widget.winfo_children():
                bind_all_children_left(child)
        
        # Vincular todos os widgets do frame direito  
        def bind_all_children_right(widget):
            bind_to_mousewheel(widget, self.right_canvas)
            for child in widget.winfo_children():
                bind_all_children_right(child)
        
        try:
            if hasattr(self, 'left_canvas'):
                bind_all_children_left(self.left_canvas)
            if hasattr(self, 'right_canvas'):
                bind_all_children_right(self.right_canvas)
        except Exception as e:
            logger.error(f"Erro ao vincular scroll: {e}")
    
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