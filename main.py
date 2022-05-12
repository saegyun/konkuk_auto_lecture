#본인 크롬버전에 맞는 chromedriver를 설치해 main.py파일과 같은 경로에 넣어주세요.

uid = "" #건국대 이캠퍼스 id
pwd = "" #건국대 이캠퍼스 pwd
doNotWatch = ["미래를 그려보기","10.1 수열"] #Todo list에서 앞의 "[온라인강의] "를 제외하고 적어주세요. 

#위쪽 설정을 마치고 실행시켜주세요.

import selenium
from selenium import webdriver
from selenium.webdriver import ActionChains

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.alert import Alert


import time


URL = 'http://ecampus.konkuk.ac.kr/ilos/main/main_form.acl'

driver = webdriver.Chrome(executable_path='chromedriver')

driver.get(url=URL)

test = driver.find_element(By.CLASS_NAME,'login-btn-color')
test.click()

driver.find_element(By.ID,"usr_id").send_keys(uid)
driver.find_element(By.ID,"usr_pwd").send_keys(pwd)
driver.find_element(By.ID,"login_btn").click()

driver.find_elements(By.CLASS_NAME,"message_item")[1].click()
element = driver.find_elements(By.CLASS_NAME,"todo_category")[0]
driver.execute_script("arguments[0].click();", element)
lists = driver.find_elements(By.CLASS_NAME,"todo_wrap.on")

lists_s = len(lists) - 1

def watch(el1, el2):
    ppppp = el2.find_element(By.XPATH,"..").find_element(By.XPATH,"..").find_element(By.XPATH,"..").find_element(By.XPATH,"..").find_element(By.XPATH,"..").find_element(By.XPATH,"..").find_elements(By.XPATH,".//*")[0]
    try:
        subtitle = ppppp.text.split("차시 ")[1]
    except Exception:
        subtitle = title
    
    if el1.text != "100%" and subtitle not in doNotWatch:
        driver.implicitly_wait(10)
        parent = el1.find_element(By.XPATH,"..")
        child = parent.find_elements(By.XPATH,".//*")[4]
        t1 = child.text.split(" / ")[2]
        t2 = child.text.split(" / ")[0]

        sec1 = 0
        sec2 = 0

        s = child.text.split(" / ")[0]
        if(s.find("시")!=-1):
            s = s.split("시")
            sec1 += 3600 * int(s[0])
            s = s[1]
        if(s.find("분")!=-1):
            s = s.split("분")
            sec1 += 60 * int(s[0])
            s = s[1]
        if(s.find("초")!=-1):
            s = s.split("초")
            sec1 += 1 * int(s[0])

        s = child.text.split(" / ")[2]
        if(s.find("시")!=-1):
            s = s.split("시")
            sec2 += 3600 * int(s[0])
            s = s[1]
        if(s.find("분")!=-1):
            s = s.split("분")
            sec2 += 60 * int(s[0])
            s = s[1]
        if(s.find("초")!=-1):
            s = s.split("초")
            sec2 += 1 * int(s[0])        

        sec = sec2 - sec1
        el2.click()
        time.sleep(15)
        print("Time out")
        print(time.ctime(time.time()),",현재 강의:",subtitle,", 강의 시간:",t1,"(",sec2,")"," 현재 수강 시간:",t2,"(",sec1,")")
        #수정
        time.sleep(sec+15)
        
        try:
            driver.find_element(By.ID,"close_").click()
            time.sleep(2)
            alert = Alert(driver)
            alert.accept()
            print("alert accepted")
        except:
            print("no alert")
        print("End")
        
title = ""
num = 0
for i in range(lists_s+1) :
    list_ss = lists[num].find_element(By.CLASS_NAME,"todo_title")
    title = str(list_ss.get_attribute('textContent').split("\n        ")[1].split("\n")[0].split("[온라인강의] ")[1])
    print(title)
    if(title in doNotWatch):
        num += 1
        continue
    else:
        print(title)
        driver.execute_script("arguments[0].click();", lists[num])
        driver.implicitly_wait(10)
        views = driver.find_elements(By.CLASS_NAME,"site-mouseover-color")
        pers = driver.find_elements(By.ID,"per_text")
        if(len(pers) == 0):
            views = driver.find_element(By.CLASS_NAME,"site-mouseover-color")
            pers = driver.find_element(By.ID,"per_text")
            watch(pers, views)
            print("success")
        else:
            for k in range(len(pers)) :
                watch(pers[k],views[k])
                driver.implicitly_wait(10)
                views = driver.find_elements(By.CLASS_NAME,"site-mouseover-color")
                pers = driver.find_elements(By.ID,"per_text")
                ibox2 = driver.find_elements(By.CLASS_NAME,"ibox2")
        time.sleep(5)
    driver.find_elements(By.CLASS_NAME,"message_item")[1].click()
    element = driver.find_elements(By.CLASS_NAME,"todo_category")[0]
    driver.execute_script("arguments[0].click();", element)
    lists = driver.find_elements(By.CLASS_NAME,"todo_wrap.on")
    num = 0
driver.quit()
