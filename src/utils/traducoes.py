"""
Dicionário de traduções de sintomas e doenças para português
Sistema de Diagnóstico Médico Simplificado
"""

# Traduções de sintomas (inglês -> português)
TRADUCOES_SINTOMAS = {
    # Sintomas gerais
    'itching': 'coceira',
    'skin_rash': 'erupção cutânea',
    'nodal_skin_eruptions': 'erupções cutâneas nodulares',
    'dischromic _patches': 'manchas descoloridas',
    'continuous_sneezing': 'espirros contínuos',
    'shivering': 'tremores',
    'chills': 'calafrios',
    'joint_pain': 'dor nas articulações',
    'stomach_pain': 'dor de estômago',
    'acidity': 'acidez',
    'ulcers_on_tongue': 'úlceras na língua',
    'muscle_wasting': 'atrofia muscular',
    'vomiting': 'vômito',
    'burning_micturition': 'micção ardente',
    'spotting_ urination': 'urina com manchas',
    'fatigue': 'fadiga',
    'weight_gain': 'ganho de peso',
    'anxiety': 'ansiedade',
    'cold_hands_and_feets': 'mãos e pés frios',
    'mood_swings': 'mudanças de humor',
    'weight_loss': 'perda de peso',
    'restlessness': 'inquietação',
    'lethargy': 'letargia',
    'patches_in_throat': 'manchas na garganta',
    'irregular_sugar_level': 'nível irregular de açúcar',
    'cough': 'tosse',
    'high_fever': 'febre alta',
    'sunken_eyes': 'olhos fundos',
    'breathlessness': 'falta de ar',
    'sweating': 'sudorese',
    'dehydration': 'desidratação',
    'indigestion': 'indigestão',
    'headache': 'dor de cabeça',
    'yellowish_skin': 'pele amarelada',
    'dark_urine': 'urina escura',
    'nausea': 'náusea',
    'loss_of_appetite': 'perda de apetite',
    'pain_behind_the_eyes': 'dor atrás dos olhos',
    'back_pain': 'dor nas costas',
    'constipation': 'constipação',
    'abdominal_pain': 'dor abdominal',
    'diarrhoea': 'diarreia',
    'mild_fever': 'febre leve',
    'yellow_urine': 'urina amarela',
    'yellowing_of_eyes': 'amarelamento dos olhos',
    'acute_liver_failure': 'insuficiência hepática aguda',
    'fluid_overload': 'sobrecarga de fluidos',
    'swelling_of_stomach': 'inchaço do estômago',
    'swelled_lymph_nodes': 'linfonodos inchados',
    'malaise': 'mal-estar',
    'blurred_and_distorted_vision': 'visão turva e distorcida',
    'phlegm': 'catarro',
    'throat_irritation': 'irritação na garganta',
    'redness_of_eyes': 'vermelhidão dos olhos',
    'sinus_pressure': 'pressão sinusal',
    'runny_nose': 'nariz escorrendo',
    'congestion': 'congestão',
    'chest_pain': 'dor no peito',
    'weakness_in_limbs': 'fraqueza nos membros',
    'fast_heart_rate': 'batimento cardíaco acelerado',
    'pain_during_bowel_movements': 'dor durante evacuações',
    'pain_in_anal_region': 'dor na região anal',
    'bloody_stool': 'fezes com sangue',
    'irritation_in_anus': 'irritação no ânus',
    'neck_pain': 'dor no pescoço',
    'dizziness': 'tontura',
    'cramps': 'cólicas',
    'bruising': 'hematomas',
    'obesity': 'obesidade',
    'swollen_legs': 'pernas inchadas',
    'swollen_blood_vessels': 'vasos sanguíneos inchados',
    'puffy_face_and_eyes': 'rosto e olhos inchados',
    'enlarged_thyroid': 'tireoide aumentada',
    'brittle_nails': 'unhas quebradiças',
    'swollen_extremeties': 'extremidades inchadas',
    'excessive_hunger': 'fome excessiva',
    'extra_marital_contacts': 'contatos extraconjugais',
    'drying_and_tingling_lips': 'lábios secos e formigando',
    'slurred_speech': 'fala arrastada',
    'knee_pain': 'dor no joelho',
    'hip_joint_pain': 'dor na articulação do quadril',
    'muscle_weakness': 'fraqueza muscular',
    'stiff_neck': 'pescoço rígido',
    'swelling_joints': 'articulações inchadas',
    'movement_stiffness': 'rigidez de movimento',
    'spinning_movements': 'movimentos giratórios',
    'loss_of_balance': 'perda de equilíbrio',
    'unsteadiness': 'instabilidade',
    'weakness_of_one_body_side': 'fraqueza de um lado do corpo',
    'loss_of_smell': 'perda do olfato',
    'bladder_discomfort': 'desconforto na bexiga',
    'foul_smell_of urine': 'odor forte na urina',
    'continuous_feel_of_urine': 'sensação contínua de urina',
    'passage_of_gases': 'passagem de gases',
    'internal_itching': 'coceira interna',
    'toxic_look_(typhos)': 'aparência tóxica (tifoide)',
    'depression': 'depressão',
    'irritability': 'irritabilidade',
    'muscle_pain': 'dor muscular',
    'altered_sensorium': 'alteração do sensório',
    'red_spots_over_body': 'manchas vermelhas pelo corpo',
    'belly_pain': 'dor na barriga',
    'abnormal_menstruation': 'menstruação anormal',
    'dischromic_patches': 'manchas descoloridas',
    'watering_from_eyes': 'lacrimejamento',
    'increased_appetite': 'aumento do apetite',
    'polyuria': 'poliúria',
    'family_history': 'histórico familiar',
    'mucoid_sputum': 'escarro mucoide',
    'rusty_sputum': 'escarro ferruginoso',
    'lack_of_concentration': 'falta de concentração',
    'visual_disturbances': 'distúrbios visuais',
    'receiving_blood_transfusion': 'recebendo transfusão de sangue',
    'receiving_unsterile_injections': 'recebendo injeções não estéreis',
    'coma': 'coma',
    'stomach_bleeding': 'sangramento no estômago',
    'distention_of_abdomen': 'distensão do abdômen',
    'history_of_alcohol_consumption': 'histórico de consumo de álcool',
    'fluid_overload.1': 'sobrecarga de fluidos',
    'blood_in_sputum': 'sangue no escarro',
    'prominent_veins_on_calf': 'veias proeminentes na panturrilha',
    'palpitations': 'palpitações',
    'painful_walking': 'caminhada dolorosa',
    'pus_filled_pimples': 'espinhas com pus',
    'blackheads': 'cravos',
    'scurring': 'cicatrização',
    'skin_peeling': 'descamação da pele',
    'silver_like_dusting': 'poeira prateada',
    'small_dents_in_nails': 'pequenos buracos nas unhas',
    'inflammatory_nails': 'unhas inflamadas',
    'blister': 'bolha',
    'red_sore_around_nose': 'ferida vermelha ao redor do nariz',
    'yellow_crust_ooze': 'crosta amarela escorrendo',
    'prognosis': 'prognóstico'
}

