# try_python.py

# 함수 print_list(the_list)를 포함

# 리스트의 항목을 차례대로 표시하며 항목 자체가 리스트(하위 리스트)인 경우 하위리스트의 항목도 차례대로 표시

def print_list(the_list):

    for each_item in the_list:

        if isinstance(each_item,list):

            print_list(each_item)

        else:

            print(each_item)

            
