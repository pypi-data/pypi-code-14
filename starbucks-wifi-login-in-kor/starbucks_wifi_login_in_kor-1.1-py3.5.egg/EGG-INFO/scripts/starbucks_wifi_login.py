#!/usr/local/opt/python3/bin/python3.5

import time
import os.path
from selenium import webdriver

# 현재 드라이버
# 셀레리엄 chrome 모듈을 로드하기위해서 필요하다.
curdir = os.path.join(os.path.dirname(__file__))

# 스타벅스 로그인 과정 자동 입력기
# Selenium을 이용해서 웹브라우저를 하나 만들고 웹브라우저를 통해서
# 자동 로그인한다.
class StarbuckPage(object):
    def __init__(self):
        self.driver = self._create_webdriver()

    def _create_webdriver(self):
        "web driver 생성."

        # Chrome용 웹드라이버다.
        # selenium에서 지원하는 웹브라우저는 모두 사용가능하다.
        driver_path = os.path.join(curdir, '..', 'webdriver', "chromedriver")
        driver = webdriver.Chrome(driver_path)
        
        return driver

    def current_url(self):
        "현재 경로 확인"

        # javascript를 통해서 현재 url을 구할 수 있다.
        return self._exec_js('return location.toString()')

    def go_url(self, url):
        "주어진 url로 이동"
        
        self.driver.get(url)

    def _exec_js(self, js):
        "javascript 실행"

        
        try:
            # 자바스크립트를 실행시킨다.
            # 자바스크립트에 return 문이 있으면 결과를 볼 수 있다.
            # 넘어오는 데이터는 json 모듈로 로드한것이라고 보면 된다.
            # json은 한정된 데이터 타입만 가지고 있다.
            # 이 데이터들이 python 타입으로 자동 변환된다.
            ret = self.driver.execute_script(js)
            return ret
        except Exception as e:
            print(type(e))
            print(e)

    def clickAccessWifi(self):
        "첫화면에서 무료 사용하기 버튼을 누른다."
        
        while True:
            # 확인 버튼 누르기
            # find_element_XXX로 element를 찾아서 click하는 것
            element = self.driver.find_element_by_css_selector(".goWifi a")
            if element:
                element.click()
                break
            
            time.sleep(0.5)

    def inputPersonInfo(self, person):
        "필요한 정보들을 입력한다."

        # 필요한 내용을 입력한다. 여기서 사용하고 있는 CSS selector는
        # 웹브라우저에서 순수 한노드 한 노드씩 찾은 것이다.
        # 이게 가장 시간이 많이 걸렸다.
        
        element = self.driver.find_element_by_css_selector("#userNm")
        element.send_keys(person["name"])
        element = self.driver.find_element_by_css_selector("#cust_email_addr")
        element.send_keys(person["email"])
        element = self.driver.find_element_by_css_selector("#kt_btn")
        # 전화번호 종류에 대한 라디오 버튼 클릭
        # 라디오 버튼도 버튼이다.
        element = self.driver.find_element_by_css_selector("#agree1")
        if element:
            element.click()
        element = self.driver.find_element_by_css_selector("input[name=cust_hp_no]")
        element.send_keys(person["tel"])

        # SEND 버튼이 눌리면 호출된는 javascript 코드를 호출했다.
        # 위 처럼 버튼을 찾아서 click해도 된다.
        self._exec_js('goAct()')

def auto_login(me):
    page = StarbuckPage()
    page.go_url('http://www.jinniahn.com/')
    
    while True:
        url = page.current_url()

        # 바로 원하는 페이지로 가게 되면
        # 이미 무료인터넷을 사용할 수 있는 것이니 여기서 끝
        if url.startswith('http://www.jinniahn.com'):
            return True

        # Login 페이지로 넘어가면
        if url.startswith('http://first.wifi.olleh.com/'):
            # 혹시 영어 페이지로 이동하도록
            # 자료 입력 로직이 영어 페이지에 맞추어져 있다.
            # 영어와 한글페이지에 요구되는 데이터가 다르다.
            page.go_url('http://first.wifi.olleh.com/starbucks/index_en_new.html')
            time.sleep(0.5)
            break

    # 확인 버튼 클릭
    page.clickAccessWifi()
    time.sleep(0.5)

    # 사용자 데이터 입력하고 
    page.inputPersonInfo(me)
    while True:
        url = page.current_url()

        # 아래 URL로 가면 성공
        if url == 'http://www.istarbucks.co.kr:8000/wireless/wireless.asp':
            return True
        time.sleep(0.5)

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


