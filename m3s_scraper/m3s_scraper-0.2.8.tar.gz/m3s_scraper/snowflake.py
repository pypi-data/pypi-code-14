import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import unicodecsv as csv
import datetime



driver = webdriver.Chrome()

timeRightNow = str(datetime.datetime.now().time())
timeRightNow = timeRightNow[:8]
print (timeRightNow)
resultDoc = csv.writer(open(timeRightNow + ".csv", "wb"), delimiter="|", encoding='utf-8')
wordlimit = 600


def getInfo():
    Username = raw_input('Please enter your Username:   ')
    Password = raw_input('Please enter your Password:    ')
    print('Please enter a search start date in this format - 2/10/2016 - or type "today"')
    startdate = raw_input('>').lower()

    print(startdate)

    print('Please enter a search stop date in this format - 2/10/2016 - or type "today"')
    stopdate = raw_input('>').lower()

    print('Please type a source')
    # print('Type "A" for Arabic, "C" for Chinese, "E" for English, "F" for Farsi, or "R" for Russian.')

    source = raw_input('>').lower()
    print('Please enter your search term.')

    searchTerm = raw_input('>')



    initalInfo = {'uName': Username, 'pWord': Password, 'sDate': startdate, 'stDate': stopdate, 'source': source, 'sTerm':searchTerm}
    return initalInfo






def logOn(userData):
    driver.get("https://m3s.tamu.edu")
    time.sleep(5)
    # driver.find_element_by_id('UserName').send_keys(userData['uName'])
    # driver.find_element_by_id('Password').send_keys(userData['pWord'])
    driver.find_element_by_id('UserName').send_keys('ryan_t_w')
    driver.find_element_by_id('Password').send_keys('CREEES#!31')

    driver.find_element_by_class_name('DisplayButton').click()
    time.sleep(2)

def initialSearch(userData):


    #SEARCH TERM
    driver.find_element_by_xpath('//*[@id="SearchBarContainer"]/table/tbody/tr/td[2]/input').click()
    driver.find_element_by_xpath('//*[@id="SearchBarContainer"]/table/tbody/tr/td[2]/input').clear()
    driver.find_element_by_xpath('//*[@id="SearchBarContainer"]/table/tbody/tr/td[2]/input').send_keys(userData['sTerm'])

    # DATE RANGE
    driver.find_element_by_xpath('//*[@id="SearchBarContainer"]/table/tbody/tr/td[2]/input').click()
    time.sleep(6)
    driver.find_element_by_xpath('// *[ @ id = "panelbar"] / li[2]').click()
    time.sleep(1)
    driver.find_element_by_xpath('//*[@id="TimestampDropDown"]/div[5] / a').click()
    WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="TimestampDropDown"]/div[5] / a')))
    driver.find_element_by_xpath('// *[ @ id = "SearchFilterContainerstart_time_adv"]').click()
    driver.find_element_by_xpath('// *[ @ id = "SearchFilterContainerstart_time_adv"]').clear()
    driver.find_element_by_xpath('// *[ @ id = "SearchFilterContainerstart_time_adv"]').send_keys(userData['sDate']+' 12:00 AM')
    driver.find_element_by_xpath('//*[@id="SearchFilterContainerend_time_adv"]').click()
    driver.find_element_by_xpath('//*[@id="SearchFilterContainerend_time_adv"]').clear()
    driver.find_element_by_xpath('//*[@id="SearchFilterContainerend_time_adv"]').send_keys(userData['stDate']+' 12:00 AM')

    # SOURCES
    driver.find_element_by_xpath('//*[@id="panelbar"]/li[3]').click()
    driver.find_element_by_xpath('// *[ @ id = "panelbar"] / li[3]').click()
    time.sleep(1)
    driver.find_element_by_xpath('//*[@id="panelbarAdvanced"]/li[3]/span').click()
    # driver.find_element_by_xpath('//*[@id="panelbarAdvanced"]/li[3]/div[1]/div/ul/li/input').click()
    time.sleep(4)
    driver.find_element_by_xpath('//*[@id="panelbarAdvanced"]/li[2]/span').click()
    time.sleep(4)
    driver.find_element_by_xpath('//*[@id="panelbarAdvanced"]/li[2]/div[2]/div/ul/li').click()
    driver.find_element_by_xpath('//*[@id="panelbarAdvanced"]/li[2]/div[2]/div/ul/li/input').clear()
    driver.find_element_by_xpath('//*[@id="panelbarAdvanced"]/li[2]/div[2]/div/ul/li/input').send_keys(userData['source'])
    time.sleep(4)
    driver.find_element_by_xpath('//*[@id="panelbarAdvanced"]/li[2]/div[2]/div/ul/li/input').send_keys(Keys.RETURN)
    time.sleep(4)

    # driver.find_element_by_xpath('//*[@id="panelbarAdvanced"]/li[3]/div[1]/div/div/ul/li[6]').click()


    # ENGAGE!!
    driver.find_element_by_xpath('//*[@id="SearchBarContainer"]/table/tbody/tr/td[3]/div').click()



