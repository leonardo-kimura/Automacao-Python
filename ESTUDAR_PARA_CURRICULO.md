# O QUE VOCÊ PRECISA ESTUDAR (Para Explicar no Currículo)

Baseado nos scripts `Cadastro_organizado.py` e `Produtos_organizado.py`, aqui estão os conceitos que você deve dominar:

---

## 1. PYTHON FUNDAMENTALS ⭐

### 1.1 Funções e Organização
- **O que é:** Dividir código em funções pequenas e reutilizáveis
- **Por que:** Facilita manutenção e testes
- **Seus scripts usam:**
  - `criar_navegador()` → configuração isolada
  - `carregar_dados()` → operação específica
  - `preencher_formulario()` → lógica principal
- **Estude:**
  - Parâmetros (obrigatórios vs opcionais)
  - Return types
  - Exceções (try/except)
  - Docstrings (Args, Returns, Raises)

**Perguntas que podem fazer:**
- "Por que você separou `criar_navegador` em uma função?"
- "Como você passa dados entre funções?"
- "O que significa `modo_headless=False`?"

### 1.2 Imports
- **Bibliotecas que você usa:**
  - `argparse` → processar argumentos de linha de comando
  - `os` → verificar se arquivo existe
  - `pandas` → trabalhar com CSV/XLSX
  - `selenium` → automação de navegador
  - `re` (regex) → extrair padrões de texto

**Estude:**
- O que cada `import` faz
- Quando usar `from X import Y` vs `import X`
- Dependências (`requirements.txt`)

---

## 2. SELENIUM (Automação Web) ⭐⭐⭐

### 2.1 Core Concepts
```python
# Seus scripts usam:
navegador = webdriver.Chrome()           # Criar navegador
navegador.get('url')                      # Navegar
elemento = navegador.find_element(By.ID, 'campo_email')  # Encontrar
elemento.send_keys('texto')               # Digitar
elemento.click()                          # Clicar
navegador.quit()                          # Fechar
```

**Estude:**
- Diferença entre `ID`, `CLASS_NAME`, `CSS_SELECTOR`
- Como encontrar elementos (inspect no navegador)
- Cliques, digitação, navegação
- Tratamento de erros (elemento não encontrado)

### 2.2 WebDriverWait (Esperas Explícitas) ⭐
```python
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

wait = WebDriverWait(navegador, 10)  # Esperar até 10 segundos
wait.until(EC.presence_of_element_located((By.ID, 'campo')))
```

**Por que é importante:**
- Evita erros de timing ("elemento não encontrado")
- Melhor que `time.sleep()` (mais rápido e confiável)
- Esperamos a condição real, não tempo fixo

**Perguntas:**
- "Por que não usar `time.sleep()`?"
- "Como você espera um elemento carregar?"
- "O que faz `expected_conditions`?"

### 2.3 Fallback de Seletores
```python
seletores = ['.ui-search-item__title', 'h2', 'a']
for seletor in seletores:
    try:
        elemento = elemento.find_element(By.CSS_SELECTOR, seletor)
        if elemento.text.strip():
            return elemento.text
    except:
        continue
```

**Por que:** Sites mudam a estrutura HTML → código quebra
**Solução:** Tenta vários seletores até encontrar

---

## 3. WEB SCRAPING ⭐⭐

### 3.1 CSS Selectors & HTML
- **Conceito:** Encontrar elementos em HTML usando CSS
- **Seus scripts:**
  - `.ui-search-layout__item` → classe CSS (começa com ponto)
  - `By.NAME` → atributo name
  - `By.CLASS_NAME` → atributo class

**Estude:**
- Inspecionar elementos com F12 (DevTools)
- Diferença entre ID, classe, atributo
- Como ler HTML básico

### 3.2 Regex (Expressões Regulares)
```python
match = re.search(r'R\$\s*[\d\.,]+', texto)
return match.group(0) if match else ''
```

