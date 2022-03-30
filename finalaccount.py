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
time.sleep(30)


address_list = []
address_type = []
timestamp = []
normal_address = []
nametag =[]
all_accountlebel_button = []
single_lebels_csv = []
menulist = []
contract_text = []
testing_list =[]
button_name = []


soup=BeautifulSoup(driver.page_source,'html.parser')
all_lebel_button=soup.find_all('button',{'class':'btn btn-sm btn-block btn-custom btn-custom-toggle dropdown-toggle'})

# removing two accounts cause that account throwing erorrs in runtime 
elements_to_remove = ["liqui.io", "remittance+"]
filtered_list = []
for element in all_lebel_button:
    if "liqui.io" not in element.get('data-url') and "remittance+" not in element.get('data-url') :
        filtered_list.append(element)

# looping all the labels names
for index in range (len(filtered_list)):
# for single_lebel in filtered_list:
    df=os.path.exists(str(filtered_list[index].get('data-url'))+".csv")
    if df == False:
        # setting headers for all csv's
        header = ['Address','address_link','nametag', 'exclamation_mark','Label_IDs_Array','address_type','timestamp','contract_text']
        with open('{}.csv'.format(str(filtered_list[index].get('data-url'))), 'w', encoding='UTF8') as f:
            writer = csv.writer(f)
        # write the header
            writer.writerow(header)
            f.close()
    else:
        pass

    # checking text file for labels name ....
    with open('accountlebels.txt') as file:
        content = file.read().splitlines()
        if all_lebel_button[index].get('data-url') not in content:
            # if labels name not present in text file , append new label name in text file 
            # setting url for labels name 
            link='https://etherscan.io/accounts/label/'+str(filtered_list[index].get('data-url')) +'?subcatid=undefined&size=100&start=0&col=1&order=asc'
            driver.get(link)
            time.sleep(6)
            soup = BeautifulSoup(driver.page_source,'html.parser')
            pageno = soup.find('li',{'class':'page-item disabled'})
            if pageno is not None:
                pagenos=pageno.find_all('strong')[1]
                print("The total number of pages is === >",pagenos.text)
                for a in range(0,int(pagenos.text)):
                    link='https://etherscan.io/accounts/label/'+str(filtered_list[index].get('data-url'))+'?subcatid=undefined&size=100&start={}&col=1&order=asc'.format(str(int(a*100)))
                    print(link)
                    driver.get(link)
                    time.sleep(3)
                    table=soup.find('tbody')
                    data=table.find_all('tr')     
                    time.sleep(8)
                    soup = BeautifulSoup(driver.page_source,'html.parser')
                    table=soup.find('tbody')
                    # to find address_type_button name like main lagecy and others
                    address_type_button = []
                    try:
                        findbutton = driver.find_element_by_xpath('//*[@id="content"]/div[3]/div[3]/div[1]/ul/li[1]/a')
                        rem = findbutton.text.rsplit(' ', 1)[0]
                    except:
                        rem =  "Main"
                    print("the Address type button name is :",rem)
                    odd_row=table.find_all('tr')
                    def main():
                        for odd in odd_row:
                            try:
                                Address = odd.find('td').text
                            except:
                                Address = "NA"
                            normal_address.append(Address)
                            
                            # link address 
                            try:
                                Address_link="https://etherscan.io/address/"+odd.find('td').text.replace(' ', '')
                            except:
                                Address_link ='NA'
                            address_list.append(Address_link)

                            
                            # name tag 
                            try:
                                name_tag=odd.find('td',{'class':'sorting_1'}).text
                                if name_tag == '':
                                    nametag.append("NA")
                                else:
                                    nametag.append(name_tag)
                            except:
                                pass
                        
                            # to find address type 
                            try:
                                Address_type = odd.find('i',{"data-original-title":"Contract"})
                                if Address_type is not None:
                                    address_type.append("Contract")
                                else:
                                    address_type.append("Wallet ")
                            except:
                                pass
                        

                            Address="https://etherscan.io/address/"+odd.find('td').text.replace(' ', '')
                            print("the address is :",Address)
                            driver.get(Address)
                            time.sleep(4)

                            soup = BeautifulSoup(driver.page_source,'html.parser')
                            body = soup.find('body')
                            # lLabel_IDs_Array 
                            findmenutxt= body.find_all('div',{'class':'mt-1'})[1].find_all('a')
                            for menu in findmenutxt:
                                try:
                                    menulist.append(menu.text)
                                except:
                                    pass    
                            translation= {39: None}
                            menuuu = (str(menulist).translate(translation))

                            # contract overview text 
                            find_contract_overview_text = body.find_all('div',{'class':'card h-100'})[0].find('span').text
                            contract_text.append(find_contract_overview_text)
                            driver.back()

                            # to add timestamp in csv
                            now = time.strftime('%d-%m-%Y %H:%M:%S')
                            timestamp.append(now)

                            # REMOVING DUPLICATES values 
                            if Address_link not in testing_list:
                                testing_list.append(Address_link)
                            
                                # labels dataframe
                                data_frame=pd.DataFrame([normal_address + address_list + [nametag] + address_type + [menuuu]+ [rem] + timestamp + contract_text])       
                                data_frame.to_csv('{}.csv'.format(str(filtered_list[index].get('data-url'))),index=False,mode='a',header=False, sep =',')
                                print(address_list)

                                # master dataframe
                                df=pd.DataFrame([normal_address + address_list + [nametag] + address_type + [menuuu]+ [rem] + timestamp + contract_text])
                                df.to_csv('AccountMaster.csv',header=False,index=False,mode='a')
                                
                                address_list.clear()
                                address_type.clear()
                                nametag.clear()
                                normal_address.clear()
                                contract_text.clear()
                                menulist.clear()
                                timestamp.clear()

                    # append new labels name in text file after completing 
                    with open('accountlebels.txt', 'a+') as f:
                        f.write("%s\n" % all_lebel_button[index].get('data-url'))

                    main()
            

                try:
                    time.sleep(5)
                    link='https://etherscan.io/accounts/label/'+str(filtered_list[index].get('data-url'))+'?subcatid=undefined&size=100&start={}&col=1&order=asc'.format(str(a))
                    # all_accountlebel_button.append(link)
                    driver.get(link)
                    time.sleep(20)
                    # this block of code for legacy or other account / for tbody 1 
                    try:
                        findbutton = driver.find_element_by_xpath('//*[@id="content"]/div[3]/div[3]/div[1]/ul/li[2]/a')
                        findbutton.click()
                    except:                         
                        findbutton = driver.find_element_by_xpath('//*[@id="content"]/div[3]/div[2]/div[1]/ul/li[2]/a')
                        findbutton.click()
                    rem = findbutton.text.rsplit(' ', 1)[0]
                    print("the Address type button name is :",rem)
                    time.sleep(20)

                    # to find number of pages 
                    soup=BeautifulSoup(driver.page_source,'html.parser')
                    findpageno = soup.find_all('li',{'class':'page-item disabled'})[2]
                    for i in findpageno:
                        p_num = i.find_all('strong')[-1].text
                    print("The total number of pages :",p_num)
                
                    for i in range (0,int(p_num)):
                        time.sleep(15)   
                        soup1 = BeautifulSoup(driver.page_source,'html.parser')
                    
                        table=soup1.find_all('tbody')[1]
                        odd_row=table.find_all('tr')

                        # calling function for other 
                        main()
                        if int(p_num) !=1:
                            try:
                                next_button=driver.find_element_by_xpath('/html/body/div[1]/main/div[3]/div[3]/div[2]/div[2]/div[2]/div/div/div[3]/div[2]/div/ul/li[4]/a')
                                if next_button is not None:
                                    driver.execute_script("arguments[0].click();", next_button)
                                    time.sleep(3)
                                else:
                                    pass
                            except:
                                next_button = driver.find_element_by_xpath('/html/body/div[1]/main/div[3]/div[2]/div[2]/div[2]/div[2]/div/div/div[3]/div[2]/div/ul/li[4]/a/i')
                                if next_button is not None:
                                    driver.execute_script("arguments[0].click();", next_button)
                                else:
                                    pass
                                time.sleep(3)
                except:
                    pass


                # code for tbody 2 ex- legacy tbody number 2
                try:
                    time.sleep(5)
                    link='https://etherscan.io/accounts/label/'+str(filtered_list[index].get('data-url'))+'?subcatid=undefined&size=100&start={}&col=1&order=asc'.format(str(a))
                    # all_accountlebel_button.append(link)
                    driver.get(link)
                    time.sleep(15)
                    try:
                        findbutton = driver.find_element_by_xpath('//*[@id="content"]/div[3]/div[3]/div[1]/ul/li[3]/a')                                             
                        findbutton.click()
                    except:
                        findbutton = driver.find_element_by_xpath('//*[@id="content"]/div[3]/div[2]/div[1]/ul/li[3]')
                        findbutton.click()
                    rem = findbutton.text.rsplit(' ', 1)[0]
                    print("the Address type button name is :",rem)
                    time.sleep(10)

                    soup=BeautifulSoup(driver.page_source,'html.parser')
                    findpageno = soup.find_all('li',{'class':'page-item disabled'})[4]
                    for i in findpageno:
                        p_num = i.find_all('strong')[-1].text
                    print("The total number of pages :",p_num)

                    for i in range (0,int(p_num)):
                        soup1 = BeautifulSoup(driver.page_source,'html.parser')
                        table=soup1.find_all('tbody')[2]
                        odd_row=table.find_all('tr')
                        # calling function for legacy 
                        main()
                        try:
                            next_button=driver.find_element_by_xpath('/html/body/div[1]/main/div[3]/div[3]/div[2]/div[2]/div[3]/div/div/div[3]/div[2]/div/ul/li[4]/a')
                            driver.execute_script("arguments[0].click();", next_button)
                            time.sleep(8)
                        except:
                            next_button = driver.find_element_by_xpath('/html/body/div[1]/main/div[3]/div[2]/div[2]/div[2]/div[3]/div/div/div[3]/div[2]/div/ul/li[4]/a')
                            driver.execute_script("arguments[0].click();", next_button)
                            time.sleep(8)
                except:
                    pass
        else:
            print("account label already present in csv")



# remove duplicates values 
df = pd.read_csv("AccountMaster.csv")

duplicate_rows = df.duplicated("Address").sum()
# check duplicates and remove
if duplicate_rows > 0:
    df = df.drop_duplicates(subset=["Address"])
    df.to_csv('AccountMasternew.csv',index=False)