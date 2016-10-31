import sys
"""Este é o módulo "recursivefunc.py" que fornece uma função chamada print_lol()
que imprime listas que podem ou não incluir listas aninhadas."""
def print_lol(the_list,indent=False,level=0,fh=sys.stdout):
        """Esta função requer um argumento posicional chamado "the_list", que é qualquer
        lista Python (de possíveis listas aninhadas). Cada item de dados na lista fornecida
        é (recursivamente) impressso na tela em sua própria linha. Um segundo argumento da
        chamada de "indent" que controla ou não o recuo e é mostrado no visor. Este padrão é False: definí-la
        como True para ligar. Um terceiro argumento chamado de "level" (que assume 0) é usado para
        inserir a tabulação quando uma lista aninhada é encontrada. Por fim, um último argumento
        chamado de "fh" define a saída padrão onde é impressa a lista de possíveis listas aninhadas.
        Por padrão seu valor é "stdout" para indicar que a saída padrão é o visor. Porém, é possível
        atribuí-lo um objeto file para indicar que a saída é um arquivo"""
        for each_item in the_list:
                        if isinstance(each_item,list):
                                print_lol(each_item,indent,level+1,fh)
                        else:
                                if indent:
                                        for tab_stop in range(level):
                                                print("\t",end="",file=fh)
                                print(each_item,file=fh)
