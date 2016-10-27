"""Este é o módulo "nester.py", e fornece uma função chamada print_lol()
que imprime listas que podem ou não incluir listas aninhadas."""

def list_vi(the_list, indent=False, level=0): 
    """Esta função requer um argumento posicional chamado "the_list", que é
        qualquer lista Python(de possíveis listas aninhadas). Cada ítem de dados na
	lista fornecida é(recursivamente) impresso na tela em sua própria linha.
	Um segundo argumento chamado 'level' é usado para inserir tabulações quando
	uma lista aninhada é encontrada"""
	
    for each_item in the_list:
        if isinstance(each_item, list):
            list_vi(each_item, indent, level+1)
        else:
            if indent:
                for tab_stop in range(level):        
                    print("\t", end='')
            print(each_item)
        
            
