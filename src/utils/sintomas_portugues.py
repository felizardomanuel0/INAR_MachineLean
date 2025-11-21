"""
Sistema de Sintomas em Português
Gerencia sintomas, traduções e entrada manual
"""

# Lista completa de sintomas em português (baseada no novo dataset)
SINTOMAS_DISPONIVEIS = [
    # Sintomas Gerais e Sistêmicos
    'Febre',
    'Febre Alta', 
    'Febre Leve',
    'Tosse', 
    'Fadiga',
    'Letargia',
    'Mal-estar',
    'Dificuldade para Respirar',
    'Falta de Ar',
    'Dor de Cabeça',
    'Dor no Corpo',
    'Dor Muscular',
    'Fraqueza Muscular',
    'Atrofia Muscular',
    'Calafrios',
    'Tremores',
    'Suor',
    'Desidratação',
    'Perda de Peso',
    'Ganho de Peso',
    'Perda de Apetite',
    'Aumento do Apetite',
    'Náusea',
    'Vômito',
    'Diarreia',
    'Constipação',
    'Dor Abdominal',
    'Dor de Estômago',
    'Inchaço do Estômago',
    'Indigestão',
    'Acidez',
    'Sangramento do Estômago',
    
    # Sintomas Respiratórios
    'Chiado no Peito',
    'Dor no Peito',
    'Pressão no Peito',
    'Tosse com Sangue',
    'Sangue no Escarro',
    'Escarro Mucoso',
    'Escarro Ferrugem',
    'Congestão',
    'Congestão Nasal',
    'Coriza',
    'Espirros Contínuos',
    'Dor de Garganta',
    'Irritação na Garganta',
    'Manchas na Garganta',
    'Pressão nos Seios da Face',
    'Catarro',
    
    # Sintomas Neurológicos e Mentais
    'Tontura',
    'Vertigem',
    'Movimentos Giratórios',
    'Perda de Equilíbrio',
    'Instabilidade',
    'Confusão Mental',
    'Alteração do Sensório',
    'Perda de Memória',
    'Falta de Concentração',
    'Convulsões',
    'Tremores',
    'Fraqueza nos Membros',
    'Fraqueza de um Lado do Corpo',
    'Dormência',
    'Formigamento',
    'Rigidez no Pescoço',
    'Dor no Pescoço',
    'Fala Arrastada',
    'Lábios Secos e Formigando',
    'Coma',
    
    # Sintomas Psicológicos
    'Ansiedade',
    'Depressão',
    'Irritabilidade',
    'Inquietação',
    'Mudanças de Humor',
    
    # Sintomas Cardiovasculares
    'Palpitações',
    'Batimento Cardíaco Rápido',
    'Batimento Cardíaco Irregular',
    'Inchaço nas Pernas',
    'Inchaço nas Extremidades',
    'Vasos Sanguíneos Inchados',
    'Veias Proeminentes na Panturrilha',
    'Pressão no Peito',
    'Mãos e Pés Frios',
    
    # Sintomas Dermatológicos
    'Coceira',
    'Erupção Cutânea',
    'Erupções Cutâneas Nodulares',
    'Vermelhidão na Pele',
    'Vermelhidão dos Olhos',
    'Feridas na Pele',
    'Feridas Vermelhas ao Redor do Nariz',
    'Mudança na Cor da Pele',
    'Pele Amarelada',
    'Amarelamento dos Olhos',
    'Manchas Descoloridas',
    'Descamação da Pele',
    'Poeira Prateada',
    'Bolhas',
    'Pequenas Depressões nas Unhas',
    'Unhas Inflamatórias',
    'Unhas Quebradiças',
    'Crosta Amarela que Escorre',
    'Cicatrizes',
    'Espinhas com Pus',
    'Cravos',
    'Aparência Tóxica (Tifo)',
    
    # Sintomas Musculoesqueléticos
    'Dor nas Articulações',
    'Dor no Joelho',
    'Dor no Quadril',
    'Rigidez Articular',
    'Rigidez de Movimento',
    'Dor Muscular',
    'Inchaço nas Articulações',
    'Dor nas Costas',
    'Cãibras',
    'Hematomas',
    'Caminhada Dolorosa',
    
    # Sintomas Urológicos
    'Micção Ardente',
    'Micção com Manchas',
    'Dor ao Urinar',
    'Sangue na Urina',
    'Urina Amarela',
    'Urina Escura',
    'Micção Frequente',
    'Poliúria',
    'Dificuldade para Urinar',
    'Desconforto na Bexiga',
    'Mau Cheiro da Urina',
    'Sensação Contínua de Urina',
    'Passagem de Gases',
    'Coceira Interna',
    
    # Sintomas Oftalmológicos
    'Visão Turva e Distorcida',
    'Distúrbios Visuais',
    'Dor nos Olhos',
    'Vermelhidão nos Olhos',
    'Lacrimejamento',
    'Sensibilidade à Luz',
    'Olhos Fundos',
    'Rosto e Olhos Inchados',
    
    # Sintomas Auditivos
    'Zumbido no Ouvido',
    'Perda Auditiva',
    'Dor de Ouvido',
    
    # Sintomas Digestivos e Abdominais
    'Úlceras na Língua',
    'Dor na Região Anal',
    'Irritação no Ânus',
    'Fezes com Sangue',
    'Dor Durante Evacuação',
    'Distensão Abdominal',
    'Dor de Barriga',
    
    # Sintomas Endócrinos e Metabólicos
    'Nível Irregular de Açúcar',
    'Obesidade',
    'Fome Excessiva',
    'Tireoide Aumentada',
    'Contatos Extramaritais',
    
    # Sintomas Hematológicos
    'Linfonodos Inchados',
    'Sobrecarga de Fluidos',
    'Transfusão de Sangue',
    'Injeções Não Estéreis',
    'Veias Proeminentes na Panturrilha',
    
    # Sintomas Hepáticos
    'Falência Hepática Aguda',
    'Histórico de Consumo de Álcool',
    
    # Sintomas Hereditários e Histórico
    'Histórico Familiar',
    
    # Sintomas Psicológicos
    'Insônia',
    'Sonolência Excessiva',
    
    # Outros Sintomas Específicos
    'Prognóstico'
]

