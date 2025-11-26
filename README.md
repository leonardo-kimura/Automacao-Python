# Automação - Cadastro em Google Forms

Este repositório contém um script `Cadastro.py` que automatiza o preenchimento de um Google Form público com nomes e e‑mails de um arquivo `CSV` ou `XLSX`.

Requisitos
- Python 3.9+
- Chrome instalado e chromedriver compatível (coloque o chromedriver no PATH ou use a versão do Chrome gerenciada pelo Selenium se suportado)

Instalação
```powershell
python -m pip install -r requirements.txt
```

Uso
```powershell
# Rodar em modo visível (útil para debug)
python Cadastro.py --input-file dados.csv --form-url "<FORM_VIEW_URL>"

# Rodar em background (headless)
python Cadastro.py --input-file dados.csv --form-url "<FORM_VIEW_URL>" --headless
```

O script gera `cadastro_log.csv` com colunas `Nome,Email,Status,Mensagem`.

Observações
- O formulário deve estar configurado para permitir respostas de qualquer pessoa com o link (`/viewform`).
- Evite fornecer credenciais em scripts. Se o formulário exigir login, automatizar login pode ser necessário, mas é menos seguro.