- `R\$` → literal "R$"
- `\s*` → zero ou mais espaços
- `[\d\.,]+` → um ou mais dígitos, pontos ou vírgulas
- `match.group(0)` → o texto encontrado

**Estude:**
- Padrões básicos: `\d` (dígito), `\s` (espaço), `+` (um ou mais)
- Como testar regex (regex101.com)
- Quando usar regex vs string methods

---

## 4. PANDAS (Dados em CSV/XLSX) ⭐

### 4.1 Carregar Dados
```python
df = pd.read_csv('arquivo.csv')      # CSV
df = pd.read_excel('arquivo.xlsx')   # XLSX
```

### 4.2 Validar Dados
```python
if coluna not in df.columns:
    raise ValueError(f'Coluna "{coluna}" não encontrada')
```

### 4.3 Iterar Linhas
```python
for index, row in df.iterrows():
    nome = row['Nome']
    email = row['Email']
```

### 4.4 Salvar Dados
```python
df.to_csv('saida.csv', index=False)
```

**Estude:**
- Estrutura básica (linhas x colunas)
- Acessar colunas
- Iterar dados
- Formatos de arquivo

---

## 5. LINHA DE COMANDO (CLI) ⭐

### 5.1 argparse
```python
parser = argparse.ArgumentParser()
parser.add_argument('--query', '-q', required=False, help='Termo de busca')
parser.add_argument('--headless', action='store_true', help='Modo sem interface')
args = parser.parse_args()
```

**Como usar:**
```powershell
python Produtos_organizado.py --query "Notebook" --headless
```

**Estude:**
- Argumentos obrigatórios vs opcionais
- Short name (`-q`) vs long name (`--query`)
- `action='store_true'` para bandeiras (flags)
- Acessar valores: `args.query`

---

## 6. ESTRUTURA DE CÓDIGO ⭐⭐

### 6.1 Padrão que você usa:
```
PARTE 1: IMPORTAÇÕES
PARTE 2: FUNÇÕES AUXILIARES (helpers, utilities)
PARTE 3: FUNÇÕES PRINCIPAIS (lógica de negócio)
PARTE 4: main() - ORQUESTRA TUDO
```

### 6.2 Por que:
- **Legibilidade:** código organizado é mais fácil de ler
- **Manutenção:** mudança em um lugar = impacto mínimo
- **Testes:** funções pequenas são testáveis
- **Reutilização:** helpers podem ser usados em vários places

**Estude:**
- Coesão (funções que fazem uma coisa bem)
- Acoplamento (reduzir dependências entre funções)
- Responsabilidade única (cada função tem um propósito)

---

## 7. TRATAMENTO DE ERROS ⭐⭐

### 7.1 Try/Except
```python
try:
    elemento = navegador.find_element(By.ID, 'campo')
except NoSuchElementException:
    print('Elemento não encontrado')
```

### 7.2 Exceções Específicas
```python
def carregar_dados(caminho):
    if not os.path.exists(caminho):
        raise FileNotFoundError(f'Arquivo não existe')
    
    if extensao not in ['.csv', '.xlsx']:
        raise ValueError(f'Formato não suportado')
```

**Estude:**
- Diferenciar: `FileNotFoundError`, `ValueError`, `TimeoutException`
- Quando capturar vs deixar falhar
- Finally (sempre executar, mesmo com erro)

---

## 8. GIT E VERSIONAMENTO (Bônus) ⭐

Seu código está em GitHub:
- https://github.com/leonardo-kimura/Sistema-locadora

**Estude:**
- Git básico: `git add`, `git commit`, `git push`
- Por que usar controle de versão
- README.md como documentação
- `.gitignore` para não committar senhas/dados

---

---

## ROADMAP DE ESTUDO (Por Prioridade)