# Tradução completa de sintomas (português -> inglês baseado no novo dataset)
TRADUCAO_SINTOMAS = {
    # Sintomas Gerais
    'Coceira': 'itching',
    'Erupção Cutânea': 'skin_rash',
    'Erupções Cutâneas Nodulares': 'nodal_skin_eruptions',
    'Espirros Contínuos': 'continuous_sneezing',
    'Tremores': 'shivering',
    'Calafrios': 'chills',
    'Dor nas Articulações': 'joint_pain',
    'Dor de Estômago': 'stomach_pain',
    'Acidez': 'acidity',
    'Úlceras na Língua': 'ulcers_on_tongue',
    'Atrofia Muscular': 'muscle_wasting',
    'Vômito': 'vomiting',
    'Micção Ardente': 'burning_micturition',
    'Micção com Manchas': 'spotting_urination',
    'Fadiga': 'fatigue',
    'Ganho de Peso': 'weight_gain',
    'Ansiedade': 'anxiety',
    'Mãos e Pés Frios': 'cold_hands_and_feets',
    'Mudanças de Humor': 'mood_swings',
    'Perda de Peso': 'weight_loss',
    'Inquietação': 'restlessness',
    'Letargia': 'lethargy',
    'Manchas na Garganta': 'patches_in_throat',
    'Nível Irregular de Açúcar': 'irregular_sugar_level',
    'Tosse': 'cough',
    'Febre Alta': 'high_fever',
    'Olhos Fundos': 'sunken_eyes',
    'Falta de Ar': 'breathlessness',
    'Suor': 'sweating',
    'Desidratação': 'dehydration',
    'Indigestão': 'indigestion',
    'Dor de Cabeça': 'headache',
    'Pele Amarelada': 'yellowish_skin',
    'Urina Escura': 'dark_urine',
    'Náusea': 'nausea',
    'Perda de Apetite': 'loss_of_appetite',
    'Dor Atrás dos Olhos': 'pain_behind_the_eyes',
    'Dor nas Costas': 'back_pain',
    'Constipação': 'constipation',
    'Dor Abdominal': 'abdominal_pain',
    'Diarreia': 'diarrhoea',
    'Febre Leve': 'mild_fever',
    'Urina Amarela': 'yellow_urine',
    'Amarelamento dos Olhos': 'yellowing_of_eyes',
    'Falência Hepática Aguda': 'acute_liver_failure',
    'Sobrecarga de Fluidos': 'fluid_overload',
    'Inchaço do Estômago': 'swelling_of_stomach',
    'Linfonodos Inchados': 'swelled_lymph_nodes',
    'Mal-estar': 'malaise',
    'Visão Turva e Distorcida': 'blurred_and_distorted_vision',
    'Catarro': 'phlegm',
    'Irritação na Garganta': 'throat_irritation',
    'Vermelhidão dos Olhos': 'redness_of_eyes',
    'Pressão nos Seios da Face': 'sinus_pressure',
    'Coriza': 'runny_nose',
    'Congestão': 'congestion',
    'Dor no Peito': 'chest_pain',
    'Fraqueza nos Membros': 'weakness_in_limbs',
    'Batimento Cardíaco Rápido': 'fast_heart_rate',
    'Dor Durante Evacuação': 'pain_during_bowel_movements',
    'Dor na Região Anal': 'pain_in_anal_region',
    'Fezes com Sangue': 'bloody_stool',
    'Irritação no Ânus': 'irritation_in_anus',
    'Dor no Pescoço': 'neck_pain',
    'Tontura': 'dizziness',
    'Cãibras': 'cramps',
    'Hematomas': 'bruising',
    'Obesidade': 'obesity',
    'Inchaço nas Pernas': 'swollen_legs',
    'Vasos Sanguíneos Inchados': 'swollen_blood_vessels',
    'Rosto e Olhos Inchados': 'puffy_face_and_eyes',
    'Tireoide Aumentada': 'enlarged_thyroid',
    'Unhas Quebradiças': 'brittle_nails',
    'Inchaço nas Extremidades': 'swollen_extremeties',
    'Fome Excessiva': 'excessive_hunger',
    'Contatos Extramaritais': 'extra_marital_contacts',
    'Lábios Secos e Formigando': 'drying_and_tingling_lips',
    'Fala Arrastada': 'slurred_speech',
    'Dor no Joelho': 'knee_pain',
    'Dor no Quadril': 'hip_joint_pain',
    'Fraqueza Muscular': 'muscle_weakness',
    'Rigidez no Pescoço': 'stiff_neck',
    'Inchaço nas Articulações': 'swelling_joints',
    'Rigidez de Movimento': 'movement_stiffness',
    'Movimentos Giratórios': 'spinning_movements',
    'Perda de Equilíbrio': 'loss_of_balance',
    'Instabilidade': 'unsteadiness',
    'Fraqueza de um Lado do Corpo': 'weakness_of_one_body_side',
    'Perda do Olfato': 'loss_of_smell',
    'Desconforto na Bexiga': 'bladder_discomfort',
    'Mau Cheiro da Urina': 'foul_smell_ofurine',
    'Sensação Contínua de Urina': 'continuous_feel_of_urine',
    'Passagem de Gases': 'passage_of_gases',
    'Coceira Interna': 'internal_itching',
    'Aparência Tóxica (Tifo)': 'toxic_look_(typhos)',
    'Depressão': 'depression',
    'Irritabilidade': 'irritability',
    'Dor Muscular': 'muscle_pain',
    'Alteração do Sensório': 'altered_sensorium',
    'Manchas Vermelhas no Corpo': 'red_spots_over_body',
    'Dor de Barriga': 'belly_pain',
    'Menstruação Anormal': 'abnormal_menstruation',
    'Manchas Descoloridas': 'dischromic_patches',
    'Lacrimejamento': 'watering_from_eyes',
    'Aumento do Apetite': 'increased_appetite',
    'Poliúria': 'polyuria',
    'Histórico Familiar': 'family_history',
    'Escarro Mucoso': 'mucoid_sputum',
    'Escarro Ferrugem': 'rusty_sputum',
    'Falta de Concentração': 'lack_of_concentration',
    'Distúrbios Visuais': 'visual_disturbances',
    'Transfusão de Sangue': 'receiving_blood_transfusion',
    'Injeções Não Estéreis': 'receiving_unsterile_injections',
    'Coma': 'coma',
    'Sangramento do Estômago': 'stomach_bleeding',
    'Distensão Abdominal': 'distention_of_abdomen',
    'Histórico de Consumo de Álcool': 'history_of_alcohol_consumption',
    'Sobrecarga de Líquidos': 'fluid_overload',
    'Sangue no Escarro': 'blood_in_sputum',
    'Veias Proeminentes na Panturrilha': 'prominent_veins_on_calf',
    'Palpitações': 'palpitations',
    'Caminhada Dolorosa': 'painful_walking',
    'Espinhas com Pus': 'pus_filled_pimples',
    'Cravos': 'blackheads',
    'Cicatrizes': 'scurring',
    'Descamação da Pele': 'skin_peeling',
    'Poeira Prateada': 'silver_like_dusting',
    'Pequenas Depressões nas Unhas': 'small_dents_in_nails',
    'Unhas Inflamatórias': 'inflammatory_nails',
    'Bolhas': 'blister',
    'Feridas Vermelhas ao Redor do Nariz': 'red_sore_around_nose',
    'Crosta Amarela que Escorre': 'yellow_crust_ooze',
    'Prognóstico': 'prognosis',
    
    # Mapeamentos adicionais para compatibilidade
    'Febre': 'high_fever',
    'Dificuldade para Respirar': 'breathlessness',
    'Dor no Corpo': 'muscle_pain',
    'Suor Noturno': 'sweating',
    'Chiado no Peito': 'breathlessness',
    'Tosse com Sangue': 'blood_in_sputum',
    'Congestão Nasal': 'congestion',
    'Espirros': 'continuous_sneezing',
    'Dor de Garganta': 'throat_irritation',
    'Vertigem': 'spinning_movements',
    'Confusão Mental': 'altered_sensorium',
    'Perda de Memória': 'lack_of_concentration',
    'Convulsões': 'altered_sensorium',
    'Dormência': 'weakness_of_one_body_side',
    'Formigamento': 'drying_and_tingling_lips',
    'Batimento Cardíaco Irregular': 'fast_heart_rate',
    'Pressão no Peito': 'chest_pain',
    'Vermelhidão na Pele': 'skin_rash',
    'Feridas na Pele': 'red_sore_around_nose',
    'Mudança na Cor da Pele': 'dischromic_patches',
    'Rigidez Articular': 'movement_stiffness',
    'Dor ao Urinar': 'burning_micturition',
    'Sangue na Urina': 'bloody_stool',
    'Micção Frequente': 'continuous_feel_of_urine',
    'Dificuldade para Urinar': 'bladder_discomfort',
    'Visão Turva': 'blurred_and_distorted_vision',
    'Dor nos Olhos': 'pain_behind_the_eyes',
    'Vermelhidão nos Olhos': 'redness_of_eyes',
    'Sensibilidade à Luz': 'visual_disturbances',
    'Zumbido no Ouvido': 'altered_sensorium',
    'Perda Auditiva': 'altered_sensorium',
    'Dor de Ouvido': 'neck_pain',
    'Insônia': 'anxiety',
    'Sonolência Excessiva': 'lethargy'
}