def sourceTokenTime(encodedlist, words):

    encodedlist.extend([(x.text + ' ') for x in words[:600]]) # conrad
    return encodedlist # conrad









def articleMonster():
    articlediagnum= 0
    blueX = "green"
    while blueX == "green":
        print(articlediagnum)
        words = []
        WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, '//*[@id="Source_Name"]')))
        WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CLASS_NAME, 'sourceToken')))
        WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.CLASS_NAME, 'sourceToken')))
        time.sleep(5)
        words = driver.find_elements_by_class_name('sourceToken')

        articleBufferString = ''


        # Adds Source Tokens to List

        encodedlist = []

        try:
            encodedlist = sourceTokenTime(encodedlist,words)

        except:
            print("""ERROR ERROR
                this was unattached. now attempting to go to the next page...
                """)
            time.sleep(7)
            driver.execute_script("AdjustTranscriptLayout.NextButton();")
            words = []
            print('major error')

            WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, '//*[@id="Source_Name"]')))
            WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CLASS_NAME, 'sourceToken')))
            WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.CLASS_NAME, 'sourceToken')))
            time.sleep(5)
            words = driver.find_elements_by_class_name('sourceToken')

            articleBufferString = ''
            time.sleep(2)
            encodedlist = sourceTokenTime(encodedlist,words)






        # metadata

        articleBufferString += articleBufferString.join(encodedlist)
        articleSource = driver.find_element_by_xpath('//*[@id="Source_Name"]')
        articleDate = driver.find_element_by_class_name('sourceCaptureTime')
        # print('this is articleSource')
        # print(articleSource.get_attribute('value'))
        # print('this is articledate')
        # print(articleDate.get_attribute('value'))

        articleBufferString = (articleSource.get_attribute('value')).encode('utf-8') + '|******' + articleBufferString

        articleBufferString = (articleDate.get_attribute('value')).encode('utf-8') + '|' + articleBufferString
        # print(articleBufferString)

        # Adds List item to CSV
        resultDoc.writerow(articleBufferString)
        articlediagnum+=1
        # ok need to get over this, it's just straight up going to be formatted into columns. FML

        WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, '// *[ @ id = "PageForward"]')))
        driver.execute_script("AdjustTranscriptLayout.NextButton();")



def searchResultsMonster():

    # # # --------------WaitCODE------------------------------


    # for x in range(13):
    #     time.sleep(3)
    #     driver.execute_script("ResultsList.PageForward();")
        # driver.find_element_by_xpath('//*[@id="PageForward"]').click()

    bluex = 'blue'
    while bluex == 'blue':
            for i in range(0, 50):
                WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.CLASS_NAME, 'ListItemTitle')))
                this = driver.find_elements_by_xpath("//*[contains(@id, 'ListItem-')]")
                idString= str(this[i].get_attribute("id"))
                print(idString)
                scriptString = "ResultsList.NavigateToDataEndPoint($('#"+idString+"').children('.ListItem'))"

                driver.execute_script(scriptString)
                articleMonster()
            print('you should never see this')






def sequence():
    userData = getInfo()

    logOn(userData)

    initialSearch(userData)
    searchResultsMonster()




sequence()