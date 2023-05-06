import PySimpleGUI as sg
from bs4 import BeautifulSoup
import pandas as pd
import requests
import os

sg.theme('DarkAmber')

layout = [
    [sg.Text('Digite o produto'), sg.Input(key='pesquisa')],
    [sg.Button('Iniciar scraping')],
]

janela = sg.Window('Pesquisa', layout)

def salvar_planilha(df):
    df = df.sort_values('Preço', ascending=False)
    df.to_excel('resultado.xlsx', index=False)
    sg.popup("Scraping finalizado :)")
    os.startfile('resultado.xlsx')


def fazer_scraping():

    url = f"https://lista.mercadolivre.com.br/{valores['pesquisa']}#D[A:{valores['pesquisa']}]"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    titulos = []
    precos = []

    containers_produto = soup.find_all('div', {'class': 'ui-search-result__content-wrapper'})

    for container in containers_produto:
 
        titulo_elemento = container.find('h2', {'class': 'ui-search-item__title'})
        if titulo_elemento:
            titulo = titulo_elemento.text.strip()
        else:
            titulo = "N/A"

        preco_inteiro_elemento = container.find('span', {'class': 'price-tag-fraction'})
        preco_centavos_elemento = container.find('span', {'class': 'price-tag-cents'})
        if preco_inteiro_elemento and preco_centavos_elemento:
            preco = float(preco_inteiro_elemento.text.strip() + '.'+ preco_centavos_elemento.text.strip())
        elif preco_inteiro_elemento:
            preco = float(preco_inteiro_elemento.text.strip() + '.00')
        else:
            preco = None

        if preco:
            titulos.append(titulo)
            precos.append(preco)

    df = pd.DataFrame({'Nome': titulos, 'Preço': precos})
    salvar_planilha(df)

def abrir_navegador():
    fazer_scraping()

while True:
    evento, valores = janela.read()
    if evento == sg.WIN_CLOSED:
        break
    if evento == 'Iniciar scraping':
        abrir_navegador()