# Duração dos sintomas
DURACAO_SINTOMAS = [
    'Menos de 1 dia',
    '1-2 dias',
    '3-7 dias',
    '1-2 semanas',
    '2-4 semanas',
    '1-3 meses',
    '3-6 meses',
    'Mais de 6 meses',
    'Crônico (mais de 1 ano)'
]

# Intensidade dos sintomas
INTENSIDADE_SINTOMAS = [
    'Leve (1-3)',
    'Moderada (4-6)',
    'Grave (7-8)',
    'Muito Grave (9-10)'
]

def obter_sintomas_principais() -> list:
    """Retorna lista dos 10 sintomas mais importantes"""
    return [
        'Febre',
        'Tosse', 
        'Fadiga',
        'Dificuldade para Respirar',
        'Dor de Cabeça',
        'Dor no Corpo',
        'Náusea',
        'Diarreia',
        'Dor no Peito',
        'Dor de Garganta'
    ]

def traduzir_sintoma_para_ingles(sintoma_pt: str) -> str:
    """Traduz sintoma do português para inglês"""
    return TRADUCAO_SINTOMAS.get(sintoma_pt, sintoma_pt)

def validar_sintoma_personalizado(sintoma: str) -> bool:
    """Valida se sintoma personalizado é válido"""
    if not sintoma or len(sintoma.strip()) < 3:
        return False
    
    # Não permitir caracteres especiais demais
    import re
    if not re.match(r'^[a-zA-ZÀ-ÿ\s\-\.]+$', sintoma):
        return False
        
    return True

def normalizar_sintoma(sintoma: str) -> str:
    """Normaliza sintoma (capitaliza primeira letra)"""
    return sintoma.strip().title() if sintoma else ""