# Traduções de doenças (inglês -> português)
TRADUCOES_DOENCAS = {
    'Fungal infection': 'Infecção fúngica',
    'Allergy': 'Alergia',
    'GERD': 'Refluxo gastroesofágico',
    'Chronic cholestasis': 'Colestase crônica',
    'Drug Reaction': 'Reação medicamentosa',
    'Peptic ulcer diseae': 'Doença ulcerosa péptica',
    'AIDS': 'AIDS',
    'Diabetes': 'Diabetes',
    'Gastroenteritis': 'Gastroenterite',
    'Bronchial Asthma': 'Asma brônquica',
    'Hypertension': 'Hipertensão',
    'Migraine': 'Enxaqueca',
    'Cervical spondylosis': 'Espondiloses cervical',
    'Paralysis (brain hemorrhage)': 'Paralisia (hemorragia cerebral)',
    'Jaundice': 'Icterícia',
    'Malaria': 'Malária',
    'Chicken pox': 'Catapora',
    'Dengue': 'Dengue',
    'Typhoid': 'Febre tifoide',
    'hepatitis A': 'Hepatite A',
    'Hepatitis B': 'Hepatite B',
    'Hepatitis C': 'Hepatite C',
    'Hepatitis D': 'Hepatite D',
    'Hepatitis E': 'Hepatite E',
    'Alcoholic hepatitis': 'Hepatite alcoólica',
    'Tuberculosis': 'Tuberculose',
    'Common Cold': 'Resfriado comum',
    'Pneumonia': 'Pneumonia',
    'Dimorphic hemmorhoids(piles)': 'Hemorroidas dimórficas',
    'Heart attack': 'Infarto do coração',
    'Varicose veins': 'Varizes',
    'Hypothyroidism': 'Hipotireoidismo',
    'Hyperthyroidism': 'Hipertireoidismo',
    'Hypoglycemia': 'Hipoglicemia',
    'Osteoarthristis': 'Osteoartrite',
    'Arthritis': 'Artrite',
    '(vertigo) Paroymsal  Positional Vertigo': 'Vertigem posicional paroxística',
    'Acne': 'Acne',
    'Urinary tract infection': 'Infecção do trato urinário',
    'Psoriasis': 'Psoríase',
    'Impetigo': 'Impetigo'
}

