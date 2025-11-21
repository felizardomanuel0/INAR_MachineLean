"""
Interface Gráfica Principal em Português - Sistema de Diagnóstico
Projeto Final INAR - Terceiro Ano, II Semestre

Sistema completo de diagnóstico médico com:
- Interface totalmente em português
- Múltiplos sintomas com entrada manual
- Duração e intensidade dos sintomas  
- Diagnóstico de doenças específicas
- Tradução automática de resultados
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
import os
import sys
import pandas as pd
import joblib
from typing import Dict, List
import threading
from datetime import datetime

# Adicionar paths dos módulos
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(os.path.join(BASE_DIR, 'src', 'utils'))

# Importar módulos de tradução e sistema atualizado
from traducao_doencas import traduzir_doenca_para_portugues, obter_todas_doencas_portugues
from sintomas_portugues import (
    SINTOMAS_DISPONIVEIS, 
    obter_sintomas_principais,
    DURACAO_SINTOMAS,
    INTENSIDADE_SINTOMAS,
    traduzir_sintoma_para_ingles,
    validar_sintoma_personalizado,
    normalizar_sintoma
)

# Importar novo sistema de diagnóstico
sys.path.append(os.path.join(BASE_DIR, 'src', 'models'))
from sistema_diagnostico_atualizado import SistemaDiagnosticoAtualizado

class SistemaDiagnosticoPortugues:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🏥 Sistema de Diagnóstico Médico - INAR (Atualizado)")
        
        # Configurar janela para ser redimensionável
        self.root.geometry("1600x900")
        self.root.minsize(1200, 700)
        self.root.resizable(True, True)
        
        # Permitir maximizar/minimizar
        self.root.state('normal')  # Permite maximizar
        
        # Inicializar novo sistema de diagnóstico
        self.sistema_diagnostico = SistemaDiagnosticoAtualizado()
        
        # Configurar ícone da janela (se disponível)
        try:
            # Tentar definir um ícone se houver um disponível
            self.root.iconname("🏥 Diagnóstico")
        except:
            pass
        
        # Centralizar janela na tela
        self.centralizar_janela()
        
        # Adicionar teclas de atalho
        self.configurar_atalhos()
        
        # Variáveis de controle
        self.modelo_carregado = None
        self.preprocessador = None
        self.sintomas_selecionados = {}
        self.sintomas_personalizados = []
        
        # Configurar diretórios de salvamento
        self.configurar_diretorios_salvamento()
        
        # Configurar estilos
        self.configurar_estilos()
        
        # Configurar interface
        self.configurar_interface()
        
        # Tentar carregar modelo automaticamente
        self.tentar_carregar_modelo_automatico()
    
    def centralizar_janela(self):
        """Centraliza a janela na tela"""
        self.root.update_idletasks()
        
        # Obter dimensões da tela
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        # Obter dimensões da janela
        window_width = 1600
        window_height = 900
        
        # Calcular posição central
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        
        # Aplicar posição
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
    
    def configurar_diretorios_salvamento(self):
        """Configura diretórios para salvamento de consultas"""
        # Diretório principal das consultas
        self.dir_consultas = os.path.join(BASE_DIR, 'consultas_salvas')
        os.makedirs(self.dir_consultas, exist_ok=True)
        
        # Subdiretórios por categoria
        self.dir_relatorios = os.path.join(self.dir_consultas, 'relatorios')
        self.dir_historico = os.path.join(self.dir_consultas, 'historico')
        self.dir_backup = os.path.join(self.dir_consultas, 'backup')
        
        # Criar subdiretórios
        for diretorio in [self.dir_relatorios, self.dir_historico, self.dir_backup]:
            os.makedirs(diretorio, exist_ok=True)
        
        # Arquivo de histórico geral
        self.arquivo_historico = os.path.join(self.dir_historico, 'historico_geral.csv')
        
        # Criar arquivo de histórico se não existir
        if not os.path.exists(self.arquivo_historico):
            self.criar_arquivo_historico()
    
    def criar_arquivo_historico(self):
        """Cria arquivo CSV para histórico de consultas"""
        import csv
        
        cabecalho = [
            'Data_Hora', 'Nome_Paciente', 'Idade', 'Genero', 
            'Sintomas_Principais', 'Sintomas_Extras', 'Duracao', 'Intensidade',
            'Pressao_Arterial', 'Colesterol', 'Diagnostico', 'Confianca',
            'Arquivo_Relatorio'
        ]
        
        with open(self.arquivo_historico, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f, delimiter=';')
            writer.writerow(cabecalho)
    
    def configurar_atalhos(self):
        """Configura atalhos de teclado"""
        # Atalhos globais
        self.root.bind('<Control-q>', lambda e: self.on_closing())  # Ctrl+Q para sair
        self.root.bind('<F11>', self.toggle_fullscreen)  # F11 para tela cheia
        self.root.bind('<Escape>', self.exit_fullscreen)  # ESC para sair da tela cheia
        self.root.bind('<Control-l>', lambda e: self.limpar_todos_campos())  # Ctrl+L para limpar
        self.root.bind('<Control-s>', lambda e: self.salvar_rapido_atalho())  # Ctrl+S para salvar rápido
        
        # Atalho para diagnóstico
        self.root.bind('<F5>', lambda e: self.realizar_diagnostico())  # F5 para diagnosticar
        
        # Atalhos para navegar entre abas
        self.root.bind('<Control-1>', lambda e: self.notebook.select(0))  # Ctrl+1 - Diagnóstico
        self.root.bind('<Control-2>', lambda e: self.notebook.select(1))  # Ctrl+2 - Treinamento  
        self.root.bind('<Control-3>', lambda e: self.notebook.select(2))  # Ctrl+3 - Resultados
        self.root.bind('<Control-4>', lambda e: self.notebook.select(3))  # Ctrl+4 - Sobre
    
    def toggle_fullscreen(self, event=None):
        """Alterna entre tela cheia e janela normal"""
        current_state = self.root.attributes('-fullscreen')
        self.root.attributes('-fullscreen', not current_state)
        
        if not current_state:
            # Entrando em tela cheia
            self.root.configure(bg='white')
        else:
            # Saindo de tela cheia
            self.root.configure(bg='SystemButtonFace')
    
    def exit_fullscreen(self, event=None):
        """Sai do modo tela cheia"""
        self.root.attributes('-fullscreen', False)
        self.root.configure(bg='SystemButtonFace')
    
    def configurar_estilos(self):
        """Configura os estilos da interface"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Estilos para títulos
        style.configure('Title.TLabel', font=('Arial', 18, 'bold'), foreground='#2c3e50')
        style.configure('Subtitle.TLabel', font=('Arial', 14, 'bold'), foreground='#34495e')
        style.configure('Header.TLabel', font=('Arial', 12, 'bold'), foreground='#2980b9')
        
        # Estilos para botões
        style.configure('Primary.TButton', font=('Arial', 11, 'bold'))
        style.configure('Success.TButton', font=('Arial', 10, 'bold'))
        style.configure('Warning.TButton', font=('Arial', 10, 'bold'))
        
        # Estilos para status
        style.configure('Success.TLabel', foreground='#27ae60', font=('Arial', 10, 'bold'))
        style.configure('Error.TLabel', foreground='#e74c3c', font=('Arial', 10, 'bold'))
        style.configure('Warning.TLabel', foreground='#f39c12', font=('Arial', 10, 'bold'))
        style.configure('Info.TLabel', foreground='#3498db', font=('Arial', 10))
    
    def configurar_interface(self):
        """Configura a interface principal"""
        # Frame principal
        main_frame = ttk.Frame(self.root, padding=15)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Cabeçalho
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        titulo = ttk.Label(header_frame, text="🏥 Sistema de Diagnóstico Médico", style='Title.TLabel')
        titulo.pack()
        
        subtitulo = ttk.Label(header_frame, text="Projeto Final INAR • Diagnóstico Inteligente com Machine Learning", 
                             style='Info.TLabel')
        subtitulo.pack(pady=(5, 0))
        
        # Criar notebook (abas)
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Criar abas
        self.criar_aba_diagnostico()
        self.criar_aba_treinamento() 
        self.criar_aba_resultados()
        self.criar_aba_sobre()
        
        # Criar barra de status
        self.criar_barra_status()
    
    def criar_aba_diagnostico(self):
        """Cria a aba principal de diagnóstico"""
        aba_diagnostico = ttk.Frame(self.notebook)
        self.notebook.add(aba_diagnostico, text="🩺 Diagnóstico")
        
        # Criar um frame principal dividido em duas colunas
        main_container = ttk.Frame(aba_diagnostico)
        main_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Configurar grid com duas colunas
        main_container.columnconfigure(0, weight=3, minsize=700)  # Coluna esquerda (formulário)
        main_container.columnconfigure(1, weight=2, minsize=600)  # Coluna direita (resultado)
        main_container.rowconfigure(0, weight=1)
        
        # === COLUNA ESQUERDA: FORMULÁRIO ===
        frame_esquerdo = ttk.Frame(main_container)
        frame_esquerdo.grid(row=0, column=0, sticky="nsew", padx=(0, 5))
        
        # Criar canvas e scrollbar para a coluna esquerda
        self.canvas_diagnostico = tk.Canvas(frame_esquerdo, highlightthickness=0)
        scrollbar_vert = ttk.Scrollbar(frame_esquerdo, orient="vertical", command=self.canvas_diagnostico.yview)
        
        # Frame scrollável que conterá todo o conteúdo do formulário
        self.frame_scrollavel = ttk.Frame(self.canvas_diagnostico)
        
        # Configurar scroll
        self.frame_scrollavel.bind(
            "<Configure>",
            lambda e: self.canvas_diagnostico.configure(scrollregion=self.canvas_diagnostico.bbox("all"))
        )
        
        # Criar janela no canvas
        self.canvas_window = self.canvas_diagnostico.create_window((0, 0), window=self.frame_scrollavel, anchor="nw")
        
        # Configurar canvas
        self.canvas_diagnostico.configure(yscrollcommand=scrollbar_vert.set)
        
        # Bind para redimensionamento
        self.canvas_diagnostico.bind('<Configure>', self.on_canvas_configure)
        
        # Layout do container esquerdo
        self.canvas_diagnostico.pack(side="left", fill="both", expand=True)
        scrollbar_vert.pack(side="right", fill="y")
        
        # Bind do mouse wheel para scroll
        self.bind_mousewheel(self.canvas_diagnostico)
        
        # Layout principal do conteúdo do formulário
        main_content = ttk.Frame(self.frame_scrollavel, padding=15)
        main_content.pack(fill=tk.BOTH, expand=True)
        
        # === COLUNA DIREITA: RESULTADO ===
        frame_direito = ttk.Frame(main_container)
        frame_direito.grid(row=0, column=1, sticky="nsew", padx=(5, 0))
        
        # Frame de resultado
        resultado_frame = ttk.LabelFrame(frame_direito, text="📋 Resultado do Diagnóstico", padding=15)
        resultado_frame.pack(fill=tk.BOTH, expand=True)
        
        # Área de resultado com scroll
        self.text_resultado = scrolledtext.ScrolledText(resultado_frame, 
                                                       font=('Consolas', 10), 
                                                       state=tk.DISABLED,
                                                       wrap=tk.WORD)
        self.text_resultado.pack(fill=tk.BOTH, expand=True)
        
        # === SEÇÃO 1: STATUS DO MODELO ===
        status_frame = ttk.LabelFrame(main_content, text="📊 Status do Sistema", padding=15)
        status_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.label_status_modelo = ttk.Label(status_frame, text="❌ Nenhum modelo carregado", style='Error.TLabel')
        self.label_status_modelo.pack(anchor=tk.W)
        
        btn_carregar_modelo = ttk.Button(status_frame, text="📂 Carregar Modelo Salvo", 
                                        command=self.carregar_modelo)
        btn_carregar_modelo.pack(anchor=tk.W, pady=(10, 0))
        
        # === SEÇÃO 2: DADOS DO PACIENTE ===
        dados_frame = ttk.LabelFrame(main_content, text="👤 Dados do Paciente", padding=15)
        dados_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Linha 1: Nome e Idade
        linha1 = ttk.Frame(dados_frame)
        linha1.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(linha1, text="Nome do Paciente:", font=('Arial', 10, 'bold')).pack(side=tk.LEFT)
        self.entry_nome = ttk.Entry(linha1, width=25, font=('Arial', 10))
        self.entry_nome.pack(side=tk.LEFT, padx=(10, 20))
        
        ttk.Label(linha1, text="Idade:", font=('Arial', 10, 'bold')).pack(side=tk.LEFT)
        self.entry_idade = ttk.Entry(linha1, width=8, font=('Arial', 10))
        self.entry_idade.pack(side=tk.LEFT, padx=(10, 0))
        
        # Linha 2: Gênero e Dados Clínicos
        linha2 = ttk.Frame(dados_frame)
        linha2.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(linha2, text="Gênero:", font=('Arial', 10, 'bold')).pack(side=tk.LEFT)
        self.combo_genero = ttk.Combobox(linha2, values=["Masculino", "Feminino"], state="readonly", width=12)
        self.combo_genero.pack(side=tk.LEFT, padx=(10, 20))
        
        ttk.Label(linha2, text="Pressão Arterial:", font=('Arial', 10, 'bold')).pack(side=tk.LEFT)
        self.combo_pressao = ttk.Combobox(linha2, values=["Baixa", "Normal", "Alta"], state="readonly", width=12)
        self.combo_pressao.pack(side=tk.LEFT, padx=(10, 20))
        
        ttk.Label(linha2, text="Colesterol:", font=('Arial', 10, 'bold')).pack(side=tk.LEFT)
        self.combo_colesterol = ttk.Combobox(linha2, values=["Baixo", "Normal", "Alto"], state="readonly", width=12)
        self.combo_colesterol.pack(side=tk.LEFT, padx=(10, 0))
        
        # === SEÇÃO 3: SINTOMAS PRINCIPAIS ===
        sintomas_frame = ttk.LabelFrame(main_content, text="🔍 Sintomas Principais", padding=15)
        sintomas_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Instrução
        ttk.Label(sintomas_frame, text="Selecione os sintomas que o paciente apresenta:", 
                 font=('Arial', 10, 'italic')).pack(anchor=tk.W, pady=(0, 10))
        
        # Frame para checkboxes dos sintomas principais
        self.frame_sintomas = ttk.Frame(sintomas_frame)
        self.frame_sintomas.pack(fill=tk.X)
        
        self.vars_sintomas = {}
        sintomas_principais = obter_sintomas_principais()
        
        # Organizar em 2 colunas
        for i, sintoma in enumerate(sintomas_principais):
            var = tk.BooleanVar()
            self.vars_sintomas[sintoma] = var
            
            cb = ttk.Checkbutton(self.frame_sintomas, text=sintoma, variable=var,
                               command=lambda s=sintoma: self.on_sintoma_change(s))
            cb.grid(row=i//2, column=i%2, sticky=tk.W, padx=10, pady=5)
        
        # === SEÇÃO 4: SINTOMAS ADICIONAIS ===
        sintomas_extra_frame = ttk.LabelFrame(main_content, text="➕ Sintomas Adicionais", padding=15)
        sintomas_extra_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Seleção de sintomas da lista completa
        lista_frame = ttk.Frame(sintomas_extra_frame)
        lista_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(lista_frame, text="Outros sintomas (selecione da lista):", font=('Arial', 10, 'bold')).pack(anchor=tk.W)
        
        # Combobox com todos os sintomas
        self.combo_sintomas_extra = ttk.Combobox(lista_frame, values=SINTOMAS_DISPONIVEIS, 
                                                state="readonly", width=40)
        self.combo_sintomas_extra.pack(side=tk.LEFT, padx=(0, 10), pady=(5, 0))
        
        btn_adicionar_lista = ttk.Button(lista_frame, text="➕ Adicionar da Lista", 
                                        command=self.adicionar_sintoma_lista)
        btn_adicionar_lista.pack(side=tk.LEFT, pady=(5, 0))
        
        # Entrada manual de sintomas
        manual_frame = ttk.Frame(sintomas_extra_frame)
        manual_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Label(manual_frame, text="Ou digite sintoma personalizado:", font=('Arial', 10, 'bold')).pack(anchor=tk.W)
        
        entrada_frame = ttk.Frame(manual_frame)
        entrada_frame.pack(fill=tk.X, pady=(5, 0))
        
        self.entry_sintoma_manual = ttk.Entry(entrada_frame, width=40)
        self.entry_sintoma_manual.pack(side=tk.LEFT, padx=(0, 10))
        
        # Adicionar placeholder manualmente
        self.entry_sintoma_manual.insert(0, "Ex: Dor no estômago, coceira...")
        self.entry_sintoma_manual.bind('<FocusIn>', self.on_entry_focus_in)
        self.entry_sintoma_manual.bind('<FocusOut>', self.on_entry_focus_out)
        
        btn_adicionar_manual = ttk.Button(entrada_frame, text="➕ Adicionar Sintoma", 
                                         command=self.adicionar_sintoma_manual)
        btn_adicionar_manual.pack(side=tk.LEFT)
        
        # Lista de sintomas adicionados
        self.frame_sintomas_adicionados = ttk.LabelFrame(sintomas_extra_frame, text="Sintomas Adicionados", padding=10)
        self.frame_sintomas_adicionados.pack(fill=tk.X, pady=(15, 0))
        
        self.text_sintomas_adicionados = tk.Text(self.frame_sintomas_adicionados, height=3, 
                                                font=('Arial', 9), state=tk.DISABLED)
        self.text_sintomas_adicionados.pack(fill=tk.X)
        
        # === SEÇÃO 5: DURAÇÃO E INTENSIDADE ===
        tempo_frame = ttk.LabelFrame(main_content, text="⏰ Informações Temporais", padding=15)
        tempo_frame.pack(fill=tk.X, pady=(0, 15))
        
        tempo_linha1 = ttk.Frame(tempo_frame)
        tempo_linha1.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(tempo_linha1, text="Há quanto tempo sente os sintomas:", font=('Arial', 10, 'bold')).pack(side=tk.LEFT)
        self.combo_duracao = ttk.Combobox(tempo_linha1, values=DURACAO_SINTOMAS, state="readonly", width=20)
        self.combo_duracao.pack(side=tk.LEFT, padx=(10, 0))
        
        tempo_linha2 = ttk.Frame(tempo_frame)
        tempo_linha2.pack(fill=tk.X)
        
        ttk.Label(tempo_linha2, text="Intensidade geral dos sintomas:", font=('Arial', 10, 'bold')).pack(side=tk.LEFT)
        self.combo_intensidade = ttk.Combobox(tempo_linha2, values=INTENSIDADE_SINTOMAS, state="readonly", width=20)
        self.combo_intensidade.pack(side=tk.LEFT, padx=(10, 0))
        
        # === SEÇÃO 6: BOTÕES DE AÇÃO ===
        acoes_frame = ttk.Frame(main_content, padding=15)
        acoes_frame.pack(fill=tk.X, pady=(15, 0))
        
        # Linha de botões
        btn_frame = ttk.Frame(acoes_frame)
        btn_frame.pack()
        
        self.btn_diagnosticar = ttk.Button(btn_frame, text="🔍 Realizar Diagnóstico", 
                                          command=self.realizar_diagnostico, style='Primary.TButton')
        self.btn_diagnosticar.pack(side=tk.LEFT, padx=(0, 15))
        
        btn_limpar = ttk.Button(btn_frame, text="🗑️ Limpar Tudo", command=self.limpar_todos_campos)
        btn_limpar.pack(side=tk.LEFT, padx=(0, 15))
        
        btn_salvar = ttk.Button(btn_frame, text="💾 Salvar Consulta", command=self.salvar_consulta)
        btn_salvar.pack(side=tk.LEFT, padx=(0, 15))
        
        btn_historico = ttk.Button(btn_frame, text="📊 Ver Histórico", command=self.visualizar_historico_consultas)
        btn_historico.pack(side=tk.LEFT)
    
    def criar_aba_treinamento(self):
        """Cria a aba de treinamento"""
        aba_treinamento = ttk.Frame(self.notebook)
        self.notebook.add(aba_treinamento, text="🤖 Treinamento")
        
        frame_principal = ttk.Frame(aba_treinamento, padding=20)
        frame_principal.pack(fill=tk.BOTH, expand=True)
        
        # Título
        titulo = ttk.Label(frame_principal, text="🤖 Treinamento de Modelos de Machine Learning", 
                          style='Subtitle.TLabel')
        titulo.pack(pady=(0, 20))
        
        # Dataset
        dataset_frame = ttk.LabelFrame(frame_principal, text="📂 Base de Dados", padding=15)
        dataset_frame.pack(fill=tk.X, pady=(0, 15))
        
        ttk.Label(dataset_frame, text="Arquivo CSV:").pack(anchor=tk.W)
        
        arquivo_frame = ttk.Frame(dataset_frame)
        arquivo_frame.pack(fill=tk.X, pady=(5, 0))
        
        self.entry_dataset = ttk.Entry(arquivo_frame, state="readonly", font=('Arial', 10))
        self.entry_dataset.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        btn_selecionar_dataset = ttk.Button(arquivo_frame, text="📁 Selecionar Conjunto de Dados", 
                                           command=self.selecionar_dataset)
        btn_selecionar_dataset.pack(side=tk.RIGHT)
        
        # Opções de treinamento
        opcoes_frame = ttk.LabelFrame(frame_principal, text="⚙️ Configurações de Treinamento", padding=15)
        opcoes_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Configurações em grid
        ttk.Label(opcoes_frame, text="Porcentagem para teste:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.scale_teste = ttk.Scale(opcoes_frame, from_=10, to=40, orient=tk.HORIZONTAL, length=200)
        self.scale_teste.set(20)
        self.scale_teste.grid(row=0, column=1, padx=10, pady=5)
        
        self.label_percent = ttk.Label(opcoes_frame, text="20%")
        self.label_percent.grid(row=0, column=2, pady=5)
        
        self.scale_teste.configure(command=lambda v: self.label_percent.configure(text=f"{int(float(v))}%"))
        
        # Grid Search
        self.var_grid_search = tk.BooleanVar(value=True)
        cb_grid = ttk.Checkbutton(opcoes_frame, text="Usar otimização avançada (Grid Search - mais lento)", 
                                 variable=self.var_grid_search)
        cb_grid.grid(row=1, column=0, columnspan=3, sticky=tk.W, pady=(10, 0))
        
        # Botões de controle
        controle_frame = ttk.Frame(frame_principal)
        controle_frame.pack(fill=tk.X, pady=(15, 0))
        
        self.btn_iniciar_treino = ttk.Button(controle_frame, text="🚀 Iniciar Treinamento", 
                                            command=self.iniciar_treinamento, style='Primary.TButton')
        self.btn_iniciar_treino.pack(side=tk.LEFT, padx=(0, 15))
        
        btn_parar = ttk.Button(controle_frame, text="⏹️ Parar", command=self.parar_treinamento)
        btn_parar.pack(side=tk.LEFT)
        
        # Progress bar
        self.progress_treino = ttk.Progressbar(frame_principal, mode='indeterminate')
        self.progress_treino.pack(fill=tk.X, pady=(20, 0))
        
        # Log do treinamento
        log_frame = ttk.LabelFrame(frame_principal, text="📊 Log do Treinamento", padding=10)
        log_frame.pack(fill=tk.BOTH, expand=True, pady=(15, 0))
        
        self.text_log_treino = scrolledtext.ScrolledText(log_frame, height=12, 
                                                        font=('Consolas', 9), state=tk.DISABLED)
        self.text_log_treino.pack(fill=tk.BOTH, expand=True)
    
    def criar_aba_resultados(self):
        """Cria a aba de resultados e histórico"""
        aba_resultados = ttk.Frame(self.notebook)
        self.notebook.add(aba_resultados, text="📈 Resultados")
        
        frame_principal = ttk.Frame(aba_resultados, padding=20)
        frame_principal.pack(fill=tk.BOTH, expand=True)
        
        titulo = ttk.Label(frame_principal, text="📈 Histórico de Diagnósticos e Estatísticas", 
                          style='Subtitle.TLabel')
        titulo.pack(pady=(0, 20))
        
        # Placeholder para futuras implementações
        info = ttk.Label(frame_principal, 
                        text="Esta seção mostrará:\n• Histórico de diagnósticos\n• Estatísticas de uso\n• Gráficos de performance\n• Relatórios detalhados",
                        font=('Arial', 12), justify=tk.LEFT)
        info.pack(expand=True)
    
    def criar_aba_sobre(self):
        """Cria a aba sobre o sistema"""
        aba_sobre = ttk.Frame(self.notebook)
        self.notebook.add(aba_sobre, text="ℹ️ Sobre")
        
        frame_principal = ttk.Frame(aba_sobre, padding=20)
        frame_principal.pack(fill=tk.BOTH, expand=True)
        
        titulo = ttk.Label(frame_principal, text="🏥 Sistema de Diagnóstico Médico Inteligente", 
                          style='Title.TLabel')
        titulo.pack(pady=(0, 20))
        
        info_texto = """
🎓 PROJETO ACADÊMICO INAR
Terceiro Ano • Segundo Semestre • 2025

🏥 SOBRE O SISTEMA:
Este é um sistema avançado de diagnóstico médico assistido por inteligência artificial,
desenvolvido especificamente para auxiliar profissionais de saúde e estudantes.

✨ CARACTERÍSTICAS PRINCIPAIS:
• Interface totalmente em português
• Mais de 70 sintomas catalogados
• Entrada manual de sintomas personalizados
• Análise de duração e intensidade dos sintomas
• Diagnóstico de mais de 100 doenças diferentes
• 8 algoritmos de Machine Learning
• Tradução automática de resultados

🤖 ALGORITMOS INCLUÍDOS:
• Random Forest (Floresta Aleatória)
• Support Vector Machine (SVM)
• Logistic Regression (Regressão Logística)
• K-Nearest Neighbors (KNN)
• Naive Bayes
• Decision Tree (Árvore de Decisão)
• Gradient Boosting
• XGBoost

🔍 DOENÇAS SUPORTADAS:
• Doenças respiratórias: Asma, Pneumonia, Tuberculose, Bronquite
• Doenças infecciosas: Malária, Gripe, Resfriado, Gastroenterite
• Doenças crônicas: Diabetes, Hipertensão, Artrite, Osteoporose
• Doenças neurológicas: AVC, Enxaqueca, Epilepsia, Alzheimer
• Doenças cardíacas: Infarto, Arritmia, Angina
• E muitas outras...

📊 MÉTRICAS DE AVALIAÇÃO:
• Acurácia (Accuracy)
• Precisão (Precision)
• Sensibilidade (Recall)
• F1-Score
• Matriz de Confusão
• Curvas ROC
• Validação cruzada

⚠️ IMPORTANTE - USO EDUCACIONAL:
Este sistema foi desenvolvido exclusivamente para fins educacionais e de pesquisa.
NÃO deve ser usado para diagnósticos médicos reais ou substituir consultas médicas.
Sempre procure um profissional de saúde qualificado para diagnósticos e tratamentos.

👨‍💻 TECNOLOGIAS UTILIZADAS:
• Python 3.12+
• Scikit-learn (Machine Learning)
• Pandas & NumPy (Processamento de dados)
• Tkinter (Interface gráfica)
• Matplotlib & Seaborn (Visualizações)
• XGBoost (Algoritmo avançado)

� SISTEMA DE ARQUIVOS:
• Consultas salvas em: consultas_salvas/
• Relatórios: consultas_salvas/relatorios/
• Histórico: consultas_salvas/historico/
• Backup: consultas_salvas/backup/

🎯 COMO SALVAR CONSULTAS:
• Botão "💾 Salvar Consulta" - Menu completo de opções
• Ctrl+S - Salvamento rápido automático
• Botão "📊 Ver Histórico" - Visualizar consultas anteriores

�📅 Desenvolvido em Novembro de 2025
        """
        
        # Área de texto scrollável
        text_sobre = scrolledtext.ScrolledText(frame_principal, font=('Arial', 10), 
                                              wrap=tk.WORD, height=25)
        text_sobre.pack(fill=tk.BOTH, expand=True)
        text_sobre.insert(1.0, info_texto)
        text_sobre.configure(state=tk.DISABLED)
    
    def criar_barra_status(self):
        """Cria barra de status na parte inferior"""
        # Frame da barra de status
        self.barra_status = ttk.Frame(self.root)
        self.barra_status.pack(side=tk.BOTTOM, fill=tk.X, padx=5, pady=(0, 5))
        
        # Separador
        ttk.Separator(self.root, orient=tk.HORIZONTAL).pack(side=tk.BOTTOM, fill=tk.X, pady=(0, 2))
        
        # Labels de status
        self.status_sistema = ttk.Label(self.barra_status, text="Sistema: Carregado", 
                                      font=('Arial', 9))
        self.status_sistema.pack(side=tk.LEFT, padx=(5, 20))
        
        self.status_modelo = ttk.Label(self.barra_status, text="Modelo: Verificando...", 
                                     font=('Arial', 9))
        self.status_modelo.pack(side=tk.LEFT, padx=(0, 20))
        
        # Informações de atalhos
        info_atalhos = ttk.Label(self.barra_status, 
                               text="Atalhos: F5=Diagnosticar | F11=Tela Cheia | Ctrl+L=Limpar | Ctrl+S=Salvar | Ctrl+Q=Sair",
                               font=('Arial', 8), foreground='gray')
        info_atalhos.pack(side=tk.RIGHT)
        
        # Atualizar status inicial
        self.atualizar_status_barra()
    
    # === MÉTODOS DE FUNCIONALIDADE ===
    
    def on_sintoma_change(self, sintoma):
        """Callback quando sintoma é selecionado/deselecionado"""
        if self.vars_sintomas[sintoma].get():
            self.sintomas_selecionados[sintoma] = {
                'presente': True,
                'duracao': None,
                'intensidade': None
            }
        else:
            if sintoma in self.sintomas_selecionados:
                del self.sintomas_selecionados[sintoma]
    
    def adicionar_sintoma_lista(self):
        """Adiciona sintoma selecionado da lista"""
        sintoma = self.combo_sintomas_extra.get()
        if sintoma and sintoma not in self.sintomas_selecionados:
            self.sintomas_selecionados[sintoma] = {
                'presente': True,
                'duracao': None,
                'intensidade': None
            }
            self.atualizar_lista_sintomas_adicionados()
            self.combo_sintomas_extra.set('')
    
    def adicionar_sintoma_manual(self):
        """Adiciona sintoma digitado manualmente"""
        sintoma = self.entry_sintoma_manual.get().strip()
        
        # Verificar se não é o placeholder
        if not sintoma or sintoma == "Ex: Dor no estômago, coceira...":
            messagebox.showwarning("Aviso", "Digite um sintoma válido.")
            return
            
        if not validar_sintoma_personalizado(sintoma):
            messagebox.showerror("Erro", "Sintoma inválido. Use apenas letras, espaços e hífens.")
            return
        
        sintoma = normalizar_sintoma(sintoma)
        
        if sintoma in self.sintomas_selecionados:
            messagebox.showinfo("Info", "Este sintoma já foi adicionado.")
            return
        
        self.sintomas_selecionados[sintoma] = {
            'presente': True,
            'duracao': None,
            'intensidade': None,
            'personalizado': True
        }
        
        self.sintomas_personalizados.append(sintoma)
        self.atualizar_lista_sintomas_adicionados()
        self.entry_sintoma_manual.delete(0, tk.END)
    
    def atualizar_lista_sintomas_adicionados(self):
        """Atualiza a exibição de sintomas adicionados"""
        sintomas_extras = [s for s in self.sintomas_selecionados.keys() 
                          if s not in obter_sintomas_principais()]
        
        self.text_sintomas_adicionados.configure(state=tk.NORMAL)
        self.text_sintomas_adicionados.delete(1.0, tk.END)
        
        if sintomas_extras:
            texto = "Sintomas adicionais: " + ", ".join(sintomas_extras)
            self.text_sintomas_adicionados.insert(1.0, texto)
        else:
            self.text_sintomas_adicionados.insert(1.0, "Nenhum sintoma adicional adicionado.")
            
        self.text_sintomas_adicionados.configure(state=tk.DISABLED)
    
    def tentar_carregar_modelo_automatico(self):
        """Tenta carregar modelo automaticamente"""
        caminho_modelo = os.path.join(BASE_DIR, 'modelos_salvos', 'melhor_modelo.pkl')
        
        if os.path.exists(caminho_modelo):
            try:
                self.modelo_carregado = joblib.load(caminho_modelo)
                self.label_status_modelo.configure(
                    text="✅ Modelo carregado automaticamente", 
                    style='Success.TLabel'
                )
                
                # Carregar preprocessador se disponível
                caminho_preprocessador = os.path.join(BASE_DIR, 'modelos_salvos')
                if os.path.exists(os.path.join(caminho_preprocessador, 'encoders.pkl')):
                    sys.path.append(os.path.join(BASE_DIR, 'src', 'utils'))
                    from preprocessador import PreProcessadorDados
                    self.preprocessador = PreProcessadorDados(pd.DataFrame())
                    self.preprocessador.carregar_preprocessadores(caminho_preprocessador)
                
                # Atualizar barra de status
                self.atualizar_status_barra()
                    
            except Exception as e:
                print(f"Erro ao carregar modelo: {e}")
                self.atualizar_status_barra()
    
    def carregar_modelo(self):
        """Carrega modelo salvo manualmente"""
        arquivo = filedialog.askopenfilename(
            title="Selecionar Modelo Treinado",
            filetypes=[("Arquivos PKL", "*.pkl"), ("Todos os arquivos", "*.*")]
        )
        
        if arquivo:
            try:
                self.modelo_carregado = joblib.load(arquivo)
                self.label_status_modelo.configure(
                    text=f"✅ Modelo carregado: {os.path.basename(arquivo)}", 
                    style='Success.TLabel'
                )
                self.atualizar_status_barra()
                messagebox.showinfo("Sucesso", "Modelo carregado com sucesso!")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao carregar modelo: {str(e)}")
                self.atualizar_status_barra()
    
    def selecionar_dataset(self):
        """Seleciona arquivo de conjunto de dados"""
        arquivo = filedialog.askopenfilename(
            title="Selecionar Conjunto de Dados CSV",
            filetypes=[("Arquivos CSV", "*.csv"), ("Todos os arquivos", "*.*")]
        )
        
        if arquivo:
            self.entry_dataset.configure(state=tk.NORMAL)
            self.entry_dataset.delete(0, tk.END)
            self.entry_dataset.insert(0, arquivo)
            self.entry_dataset.configure(state="readonly")
    
    def iniciar_treinamento(self):
        """Inicia processo de treinamento"""
        # Usar conjunto de dados padrão se não selecionado
        if not self.entry_dataset.get():
            dataset_padrao = os.path.join(BASE_DIR, 'dataset', 'Disease_symptom_and_patient_profile_dataset.csv')
            if os.path.exists(dataset_padrao):
                self.entry_dataset.configure(state=tk.NORMAL)
                self.entry_dataset.delete(0, tk.END)
                self.entry_dataset.insert(0, dataset_padrao)
                self.entry_dataset.configure(state="readonly")
            else:
                messagebox.showerror("Erro", "Selecione um arquivo de dataset.")
                return
        
        self.progress_treino.start()
        self.btn_iniciar_treino.configure(state=tk.DISABLED)
        
        # Executar em thread separada
        thread = threading.Thread(target=self.executar_treinamento)
        thread.daemon = True
        thread.start()
    
    def executar_treinamento(self):
        """Executa treinamento em background"""
        try:
            self.adicionar_log_treino("🚀 Iniciando treinamento dos modelos...")
            
            # Adicionar paths
            sys.path.append(os.path.join(BASE_DIR, 'src', 'utils'))
            sys.path.append(os.path.join(BASE_DIR, 'src', 'models'))
            
            # Importar módulos
            from carregador_dados import CarregadorDados
            from preprocessador import PreProcessadorDados
            from treinador_modelos import TreinadorModelos
            
            # Carregar dados
            self.adicionar_log_treino("📂 Carregando base de dados...")
            carregador = CarregadorDados(self.entry_dataset.get())
            dados = carregador.carregar_dados()
            self.adicionar_log_treino(f"✅ Dados carregados: {len(dados)} registros")
            
            # Pré-processar
            self.adicionar_log_treino("🔧 Processando e preparando dados...")
            preprocessador = PreProcessadorDados(dados)
            dados_processados = preprocessador.processar_dados_completo(
                test_size=int(self.scale_teste.get())/100
            )
            
            # Treinar modelos
            self.adicionar_log_treino("🤖 Treinando algoritmos de Machine Learning...")
            treinador = TreinadorModelos()
            
            usar_grid = self.var_grid_search.get()
            if usar_grid:
                self.adicionar_log_treino("⚙️ Usando otimização avançada (pode demorar mais)...")
            
            resultados = treinador.treinar_todos_modelos(
                dados_processados['X_train'],
                dados_processados['y_train'],
                usar_grid_search=usar_grid
            )
            
            # Salvar modelos
            self.adicionar_log_treino("💾 Salvando modelos treinados...")
            caminho_salvar = os.path.join(BASE_DIR, 'modelos_salvos')
            os.makedirs(caminho_salvar, exist_ok=True)
            
            treinador.salvar_modelos(caminho_salvar)
            preprocessador.salvar_preprocessadores(caminho_salvar)
            
            # Avaliar modelos
            self.adicionar_log_treino("📊 Avaliando performance dos modelos...")
            ranking = treinador.obter_ranking_modelos(
                dados_processados['X_test'],
                dados_processados['y_test']
            )
            
            self.adicionar_log_treino("\n🏆 RANKING DOS MODELOS:")
            self.adicionar_log_treino(str(ranking))
            
            self.adicionar_log_treino("\n✅ Treinamento concluído com sucesso!")
            self.adicionar_log_treino("🎯 O melhor modelo foi salvo automaticamente.")
            
            # Carregar o melhor modelo
            self.tentar_carregar_modelo_automatico()
            
        except Exception as e:
            self.adicionar_log_treino(f"❌ Erro durante o treinamento: {str(e)}")
        finally:
            self.root.after(0, self.finalizar_treinamento)
    
    def finalizar_treinamento(self):
        """Finaliza treinamento na thread principal"""
        self.progress_treino.stop()
        self.btn_iniciar_treino.configure(state=tk.NORMAL)
    
    def parar_treinamento(self):
        """Para o treinamento"""
        self.adicionar_log_treino("⏹️ Treinamento interrompido pelo usuário")
        self.finalizar_treinamento()
    
    def adicionar_log_treino(self, texto: str):
        """Adiciona texto ao log de treinamento"""
        def _adicionar():
            self.text_log_treino.configure(state=tk.NORMAL)
            timestamp = datetime.now().strftime("%H:%M:%S")
            self.text_log_treino.insert(tk.END, f"[{timestamp}] {texto}\n")
            self.text_log_treino.see(tk.END)
            self.text_log_treino.configure(state=tk.DISABLED)
        
        if hasattr(self, 'root'):
            self.root.after(0, _adicionar)
    
    def realizar_diagnostico(self):
        """Realiza diagnóstico completo usando o novo sistema"""
        # Validar dados obrigatórios
        if not self.entry_nome.get().strip():
            messagebox.showwarning("Aviso", "Por favor, digite o nome do paciente.")
            return
        
        if not self.entry_idade.get().strip():
            messagebox.showwarning("Aviso", "Por favor, digite a idade do paciente.")
            return
        
        if not self.sintomas_selecionados:
            messagebox.showwarning("Aviso", "Selecione pelo menos um sintoma.")
            return
        
        try:
            # Mostrar indicador de carregamento
            self.btn_diagnosticar.configure(text="Diagnosticando...", state=tk.DISABLED)
            self.root.update()
            
            # Obter lista de sintomas selecionados
            sintomas_lista = list(self.sintomas_selecionados.keys())
            
            # Usar o novo sistema de diagnóstico
            resultado = self.sistema_diagnostico.diagnosticar_sintomas(
                sintomas_lista,
                incluir_detalhes=True
            )
            
            if resultado['sucesso']:
                # Coletar dados do paciente para o relatório
                dados_paciente = self.coletar_dados_paciente_basicos()
                
                # Exibir resultado usando o novo sistema
                self.exibir_resultado_novo_sistema(dados_paciente, resultado)
                
            else:
                messagebox.showerror("Erro", f"Erro no diagnóstico: {resultado.get('erro', 'Erro desconhecido')}")
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao realizar diagnóstico: {str(e)}")
        
        finally:
            # Restaurar botão
            self.btn_diagnosticar.configure(text="🔍 Executar Diagnóstico", state=tk.NORMAL)
    
    def coletar_dados_paciente_basicos(self) -> Dict:
        """Coleta dados básicos do paciente para o relatório"""
        return {
            'nome': self.entry_nome.get().strip(),
            'idade': self.entry_idade.get().strip(),
            'genero': self.combo_genero.get(),
            'telefone': getattr(self, 'entry_telefone', {}).get() if hasattr(self, 'entry_telefone') else '',
            'sintomas_selecionados': dict(self.sintomas_selecionados),
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    
    def processar_dados_basico(self, df: pd.DataFrame) -> pd.DataFrame:
        """Processamento básico quando não há preprocessador"""
        df_proc = df.copy()
        
        # Codificar sintomas
        sintomas = ['Fever', 'Cough', 'Fatigue', 'Difficulty Breathing']
        for sintoma in sintomas:
            df_proc[sintoma] = df_proc[sintoma].map({'Yes': 1, 'No': 0})
        
        # Codificar outros campos
        # Mapear valores em português para os valores esperados pelo modelo
        mapeamento_genero = {'Masculino': 1, 'Feminino': 0}
        mapeamento_pressao = {'Baixa': 0, 'Normal': 1, 'Alta': 2}
        mapeamento_colesterol = {'Baixo': 0, 'Normal': 1, 'Alto': 2}
        
        df_proc['Gender'] = df_proc['Gender'].map(mapeamento_genero)
        df_proc['Blood Pressure'] = df_proc['Blood Pressure'].map(mapeamento_pressao)
        df_proc['Cholesterol Level'] = df_proc['Cholesterol Level'].map(mapeamento_colesterol)
        
        return df_proc
    
    def determinar_doenca_especifica(self) -> str:
        """Determina doença específica baseada nos sintomas"""
        sintomas = list(self.sintomas_selecionados.keys())
        
        # Regras básicas de diagnóstico diferencial
        if 'Febre' in sintomas and 'Tosse' in sintomas:
            if 'Dificuldade para Respirar' in sintomas:
                return 'Pneumonia'
            elif 'Dor de Garganta' in sintomas:
                return 'Gripe'
            else:
                return 'Resfriado Comum'
        
        elif 'Febre' in sintomas and 'Dor de Cabeça' in sintomas:
            if 'Calafrios' in sintomas or 'Suor Noturno' in sintomas:
                return 'Malária'
            else:
                return 'Gripe'
        
        elif 'Tosse' in sintomas and 'Perda de Peso' in sintomas:
            if 'Suor Noturno' in sintomas:
                return 'Tuberculose'
            else:
                return 'Bronquite'
        
        elif 'Dificuldade para Respirar' in sintomas:
            if 'Chiado no Peito' in sintomas:
                return 'Asma'
            else:
                return 'Problema Respiratório'
        
        elif 'Dor de Cabeça' in sintomas:
            if 'Náusea' in sintomas:
                return 'Enxaqueca'
            else:
                return 'Cefaleia'
        
        elif 'Fadiga' in sintomas:
            if 'Dor nas Articulações' in sintomas:
                return 'Artrite'
            else:
                return 'Síndrome da Fadiga'
        
        # Casos específicos
        elif any(s in sintomas for s in ['Náusea', 'Vômito', 'Diarreia']):
            return 'Gastroenterite'
        
        elif any(s in sintomas for s in ['Dor no Peito', 'Palpitações']):
            return 'Problema Cardíaco'
        
        else:
            return 'Condição Geral a Investigar'
    
    def exibir_resultado_novo_sistema(self, dados_paciente: Dict, resultado_diagnostico: Dict):
        """Exibe resultado completo do novo sistema de diagnóstico"""
        timestamp = datetime.now().strftime("%d/%m/%Y às %H:%M:%S")
        
        # Cabeçalho do relatório
        relatorio = f"""
╔══════════════════════════════════════════════════════════════════╗
║              🏥 RELATÓRIO DE DIAGNÓSTICO ATUALIZADO              ║
║                      {timestamp}                     ║
╚══════════════════════════════════════════════════════════════════╝

👤 DADOS DO PACIENTE:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• Nome: {dados_paciente['nome']}
• Idade: {dados_paciente['idade']} anos
• Gênero: {dados_paciente['genero']}
• Data/Hora: {dados_paciente['timestamp']}

🔍 SINTOMAS ANALISADOS:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
        
        # Listar sintomas com seus scores
        sintomas_scores = resultado_diagnostico.get('sintomas_scores', {})
        for i, sintoma in enumerate(resultado_diagnostico['sintomas_informados'], 1):
            score = sintomas_scores.get(sintoma, 0)
            relatorio += f"  {i}. ✅ {sintoma} (Severidade: {score})\n"
        
        relatorio += f"\n📊 Score Total dos Sintomas: {resultado_diagnostico['score_total']:.1f}\n"
        
        # Informações temporais se disponíveis
        if hasattr(self, 'combo_duracao') and (self.combo_duracao.get() or self.combo_intensidade.get()):
            relatorio += f"\n⏰ INFORMAÇÕES TEMPORAIS:\n"
            relatorio += f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            
            if hasattr(self, 'combo_duracao') and self.combo_duracao.get():
                relatorio += f"• Duração dos sintomas: {self.combo_duracao.get()}\n"
            if hasattr(self, 'combo_intensidade') and self.combo_intensidade.get():
                relatorio += f"• Intensidade geral: {self.combo_intensidade.get()}\n"
        
        # Diagnósticos encontrados
        diagnosticos = resultado_diagnostico.get('diagnosticos', [])
        
        if diagnosticos:
            relatorio += f"""
🎯 POSSÍVEIS DIAGNÓSTICOS:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
            
            # Listar todos os diagnósticos
            for i, diag in enumerate(diagnosticos, 1):
                probabilidade = diag['probabilidade']
                emoji = "🔴" if probabilidade >= 70 else "🟡" if probabilidade >= 40 else "🟢"
                nivel_confianca = "Alta" if probabilidade >= 70 else "Média" if probabilidade >= 40 else "Baixa"
                
                relatorio += f"""
{i}. {emoji} {diag['doenca']} - {probabilidade:.1f}%
   Nível de Confiança: {nivel_confianca}
"""
                
                # Adicionar descrição se disponível
                if diag.get('descricao'):
                    descricao = diag['descricao'][:200] + "..." if len(diag['descricao']) > 200 else diag['descricao']
                    relatorio += f"   📋 Descrição: {descricao}\n"
                
                relatorio += "\n"
            
            # Diagnóstico principal detalhado
            principal = diagnosticos[0]
            relatorio += f"""
🏥 DIAGNÓSTICO PRINCIPAL: {principal['doenca']}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Probabilidade: {principal['probabilidade']:.1f}%
"""
            
            # Descrição completa da doença principal
            if principal.get('descricao'):
                relatorio += f"\n📖 SOBRE A CONDIÇÃO:\n"
                relatorio += f"{principal['descricao']}\n"
            
            # Precauções e recomendações
            if principal.get('precaucoes'):
                relatorio += f"""
🛡️  PRECAUÇÕES E CUIDADOS:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
                for i, precaucao in enumerate(principal['precaucoes'], 1):
                    relatorio += f"  {i}. • {precaucao}\n"
        
        else:
            relatorio += f"""
🎯 RESULTADO DO DIAGNÓSTICO:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
❓ Não foi possível determinar um diagnóstico específico com os sintomas informados.
   Recomenda-se consultar um médico para avaliação mais detalhada.
"""
        
        # Aviso médico obrigatório
        relatorio += f"""

⚠️  AVISO MÉDICO IMPORTANTE:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Este diagnóstico é uma ESTIMATIVA baseada em algoritmos de IA e
análise de sintomas. NÃO substitui uma consulta médica profissional.

🏨 PRÓXIMOS PASSOS RECOMENDADOS:
• Procure um médico qualificado para confirmação
• Realize exames específicos conforme orientação médica
• Siga tratamento prescrito por profissional de saúde
• Em caso de emergência, procure atendimento imediato

📊 Sistema baseado em dados de: {len(sintomas_scores)} sintomas analisados
🔬 Algoritmo atualizado com pesos de severidade e base médica expandida
🎓 Sistema desenvolvido para fins educacionais - INAR 2025
"""
        
        # Exibir resultado
        self.text_resultado.configure(state=tk.NORMAL)
        self.text_resultado.delete(1.0, tk.END)
        self.text_resultado.insert(1.0, relatorio)
        self.text_resultado.configure(state=tk.DISABLED)
        
        # Opção para salvar o resultado
        self.dados_ultimo_diagnostico = {
            'dados_paciente': dados_paciente,
            'resultado': resultado_diagnostico,
            'relatorio_completo': relatorio
        }
    
    def gerar_recomendacoes(self, doenca: str, predicao: int) -> str:
        """Gera recomendações baseadas no diagnóstico"""
        recomendacoes = {
            'Pneumonia': "• Procure atendimento médico urgente\n• Mantenha repouso absoluto\n• Hidrate-se bem\n• Evite esforços físicos",
            'Malária': "• Busque atendimento médico imediatamente\n• Realize exames de sangue específicos\n• Mantenha-se hidratado\n• Evite automedicação",
            'Tuberculose': "• Procure um pneumologista urgentemente\n• Realize raio-X do tórax\n• Faça teste de escarro\n• Evite contato próximo com outras pessoas",
            'Gripe': "• Mantenha repouso\n• Hidrate-se bem\n• Use medicação sintomática se necessário\n• Procure médico se piorar",
            'Asma': "• Procure um pneumologista\n• Evite alérgenos conhecidos\n• Mantenha medicação de emergência\n• Monitore os sintomas",
            'Resfriado Comum': "• Repouso e hidratação\n• Medicação sintomática\n• Procure médico se não melhorar em 7 dias",
        }
        
        recomendacao = recomendacoes.get(doenca, "• Procure orientação médica para avaliação adequada\n• Monitore a evolução dos sintomas\n• Mantenha hábitos saudáveis")
        
        if predicao == 1:
            recomendacao += "\n• ⚠️ Resultado POSITIVO - Atenção médica recomendada"
        
        return recomendacao
    
    def limpar_todos_campos(self):
        """Limpa todos os campos do formulário"""
        # Limpar dados pessoais
        self.entry_nome.delete(0, tk.END)
        self.entry_idade.delete(0, tk.END)
        self.combo_genero.set('')
        self.combo_pressao.set('')
        self.combo_colesterol.set('')
        
        # Limpar sintomas principais
        for var in self.vars_sintomas.values():
            var.set(False)
        
        # Limpar sintomas adicionais
        self.sintomas_selecionados.clear()
        self.sintomas_personalizados.clear()
        self.combo_sintomas_extra.set('')
        self.entry_sintoma_manual.delete(0, tk.END)
        self.atualizar_lista_sintomas_adicionados()
        
        # Limpar informações temporais
        self.combo_duracao.set('')
        self.combo_intensidade.set('')
        
        # Limpar resultado
        self.text_resultado.configure(state=tk.NORMAL)
        self.text_resultado.delete(1.0, tk.END)
        self.text_resultado.configure(state=tk.DISABLED)
        
        messagebox.showinfo("Sucesso", "Todos os campos foram limpos!")
    
    def salvar_consulta(self):
        """Menu de opções para salvar consulta"""
        if not self.text_resultado.get(1.0, tk.END).strip():
            messagebox.showwarning("Aviso", "Nenhum resultado para salvar. Realize um diagnóstico primeiro.")
            return
        
        # Criar janela de opções de salvamento
        janela_salvar = tk.Toplevel(self.root)
        janela_salvar.title("💾 Salvar Consulta")
        janela_salvar.geometry("500x350")
        janela_salvar.resizable(False, False)
        janela_salvar.transient(self.root)
        janela_salvar.grab_set()
        
        # Centralizar janela
        janela_salvar.update_idletasks()
        x = (janela_salvar.winfo_screenwidth() // 2) - (500 // 2)
        y = (janela_salvar.winfo_screenheight() // 2) - (350 // 2)
        janela_salvar.geometry(f"500x350+{x}+{y}")
        
        # Conteúdo da janela
        frame_principal = ttk.Frame(janela_salvar, padding=20)
        frame_principal.pack(fill=tk.BOTH, expand=True)
        
        # Título
        ttk.Label(frame_principal, text="📋 Opções de Salvamento", 
                 font=('Arial', 14, 'bold')).pack(pady=(0, 20))
        
        # Informações da consulta
        info_frame = ttk.LabelFrame(frame_principal, text="Informações da Consulta", padding=10)
        info_frame.pack(fill=tk.X, pady=(0, 15))
        
        nome_paciente = self.entry_nome.get() or "Sem_nome"
        timestamp = datetime.now().strftime("%d/%m/%Y às %H:%M:%S")
        
        ttk.Label(info_frame, text=f"Paciente: {nome_paciente}").pack(anchor=tk.W)
        ttk.Label(info_frame, text=f"Data/Hora: {timestamp}").pack(anchor=tk.W)
        
        # Opções de salvamento
        opcoes_frame = ttk.LabelFrame(frame_principal, text="Escolha uma opção:", padding=15)
        opcoes_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Botão 1: Salvamento rápido automático
        btn_rapido = ttk.Button(opcoes_frame, text="⚡ Salvamento Rápido (Pasta Automática)", 
                               command=lambda: self.salvar_rapido(janela_salvar))
        btn_rapido.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(opcoes_frame, text="Salva automaticamente em: consultas_salvas/relatorios/", 
                 font=('Arial', 8), foreground='gray').pack(anchor=tk.W)
        
        # Botão 2: Escolher localização
        btn_escolher = ttk.Button(opcoes_frame, text="📁 Escolher Local de Salvamento", 
                                 command=lambda: self.salvar_escolhendo_local(janela_salvar))
        btn_escolher.pack(fill=tk.X, pady=(10, 10))
        
        ttk.Label(opcoes_frame, text="Abre janela para escolher onde salvar o arquivo", 
                 font=('Arial', 8), foreground='gray').pack(anchor=tk.W)
        
        # Botão 3: Salvar e abrir pasta
        btn_salvar_abrir = ttk.Button(opcoes_frame, text="💾 Salvar e Abrir Pasta", 
                                     command=lambda: self.salvar_e_abrir_pasta(janela_salvar))
        btn_salvar_abrir.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Label(opcoes_frame, text="Salva e abre a pasta de consultas no explorador", 
                 font=('Arial', 8), foreground='gray').pack(anchor=tk.W)
        
        # Botões de controle
        controle_frame = ttk.Frame(frame_principal)
        controle_frame.pack(fill=tk.X)
        
        ttk.Button(controle_frame, text="❌ Cancelar", 
                  command=janela_salvar.destroy).pack(side=tk.RIGHT, padx=(10, 0))
        
        ttk.Button(controle_frame, text="📂 Abrir Pasta de Consultas", 
                  command=self.abrir_pasta_consultas).pack(side=tk.LEFT)
    
    def salvar_rapido(self, janela_pai):
        """Salvamento rápido na pasta automática"""
        try:
            nome_paciente = self.entry_nome.get() or "Paciente"
            nome_paciente = "".join(c for c in nome_paciente if c.isalnum() or c in (' ', '-', '_')).strip()
            nome_paciente = nome_paciente.replace(' ', '_')
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            nome_arquivo = f"diagnostico_{nome_paciente}_{timestamp}.txt"
            
            caminho_arquivo = os.path.join(self.dir_relatorios, nome_arquivo)
            
            # Salvar relatório
            with open(caminho_arquivo, 'w', encoding='utf-8') as f:
                f.write(self.text_resultado.get(1.0, tk.END))
            
            # Salvar no histórico
            self.salvar_no_historico(caminho_arquivo)
            
            janela_pai.destroy()
            messagebox.showinfo("Sucesso", f"✅ Relatório salvo com sucesso!\n\n"
                                         f"Arquivo: {nome_arquivo}\n"
                                         f"Local: consultas_salvas/relatorios/\n\n"
                                         f"💡 Use Ctrl+S para acesso rápido!")
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar: {str(e)}")
    
    def salvar_escolhendo_local(self, janela_pai):
        """Salvar escolhendo o local"""
        nome_paciente = self.entry_nome.get() or "Paciente"
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        nome_sugerido = f"diagnostico_{nome_paciente}_{timestamp}.txt"
        
        arquivo = filedialog.asksaveasfilename(
            title="Salvar Relatório de Diagnóstico",
            defaultextension=".txt",
            filetypes=[("Arquivos de Texto", "*.txt"), 
                      ("Arquivos PDF", "*.pdf"),
                      ("Todos os arquivos", "*.*")],
            initialvalue=nome_sugerido,
            initialdir=self.dir_relatorios
        )
        
        if arquivo:
            try:
                with open(arquivo, 'w', encoding='utf-8') as f:
                    f.write(self.text_resultado.get(1.0, tk.END))
                
                # Salvar no histórico
                self.salvar_no_historico(arquivo)
                
                janela_pai.destroy()
                messagebox.showinfo("Sucesso", f"✅ Relatório salvo em:\n{arquivo}")
                
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao salvar: {str(e)}")
    
    def salvar_e_abrir_pasta(self, janela_pai):
        """Salva e abre a pasta no explorador"""
        self.salvar_rapido(janela_pai)
        
        # Aguardar um pouco e abrir pasta
        self.root.after(1000, self.abrir_pasta_consultas)
    
    def salvar_no_historico(self, caminho_arquivo):
        """Salva informações no histórico CSV"""
        import csv
        
        try:
            # Coletar dados da consulta atual
            dados_historico = [
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                self.entry_nome.get() or "N/A",
                self.entry_idade.get() or "N/A",
                self.combo_genero.get() or "N/A",
                ", ".join([s for s in self.sintomas_selecionados.keys() if s in obter_sintomas_principais()]),
                ", ".join([s for s in self.sintomas_selecionados.keys() if s not in obter_sintomas_principais()]),
                self.combo_duracao.get() or "N/A",
                self.combo_intensidade.get() or "N/A",
                self.combo_pressao.get() or "N/A",
                self.combo_colesterol.get() or "N/A",
                "Positivo" if "POSITIVO" in self.text_resultado.get(1.0, tk.END) else "Negativo",
                "Alto" if "Alto" in self.text_resultado.get(1.0, tk.END) else "Médio",
                os.path.basename(caminho_arquivo)
            ]
            
            # Adicionar ao arquivo CSV
            with open(self.arquivo_historico, 'a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f, delimiter=';')
                writer.writerow(dados_historico)
                
        except Exception as e:
            print(f"Erro ao salvar no histórico: {e}")
    
    def abrir_pasta_consultas(self):
        """Abre a pasta de consultas no explorador de arquivos"""
        try:
            import subprocess
            import platform
            
            sistema = platform.system()
            
            if sistema == "Windows":
                os.startfile(self.dir_consultas)
            elif sistema == "Darwin":  # macOS
                subprocess.run(["open", self.dir_consultas])
            else:  # Linux
                subprocess.run(["xdg-open", self.dir_consultas])
                
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível abrir a pasta: {str(e)}\n\n"
                                        f"Local manual: {self.dir_consultas}")
            
    def visualizar_historico_consultas(self):
        """Abre janela para visualizar histórico de consultas"""
        if not os.path.exists(self.arquivo_historico):
            messagebox.showinfo("Info", "Nenhum histórico encontrado. Realize algumas consultas primeiro.")
            return
        
        # Criar janela de histórico
        janela_historico = tk.Toplevel(self.root)
        janela_historico.title("📊 Histórico de Consultas")
        janela_historico.geometry("900x600")
        janela_historico.transient(self.root)
        
        # Ler dados do CSV
        try:
            import csv
            import pandas as pd
            
            df = pd.read_csv(self.arquivo_historico, delimiter=';')
            
            # Criar treeview para mostrar dados
            frame = ttk.Frame(janela_historico, padding=10)
            frame.pack(fill=tk.BOTH, expand=True)
            
            ttk.Label(frame, text="📊 Histórico de Consultas Realizadas", 
                     font=('Arial', 14, 'bold')).pack(pady=(0, 10))
            
            # Treeview com scrollbar
            tree_frame = ttk.Frame(frame)
            tree_frame.pack(fill=tk.BOTH, expand=True)
            
            tree = ttk.Treeview(tree_frame, columns=list(df.columns), show='headings')
            
            # Configurar colunas
            for col in df.columns:
                tree.heading(col, text=col.replace('_', ' '))
                tree.column(col, width=100)
            
            # Adicionar dados
            for index, row in df.iterrows():
                tree.insert('', 'end', values=list(row))
            
            # Scrollbars
            scroll_y = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=tree.yview)
            scroll_x = ttk.Scrollbar(tree_frame, orient=tk.HORIZONTAL, command=tree.xview)
            
            tree.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
            
            # Layout
            tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
            scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
            
            # Botões
            btn_frame = ttk.Frame(frame)
            btn_frame.pack(fill=tk.X, pady=(10, 0))
            
            ttk.Button(btn_frame, text="📂 Abrir Pasta", 
                      command=self.abrir_pasta_consultas).pack(side=tk.LEFT)
            
            ttk.Button(btn_frame, text="❌ Fechar", 
                      command=janela_historico.destroy).pack(side=tk.RIGHT)
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar histórico: {str(e)}")
    
    def salvar_rapido_atalho(self):
        """Salvamento rápido via atalho Ctrl+S"""
        if not self.text_resultado.get(1.0, tk.END).strip():
            messagebox.showwarning("Aviso", "Nenhum resultado para salvar. Realize um diagnóstico primeiro.")
            return
        
        try:
            nome_paciente = self.entry_nome.get() or "Paciente"
            nome_paciente = "".join(c for c in nome_paciente if c.isalnum() or c in (' ', '-', '_')).strip()
            nome_paciente = nome_paciente.replace(' ', '_')
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            nome_arquivo = f"diagnostico_{nome_paciente}_{timestamp}.txt"
            
            caminho_arquivo = os.path.join(self.dir_relatorios, nome_arquivo)
            
            # Salvar relatório
            with open(caminho_arquivo, 'w', encoding='utf-8') as f:
                f.write(self.text_resultado.get(1.0, tk.END))
            
            # Salvar no histórico
            self.salvar_no_historico(caminho_arquivo)
            
            # Mostrar notificação rápida
            self.root.title(f"🏥 Sistema de Diagnóstico Médico - INAR ✅ SALVO: {nome_arquivo}")
            self.root.after(3000, lambda: self.root.title("🏥 Sistema de Diagnóstico Médico - INAR"))
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar: {str(e)}")
    
    def on_entry_focus_in(self, event):
        """Remove placeholder quando campo recebe foco"""
        if self.entry_sintoma_manual.get() == "Ex: Dor no estômago, coceira...":
            self.entry_sintoma_manual.delete(0, tk.END)
    
    def on_entry_focus_out(self, event):
        """Adiciona placeholder quando campo perde foco e está vazio"""
        if not self.entry_sintoma_manual.get():
            self.entry_sintoma_manual.insert(0, "Ex: Dor no estômago, coceira...")
    
    def on_canvas_configure(self, event):
        """Ajusta o tamanho do frame scrollável quando canvas é redimensionado"""
        # Ajustar largura do frame scrollável para preencher o canvas
        canvas_width = event.width
        self.canvas_diagnostico.itemconfig(self.canvas_window, width=canvas_width)
    
    def bind_mousewheel(self, widget):
        """Vincula eventos de mouse wheel para scroll"""
        def _on_mousewheel(event):
            # Verificar se o scroll vertical está visível
            if self.canvas_diagnostico.winfo_exists():
                # Scroll no Linux/Windows
                if event.delta:
                    delta = -1 * (event.delta / 120)
                else:
                    # Para sistemas que não têm event.delta
                    if event.num == 4:
                        delta = -1
                    elif event.num == 5:
                        delta = 1
                    else:
                        delta = 0
                
                self.canvas_diagnostico.yview_scroll(int(delta), "units")
        
        # Bind para diferentes sistemas
        widget.bind("<MouseWheel>", _on_mousewheel)  # Windows/MacOS
        widget.bind("<Button-4>", _on_mousewheel)    # Linux
        widget.bind("<Button-5>", _on_mousewheel)    # Linux
        
        # Aplicar o bind também aos widgets filhos recursivamente
        def bind_to_children(parent):
            for child in parent.winfo_children():
                child.bind("<MouseWheel>", _on_mousewheel)
                child.bind("<Button-4>", _on_mousewheel)
                child.bind("<Button-5>", _on_mousewheel)
                if child.winfo_children():
                    bind_to_children(child)
        
        # Aplicar o scroll a todos os widgets da aba
        self.root.after(100, lambda: bind_to_children(self.frame_scrollavel))
    
    def executar(self):
        """Executa a aplicação"""
        # Configurar protocolo de fechamento da janela
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()
    
    def atualizar_status_barra(self):
        """Atualiza informações na barra de status"""
        if hasattr(self, 'status_sistema') and hasattr(self, 'status_modelo'):
            # Status do sistema
            timestamp = datetime.now().strftime("%H:%M:%S")
            self.status_sistema.configure(text=f"Sistema: Ativo ({timestamp})")
            
            # Status do modelo
            if self.modelo_carregado:
                modelo_nome = type(self.modelo_carregado).__name__
                self.status_modelo.configure(text=f"Modelo: {modelo_nome} ✅")
            else:
                self.status_modelo.configure(text="Modelo: Não carregado ❌")
    
    def on_closing(self):
        """Manipula o fechamento da janela"""
        if messagebox.askokcancel("Sair", "Deseja realmente sair do sistema?"):
            self.root.destroy()

# Função principal
def main():
    try:
        app = SistemaDiagnosticoPortugues()
        app.executar()
    except Exception as e:
        print(f"Erro ao iniciar aplicação: {e}")
        messagebox.showerror("Erro Fatal", f"Erro ao iniciar aplicação: {e}")

if __name__ == "__main__":
    main()