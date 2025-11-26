"""Coletor de preços MercadoLivre - Versão organizada.

Estrutura:
  1. Importações
  2. Funções auxiliares (operações simples)
  3. Funções principais (lógica de negócio)
  4. main() - orquestra o fluxo

Como usar:
  python Produtos_organizado.py --query "Notebook" --max-items 5 --output precos.csv
"""

import argparse
import os
import re
import sys

import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


# ============================================================================
# PARTE 1: FUNÇÕES AUXILIARES (Pequenas operações)
# ============================================================================

def criar_navegador(modo_headless=False):
    """
    Cria um navegador Chrome com opções configuradas.
    
    Args:
        modo_headless (bool): Se True, executa sem interface visual.
    
    Returns:
        webdriver.Chrome: Navegador configurado.
    """
    opcoes = webdriver.ChromeOptions()
    
    if modo_headless:
        opcoes.add_argument('--headless')
        opcoes.add_argument('--window-size=1600,1200')
    
    opcoes.add_argument('--no-sandbox')
    opcoes.add_argument('--disable-dev-shm-usage')
    
    return webdriver.Chrome(options=opcoes)


def extrair_preco(texto):
    """
    Procura por um preço no formato 'R$ 1.234,56' em um texto.
    
    Args:
        texto (str): Texto para procurar.
    
    Returns:
        str: Preço encontrado ou string vazia.
    """
    match = re.search(r'R\$\s*[\d\.,]+', texto)
    return match.group(0) if match else ''


def extrair_titulo(elemento):
    """
    Extrai o título de um elemento do produto.
    
    Tenta vários seletores CSS até encontrar um com texto.
    
    Args:
        elemento: Elemento Selenium do produto.
    
    Returns:
        str: Título encontrado ou string vazia.
    """
    seletores = ['.ui-search-item__title', 'h2', 'a']
    
    # Tentar cada seletor
    for seletor in seletores:
        try:
            elemento_titulo = elemento.find_element(By.CSS_SELECTOR, seletor)
            texto = elemento_titulo.text.strip()
            if texto:
                return texto
        except Exception:
            continue
    
    # Fallback: primeira linha do texto do elemento
    try:
        return elemento.text.split('\n')[0].strip()
    except Exception:
        return ''


def extrair_preco_elemento(elemento):
    """
    Extrai o preço de um elemento do produto.
    
    Tenta vários seletores CSS, depois regex.
    
    Args:
        elemento: Elemento Selenium do produto.
    
    Returns:
        str: Preço encontrado ou string vazia.
    """
    seletores = ['.ui-search-price__part', '.price-tag-fraction', '.andes-money-amount__fraction']
    
    # Tentar cada seletor
    for seletor in seletores:
        try:
            elemento_preco = elemento.find_element(By.CSS_SELECTOR, seletor)
            texto = elemento_preco.text.strip()
            if texto:
                return texto
        except Exception:
            continue
    
    # Fallback: usar regex no texto completo
    return extrair_preco(elemento.text)


# ============================================================================
# PARTE 2: FUNÇÕES PRINCIPAIS (Lógica de negócio)
# ============================================================================

def buscar_no_mercadolivre(navegador, termo, timeout=10):
    """
    Abre MercadoLivre, busca um termo e retorna quando os resultados carregarem.
    
    Args:
        navegador (webdriver.Chrome): Navegador aberto.
        termo (str): Termo de busca.
        timeout (int): Tempo máximo de espera em segundos.
    
    Raises:
        TimeoutException: Se os resultados não carregarem a tempo.
    """
    # Acessar MercadoLivre
    navegador.get('https://www.mercadolivre.com.br')
    
    # Esperar a barra de busca aparecer
    wait = WebDriverWait(navegador, timeout)
    wait.until(EC.presence_of_element_located((By.NAME, 'as_word')))
    
    # Digitar na barra e buscar
    barra_busca = navegador.find_element(By.NAME, 'as_word')
    barra_busca.send_keys(termo)
    barra_busca.send_keys(Keys.RETURN)
    
    # Esperar os resultados aparecerem
    wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'ui-search-layout__item')))


