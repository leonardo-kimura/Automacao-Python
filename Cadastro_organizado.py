"""Automação para preencher Google Forms - Versão organizada.

Estrutura:
  1. Importações
  2. Funções auxiliares (organizar o navegador)
  3. Função principal (fazer o trabalho pesado)
  4. main() - orquestra o fluxo

Como usar:
  python Cadastro_organizado.py --input-file dados.csv
"""

import argparse
import os
import sys
import time

import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


# ============================================================================
# PARTE 1: FUNÇÕES AUXILIARES
# ============================================================================

def criar_navegador(modo_headless=False):
    """
    Cria e retorna um navegador Chrome.
    
    Args:
        modo_headless (bool): Se True, roda sem interface visual.
    
    Returns:
        webdriver.Chrome: Um objeto de navegador.
    """
    opcoes = webdriver.ChromeOptions()
    
    if modo_headless:
        opcoes.add_argument('--headless')
        opcoes.add_argument('--window-size=1600,1200')
    
    # Opções recomendadas para estabilidade
    opcoes.add_argument('--no-sandbox')
    opcoes.add_argument('--disable-dev-shm-usage')
    
    return webdriver.Chrome(options=opcoes)


def carregar_dados(caminho_arquivo):
    """
    Carrega dados de um arquivo CSV ou XLSX.
    
    Args:
        caminho_arquivo (str): Caminho do arquivo.
    
    Returns:
        pd.DataFrame: DataFrame com os dados.
    
    Raises:
        FileNotFoundError: Se o arquivo não existir.
        ValueError: Se o formato não for suportado.
    """
    if not os.path.exists(caminho_arquivo):
        raise FileNotFoundError(f'Arquivo "{caminho_arquivo}" não encontrado.')
    
    extensao = os.path.splitext(caminho_arquivo)[1].lower()
    
    if extensao == '.csv':
        return pd.read_csv(caminho_arquivo)
    elif extensao in ['.xlsx', '.xls']:
        return pd.read_excel(caminho_arquivo)
    else:
        raise ValueError(f'Formato "{extensao}" não suportado. Use .csv ou .xlsx')


def validar_dados(df):
    """
    Verifica se o DataFrame tem as colunas necessárias.
    
    Args:
        df (pd.DataFrame): DataFrame a validar.
    
    Raises:
        ValueError: Se faltarem colunas.
    """
    colunas_necessarias = ['Nome', 'Email']
    for coluna in colunas_necessarias:
        if coluna not in df.columns:
            raise ValueError(f'Coluna "{coluna}" não encontrada no arquivo.')


def criar_arquivo_exemplo(caminho='dados.csv'):
    """
    Cria um arquivo CSV de exemplo com estrutura correta.
    
    Args:
        caminho (str): Caminho onde criar o arquivo.
    """
    dados_exemplo = {
        'Nome': ['João Silva', 'Maria Santos', 'Pedro Oliveira'],
        'Email': ['joao@email.com', 'maria@email.com', 'pedro@email.com']
    }
    df = pd.DataFrame(dados_exemplo)
    df.to_csv(caminho, index=False)
    print(f'   ✓ Arquivo exemplo criado: {caminho}')
    print(f'   ℹ Edite o arquivo com seus dados (colunas: Nome, Email)')
    print(f'   ℹ Execute novamente após preencher os dados')


# ============================================================================
# PARTE 2: FUNÇÃO PRINCIPAL (O TRABALHO PESADO)
# ============================================================================

def preencher_formulario(navegador, url_formulario, nome, email):
    """
    Preenche e submete um Google Form com nome e email.
    
    Args:
        navegador (webdriver.Chrome): Navegador aberto.
        url_formulario (str): URL do formulário.
        nome (str): Nome a preencher.
        email (str): Email a preencher.
    
    Returns:
        tuple: (sucesso: bool, mensagem: str)
    """
    try:
        # Abrir a página do formulário
        navegador.get(url_formulario)
        
        # Esperar até que os campos apareçam (máximo 10 segundos)
        wait = WebDriverWait(navegador, 10)
        wait.until(EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, "input[type='text'], input[type='email'], textarea")
        ))
        
        # Pegar todos os campos de entrada
        campos = navegador.find_elements(
            By.CSS_SELECTOR, "input[type='text'], input[type='email'], textarea"
        )
        
        # Tentar preencher procurando pela label
        nome_preenchido = False
        email_preenchido = False
        
        for campo in campos:
            label = (campo.get_attribute('aria-label') or '').lower()
            tipo = (campo.get_attribute('type') or '').lower()
            
            # Se a label menciona "nome" e ainda não preencheu
            if not nome_preenchido and 'nome' in label:
                campo.send_keys(nome)
                nome_preenchido = True
            
            # Se a label menciona "email" ou é um input de email
            elif not email_preenchido and ('email' in label or tipo == 'email'):
                campo.send_keys(email)
                email_preenchido = True
        
        # Se não encontrou por label, preencher os primeiros campos
        if not nome_preenchido and len(campos) > 0:
            campos[0].send_keys(nome)
            nome_preenchido = True
        
        if not email_preenchido and len(campos) > 1:
            campos[1].send_keys(email)
            email_preenchido = True
        
        # Procurar e clicar no botão "Enviar"
        navegador.execute_script("""
            const spans = document.querySelectorAll('span');
            for (let s of spans) {
                if (s.innerText && s.innerText.trim() === 'Enviar') {
                    const botao = s.closest('[role="button"]') || s.parentElement;
                    if (botao) botao.click();
                    break;
                }
            }
        """)
        
        # Aguardar a submissão processar
        time.sleep(1)
        
        return True, 'Enviado com sucesso'
        
    except Exception as e:
        return False, str(e)


