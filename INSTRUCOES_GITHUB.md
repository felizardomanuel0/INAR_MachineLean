# 🚀 INSTRUÇÕES PARA SUBIR NO GITHUB

## ✅ Status Atual
- ✅ Repositório Git inicializado
- ✅ Arquivos adicionados e commitados
- ✅ README.md profissional criado
- ✅ .gitignore configurado
- ✅ requirements.txt atualizado

## 📋 Próximos Passos para GitHub

### 1. Criar Repositório no GitHub
1. Acesse https://github.com
2. Clique em "New repository" (botão verde)
3. Configure o repositório:
   - **Nome**: `sistema-diagnostico-medico-inar`
   - **Descrição**: `Sistema de diagnóstico médico com ML - Projeto INAR 2025`
   - **Visibilidade**: Public (ou Private se preferir)
   - **NÃO** marque "Add a README file" (já temos um)
   - **NÃO** adicione .gitignore (já temos um)

### 2. Conectar Repositório Local ao GitHub
Execute os comandos no terminal (substitua SEU-USUARIO pelo seu username do GitHub):

```bash
cd "/home/felizado-manuel/Documentos/Faculdade/Terceiro/II Semestre/INAR/Projecto final 01"

# Adicionar repositório remoto
git remote add origin https://github.com/SEU-USUARIO/sistema-diagnostico-medico-inar.git

# Subir código para o GitHub
git push -u origin main
```

### 3. Verificar Upload
- Acesse seu repositório no GitHub
- Verifique se todos os arquivos foram enviados
- Confirme que o README.md está sendo exibido corretamente

## 📝 Comandos Alternativos (caso necessário)

### Se já existir um repositório remoto:
```bash
git remote set-url origin https://github.com/SEU-USUARIO/sistema-diagnostico-medico-inar.git
```

### Para verificar repositórios remotos:
```bash
git remote -v
```

### Para forçar o push (use com cuidado):
```bash
git push --force-with-lease origin main
```

## 🔐 Autenticação GitHub

### Usando Token Pessoal (Recomendado):
1. GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Generate new token (classic)
3. Selecione escopo "repo"
4. Use o token como senha quando solicitar credenciais

### Usando SSH (Alternativa):
1. Gere chave SSH: `ssh-keygen -t ed25519 -C "seu-email@exemplo.com"`
2. Adicione ao GitHub: Settings → SSH and GPG keys
3. Use URL SSH: `git remote add origin git@github.com:SEU-USUARIO/sistema-diagnostico-medico-inar.git`

## 📊 Estrutura Final no GitHub

Seu repositório terá:
```
sistema-diagnostico-medico-inar/
├── 📄 README.md                     # Documentação principal
├── 📄 .gitignore                   # Arquivos ignorados
├── 📄 requirements.txt             # Dependências
├── 📄 main_atualizado.py          # Script principal
├── 📂 src/                        # Código fonte
├── 📂 dataset/                    # Datasets médicos
├── 📂 consultas_salvas/           # Históricos
└── 📂 notebooks/                  # Jupyter notebooks
```

## 🎯 Dicas Importantes

1. **Mantenha private** se contém dados sensíveis
2. **Use .gitignore** para não enviar:
   - Arquivos de modelo (.pkl, .joblib)
   - Logs
   - Ambiente virtual (venv/)
   - Cache Python (__pycache__)

3. **Organize commits** futuros:
   ```bash
   git add arquivo_modificado.py
   git commit -m "🐛 Fix: Corrige bug no diagnóstico de diabetes"
   git push origin main
   ```

## 🏆 Resultado Final
- ✅ Projeto profissional no GitHub
- ✅ Documentação completa
- ✅ Código organizado e versionado
- ✅ Pronto para apresentação/portfólio

## 💡 Próximos Passos Sugeridos
1. Criar releases (tags) para versões
2. Adicionar GitHub Actions para CI/CD
3. Criar Issues para melhorias futuras
4. Adicionar Wiki com documentação adicional

---
🚀 **Seu projeto está pronto para ser compartilhado com o mundo!**