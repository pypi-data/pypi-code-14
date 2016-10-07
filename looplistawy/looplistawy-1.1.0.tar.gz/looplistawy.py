def print_lol(the_list,level):
"""Esta função serve para imprimir na tela todos os itens de uma lista, até mesmo listas aninhadas, isto é, elementos-listas que podem conter dentro de listas"""
	for each_item in the_list:
		if isinstance(each_item,list):
			print_lol(each_item,level+1)
		else:
                        for tab_stop in range(level):
                                print("\t",end='')
                        print(each_item)
