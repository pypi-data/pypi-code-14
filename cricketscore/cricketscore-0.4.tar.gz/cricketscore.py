from bs4 import BeautifulSoup
import requests
import notify2


url = "http://www.espncricinfo.com/ci/engine/match/1034809.html"
filename = "cricket_summary.txt"
info_dict = {'old_info': ""}

while True:
    r = requests.get(url)
    data = r.text
    soup = BeautifulSoup(data, "html.parser")


    def send_notification():
        notify2.init('app')
        with open(filename,'r') as f:
            cric_sum = f.readline()
        n = notify2.Notification(cric_sum)
        n.show()
        n.close()


    for i in soup.find_all('title'):
        info = i.get_text()
        new_info = str(info)
        info_dict['new_info'] = new_info
        if info_dict['new_info'] != info_dict['old_info']:
            print "Difference"
            print 'new_info: ' + info_dict['new_info']
            print 'old_info: ' + info_dict['old_info']
            with open(filename, 'wb') as f:
                f.write(new_info.strip())
            info_dict['old_info'] = info_dict['new_info']
            send_notification()