def coletar_produtos(navegador, quantidade_maxima=3):
    """
    Coleta dados de produtos da página de resultados atual.
    
    Args:
        navegador (webdriver.Chrome): Navegador com página de resultados.
        quantidade_maxima (int): Número máximo de produtos a coletar.
    
    Returns:
        list: Lista de dicionários com {'Produto': str, 'Preco': str}
    """
    # Pegar todos os elementos de produto
    elementos = navegador.find_elements(By.CLASS_NAME, 'ui-search-layout__item')
    
    produtos = []
    
    # Processar até quantidade_maxima produtos
    for elemento in elementos[:quantidade_maxima]:
        titulo = extrair_titulo(elemento)
        preco = extrair_preco_elemento(elemento)
        
        produtos.append({
            'Produto': titulo,
            'Preco': preco
        })
    
    return produtos


# ============================================================================
# PARTE 3: FUNÇÃO main() - ORQUESTRA TUDO
# ============================================================================

def main():
    """Função principal: coordena todo o fluxo."""
    
    # 1. LER ARGUMENTOS
    parser = argparse.ArgumentParser(description='Coletor de preços no MercadoLivre')
    parser.add_argument('--query', '-q', required=False, help='Termo de busca (ex: Notebook)')
    parser.add_argument('--max-items', '-n', type=int, default=3, help='Número de itens a coletar')
    parser.add_argument('--output', '-o', default='precos.csv', help='Arquivo CSV de saída')
    parser.add_argument('--headless', action='store_true', help='Executar sem interface visual')
    args = parser.parse_args()
    
    # Se não passou query, pedir interativamente
    if not args.query:
        args.query = input('Informe o termo de busca (ex: Notebook): ').strip()
        if not args.query:
            print('Erro: termo de busca não informado.')
            sys.exit(1)
    
    print('=' * 60)
    print('COLETOR DE PREÇOS - MERCADOLIVRE')
    print('=' * 60)
    
    # 2. CRIAR NAVEGADOR
    print(f'\n1. Iniciando navegador...')
    try:
        navegador = criar_navegador(modo_headless=args.headless)
        print(f'   ✓ Navegador pronto')
    except Exception as e:
        print(f'   ✗ Erro: {e}')
        sys.exit(1)
    
    # 3. BUSCAR
    print(f'\n2. Buscando "{args.query}" no MercadoLivre...')
    try:
        buscar_no_mercadolivre(navegador, args.query)
        print(f'   ✓ Busca concluída')
    except Exception as e:
        print(f'   ✗ Erro na busca: {e}')
        navegador.quit()
        sys.exit(1)
    
    # 4. COLETAR PRODUTOS
    print(f'\n3. Coletando até {args.max_items} produtos...')
    try:
        produtos = coletar_produtos(navegador, quantidade_maxima=args.max_items)
        print(f'   ✓ {len(produtos)} produtos coletados')
    except Exception as e:
        print(f'   ✗ Erro ao coletar: {e}')
        produtos = []
    finally:
        navegador.quit()
    
    # 5. EXIBIR RESULTADOS
    print(f'\n4. Resultados:')
    for i, prod in enumerate(produtos, 1):
        print(f'   [{i}] {prod["Produto"]}')
        print(f'       Preço: {prod["Preco"]}')
    
    # 6. SALVAR EM CSV
    print(f'\n5. Salvando em "{args.output}"...')
    df = pd.DataFrame(produtos)
    df.to_csv(args.output, index=False)
    print(f'   ✓ Arquivo salvo')
    
    print(f'\n' + '=' * 60)
    print(f'CONCLUÍDO: {len(produtos)} produtos')
    print('=' * 60)


# ============================================================================
# EXECUTAR
# ============================================================================

if __name__ == '__main__':
    main()
