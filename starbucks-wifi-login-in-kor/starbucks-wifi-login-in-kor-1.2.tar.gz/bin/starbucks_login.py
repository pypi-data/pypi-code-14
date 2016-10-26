from starbucks_wifi.login import auto_login

if __name__ == '__main__':
    import os.path
    import json

    #{{{ 여기서를 자신에게 맞게 수정
    my_data = json.load(open(os.path.expanduser("~/.me/me.json"), encoding='utf-8'))

    info = {
        "name": my_data["name"],
        "email": my_data["email"],
        "tel": my_data["tel"]
    }
    #}}}
    
    if auto_login(info):
        print("[!] Enjoy starbuck life")




