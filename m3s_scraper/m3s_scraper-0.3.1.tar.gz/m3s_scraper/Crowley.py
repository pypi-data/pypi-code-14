import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
import unicodecsv as csv



driver = webdriver.Chrome('/Users/old/Downloads/chromedriver')
searchTerm = 'Russian Economy'
fromDate ='2/10/2016 6:29 PM'
toDate='7/18/2016 6:29 PM'
resultDoc = csv.writer(open("trumpTestResults.csv", "wb"), delimiter="|", encoding='utf-8')

def logOn():
    driver.get("https://m3s.tamu.edu")
    time.sleep(5)
    driver.find_element_by_id('UserName').send_keys('ryan_t_w')
    driver.find_element_by_id('Password').send_keys('CREEES#!31')
    driver.find_element_by_class_name('DisplayButton').click()
    time.sleep(2)

def initialSearch():


    #SEARCH TERM
    driver.find_element_by_xpath('//*[@id="SearchBarContainer"]/table/tbody/tr/td[2]/input').click()
    driver.find_element_by_xpath('//*[@id="SearchBarContainer"]/table/tbody/tr/td[2]/input').send_keys(searchTerm)

    # DATE RANGE

    driver.find_element_by_xpath('//*[@id="SearchBarContainer"]/table/tbody/tr/td[2]/input').click()
    time.sleep(6)
    driver.find_element_by_xpath('// *[ @ id = "panelbar"] / li[2]').click()
    time.sleep(1)
    driver.find_element_by_xpath('//*[@id="TimestampDropDown"]/div[5] / a').click()
    driver.find_element_by_xpath('// *[ @ id = "SearchFilterContainerstart_time_adv"]').click()
    driver.find_element_by_xpath('// *[ @ id = "SearchFilterContainerstart_time_adv"]').clear()
    driver.find_element_by_xpath('// *[ @ id = "SearchFilterContainerstart_time_adv"]').send_keys(fromDate)
    driver.find_element_by_xpath('//*[@id="SearchFilterContainerend_time_adv"]').click()
    driver.find_element_by_xpath('//*[@id="SearchFilterContainerend_time_adv"]').clear()
    driver.find_element_by_xpath('//*[@id="SearchFilterContainerend_time_adv"]').send_keys(toDate)



    # SOURCES
    driver.find_element_by_xpath('//*[@id="panelbar"]/li[3]').click()
    driver.find_element_by_xpath('// *[ @ id = "panelbar"] / li[3]').click()
    driver.find_element_by_xpath('//*[@id="panelbarAdvanced"]/li[3]/span').click()
    driver.find_element_by_xpath('//*[@id="panelbarAdvanced"]/li[3]/div[1]/div/ul/li/input').click()
    time.sleep(1)
    driver.find_element_by_xpath('//*[@id="panelbarAdvanced"]/li[3]/div[1]/div/div/ul/li[6]').click()


    # ENGAGE!!
    driver.find_element_by_xpath('//*[@id="SearchBarContainer"]/table/tbody/tr/td[3]/div').click()
    time.sleep(7)



def sourceTokenTime(encodedlist, words):
    if len(words) > 600:
        for x in range(600):
            encodedlist.append(words[x].text + ' ')
    else:
        for word in words:
            encodedlist.append((word.text + ' '))
    return encodedlist


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
        print(len(words))

        # Adds Source Tokens to List

        encodedlist = []

        try:
            encodedlist = sourceTokenTime(encodedlist,words)

        except:
            print("""ERROR ERROR
                this was unattached. now attempting to go to the next page...
                """)
            time.sleep(7)
            driver.execute_script("($('#NextButton')).click()")
            words = []
            if driver.find_element_by_class_name('communication-error'):
                print "MAJOR ERROR"
            else:
                continue

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

        WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, '// *[ @ id = "NextButton"]')))
        driver.execute_script("($('#NextButton')).click()")













def searchResultsMonster():
    # driver.find_element_by_xpath("//*[@id='PageForward']").click()
    # time.sleep(3)
    # driver.find_element_by_xpath("//*[@id='PageForward']").click()
    # time.sleep(3)
    # driver.find_element_by_xpath("//*[@id='PageForward']").click()
    for x in range(12):
        time.sleep(3)
        driver.find_element_by_xpath("//*[@id='PageForward']").click()

    bluex = 'blue'
    while bluex == 'blue':
            for i in range(0, 50):
                WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.CLASS_NAME, 'ListItemTitle')))
                this = driver.find_elements_by_xpath("//*[contains(@id, 'ListItem-')]")
                idString= str(this[i].get_attribute("id"))
                print(idString)
                scriptString = "ResultsList.NavigateToDataEndPoint($('#"+idString+"').children('.ListItem'))"
                print(scriptString)
                driver.execute_script(scriptString)
                articleMonster()
            print('you should never see this')


def scrapeIntro():
    print("""Welcome to m3s_scraper. Have you downloaded chromedriver?""")
    chromedrivercheck = raw_input('Please type "yes" or "no"')
    if chromedrivercheck == "yes":
        pass
    else:
        print('Please download chromedriver and try again.')
        return

    print('Please paste the path to chromedriver.')
    chromedriverpath = raw_input('>')
    un = raw_input('Please enter your M3S username')
    pw = raw_input('Please enter your M3S password')
    usersearchTerm= raw_input('Please enter your search term')
    userstartDate = raw_input('Please enter your starting date in the format "2/10/2016 6:29 PM"')
    userendDate = raw_input('Please enter your ending date in the format "2/10/2016 6:29 PM"')





# 'ryan_t_w'
# 'CREEES#!31'

def sequence():




    logOn()

    initialSearch()
    searchResultsMonster()




sequence()