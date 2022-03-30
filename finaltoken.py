import selenium
import random
import os
from selenium.webdriver.common import keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.webdriver.chrome.options import Options
import time
import requests
from bs4 import BeautifulSoup
import os.path

# install recapcha libraries
from selenium.webdriver.common.keys import Keys
import speech_recognition as sr
import ffmpy
import urllib
import pydub

# for csv file 
import pandas as pd
import csv
import re
import random
import urllib
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import os
import sys
import time
import requests


audioToTextDelay = 10
delayTime = 2
audioFile = "\\payload.mp3"
URL = "https://etherscan.io/login"
SpeechToTextURL = "https://speech-to-text-demo.ng.bluemix.net/"
def delay():
    time.sleep(random.randint(2, 3))
def audioToText(audioFile):
    driver.execute_script('''window.open("","_blank")''')
    driver.switch_to.window(driver.window_handles[1])
    driver.get(SpeechToTextURL)
    delay()
    audioInput = driver.find_element(By.XPATH, '//*[@id="root"]/div/input')
    audioInput.send_keys(audioFile)
    time.sleep(audioToTextDelay)
    text = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[7]/div/div/div/span')
    while text is None:
        text = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[7]/div/div/div/span')
    result = text.text
    driver.close()
    driver.switch_to.window(driver.window_handles[0])
    return result

try:
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.maximize_window()
    delay()
    # go to website which have recaptcha protection
    driver.get(URL)
    username = driver.find_element_by_id("ContentPlaceHolder1_txtUserName").send_keys("tapendra")
    password = driver.find_element_by_id("ContentPlaceHolder1_txtPassword").send_keys("12345678")
    soup = BeautifulSoup(driver.page_source,'html.parser')
except Exception as e:
    sys.exit(
        "[-] Please update the chromedriver.exe in the webdriver folder according to your chrome version:https://chromedriver.chromium.org/downloads")

g_recaptcha = driver.find_elements_by_class_name('g-recaptcha')[0]
outerIframe = g_recaptcha.find_element_by_tag_name('iframe')
outerIframe.click()
iframes = driver.find_elements_by_tag_name('iframe')
audioBtnFound = False
audioBtnIndex = -1
for index in range(len(iframes)):
    driver.switch_to.default_content()
    iframe = driver.find_elements_by_tag_name('iframe')[index]
    driver.switch_to.frame(iframe)
    driver.implicitly_wait(delayTime)
    try:
        audioBtn = driver.find_element_by_id("recaptcha-audio-button")
        audioBtn.click()
        audioBtnFound = True
        audioBtnIndex = index
        break
    except Exception as e:
        pass
if audioBtnFound:
    try:
        while True:
            # get the mp3 audio file
            src = driver.find_element_by_id("audio-source").get_attribute("src")
            print("[INFO] Audio src: %s" % src)

            # download the mp3 audio file from the source
            urllib.request.urlretrieve(src, os.getcwd() + audioFile)

            # Speech To Text Conversion
            key = audioToText(os.getcwd() + audioFile)
            print("[INFO] Recaptcha Key: %s" % key)

            driver.switch_to.default_content()
            iframe = driver.find_elements_by_tag_name('iframe')[audioBtnIndex]
            driver.switch_to.frame(iframe)

            # key in results and submit
            inputField = driver.find_element_by_id("audio-response")
            inputField.send_keys(key)
            delay()
            inputField.send_keys(Keys.ENTER)
            delay()
            driver.switch_to.default_content()
            time.sleep(2)

            button = driver.find_element_by_xpath("/html/body/div[1]/main/div/form/div[8]/div[2]/input")
            driver.execute_script("arguments[0].click();", button)
            print("Login Button =>", button)

            err = driver.find_elements_by_class_name('rc-audiochallenge-error-message')[0]
            if err.text == "" or err.value_of_css_property('display') == 'none':
                print("[INFO] Success!")
                break
    except Exception as e:
        print(e)
        print("[INFO] Possibly blocked by google. Change IP,Use Proxy method for requests")
    time.sleep(5)      
else:
    print("[INFO] Audio Play Button not found! In Very rare cases!")

# to get list of labels
driver.get('https://etherscan.io/labelcloud')
time.sleep(20)

contract_text = []
public_name_tag_link = []
lebel_list = []
listt = []
address= []
sociallinks = []
overview = []
imglinks = []
address_type_button = []
p2p = []
fortimestamp = []
menulist = []
menulist1 = []
menu_id_list = []
token_overview_text = []

