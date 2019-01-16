#!python3

""" Programa que faz um web scrapping básico e retorna os números
	da Mega Sena. Em seguida os armazena num banco de dados."""

import requests, sqlite3
from bs4 import BeautifulSoup

def scrapping():
	""" Função que faz o web scrapping """

	# Fazer o request da página
	pagina = requests.get("http://loterias.caixa.gov.br/wps/portal/loterias/landing/megasena/")

	# Verifica se o request deu certo
	if (pagina.status_code == 200):

		# Instanciar o BeautifulSoup
		soup = BeautifulSoup(pagina.content, 'html.parser')

		# Procurar na pagina onde fica
		concursoDiv = soup.find(class_="title-bar")
		grupo = soup.find(class_="numbers megasena")
		# Adentrar no concursoDiv para pegar o texto
		concurso = concursoDiv.find("span")
		concurso = concurso.get_text()
		# Adentrar no grupo de numeros para pega-los individualmente
		numeros = grupo("li")

		# Cria a lista que receberá os numeros
		listaNumeros = []

		# Itera nos numeros adicionando-os a lista
		for i in numeros:

			listaNumeros.append((i.get_text()))

		# Printa resultado
		print(concurso)
		print(" - ".join(listaNumeros))

		return {'concurso': concurso, 'numeros': listaNumeros}

	else: # Caso o request retorne erro
		print("Erro no request da página")
		return False

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
	print(lista)
	if lista:
		save(lista)

if __name__ == '__main__':
	main()