### OBRIGATÓRIO (sem isso não explica):
1. ✅ Funções em Python (já usa bem!)
2. ✅ Selenium básico (já usa!)
3. ✅ WebDriverWait (já usa!)
4. ✅ CSS Selectors (já usa!)
5. ✅ Pandas básico (já usa!)
6. ✅ Argparse (já usa!)

### IMPORTANTE (fortaleça):
7. Regex (extrair padrões) - **APROFUNDE**
8. Tratamento de erros - **APROFUNDE**
9. Estrutura de código - **APRENDA A NOMEAR BEM**
10. Git/GitHub - **DOMINE**

### BÔNUS (impressiona):
11. Async/await (requisições paralelas)
12. Logging profissional
13. Unit tests (pytest)
14. Docker (containerizar)

---

---

## EXERCÍCIOS PRÁTICOS

### 1. Entender seu próprio código
- [ ] Rode `Cadastro_organizado.py` com `--help` e entenda cada opção
- [ ] Rode `Produtos_organizado.py` com `--help` e entenda cada opção
- [ ] Explique em voz alta (ou escreva) o que cada função faz
- [ ] Modifique um seletor e veja o script quebrar (e conserte)

### 2. Aprofundar Regex
```python
# Teste esses padrões no regex101.com
r'R\$\s*[\d\.,]+'     # Preço em reais
r'\d{2}\.\d{3}-\d{3}' # CPF
r'[\w\.-]+@[\w\.-]+\.\w+' # Email
```

### 3. Aprofundar Selenium
- [ ] Inspecione MercadoLivre com F12
- [ ] Encontre 5 seletores diferentes para o mesmo elemento
- [ ] Teste cliques, digitação, envio de formulário
- [ ] Trate a exceção quando elemento não existe

### 4. Git
- [ ] Clone seu repositório: `git clone https://github.com/leonardo-kimura/Sistema-locadora`
- [ ] Crie uma branch: `git checkout -b meus-testes`
- [ ] Faça um commit: `git add .` → `git commit -m "Descrição"`
- [ ] Faça um push: `git push origin meus-testes`

---

---

## COMO EXPLICAR NO CURRÍCULO / ENTREVISTA

### Frase de apresentação:
> "Desenvolvi 2 scripts de automação web com Python e Selenium que coletam dados de MercadoLivre e preenchem formulários Google Forms. Usei WebDriverWait para sincronização robusta, fallback de seletores CSS para resiliência, e pandas para manipulação de dados."

### Estrutura de resposta (quando perguntarem):

**"Como você preenche um campo de formulário?"**
```
1. Encontro o elemento usando CSS Selector ou XPath
2. Espero que ele esteja visível com WebDriverWait (máx 10 segundos)
3. Digito com element.send_keys()
4. Se falhar, trato a exceção específica (NoSuchElementException, TimeoutException)
```

**"Como você lida com mudanças no HTML?"**
```
1. Uso múltiplos seletores como fallback
2. Trato exceções quando seletor não encontra nada
3. Mantenho logs detalhados para rastrear quando quebra
4. Testo script periodicamente em ambiente de produção
```

**"Como você estrutura seu código?"**
```
1. Separo responsabilidades: setup do navegador, lógica de negócio, orquestração
2. Cada função tem um propósito único (criar_navegador não preenche, preencher_formulario não cria navegador)
3. Uso docstrings (Args, Returns, Raises) para clareza
4. Argparse para CLI flexível (sem mudar código)
```

---

## RECURSOS PARA ESTUDAR

- **Python Básico:** Real Python (python.readthedocs.io)
- **Selenium:** Documentação oficial (selenium.dev)
- **Regex:** regex101.com (testar padrões)
- **CSS Selectors:** MDN Web Docs
- **Pandas:** pandas.pydata.org (documentação oficial)
- **Git:** GitHub Learning Lab

---

**Resumo:** Você já usa tudo isso bem. Agora é APROFUNDAR em cada área para poder explicar com confiança.