def traduzir_sintoma(sintoma_ingles):
    """
    Traduz um sintoma do inglês para o português
    
    Args:
        sintoma_ingles (str): Sintoma em inglês
        
    Returns:
        str: Sintoma traduzido para português
    """
    # Limpar espaços e normalizar
    sintoma_limpo = sintoma_ingles.strip().lower()
    
    # Buscar tradução
    if sintoma_limpo in TRADUCOES_SINTOMAS:
        return TRADUCOES_SINTOMAS[sintoma_limpo].title()
    
    # Se não encontrar, retornar o original formatado
    return sintoma_ingles.replace('_', ' ').title()

def traduzir_doenca(doenca_ingles):
    """
    Traduz uma doença do inglês para o português
    
    Args:
        doenca_ingles (str): Doença em inglês
        
    Returns:
        str: Doença traduzida para português
    """
    doenca_limpa = doenca_ingles.strip()
    
    if doenca_limpa in TRADUCOES_DOENCAS:
        return TRADUCOES_DOENCAS[doenca_limpa]
    
    # Se não encontrar, retornar o original
    return doenca_ingles

def traduzir_lista_sintomas(lista_sintomas):
    """
    Traduz uma lista de sintomas
    
    Args:
        lista_sintomas (list): Lista de sintomas em inglês
        
    Returns:
        list: Lista de sintomas traduzidos
    """
    return [traduzir_sintoma(sintoma) for sintoma in lista_sintomas if sintoma.strip()]

def obter_todas_traducoes_sintomas():
    """
    Retorna todas as traduções de sintomas disponíveis
    
    Returns:
        dict: Dicionário com traduções
    """
    return TRADUCOES_SINTOMAS.copy()

def obter_todas_traducoes_doencas():
    """
    Retorna todas as traduções de doenças disponíveis
    
    Returns:
        dict: Dicionário com traduções
    """
    return TRADUCOES_DOENCAS.copy()

# Textos da interface em português
TEXTOS_INTERFACE = {
    'titulo_principal': 'Sistema de Diagnóstico Médico',
    'subtitulo': 'Versão Simplificada',
    'aba_diagnostico': '🩺 Diagnóstico',
    'aba_estatisticas': '📊 Estatísticas',
    'aba_historico': '📋 Histórico',
    'selecionar_sintomas': 'Selecionar Sintomas',
    'buscar_sintoma': 'Buscar sintoma:',
    'adicionar_selecionados': 'Adicionar Selecionados',
    'limpar_selecao': 'Limpar Seleção',
    'sintomas_selecionados': 'Sintomas Selecionados',
    'realizar_diagnostico': '🔍 Realizar Diagnóstico',
    'resultados_diagnostico': 'Resultados do Diagnóstico',
    'nenhum_sintoma_selecionado': 'Nenhum sintoma selecionado.',
    'sistema_carregado': 'Sistema carregado com sucesso!',
    'erro_carregar_dados': '❌ Erro ao carregar dados do sistema',
    'sintomas_carregados': 'sintomas carregados',
    'selecione_sintomas': 'Selecione pelo menos um sintoma para realizar o diagnóstico.',
    'diagnostico_realizado': 'Diagnóstico realizado com sucesso',
    'top_3_diagnosticos': '🏥 TOP 3 DIAGNÓSTICOS MAIS PROVÁVEIS:',
    'nivel_confianca': 'Nível de confiança',
    'probabilidade': 'Probabilidade',
    'sintomas_em_comum': 'Sintomas em comum',
    'sintomas_coincidentes': 'Sintomas coincidentes',
    'nenhum_diagnostico': '⚠️ Nenhum diagnóstico encontrado com os sintomas informados.',
    'aviso_medico': 'IMPORTANTE: Este é um sistema de apoio ao diagnóstico.\nSempre consulte um médico profissional para\nconfirmação e tratamento adequado.',
    'informacoes_sistema': 'Informações do Sistema',
    'atualizar_estatisticas': '🔄 Atualizar Estatísticas',
    'historico_diagnosticos': 'Histórico de Diagnósticos',
    'diagnosticos_realizados': 'Diagnósticos Realizados',
    'atualizar_historico': '🔄 Atualizar Histórico',
    'limpar_historico': '🗑️ Limpar Histórico',
    'nenhum_diagnostico_historico': '📋 Nenhum diagnóstico realizado ainda.',
    'confirmar_limpar': 'Deseja realmente limpar todo o histórico?',
    'historico_limpo': '✅ Histórico limpo'
}

def obter_texto_interface(chave):
    """
    Obtém texto da interface em português
    
    Args:
        chave (str): Chave do texto
        
    Returns:
        str: Texto em português
    """
    return TEXTOS_INTERFACE.get(chave, chave)