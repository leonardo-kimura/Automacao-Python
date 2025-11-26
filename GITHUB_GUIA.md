# Como Conectar seu Código a um Repositório GitHub

## 1. VERIFICAR SE JÁ TEM GIT INSTALADO

```powershell
git --version
```

Se aparecer a versão (ex: `git version 2.42.0`), OK. Se não, baixe em https://git-scm.com/

---

## 2. CONFIGURAR GIT (Primeira vez apenas)

```powershell
git config --global user.name "Seu Nome"
git config --global user.email "seu.email@gmail.com"
```

**Verifique:**
```powershell
git config --list
```

---

## 3. OPÇÃO A: Já tem um repositório no GitHub

Se você já criou o repositório em GitHub (ex: `leonardo-kimura/Automacao-Python`):

### Passo 1: Entre na pasta do seu projeto
```powershell
cd "C:\Users\Leo\Downloads\Automação"
```

### Passo 2: Inicializar Git localmente
```powershell
git init
```

### Passo 3: Adicionar arquivo remoto
```powershell
git remote add origin https://github.com/leonardo-kimura/Automacao-Python.git
```

**Verifique:**
```powershell
git remote -v
```

Deve aparecer:
```
origin  https://github.com/leonardo-kimura/Automacao-Python.git (fetch)
origin  https://github.com/leonardo-kimura/Automacao-Python.git (push)
```

### Passo 4: Adicionar arquivos
```powershell
git add .
```

### Passo 5: Fazer primeiro commit
```powershell
git commit -m "Initial commit: scripts de automação"
```

### Passo 6: Enviar para GitHub (push)
```powershell
git branch -M main
git push -u origin main
```

---

## 4. OPÇÃO B: Não tem repositório no GitHub ainda

### Passo 1: Criar repositório no GitHub
1. Vá em https://github.com/new
2. Defina:
   - **Repository name:** `Automacao-Python`
   - **Description:** Scripts de automação web com Python e Selenium
   - **Visibility:** Public (se quer mostrar no currículo)
   - **Initialize with:** NÃO marque nada
3. Clique **Create repository**

### Passo 2: Copiar os comandos que aparecem

GitHub vai mostrar uma sequência de comandos. Siga-os no seu PowerShell:

```powershell
cd "C:\Users\Leo\Downloads\Automação"
git init
git add .
git commit -m "Initial commit: scripts de automação"
git branch -M main
git remote add origin https://github.com/leonardo-kimura/Automacao-Python.git
git push -u origin main
```

---

## 5. DEPOIS: Trabalhar com Git (Dia a dia)

### Fazer mudanças e enviar:

```powershell
# Ver o que mudou
git status

# Adicionar todas as mudanças
git add .

# Fazer commit com mensagem
git commit -m "Descrição do que mudou"

# Enviar para GitHub
git push
```

### Exemplos de mensagens boas:
```
git commit -m "Fix: tratamento de erro no Cadastro_organizado.py"
git commit -m "Feature: adicionar criação automática de dados.csv"
git commit -m "Docs: atualizar README com instruções"
git commit -m "Refactor: melhorar estrutura de funções"
```

---

## 6. CRIAR .gitignore (Importante!)

Crie um arquivo chamado `.gitignore` na raiz da pasta:

```powershell
# Criar arquivo
New-Item -Path "C:\Users\Leo\Downloads\Automação\.gitignore" -ItemType File
```

Adicione este conteúdo:

```
# Arquivos de dados sensíveis
dados.csv
cadastro_log.csv
precos.csv
precos_iphone.csv

# Credenciais
*.env
.env

# Python
__pycache__/
*.pyc
*.pyo
*.egg-info/
dist/
build/

# IDE
.vscode/
.idea/
*.code-workspace

# OS
.DS_Store
Thumbs.db
```

Depois faça commit:

```powershell
git add .gitignore
git commit -m "Add: .gitignore para proteger dados sensíveis"
git push
```

---

## 7. ADICIONAR LICENÇA

Crie um arquivo `LICENSE` (MIT é popular):

```powershell
New-Item -Path "C:\Users\Leo\Downloads\Automação\LICENSE" -ItemType File
```

Adicione:
```
MIT License

Copyright (c) 2025 Leonardo Kimura

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, and/or sell copies of the
Software...

[Veja: https://opensource.org/licenses/MIT]
```

Ou copie de: https://opensource.org/licenses/MIT

---

## 8. ATUALIZAR README (Para showcase)

No seu `README.md`, adicione:

```markdown
# Automação Python - Web Scraping & Form Filling

Scripts de automação web com Python e Selenium para MercadoLivre e Google Forms.

## 📋 O que faz

- **Cadastro_organizado.py**: Preenche formulários Google automaticamente
- **Produtos_organizado.py**: Coleta preços de MercadoLivre

## 🚀 Quick Start

```bash
pip install -r requirements.txt
python Cadastro_organizado.py --help
```

## 📚 Conceitos

- Selenium WebDriver
- WebDriverWait (esperas explícitas)
- CSS Selectors & HTML parsing
- Pandas para manipulação de dados
- Argparse para CLI

## 📝 Licença

MIT License - veja `LICENSE`
```

---

## 9. VERIFICA DO FINAL

### Ver histórico de commits:
```powershell
git log --oneline
```

### Ver status:
```powershell
git status
```

Deve aparecer: `On branch main nothing to commit, working tree clean`

### Verificar remoto:
```powershell
git remote -v
```

---

## 10. ERROS COMUNS

### Erro: "fatal: not a git repository"
**Solução:** Você não está na pasta certa ou não rodou `git init`
```powershell
cd "C:\Users\Leo\Downloads\Automação"
git init
```

### Erro: "fatal: remote origin already exists"
**Solução:** Já tem um remote. Verifique:
```powershell
git remote -v
git remote remove origin  # Se quiser trocar
git remote add origin https://...
```

### Erro: "Permission denied" ao fazer push
**Solução:** Token de autenticação. GitHub pedirá para gerar um token pessoal:
1. Vá em Settings → Developer settings → Personal access tokens
2. Generate new token (escopo: `repo`)
3. Use o token como senha ao fazer `git push`

### Erro: "Tudo em vermelho no push"
**Solução:** Geralmente é conflito de ramo. Tente:
```powershell
git pull --rebase origin main
git push origin main
```

---

## 11. COMANDOS RÁPIDOS (Resumo)

```powershell
# Primeira vez
git init
git remote add origin https://github.com/usuario/repo.git
git add .
git commit -m "Initial commit"
git push -u origin main

# Depois: cada mudança
git add .
git commit -m "descrição"
git push

# Ver histórico
git log --oneline

# Desfazer último commit (não enviado ainda)
git reset --soft HEAD~1

# Desfazer mudanças em um arquivo
git checkout -- nome_arquivo.py
```

---

## 12. PRÓXIMOS PASSOS

- [ ] Criar repositório no GitHub
- [ ] Conectar com `git remote add origin`
- [ ] Fazer primeiro `git push`
- [ ] Criar `.gitignore`
- [ ] Adicionar `LICENSE`
- [ ] Melhorar `README.md`
- [ ] Fazer commits regulares
- [ ] Usar para portfolio/currículo

---

**Dúvidas? Teste com:**
```powershell
git --help
git config --help
```

Ou visite: https://github.com/git-tips/tips
