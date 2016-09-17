import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import unicodecsv as csv


#'/Users/old/Downloads/chromedriver'

driver = webdriver.Chrome()
fromDate ='2/10/2016 6:29 PM'
toDate = '7/18/2016 6:29 PM'
sourceListLength= 0
currentSourceIndex = 0




resultDoc = csv.writer(open("M3S_Results.csv", "wb"), delimiter=" ", encoding='utf-8')
wordlimit = 600


















def getInfo():
    Username = raw_input('Please enter your Username:   ')
    Password = raw_input('Please enter your Password:    ')
    print('Please enter a search start date in this format - 2/10/2016 - or type "today"')
    startdate = raw_input('>').lower()

    print(startdate)

    print('Please enter a search stop date in this format - 2/10/2016 - or type "today"')
    stopdate = raw_input('>').lower()

    print('Please choose a source language')
    print('Type "A" for Arabic, "C" for Chinese, "E" for English, "F" for Farsi, or "R" for Russian.')

    language = raw_input('>')
    print('Please enter your search term.')

    searchTerm = raw_input('>')



    initalInfo = {'uName': Username, 'pWord': Password, 'sDate': startdate, 'stDate': stopdate, 'lang': language, 'sTerm':searchTerm}
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


def initialSearch(userData, sourceList):


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
    time.sleep(15)
    resultCount = driver.find_element_by_xpath('//*[@id="ToolbarContentTitle"]/span[1]').text
    resultCount = int(resultCount)
    print(resultCount)

    if resultCount == 0:
        print ('yeah this is definitely it, problem-wise.')
        return 'MI7: Ghost Protocol: Tokyo Drift Edition TM'
    else:
        WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.CLASS_NAME, 'ListItemTitle')))
        this = driver.find_elements_by_xpath("//*[contains(@id, 'ListItem-')]")
        idString = str(this[i].get_attribute("id"))
        print(idString)
        scriptString = "ResultsList.NavigateToDataEndPoint($('#" + idString + "').children('.ListItem'))"
        print(scriptString)
        driver.execute_script(scriptString)
        articleMonster(sourceList)





def sourceTokenTime(encodedlist, words):

    encodedlist.extend([(x.text + ' ') for x in words[:600]]) # conrad
    return encodedlist # conrad



def changeSourceSearch(sourceList, currentSourceIndex):
    time.sleep(17)

    driver.find_element_by_xpath('//*[@id="SearchBarContainer"]').click()
    driver.find_element_by_xpath('//*[@id="SearchBarContainer"]/table/tbody/tr/td[2]/input').click()
    driver.find_element_by_xpath('//*[@id="SearchBarContainer"]/table/tbody/tr/td[2]').click()
    time.sleep(1)
    driver.find_element_by_xpath('//*[@id="panelbarAdvanced"]/li[2]/div[2]/div/ul/li[1]/a').click()
    time.sleep(1)
    driver.find_element_by_xpath('//*[@id="panelbarAdvanced"]/li[2]/div[2]/div').click()
    time.sleep(1)


    driver.find_element_by_xpath('//*[@id="panelbarAdvanced"]/li[2]/div[2]/div/ul/li/input').send_keys(sourceList[currentSourceIndex])
    time.sleep(1)
    driver.find_element_by_xpath('//*[@id="panelbarAdvanced"]/li[2]/div[2]/div/ul/li/input').send_keys(Keys.RETURN)
    time.sleep(1)
    driver.find_element_by_xpath('//*[@id="SearchBarContainer"]/table/tbody/tr/td[2]/input').click()
    time.sleep(1)
    driver.find_element_by_xpath('//*[@id="SearchBarContainer"]/table/tbody/tr/td[2]/input').send_keys(Keys.RETURN)

    

    time.sleep(8)


    time.sleep(4)


def searchIterator(sourceList):
    currentSourceIndex = 1
    sourceListLength = len(sourceList)
    for x in range(1, sourceListLength):
        time.sleep(4)
        resultCount = driver.find_element_by_xpath('//*[@id="ToolbarContentTitle"]/span[1]').text
        print(resultCount)
        print(int(resultCount))
        resultCount = int(resultCount)
        if resultCount == 0:
            print'no results here boss'
        else:
            searchResultsMonster(sourceList, resultCount)
        changeSourceSearch(sourceList, currentSourceIndex)
        currentSourceIndex +=1















def articleMonster(sourceList, resultCount):
    articlediagnum= 0

    while articlediagnum < resultCount:
        print(sourceList[currentSourceIndex])
        print(articlediagnum)
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

        printinglist = []
        printinglist.append(articleBufferString)
        printinglist.append('*' + articleSource.get_attribute('value').encode('utf-8') + '*')
        printinglist.append('*' + articleDate.get_attribute('value').encode('utf-8') + '*')

        #
        # articleBufferString = (articleSource.get_attribute('value')).encode('utf-8') + '******' + articleBufferString
        #
        # articleBufferString = (articleDate.get_attribute('value')).encode('utf-8') + ' ' + articleBufferString
        # # print(articleBufferString)

        # Adds List item to CSV


        resultDoc.writerow(printinglist)
        WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, '// *[ @ id = "PageForward"]')))
        driver.execute_script("AdjustTranscriptLayout.NextButton();")
        articlediagnum+=1
    print('articlemonster quit.')






def searchResultsMonster(sourceList, resultCount):
    WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.CLASS_NAME, 'ListItemTitle')))
    this = driver.find_elements_by_xpath("//*[contains(@id, 'ListItem-')]")

    # experimenting with this line of problem code
    idString = str(this[0].get_attribute("id"))
    print(idString)
    scriptString = "ResultsList.NavigateToDataEndPoint($('#" + idString + "').children('.ListItem'))"
    print(scriptString)
    driver.execute_script(scriptString)
    articleMonster(sourceList,resultCount)

    # # # --------------WaitCODE------------------------------


    # for x in range(13):
    #     time.sleep(3)
    #     driver.execute_script("ResultsList.PageForward();")
        # driver.find_element_by_xpath('//*[@id="PageForward"]').click()







def searchDeterminer(userData):
    rusSourceList = ['Arguments','Chastny','EJ','gazeta','grani','inopressa','izvestia','kasparov','kommersant','komsom','moscow news', 'moskovski','newsru','Newtimes','novaya gazeta','Rossiya24','rossiyskaya','slon','sobkorr','specletter']
    if userData['lang'] == 'R':
        sourceListLength = len(rusSourceList)

        return rusSourceList








def sequence():
    currentSourceIndex = 0
    userData = getInfo()


    logOn(userData)
    sourceList = searchDeterminer(userData)


    userData['source']= sourceList[currentSourceIndex]
    initialSearch(userData, sourceList)

    currentSourceIndex += 1

    searchIterator(sourceList)

    print('will I see this? THE RETURN')

    # test out my source list

    # for x in range(len(sourceList)):
    #     userData['source'] = sourceList[x+1]
    #     changeSourceSearch(userData)
    #
    #     time.sleep(5)












sequence()