soup=BeautifulSoup(driver.page_source,'html.parser')
all_lebel_button=soup.find_all('button',{'class':'btn btn-sm btn-block btn-custom btn-custom-toggle dropdown-toggle'})
testing_list=[]
# for single_lebel in all_lebel_button:
for index in range(len(all_lebel_button)):
    df=os.path.exists(str(all_lebel_button[index].get('data-url'))+".csv")
    if df == False:
        header = ['Address','Address_link','Token_name,','Token_Abbrevation', 'Market_Cap','Holder','website','Image_url','Exclamation_mark','Label_IDs_Array','social_links' ,'Overview','Token_Address_type','timestamp','Public_Name_tag','token_overview_text']
        with open('{}.csv'.format(str(all_lebel_button[index].get('data-url'))), 'w', encoding='UTF8') as f:
            writer = csv.writer(f)
        # write the header
            writer.writerow(header)
            f.close()
    else:
        pass

    with open('lebels.txt') as file:
        content = file.read().splitlines()
        if all_lebel_button[index].get('data-url') not in content:
            link='https://etherscan.io/tokens/label/'+str(all_lebel_button[index].get('data-url'))+'?subcatid=undefined&size=100&start=0&col=3&order=desc'
            driver.get(link)
            time.sleep(6)
            soup = BeautifulSoup(driver.page_source,'html.parser')
            pageno = soup.find('li',{'class':'page-item disabled'})
            if pageno is not None:
                pagenos=pageno.find_all('strong')[1]
                print("The page number is :",pagenos.text)
                for a in range(0,int(pagenos.text)):      
                    link='https://etherscan.io/tokens/label/'+str(all_lebel_button[index].get('data-url'))+'?subcatid=undefined&size=100&start={}&col=3&order=desc'.format(str(int(a*100)))
                    print(link)
                    driver.get(link)
                    time.sleep(3)
                    soup = BeautifulSoup(driver.page_source,'html.parser')
                    table=soup.find('tbody')
                    try:
                        findbutton = driver.find_element_by_xpath('/html/body/div[1]/main/div[2]/div[3]/div[1]/ul/li[1]/a')
                        rem = findbutton.text.rsplit(' ', 1)[0]
                    except:
                        rem="main"
                    print("the Address type button name is :",rem)
                    data=table.find_all('tr')
                    def main():
                        for t in data:
                            #to get  contract addresses
                            address_ = t.find_all('td')[1].text
                            print("the length of address is " ,len(address_),address_)
                            listt.append(address_)

                            Address_link="https://etherscan.io/address/"+t.find_all('td')[1].text
                            listt.append(Address_link)

                            # # # to get token
                            token = t.find('div',{'class':'media-body'})
                            if  token is not None :
                                listt.append(token.text.rsplit(' ', 1)[0])
                            else:
                                pass
                                # listt.append("Na")
                            # token abbreviation 
                            try:
                                abbreviation = t.find('div',{'class':'media-body'}).text.split()[-1]
                                abb = abbreviation[1:-1]
                                listt.append(abb)
                            except:
                                pass

                            # # to get market cap
                            market_cap = t.find('td',{'class':'sorting_1'}).text
                            listt.append(market_cap)

                            # # to get holders
                            holder = t.find_all('td')[-2].text
                            listt.append(holder)

                            # to get token image src or href
                            tokensrc = "https://etherscan.io"+t.find('img').get('src')
                            imglinks.append(tokensrc)

                            #  to find address type
                            Address_type = t.find('i',{"class":"fa fa-info-circle text-secondary mr-1"})
                            try:
                                p2p.append(Address_type.get('data-original-title'))
                            except:
                                pass


                            # # to click all the toekn links one by one 
                            linkss = []
                            tlink = "https://etherscan.io"+t.find_all('td')[2].find('a').get('href').replace(' ', '')
                            linkss.append(tlink)
                            # website = []
                            for li in linkss:
                                driver.get(li)
                                time.sleep(2)
                                soup = BeautifulSoup(driver.page_source,'html.parser')
                                body = soup.find('body')

                                # to find the website links 
                                link = body.find('div',{'id':'ContentPlaceHolder1_tr_officialsite_1'})
                                try:
                                    ff = link.find('a').get('href')
                                    listt.append(ff)
                                except:
                                    pass
                            
                            # to get all the social links of website 
                            
                                social_links = body.find_all('ul',{'class':'list-inline mb-0'})[0]
                                aa = social_links.find_all('li')
                                social_link_dict={}
                                for i in aa:
                                    # sociallinks.append
                                    b=i.find('a').get('data-original-title').split(':')[0]
                                    c=i.find('a').get('href').replace("mailto:","")
                                    social_link_dict[b]=c
                            driver.back()
                            

                            infoo = []
                            k = "https://etherscan.io"+t.find_all('td')[1].find('a').get('href').replace(' ', '')
                            infoo.append(k)
                            # time.sleep(2)
                            for i in infoo:
                                driver.get(i)
                                time.sleep(2)
                                soup = BeautifulSoup(driver.page_source,'html.parser')
                                body = soup.find('body')
                                try:
                                    dd = driver.find_element_by_id("ContentPlaceHolder1_li_notes")
                                    if dd:
                                        dd.click()
                                        time.sleep(10)
                                        vieww = body.find('div',{'class':'table-responsive mb-2'}).text
                                        newString = vieww.replace('OVERVIEW', '')
                                        aaa = newString.strip()
                                        overview.append((re.sub('\s+',' ', aaa)))
                                        print(overview)
                                    else:
                                        overview.append("na")
                                except:
                                    overview.append("NA")
                                    pass
                            

                            # for label id's array
                            try:
                                soup = BeautifulSoup(driver.page_source,'html.parser')
                                body = soup.find('body')

                                findmenutxt= body.find_all('div',{'class':'mt-1'})[1].find_all('a')
                            except:
                                pass

                            for menu in findmenutxt:
                                try:
                                    menulist.append(menu.text)
                                except:
                                    pass 
                            translation= {39: None}
                            menuuu = (str(menulist).translate(translation))
                            

                            # public name tag
                            try:
                                find_contract_overview_text = driver.find_element_by_xpath('/html/body/div[1]/main/div[4]/div[1]/div[1]/div/div[1]/div/span').text
                                contract_text.append(find_contract_overview_text)
                            except:
                                contract_text.append("NA")

                            driver.back()

                            # labels id's for token
                            token_label_id = "https://etherscan.io"+t.find_all('td')[2].find('a').get('href').replace(' ', '')
                            # time.sleep(3)
                            driver.get(token_label_id)
                            time.sleep(10)
                            soup = BeautifulSoup(driver.page_source,'html.parser')
                            body = soup.find('body')

                            findmenutxt= body.find_all('div',{'class':'mt-1'})[1].find_all('a')
                            for menu in findmenutxt:
                                try:
                                    if menu.text not in menulist:
                                        menulist.append(menu.text)
                                except:
                                    pass 
                            translation= {39: None}
                            menu1 = (str(menulist).translate(translation))

                            # overview text of token name 
                            try:
                                find_token_overview_text = driver.find_element_by_xpath('/html/body/div[1]/main/div[4]/div[1]/div[1]/div/div[1]/h2/span').text
                                token_overview_text.append(find_token_overview_text)
                            except:
                                pass
                            
                            driver.back()

                            # to add timestamp in csv
                            now = time.strftime('%d-%m-%Y %H:%M:%S') 
                            fortimestamp.append(now)

                            # condition for duplicate values of seprate labels csv
                            if Address_link not in testing_list:
                                testing_list.append(Address_link)

                                data_frame=pd.DataFrame([listt])
                                data_frame['img link'] = [imglinks]
                                data_frame['P2P exchange'] = [p2p]
                                data_frame['menus'] = [menu1]
                                data_frame['social link'] = [social_link_dict]
                                data_frame['overview'] = [overview]
                                data_frame['address type button'] = rem
                                data_frame['timestamp'] = fortimestamp
                                data_frame['Contract text'] = contract_text
                                # data_frame['public_name_tag_link'] = public_name_tag_link
                                data_frame['token_overview_text'] = token_overview_text
                                data_frame.to_csv('{}.csv'.format(str(all_lebel_button[index].get('data-url'))),index=False,mode='a',header=False, sep =',')
                                
                                df=pd.DataFrame([listt + [imglinks] + [p2p] + [menu1]+ [social_link_dict]+[overview]+[rem] +fortimestamp  + contract_text + public_name_tag_link + token_overview_text])
                                df.to_csv('TokenMaster.csv',header=False,index=False,mode='a')
                                overview.clear()
                                p2p.clear()
                                imglinks.clear()
                                print(social_link_dict)
                                social_link_dict.clear()
                                menulist.clear()
                                address.clear()
                                token_overview_text.clear()
                                fortimestamp.clear()
                                contract_text.clear()
                                menu_id_list.clear()
                                public_name_tag_link.clear()
                                print(listt)
                                listt.clear()
                                print("label done ")

                                lebel_list.clear()
                            else:
                                overview.clear()
                                p2p.clear()
                                imglinks.clear()
                                print(social_link_dict)
                                social_link_dict.clear()
                                menulist.clear()
                                address.clear()
                                token_overview_text.clear()
                                fortimestamp.clear()
                                contract_text.clear()
                                menu_id_list.clear()
                                public_name_tag_link.clear()
                                print(listt)
                                listt.clear()
                                lebel_list.clear()
                        with open('lebels.txt', 'a+') as f:
                            f.write("%s\n" % all_lebel_button[index].get('data-url'))
                    main()

                # for other and legacy accounts     
                try:
                    link='https://etherscan.io/tokens/label/'+str(all_lebel_button[index].get('data-url'))+'?subcatid=undefined&size=100&start=0&col=3&order=desc'
                    driver.get(link)
                    time.sleep(10)
                    try:
                        findbutton = driver.find_element_by_xpath('//*[@id="content"]/div[2]/div[3]/div[1]/ul/li[2]')
                        findbutton.click()
                        rem = findbutton.text.rsplit(' ', 1)[0]
                        print("the Address type button name is :",rem)
                        time.sleep(20)
                    except:
                        findbutton = driver.find_element_by_xpath('//*[@id="content"]/div[2]/div[2]/div[1]/ul/li[2]/a')
                        findbutton.click()
                        rem = findbutton.text.rsplit(' ', 1)[0]
                        print("the Address type button name is :",rem)
                        time.sleep(20)

                    soup=BeautifulSoup(driver.page_source,'html.parser')
                    findpageno = soup.find_all('li',{'class':'page-item disabled'})[2]
                    for i in findpageno:
                        p_num = i.find_all('strong')[-1].text
                    print("The total number of pages :",p_num)

                    for i in range (0,int(p_num)):
                        time.sleep(15)   
                        soup1 = BeautifulSoup(driver.page_source,'html.parser')
                        table=soup1.find_all('tbody')[1]
                        data=table.find_all('tr')
                        # calling main function here for other account 
                        main()
                        try:
                            next_button=driver.find_element_by_xpath('/html/body/div[1]/main/div[3]/div[3]/div[2]/div[2]/div[2]/div/div/div[3]/div[2]/div/ul/li[4]')
                            driver.execute_script("arguments[0].click();", next_button)           
                            time.sleep(7)
                        except:
                            next_button = driver.find_element_by_xpath('/html/body/div[1]/main/div[2]/div[3]/div[2]/div/div/div[3]/div[2]/div/div/div[3]/div[2]/div/ul/li[4]')
                            driver.execute_script("arguments[0].click();", next_button)           
                            time.sleep(7)
                except:
                    pass

                # code for legacy account / tbody 2
                try:
                    time.sleep(3)
                    link='https://etherscan.io/tokens/label/'+str(all_lebel_button[index].get('data-url'))+'?subcatid=undefined&size=100&start=0&col=3&order=desc'
                    driver.get(link)
                    time.sleep(2)
                    findbutton = driver.find_element_by_xpath('//*[@id="content"]/div[2]/div[3]/div[1]/ul/li[3]/a')
                    findbutton.click()
                    rem = findbutton.text.rsplit(' ', 1)[0]
                    # address_type_button.append(rem)
                    print("the Address type button name is :",rem)

                    time.sleep(15)
                    findpageno = driver.find_element_by_xpath('/html/body/div[1]/main/div[2]/div[3]/div[2]/div/div/div[3]/div[3]/div/div/div[3]/div[2]/div/ul/li[3]/span/strong[2]').text
                    print("The total number of pages  :",findpageno)

                    if int(findpageno) is  None:
                        findpageno=1
                    else:
                        findpageno=findpageno    

                    for i in range (0,int(findpageno)):
                        time.sleep(15)  
                        soup1 = BeautifulSoup(driver.page_source,'html.parser')

                        table=soup1.find_all('tbody')[2]
                        data=table.find_all('tr')
                        # calling main function for legacy 
                        main()
                        next_button=driver.find_element_by_xpath('/html/body/div[1]/main/div[2]/div[3]/div[2]/div/div/div[3]/div[3]/div/div/div[3]/div[2]/div/ul/li[4]/a')
                        driver.execute_script("arguments[0].click();", next_button)
                        time.sleep(7)
                except:
                    pass
        else:
            print("account label already present in text file")

# making data frame from csv file
df = pd.read_csv("TokenMaster.csv")
duplicate_rows = df.duplicated("Address").sum()

# check duplicates and remove
if duplicate_rows > 0:
    df = df.drop_duplicates(subset=["Address"])
    df.to_csv('TokenMasternew.csv',index=False)