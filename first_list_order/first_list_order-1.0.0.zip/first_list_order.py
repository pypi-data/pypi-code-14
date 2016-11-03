"""Esse módulo nester.py fornece um função chamada print_lol que permite processar e imprimir uma lista ela estando aninhadas ou não."""

def print_lol(the_list):

    """Essa função requer um argumento posicional chamado "the_list", que é qualquer lista em python. Cada item de dados na lista fornecida é
(recursivamente) impresso na tela em sua propria linha"""
    
    for each_item in the_list:
        if isinstance(each_item, list):
            print_lol(each_item)
        else:
            print(each_item)

            
