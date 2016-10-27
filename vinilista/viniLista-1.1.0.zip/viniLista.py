"""Este é o módulo "nester.py", e fornece uma função chamada print_lol()
que imprime listas que podem ou não incluir listas aninhadas."""

def list_vi(the_list, tabula): 
    """Esta função requer um argumento posicional chamado "the_list", que é
        qualquer lista Python(de possíveis listas aninhadas). Cada ítem de dados na
	lista fornecida é(recursivamente) impresso na tela em sua própria linha.
	Um segundo argumento chamado 'tabula' é usado para inserir tabulações quando
	uma lista aninhada é encontrada"""
	
    for each_item in the_list:
        if isinstance(each_item, list):
            list_vi(each_item, tabula+1)
        else:
            for tab_stop in range(tabula):        
                print("\t", end='')
                print(each_item)
        
