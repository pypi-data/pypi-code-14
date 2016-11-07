import sys
import requests
from bs4 import BeautifulSoup
import re
import os
import socket
def print_globalip():
    pass
def parse(find_list):
    parse_list=[]
    for i in find_list:
        parse_list.append(list(i)[1])
    return parse_list
def create_file(file_name):
    file=open(os.getcwd()+"\\search\\"+file_name+".txt","w")
    file.close()
def save(file_name,parsed_list,page_number):
    file = open(os.getcwd()+"\\search\\"+file_name + ".txt", "a")
    file.write(str((page_number//10)+1)+"\n")
    for i in parsed_list:
        file.write(i)
        file.write("\n")
    file.close()
def find_rank(parsed_list,page_number,search_query):
    for i in parsed_list:
        if i.find(search_query)!=-1:
            print(i)
            print("Your Website Is In Page " + str((page_number // 10) + 1)+" Number :"+str(parsed_list.index(i)))
            return True
    return False

def enter_website(query_list):
    website_pattern=r"(www)(\.)(.*)(\.)(.+)"
    search_query = input("Please Enter Your Website:")
    if re.match(website_pattern,search_query):
        query_list.append(search_query)
        return query_list
    else:
        print("Wrong Pattern")
        query_list.append(search_query)
        enter_website(query_list)
def make_dir(dir_name="search"):
    list_dir=os.listdir()
    if dir_name not in list_dir:
        os.mkdir(dir_name)
def search_in(num_page,static_string,query,pattern,end_pattern,search_query):
    traffic_pattern="Our systems have detected unusual traffic from your computer network"
    traffic_flag=False
    make_dir()
    create_file(query)
    try:
        find_flag = []
        if num_page < 1:
            num_page = 1
        num_page_range = list(range(0, num_page * 10, 10))

        for i in num_page_range:
            content_1 = requests.get(static_string + query + "&start=" + str(i))

            files = BeautifulSoup(content_1.content, "html.parser")
            preti = files.prettify()
            if preti.find(end_pattern)!=-1:
                print("There Is No More Page")
                break
            traffic_flag=preti.find(traffic_pattern)
            if traffic_flag!=-1:
                print("Unusual Traffic In Network Try later")
                print(socket.gethostbyname(socket.gethostname())+" Is your Local IP")
                break
            finds = re.findall(pattern, preti)
            parsed_list = parse(finds)
            find_flag.append(find_rank(parsed_list, i, search_query))
            save(query, parsed_list, i)
            print("Page "+str((i // 10) + 1) + " Scraped!!")
        if not any(find_flag) and traffic_flag==False:
            print("Your Website: "+search_query+" is not in google search for "+query+" until page "+str(num_page+1))
    except:
        repeat=input("Error In Scraping , [1] Try Again , [2] Exit")
        if int(repeat)==1:
            main()
        else:
            sys.exit()
def f_query(query_list):
    num_wrong_attempt=len(query_list)-1
    return [num_wrong_attempt,query_list.pop(-1)]
def main():
    search_query_list=[]
    end_pattern="did not match any documents"
    pattern = r'(href="/url.q=)(.*)(">)'
    static_string = "https://www.google.com/search?q="
    query = input("Please Enter Your Request:")
    num_page = int(input("Please Enter Number Of Pages:"))
    enter_website(search_query_list)
    search_query=f_query(search_query_list)
    print(str(search_query[0])+" Wrong Attempts!!")
    if len(search_query_list)!=0:
        print(search_query_list)
    search_in(num_page,static_string,query,pattern,end_pattern,search_query[1])