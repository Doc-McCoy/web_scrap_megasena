#!python3

"""
Programa que faz um web scrapping básico e retorna os números
da Mega Sena. Em seguida os armazena num banco de dados.
"""

import sqlite3
from bs4 import BeautifulSoup
from selenium import webdriver

""" 
Utilizei o selenium ao invés do requests que é bem mais simples,
pois a página da caixa tem seu conteúdo gerado dinamicamente.
"""

def scrapping():
	""" Função que faz o web scrapping """

	# Fazer o request da página
	url = "http://loterias.caixa.gov.br/wps/portal/loterias/landing/megasena/"
	driver = webdriver.Firefox()
	driver.implicitly_wait(3)
	driver.get(url)
	html = driver.page_source
	driver.close()

	# Instanciar o BeautifulSoup
	soup = BeautifulSoup(html, "html.parser")

	# Procurar na pagina onde fica
	concursoDiv = soup.find(class_="title-bar")
	grupo = soup.find(class_="numbers megasena")
	# Adentrar no concursoDiv para pegar o texto
	concurso = concursoDiv.find("span")
	concurso = concurso.get_text(strip=True) # A opção strip corta fora os \n, \t, etc.
	# Adentrar no grupo de numeros para pega-los individualmente
	numeros = grupo("li")

	# Cria a lista que receberá os numeros
	listaNumeros = []

	# Itera nos numeros adicionando-os a lista
	for i in numeros:
		listaNumeros.append((i.get_text()))

	return {'concurso': concurso, 'numeros': listaNumeros}

def save(lista):
	''' Função que recebe o array e faz as inserções '''

	conn = sqlite3.connect('megasena_simples.db')
	cursor = conn.cursor()
	
	cursor.execute("""
		CREATE TABLE IF NOT EXISTS megasena (
			id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
			concurso TEXT,
			val1 INTEGER,
			val2 INTEGER,
			val3 INTEGER,
			val4 INTEGER,
			val5 INTEGER,
			val6 INTEGER
		);
	""")

	cursor.execute("""
		INSERT INTO megasena (concurso, val1, val2, val3, val4, val5, val6)
		VALUES (?, ?, ?, ?, ?, ?, ?)
	""", (lista['concurso'], lista['numeros'][0], lista['numeros'][1], lista['numeros'][2], lista['numeros'][3], lista['numeros'][4], lista['numeros'][5])
	)

	conn.commit()

	conn.close()

def main():
	lista = scrapping()
	# print(lista)
	if lista:
		save(lista)

if __name__ == '__main__':
	main()