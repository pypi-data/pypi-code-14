from bs4 import BeautifulSoup
import requests
import pynotify


url = "http://www.espncricinfo.com/ci/engine/match/1034809.html"
filename = "cricket_summary.txt"
info_dict = {'old_info': ""}

while True:
    r = requests.get(url)
    data = r.text
    soup = BeautifulSoup(data, "html.parser")


    def send_notification():
        pynotify.init('app')
        with open(filename,'r') as f:
            cric_sum = f.readline()
        n = pynotify.Notification(cric_sum)
        n.show()


    for i in soup.find_all('title'):
        info = i.get_text()
        new_info = str(info)
        info_dict['new_info'] = new_info
        if info_dict['new_info'] != info_dict['old_info']:
            print "rajat"
            with open(filename, 'wb') as f:
                f.write(new_info.strip())
            info_dict['old_info'] = info_dict['new_info']
            send_notification()

