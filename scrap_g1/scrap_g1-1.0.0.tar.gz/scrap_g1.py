import re
from bs4 import BeautifulSoup
from urllib.request import urlopen


def scrap_g1(bsObj):


	with open('redirecionadores_duplicados.txt','w') as redirecionadores_duplicados_txt:
		for link in bsObj.findAll('a', href = re.compile('^(//g1.globo.com/busca/)')):
			print(link['href'], file = redirecionadores_duplicados_txt)


	with open('redirecionadores_duplicados.txt','r') as redirecionadores_duplicados_txt:
		links = redirecionadores_duplicados_txt.read().splitlines() #lista contendo todos os redirecionadores da pagina
		links = sorted(set(links)) #Formatacao da lista contendo os redirecionadores, removendo os duplicados
		with open('redirecionadores.txt','a') as links_busca: #cria um arquivo para armazenar os redirecionadores finais
			for link in links: #insere os links no arquivo txt
				print(link, file = links_busca)


	with open('materias.txt','a') as materias:
		for link in links:
			html_redirecionador = urlopen("http:"+link) #E necessario inserir o http: para funcionar o comando
			bsObj_redirecionador = BeautifulSoup(html_redirecionador) #Beautiful Soup do redirecionador, usado para buscar o link real da materia
			buscador_link_materia = bsObj_redirecionador.find('meta', attrs={'http-equiv': 'refresh'}) #Busca o link da pagina
			link_final = buscador_link_materia['content'].partition('=')[2].replace("'","") #higieniza o link
			print(link_final, file = materias) #insere o link em um arquivo de texto	