# ============================================================================
# PARTE 3: FUNÇÃO main() - ORQUESTRA TUDO
# ============================================================================

def main():
    """Função principal: coordena todo o fluxo."""
    
    # 1. LER ARGUMENTOS
    parser = argparse.ArgumentParser(description='Preenche Google Forms automaticamente')
    parser.add_argument('--input-file', '-i', default='dados.csv', 
                        help='Arquivo CSV/XLSX com colunas "Nome" e "Email"')
    parser.add_argument('--form-url', '-u', 
                        default='https://docs.google.com/forms/d/1od6sjuIEOibDMUcuDjOvlqbX8T8Z7rjhMMY4hf-OVHw/viewform',
                        help='URL pública do formulário')
    parser.add_argument('--headless', action='store_true', help='Executar sem interface visual')
    args = parser.parse_args()
    
    print('=' * 60)
    print('AUTOMAÇÃO DE GOOGLE FORMS')
    print('=' * 60)
    
    # 2. CARREGAR E VALIDAR DADOS
    print(f'\n1. Carregando arquivo: {args.input_file}')
    
    # Se arquivo não existir, criar exemplo
    if not os.path.exists(args.input_file):
        print(f'   ⓘ Arquivo não encontrado. Criando exemplo...')
        criar_arquivo_exemplo(args.input_file)
        sys.exit(0)
    
    try:
        df = carregar_dados(args.input_file)
        validar_dados(df)
        print(f'   ✓ Arquivo carregado com {len(df)} linhas')
    except Exception as e:
        print(f'   ✗ Erro: {e}')
        sys.exit(1)
    
    # 3. CRIAR NAVEGADOR
    print(f'\n2. Iniciando navegador...')
    try:
        navegador = criar_navegador(modo_headless=args.headless)
        print(f'   ✓ Navegador pronto')
    except Exception as e:
        print(f'   ✗ Erro ao criar navegador: {e}')
        sys.exit(1)
    
    # 4. PROCESSAR CADA LINHA
    print(f'\n3. Processando linhas...\n')
    resultados = []
    
    try:
        for indice, linha in df.iterrows():
            nome = str(linha.get('Nome', '')).strip()
            email = str(linha.get('Email', '')).strip()
            
            numero_linha = indice + 1
            print(f'   [{numero_linha}/{len(df)}] {nome} ({email})', end=' ... ')
            
            sucesso, mensagem = preencher_formulario(
                navegador, args.form_url, nome, email
            )
            
            if sucesso:
                print('✓')
                resultados.append({
                    'Nome': nome,
                    'Email': email,
                    'Status': 'OK',
                    'Mensagem': mensagem
                })
            else:
                print('✗')
                resultados.append({
                    'Nome': nome,
                    'Email': email,
                    'Status': 'ERRO',
                    'Mensagem': mensagem
                })
    
    finally:
        # 5. FECHAR NAVEGADOR
        print(f'\n4. Finalizando...')
        try:
            navegador.quit()
            print(f'   ✓ Navegador fechado')
        except Exception:
            pass
    
    # 6. SALVAR LOG
    log_df = pd.DataFrame(resultados)
    log_df.to_csv('cadastro_log.csv', index=False)
    print(f'   ✓ Log salvo em "cadastro_log.csv"')
    
    # 7. RESUMO
    total_ok = len([r for r in resultados if r['Status'] == 'OK'])
    total_erro = len([r for r in resultados if r['Status'] == 'ERRO'])
    
    print(f'\n' + '=' * 60)
    print(f'RESUMO: {total_ok} OK, {total_erro} ERRO')
    print('=' * 60)


# ============================================================================
# EXECUTAR
# ============================================================================

if __name__ == '__main__':
    main()
