# 💾 Sistema de Salvamento de Consultas

## 📍 Localização das Consultas

Todas as consultas médicas realizadas no sistema são organizadas automaticamente na pasta:

```
📁 consultas_salvas/
├── 📁 relatorios/          # Relatórios individuais (.txt)
├── 📁 historico/           # Arquivo CSV com histórico completo
└── 📁 backup/              # Backups automáticos
```

**Caminho completo**: `/home/felizado-manuel/Documentos/Faculdade/Terceiro/II Semestre/INAR/Projecto final 01/consultas_salvas/`

---

## 🚀 Como Salvar uma Consulta

### **Opção 1: Salvamento Rápido (Recomendado)**
- **Atalho**: `Ctrl + S`
- **Resultado**: Salva automaticamente em `consultas_salvas/relatorios/`
- **Nome do arquivo**: `diagnostico_[Nome]_[Data]_[Hora].txt`
- **Exemplo**: `diagnostico_João_Silva_20251111_160530.txt`

### **Opção 2: Menu Completo**
- **Botão**: "💾 Salvar Consulta"
- **Opções disponíveis**:
  1. ⚡ **Salvamento Rápido** - Pasta automática
  2. 📁 **Escolher Local** - Selecionar onde salvar
  3. 💾 **Salvar e Abrir Pasta** - Salva e mostra a pasta

### **Opção 3: Visualizar Histórico**
- **Botão**: "📊 Ver Histórico"
- **Mostra**: Tabela com todas as consultas realizadas
- **Inclui**: Data, paciente, sintomas, diagnóstico, etc.

---

## 📊 Estrutura dos Arquivos

### **Relatório Individual (.txt)**
Cada consulta gera um arquivo completo com:
- ✅ Dados do paciente (nome, idade, gênero)
- 🩺 Sintomas reportados (principais + extras)
- ⏰ Duração e intensidade dos sintomas
- 🎯 Resultado do diagnóstico
- 📈 Confiança do modelo IA
- 💡 Recomendações médicas específicas
- ⚠️ Avisos importantes

### **Histórico Geral (CSV)**
Arquivo: `consultas_salvas/historico/historico_geral.csv`

**Campos incluídos**:
- Data e hora da consulta
- Nome e dados do paciente
- Lista de sintomas (principais e extras)
- Duração e intensidade
- Pressão arterial e colesterol
- Diagnóstico final
- Nível de confiança
- Nome do arquivo do relatório

---

## 🔧 Funcionalidades Avançadas

### **Abertura Automática de Pasta**
- **Windows**: `explorer consultas_salvas`
- **Linux**: `xdg-open consultas_salvas`
- **macOS**: `open consultas_salvas`

### **Atalhos Úteis**
- `Ctrl + S` → Salvar rápido
- `Ctrl + L` → Limpar formulário
- `F5` → Realizar diagnóstico
- `Ctrl + Q` → Sair do sistema

### **Segurança dos Dados**
- ✅ Codificação UTF-8 (suporte a acentos)
- ✅ Nomes de arquivo seguros
- ✅ Estrutura organizada por data
- ✅ Backup automático do histórico
- ✅ Validação de dados antes de salvar

---

## 📁 Exemplo de Estrutura Completa

```
consultas_salvas/
├── relatorios/
│   ├── diagnostico_João_Silva_20251111_160530.txt
│   ├── diagnostico_Maria_Santos_20251111_161245.txt
│   └── diagnostico_Pedro_Costa_20251111_162010.txt
├── historico/
│   └── historico_geral.csv
└── backup/
    └── (backups automáticos futuros)
```

---

## 💡 Dicas de Uso

1. **Use Ctrl+S** para salvamento rápido após cada diagnóstico
2. **Preencha sempre o nome** do paciente para organização
3. **Verifique o histórico** regularmente com "📊 Ver Histórico"
4. **Abra a pasta** ocasionalmente para verificar os arquivos
5. **Faça backup** da pasta `consultas_salvas` periodicamente

---

## 📞 Suporte

Este sistema foi desenvolvido para o **Projeto Final INAR - 2025**.

- **Pasta do projeto**: `/home/felizado-manuel/Documentos/Faculdade/Terceiro/II Semestre/INAR/Projecto final 01/`
- **Sistema operacional**: Linux
- **Versão Python**: 3.12+

**⚠️ Importante**: Este sistema é apenas para fins educacionais. Não deve ser usado para diagnósticos médicos reais.