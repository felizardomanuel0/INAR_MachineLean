"""
Interface Gráfica Principal do Sistema de Diagnóstico
Projeto Final INAR - Terceiro Ano, II Semestre
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
import sys
import pandas as pd
import joblib
from typing import Dict
import threading

class SistemaDiagnostico:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🏥 Sistema de Diagnóstico de Doenças")
        self.root.geometry("1200x800")
        self.root.minsize(800, 600)
        
        # Variáveis de controle
        self.modelo_carregado = None
        self.preprocessador = None
        
        # Configurar estilos
        self.configurar_estilos()
        
        # Configurar interface
        self.configurar_interface()
        
        # Tentar carregar modelo automaticamente
        self.tentar_carregar_modelo_automatico()
    
    def configurar_estilos(self):
        """Configura os estilos da interface"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Estilo para títulos
        style.configure('Title.TLabel', font=('Arial', 16, 'bold'))
        style.configure('Subtitle.TLabel', font=('Arial', 12, 'bold'))
        
        # Estilo para botões personalizados
        style.configure('Custom.TButton', font=('Arial', 10, 'bold'))
        
        # Estilos para status
        style.configure('Success.TLabel', foreground='green', font=('Arial', 10, 'bold'))
        style.configure('Danger.TLabel', foreground='red', font=('Arial', 10, 'bold'))
    
    def configurar_interface(self):
        """Configura a interface principal"""
        # Frame principal
        main_frame = ttk.Frame(self.root, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        titulo = ttk.Label(main_frame, text="🏥 Sistema de Diagnóstico de Doenças", 
                          style='Title.TLabel')
        titulo.pack(pady=(0, 20))
        
        # Criar notebook (abas)
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Criar abas
        self.criar_aba_diagnostico()
        self.criar_aba_treinamento()
        self.criar_aba_visualizacao()
        self.criar_aba_sobre()
    
    def criar_aba_diagnostico(self):
        """Cria a aba de diagnóstico"""
        aba_diagnostico = ttk.Frame(self.notebook)
        self.notebook.add(aba_diagnostico, text="🔍 Diagnóstico")
        
        # Frame esquerdo - Entrada de dados
        frame_entrada = ttk.LabelFrame(aba_diagnostico, text="Dados do Paciente", padding=15)
        frame_entrada.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Status do modelo
        self.status_modelo = ttk.Label(frame_entrada, text="❌ Nenhum modelo carregado", 
                                      style='Danger.TLabel')
        self.status_modelo.pack(anchor=tk.W, pady=(0, 15))
        
        # Frame para sintomas
        frame_sintomas = ttk.LabelFrame(frame_entrada, text="Sintomas", padding=10)
        frame_sintomas.pack(fill=tk.X, pady=(0, 10))
        
        # Variáveis para sintomas
        self.var_febre = tk.BooleanVar()
        self.var_tosse = tk.BooleanVar()
        self.var_fadiga = tk.BooleanVar()
        self.var_dificuldade_respirar = tk.BooleanVar()
        
        # Checkboxes para sintomas
        sintomas = [
            ("Febre", self.var_febre),
            ("Tosse", self.var_tosse),
            ("Fadiga", self.var_fadiga),
            ("Dificuldade para Respirar", self.var_dificuldade_respirar)
        ]
        
        for i, (texto, variavel) in enumerate(sintomas):
            cb = ttk.Checkbutton(frame_sintomas, text=texto, variable=variavel)
            cb.grid(row=i//2, column=i%2, sticky=tk.W, padx=5, pady=2)
        
        # Frame para dados demográficos
        frame_demograficos = ttk.LabelFrame(frame_entrada, text="Dados Demográficos", padding=10)
        frame_demograficos.pack(fill=tk.X, pady=(0, 10))
        
        # Idade
        ttk.Label(frame_demograficos, text="Idade:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.entry_idade = ttk.Entry(frame_demograficos, width=10)
        self.entry_idade.grid(row=0, column=1, sticky=tk.W, padx=(5, 20))
        
        # Gênero
        ttk.Label(frame_demograficos, text="Gênero:").grid(row=0, column=2, sticky=tk.W, pady=2)
        self.combo_genero = ttk.Combobox(frame_demograficos, values=["Male", "Female"], 
                                        state="readonly", width=10)
        self.combo_genero.grid(row=0, column=3, sticky=tk.W, padx=5)
        
        # Frame para dados clínicos
        frame_clinicos = ttk.LabelFrame(frame_entrada, text="Dados Clínicos", padding=10)
        frame_clinicos.pack(fill=tk.X, pady=(0, 10))
        
        # Pressão arterial
        ttk.Label(frame_clinicos, text="Pressão Arterial:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.combo_pressao = ttk.Combobox(frame_clinicos, values=["Baixa", "Normal", "Alta"], 
                                          state="readonly", width=12)
        self.combo_pressao.grid(row=0, column=1, sticky=tk.W, padx=5)
        
        # Colesterol
        ttk.Label(frame_clinicos, text="Colesterol:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.combo_colesterol = ttk.Combobox(frame_clinicos, values=["Baixo", "Normal", "Alto"], 
                                            state="readonly", width=12)
        self.combo_colesterol.grid(row=1, column=1, sticky=tk.W, padx=5)
        
        # Botões
        frame_botoes = ttk.Frame(frame_entrada)
        frame_botoes.pack(fill=tk.X, pady=(20, 0))
        
        self.btn_carregar_modelo = ttk.Button(frame_botoes, text="📂 Carregar Modelo", 
                                             command=self.carregar_modelo)
        self.btn_carregar_modelo.pack(side=tk.LEFT, padx=(0, 10))
        
        self.btn_diagnosticar = ttk.Button(frame_botoes, text="🔍 Diagnosticar", 
                                          command=self.realizar_diagnostico, style='Custom.TButton')
        self.btn_diagnosticar.pack(side=tk.LEFT, padx=(0, 10))
        
        self.btn_limpar = ttk.Button(frame_botoes, text="🗑️ Limpar", command=self.limpar_campos)
        self.btn_limpar.pack(side=tk.LEFT)
        
        # Frame direito - Resultados
        frame_resultado = ttk.LabelFrame(aba_diagnostico, text="Resultado do Diagnóstico", padding=15)
        frame_resultado.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Área de resultado
        self.text_resultado = tk.Text(frame_resultado, height=15, width=50, 
                                     font=('Courier', 10), state=tk.DISABLED)
        self.text_resultado.pack(fill=tk.BOTH, expand=True)
        
        # Scrollbar para o texto
        scrollbar = ttk.Scrollbar(frame_resultado, orient=tk.VERTICAL, command=self.text_resultado.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.text_resultado.config(yscrollcommand=scrollbar.set)
    
    def criar_aba_treinamento(self):
        """Cria a aba de treinamento de modelos"""
        aba_treinamento = ttk.Frame(self.notebook)
        self.notebook.add(aba_treinamento, text="🤖 Treinamento")
        
        # Frame principal
        frame_principal = ttk.Frame(aba_treinamento)
        frame_principal.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Título
        titulo = ttk.Label(frame_principal, text="Treinamento de Modelos", style='Subtitle.TLabel')
        titulo.pack(pady=(0, 20))
        
        # Frame para seleção de dataset
        frame_dataset = ttk.LabelFrame(frame_principal, text="Conjunto de Dados", padding=10)
        frame_dataset.pack(fill=tk.X, pady=(0, 15))
        
        ttk.Label(frame_dataset, text="Arquivo CSV:").pack(anchor=tk.W)
        frame_arquivo = ttk.Frame(frame_dataset)
        frame_arquivo.pack(fill=tk.X, pady=(5, 0))
        
        self.entry_arquivo = ttk.Entry(frame_arquivo, state="readonly")
        self.entry_arquivo.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        btn_selecionar = ttk.Button(frame_arquivo, text="Selecionar", command=self.selecionar_dataset)
        btn_selecionar.pack(side=tk.RIGHT)
        
        # Frame para opções de treinamento
        frame_opcoes = ttk.LabelFrame(frame_principal, text="Opções de Treinamento", padding=10)
        frame_opcoes.pack(fill=tk.X, pady=(0, 15))
        
        # Proporção teste
        ttk.Label(frame_opcoes, text="Proporção de Teste (%):").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.scale_teste = ttk.Scale(frame_opcoes, from_=10, to=40, orient=tk.HORIZONTAL, length=200)
        self.scale_teste.set(20)
        self.scale_teste.grid(row=0, column=1, sticky=tk.W, padx=10)
        
        self.label_teste = ttk.Label(frame_opcoes, text="20%")
        self.label_teste.grid(row=0, column=2, sticky=tk.W)
        
        # Atualizar label da escala
        self.scale_teste.configure(command=lambda val: self.label_teste.configure(text=f"{int(float(val))}%"))
        
        # Grid Search
        self.var_grid_search = tk.BooleanVar(value=True)
        cb_grid = ttk.Checkbutton(frame_opcoes, text="Usar Grid Search (mais lento, melhor resultado)", 
                                 variable=self.var_grid_search)
        cb_grid.grid(row=1, column=0, columnspan=3, sticky=tk.W, pady=(10, 0))
        
        # Botões de treinamento
        frame_botoes_treino = ttk.Frame(frame_principal)
        frame_botoes_treino.pack(fill=tk.X, pady=(20, 0))
        
        self.btn_treinar = ttk.Button(frame_botoes_treino, text="🚀 Iniciar Treinamento", 
                                     command=self.iniciar_treinamento, style='Custom.TButton')
        self.btn_treinar.pack(side=tk.LEFT, padx=(0, 10))
        
        btn_parar = ttk.Button(frame_botoes_treino, text="⏹️ Parar", command=self.parar_treinamento)
        btn_parar.pack(side=tk.LEFT)
        
        # Progress bar
        self.progress_treino = ttk.Progressbar(frame_principal, mode='indeterminate')
        self.progress_treino.pack(fill=tk.X, pady=(20, 0))
        
        # Área de log
        frame_log = ttk.LabelFrame(frame_principal, text="Log de Treinamento", padding=10)
        frame_log.pack(fill=tk.BOTH, expand=True, pady=(15, 0))
        
        self.text_log = tk.Text(frame_log, height=10, font=('Courier', 9), state=tk.DISABLED)
        self.text_log.pack(fill=tk.BOTH, expand=True)
    
    def criar_aba_visualizacao(self):
        """Cria a aba de visualização de resultados"""
        aba_visualizacao = ttk.Frame(self.notebook)
        self.notebook.add(aba_visualizacao, text="📊 Visualização")
        
        # Frame principal
        frame_principal = ttk.Frame(aba_visualizacao)
        frame_principal.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Título
        titulo = ttk.Label(frame_principal, text="Visualização de Resultados", style='Subtitle.TLabel')
        titulo.pack(pady=(0, 15))
        
        # Frame para gráficos
        self.frame_graficos = ttk.Frame(frame_principal)
        self.frame_graficos.pack(fill=tk.BOTH, expand=True)
        
        # Placeholder
        placeholder = ttk.Label(self.frame_graficos, 
                               text="📈 Gráficos de resultados aparecerão aqui após o treinamento",
                               font=('Arial', 12))
        placeholder.pack(expand=True)
    
    def criar_aba_sobre(self):
        """Cria a aba sobre o sistema"""
        aba_sobre = ttk.Frame(self.notebook)
        self.notebook.add(aba_sobre, text="ℹ️ Sobre")
        
        # Frame principal
        frame_principal = ttk.Frame(aba_sobre)
        frame_principal.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Título
        titulo = ttk.Label(frame_principal, text="Sistema de Diagnóstico de Doenças", 
                          style='Title.TLabel')
        titulo.pack(pady=(0, 20))
        
        # Informações
        info_text = """
🏥 SISTEMA DE DIAGNÓSTICO DE DOENÇAS

Desenvolvido para o curso de INAR
Faculdade: Terceiro Ano, II Semestre

📋 FUNCIONALIDADES:
• Análise exploratória de dados médicos
• Treinamento de múltiplos algoritmos de ML
• Diagnóstico baseado em sintomas
• Visualização de resultados e métricas
• Interface gráfica amigável

🤖 ALGORITMOS SUPORTADOS:
• Random Forest
• Logistic Regression  
• Support Vector Machine (SVM)
• K-Nearest Neighbors
• Naive Bayes
• Decision Tree
• Gradient Boosting
• XGBoost

📊 MÉTRICAS DE AVALIAÇÃO:
• Accuracy, Precision, Recall, F1-Score
• Matriz de Confusão
• Curvas ROC e Precisão-Recall
• Cross-validation

⚠️ AVISO IMPORTANTE:
Este sistema é apenas para fins educacionais.
Não deve ser usado para diagnósticos médicos reais.
Sempre consulte um profissional de saúde qualificado.
        """
        
        label_info = ttk.Label(frame_principal, text=info_text, font=('Arial', 10), 
                              justify=tk.LEFT)
        label_info.pack(anchor=tk.W)
    
    def tentar_carregar_modelo_automatico(self):
        """Tenta carregar automaticamente o melhor modelo salvo"""
        caminho_modelo = os.path.join(os.path.dirname(__file__), '..', '..', 'modelos_salvos', 'melhor_modelo.pkl')
        caminho_preprocessador = os.path.join(os.path.dirname(__file__), '..', '..', 'modelos_salvos')
        
        if os.path.exists(caminho_modelo):
            try:
                self.modelo_carregado = joblib.load(caminho_modelo)
                
                # Tentar carregar preprocessador
                if os.path.exists(os.path.join(caminho_preprocessador, 'encoders.pkl')):
                    sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'utils'))
                    from preprocessador import PreProcessadorDados
                    self.preprocessador = PreProcessadorDados(pd.DataFrame())  # Dummy DataFrame
                    self.preprocessador.carregar_preprocessadores(caminho_preprocessador)
                
                self.status_modelo.configure(text="✅ Modelo carregado automaticamente", 
                                           style='Success.TLabel')
                
            except Exception as e:
                print(f"Erro ao carregar modelo automático: {str(e)}")
    
    def carregar_modelo(self):
        """Carrega um modelo salvo"""
        arquivo_modelo = filedialog.askopenfilename(
            title="Selecionar Modelo",
            filetypes=[("Arquivos PKL", "*.pkl"), ("Todos os arquivos", "*.*")]
        )
        
        if arquivo_modelo:
            try:
                self.modelo_carregado = joblib.load(arquivo_modelo)
                self.status_modelo.configure(text=f"✅ Modelo carregado: {os.path.basename(arquivo_modelo)}", 
                                           style='Success.TLabel')
                
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao carregar modelo: {str(e)}")
    
    def selecionar_dataset(self):
        """Seleciona o arquivo de dataset"""
        arquivo = filedialog.askopenfilename(
            title="Selecionar Conjunto de Dados",
            filetypes=[("Arquivos CSV", "*.csv"), ("Todos os arquivos", "*.*")]
        )
        
        if arquivo:
            self.entry_arquivo.configure(state=tk.NORMAL)
            self.entry_arquivo.delete(0, tk.END)
            self.entry_arquivo.insert(0, arquivo)
            self.entry_arquivo.configure(state="readonly")
    
    def iniciar_treinamento(self):
        """Inicia o processo de treinamento"""
        if not self.entry_arquivo.get():
            # Usar dataset padrão se não selecionado
            dataset_padrao = os.path.join(os.path.dirname(__file__), '..', '..', 'dataset', 'Disease_symptom_and_patient_profile_dataset.csv')
            if os.path.exists(dataset_padrao):
                self.entry_arquivo.configure(state=tk.NORMAL)
                self.entry_arquivo.delete(0, tk.END)
                self.entry_arquivo.insert(0, dataset_padrao)
                self.entry_arquivo.configure(state="readonly")
            else:
                messagebox.showerror("Erro", "Selecione um arquivo de dataset primeiro.")
                return
        
        # Executar treinamento em thread separada
        self.progress_treino.start()
        self.btn_treinar.configure(state=tk.DISABLED)
        
        thread_treino = threading.Thread(target=self.executar_treinamento)
        thread_treino.daemon = True
        thread_treino.start()
    
    def executar_treinamento(self):
        """Executa o treinamento em background"""
        try:
            self.adicionar_log("🚀 Iniciando treinamento...")
            
            # Adicionar paths dos módulos
            sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'utils'))
            sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'models'))
            
            # Importar módulos necessários
            from carregador_dados import CarregadorDados
            from preprocessador import PreProcessadorDados
            from treinador_modelos import TreinadorModelos
            
            # Carregar dados
            self.adicionar_log("📂 Carregando dados...")
            carregador = CarregadorDados(self.entry_arquivo.get())
            dados = carregador.carregar_dados()
            
            # Pré-processar
            self.adicionar_log("🔧 Pré-processando dados...")
            preprocessador = PreProcessadorDados(dados)
            dados_processados = preprocessador.processar_dados_completo(
                test_size=int(self.scale_teste.get())/100
            )
            
            # Treinar modelos
            self.adicionar_log("🤖 Treinando modelos...")
            treinador = TreinadorModelos()
            resultados = treinador.treinar_todos_modelos(
                dados_processados['X_train'],
                dados_processados['y_train'],
                usar_grid_search=self.var_grid_search.get()
            )
            
            # Salvar modelos
            self.adicionar_log("💾 Salvando modelos...")
            caminho_salvar = os.path.join(os.path.dirname(__file__), '..', '..', 'modelos_salvos')
            os.makedirs(caminho_salvar, exist_ok=True)
            treinador.salvar_modelos(caminho_salvar)
            preprocessador.salvar_preprocessadores(caminho_salvar)
            
            # Avaliar modelos
            self.adicionar_log("📊 Avaliando modelos...")
            ranking = treinador.obter_ranking_modelos(
                dados_processados['X_test'],
                dados_processados['y_test']
            )
            
            self.adicionar_log("\n🏆 RANKING DOS MODELOS:")
            self.adicionar_log(str(ranking))
            
            self.adicionar_log("\n✅ Treinamento concluído com sucesso!")
            
            # Tentar carregar o melhor modelo automaticamente
            self.tentar_carregar_modelo_automatico()
            
        except Exception as e:
            self.adicionar_log(f"❌ Erro durante treinamento: {str(e)}")
        
        finally:
            # Atualizar interface na thread principal
            self.root.after(0, self.finalizar_treinamento)
    
    def finalizar_treinamento(self):
        """Finaliza o treinamento na thread principal"""
        self.progress_treino.stop()
        self.btn_treinar.configure(state=tk.NORMAL)
    
    def parar_treinamento(self):
        """Para o treinamento"""
        self.adicionar_log("⏹️ Treinamento interrompido pelo usuário")
        self.finalizar_treinamento()
    
    def adicionar_log(self, texto: str):
        """Adiciona texto ao log de treinamento"""
        def _adicionar():
            self.text_log.configure(state=tk.NORMAL)
            self.text_log.insert(tk.END, texto + "\n")
            self.text_log.see(tk.END)
            self.text_log.configure(state=tk.DISABLED)
        
        # Garantir que a atualização aconteça na thread principal
        if hasattr(self, 'root'):
            self.root.after(0, _adicionar)
    
    def coletar_dados_paciente(self) -> Dict:
        """Coleta os dados inseridos pelo usuário"""
        try:
            dados = {
                'Fever': 'Yes' if self.var_febre.get() else 'No',
                'Cough': 'Yes' if self.var_tosse.get() else 'No', 
                'Fatigue': 'Yes' if self.var_fadiga.get() else 'No',
                'Difficulty Breathing': 'Yes' if self.var_dificuldade_respirar.get() else 'No',
                'Age': int(self.entry_idade.get()) if self.entry_idade.get() else 0,
                'Gender': self.combo_genero.get() if self.combo_genero.get() else 'Male',
                'Blood Pressure': self.combo_pressao.get() if self.combo_pressao.get() else 'Normal',
                'Cholesterol Level': self.combo_colesterol.get() if self.combo_colesterol.get() else 'Normal'
            }
            return dados
            
        except ValueError as e:
            raise ValueError("Por favor, verifique se a idade está correta")
    
    def realizar_diagnostico(self):
        """Realiza o diagnóstico baseado nos dados inseridos"""
        if not self.modelo_carregado:
            messagebox.showerror("Erro", "Nenhum modelo carregado. Carregue um modelo primeiro.")
            return
        
        try:
            # Coletar dados
            dados_paciente = self.coletar_dados_paciente()
            
            # Criar DataFrame
            df_paciente = pd.DataFrame([dados_paciente])
            
            # Pré-processar se preprocessador disponível
            if self.preprocessador:
                df_processado = self.preprocessador.preprocessar_novos_dados(df_paciente)
            else:
                # Processamento básico sem preprocessador salvo
                df_processado = self.processar_dados_basico(df_paciente)
            
            # Fazer predição
            predicao = self.modelo_carregado.predict(df_processado)[0]
            
            # Obter probabilidades se disponível
            probabilidades = None
            if hasattr(self.modelo_carregado, 'predict_proba'):
                prob = self.modelo_carregado.predict_proba(df_processado)[0]
                probabilidades = {'Negativo': prob[0], 'Positivo': prob[1]}
            
            # Exibir resultado
            self.exibir_resultado_diagnostico(dados_paciente, predicao, probabilidades)
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao realizar diagnóstico: {str(e)}")
    
    def processar_dados_basico(self, df: pd.DataFrame) -> pd.DataFrame:
        """Processamento básico sem preprocessador salvo"""
        df_proc = df.copy()
        
        # Codificar sintomas
        sintomas = ['Fever', 'Cough', 'Fatigue', 'Difficulty Breathing']
        for sintoma in sintomas:
            df_proc[sintoma] = df_proc[sintoma].map({'Yes': 1, 'No': 0})
        
        # Codificar gênero
        df_proc['Gender'] = df_proc['Gender'].map({'Male': 1, 'Female': 0})
        
        # Codificar pressão arterial (português e inglês)
        mapeamento_pressao = {'Baixa': 0, 'Normal': 1, 'Alta': 2, 'Low': 0, 'High': 2}
        df_proc['Blood Pressure'] = df_proc['Blood Pressure'].map(mapeamento_pressao)
        
        # Codificar colesterol (português e inglês)
        mapeamento_colesterol = {'Baixo': 0, 'Normal': 1, 'Alto': 2, 'Low': 0, 'High': 2}
        df_proc['Cholesterol Level'] = df_proc['Cholesterol Level'].map(mapeamento_colesterol)
        
        return df_proc
    
    def exibir_resultado_diagnostico(self, dados_paciente: Dict, predicao: int, probabilidades: Dict = None):
        """Exibe o resultado do diagnóstico"""
        resultado_texto = "RESULTADO DO DIAGNÓSTICO\n"
        resultado_texto += "=" * 40 + "\n\n"
        
        # Dados do paciente
        resultado_texto += "DADOS DO PACIENTE:\n"
        resultado_texto += f"• Idade: {dados_paciente['Age']} anos\n"
        resultado_texto += f"• Gênero: {dados_paciente['Gender']}\n"
        resultado_texto += f"• Pressão Arterial: {dados_paciente['Blood Pressure']}\n"
        resultado_texto += f"• Colesterol: {dados_paciente['Cholesterol Level']}\n\n"
        
        # Sintomas
        resultado_texto += "SINTOMAS REPORTADOS:\n"
        sintomas = {
            'Fever': 'Febre',
            'Cough': 'Tosse', 
            'Fatigue': 'Fadiga',
            'Difficulty Breathing': 'Dificuldade para Respirar'
        }
        
        for sintoma_en, sintoma_pt in sintomas.items():
            status = "✅ Sim" if dados_paciente[sintoma_en] == 'Yes' else "❌ Não"
            resultado_texto += f"• {sintoma_pt}: {status}\n"
        
        resultado_texto += "\n" + "=" * 40 + "\n"
        
        # Resultado da predição
        resultado_final = "POSITIVO" if predicao == 1 else "NEGATIVO"
        cor_resultado = "🔴" if predicao == 1 else "🟢"
        
        resultado_texto += f"RESULTADO: {cor_resultado} {resultado_final}\n\n"
        
        # Probabilidades
        if probabilidades:
            resultado_texto += "CONFIANÇA DO MODELO:\n"
            resultado_texto += f"• Probabilidade Negativa: {probabilidades['Negativo']:.2%}\n"
            resultado_texto += f"• Probabilidade Positiva: {probabilidades['Positivo']:.2%}\n\n"
        
        # Aviso
        resultado_texto += "⚠️  AVISO IMPORTANTE:\n"
        resultado_texto += "Este resultado é apenas uma estimativa\n"
        resultado_texto += "baseada em dados históricos.\n"
        resultado_texto += "Sempre consulte um médico para\n"
        resultado_texto += "diagnóstico e tratamento adequados.\n"
        
        # Atualizar interface
        self.text_resultado.configure(state=tk.NORMAL)
        self.text_resultado.delete(1.0, tk.END)
        self.text_resultado.insert(1.0, resultado_texto)
        self.text_resultado.configure(state=tk.DISABLED)
    
    def limpar_campos(self):
        """Limpa todos os campos da interface"""
        # Limpar sintomas
        self.var_febre.set(False)
        self.var_tosse.set(False) 
        self.var_fadiga.set(False)
        self.var_dificuldade_respirar.set(False)
        
        # Limpar demográficos
        self.entry_idade.delete(0, tk.END)
        self.combo_genero.set('')
        
        # Limpar clínicos
        self.combo_pressao.set('')
        self.combo_colesterol.set('')
        
        # Limpar resultado
        self.text_resultado.configure(state=tk.NORMAL)
        self.text_resultado.delete(1.0, tk.END)
        self.text_resultado.configure(state=tk.DISABLED)
    
    def executar(self):
        """Executa a aplicação"""
        self.root.mainloop()

def main():
    """Função principal"""
    try:
        app = SistemaDiagnostico()
        app.executar()
    except Exception as e:
        print(f"Erro ao iniciar aplicação: {e}")
        messagebox.showerror("Erro Fatal", f"Erro ao iniciar aplicação: {e}")

if __name__ == "__main__":
    main()