from colorama import init, Fore, Back, Style; init(autoreset=True)

def prRed(*message, **kwargs):
    print(Fore.RED + ' '.join(message), **kwargs)