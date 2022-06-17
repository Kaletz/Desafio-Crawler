from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import pandas as pd

cards = []

url = 'https://www.oceans14.com.br/acoes/oi/oibr/balanco-dividendos'

headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36 OPR/87.0.4390.58'}

req = Request(url, headers = headers)

response = urlopen(req)

html = response.read().decode('utf-8')
soup = BeautifulSoup(html, 'html.parser')
tabelaNumeros = soup.find('div', {"id": "tabelaLucratividade"}).findAll('td', class_="fonteNormal")
tabelaAnos = soup.find('div', {"id": "tabelaLucratividade"}).findAll('td', class_="fonteDestaque")
tabelaNomes = soup.find('div', {"id": "tabelaLucratividade"}).findAll('th', class_="fonteDestaque")

listaAnos = []
for ano in tabelaAnos:
  listaAnos.append(int(ano.get_text()))

listaAnos.pop() #Removo 2022 por não ser um ano cheio

listaNomes = []

for nome in tabelaNomes:
  listaNomes.append((nome.get_text()))


#Criei duas listas com os valores já tratados, deixados passos futuros mais legíves 

i = 1
for valores in tabelaNumeros:
  card = {}
  # a cada (len(listaAnos) + 1) valores é uma linha, com len(listaNomes) parametros => Nesse caso, 288 números
  card [str(i)] = valores.get_text()
  i = i + 1 
  cards.append(card)
  

for a in range((len(listaAnos)+1)*len(listaNomes) - 1):
  r = int(a / (len(listaAnos) + 1))
  cards[a][tabelaNomes[r].getText()] = cards[a].pop(str(a+1))

final = []
j = 0
k = 0
for ano in listaAnos:
  reorg = {}
  reorg['Ano'] = ano
  for nome in listaNomes:
    reorg[nome] = cards[j][nome]
    j = j + (len(listaAnos) + 1)
  final.append(reorg)
  k = k + 1
  j = k

dataset = pd.DataFrame(final)

dataset.to_csv(r'C:\Users\grand\OneDrive\Documentos\Alura\Python para Data Science\Desafio\export.csv', sep=';', index = False, encoding = 'utf-8-sig')
