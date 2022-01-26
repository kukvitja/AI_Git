from Include.work_json import remember_data, get_remember_data
import time
import os
import pyautogui
from pywinauto.application import Application
# import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary


# pach_file_train_dataset = "data/traindataset.json"

def init_driver():
    binary = FirefoxBinary(r'C:\Program Files\Mozilla Firefox\firefox.exe')
    driver = webdriver.Firefox(firefox_binary=binary)
    driver.wait = WebDriverWait(driver, 5)
    return driver

pach_file_remember = "data/memory.json"

def remember_data_write(pach_file_remember = pach_file_remember, **kwargs):
    print(kwargs)
    del kwargs['arr_text_input'][0]
    str = kwargs['arr_text_input'][0] + ' ' + kwargs['arr_text_input'][1] + ' ' + kwargs['arr_text_input'][2]
    remember_data(str, kwargs['arr_text_input'], pach_file_remember)



def get_remember(pach_file_remember = pach_file_remember, **kwargs):
    del kwargs['arr_text_input'][0]
    task = ' '.join(kwargs['arr_text_input'])
    return get_remember_data(task, pach_file_remember)


def start_main_work():
    os.system(r'D:\MasterD\MDUPDATE.exe a')
    os.startfile(r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe')
    os.startfile(r"C:\Users\Viktor\Documents\Work")
    os.startfile(r"C:\Users\Viktor\Documents\Doky")
    # open_scanner()
    pyautogui.hotkey('winleft', 'd')
    os.startfile(r'D:\MasterD\MD-Declaration\DeclPlus.exe')


def search(task):
    search_work = task.split()
    del search_work[0]
    str = ' '.join(search_work)
    # print(str)
    driver = init_driver()
    lookup(driver, str)


def lookup(driver, query):
    driver.get("http://www.google.com")
    try:
        box = driver.wait.until(EC.presence_of_element_located(
            (By.NAME, "q")))
        box.send_keys(query)
        box.send_keys(Keys.ENTER)

    except TimeoutException:
        print("Box  not found in google.com")


def talk_storis(driver):

    driver.get("https://zefirka.net/2016/03/01/korotkie-i-lyubopytnye-fakty-obo-vsem-na-svete/")

    try:
        articles = driver.find_elements_by_css_selector('.entry-content-inner>p')
        lends = len(articles)
        lends1 = randint(2, lends)
        article = articles[lends1].text
        print(articles[lends1].text)
        driver.quit()
    except TimeoutException:
        print("Articles  not found")
    return article


def open_scanner():
    app = Application(backend="win32").start("C:\Program Files\VueScan\vuescan.exe")
    time.sleep(1)
    # app['Cовет дня'].Закрыть.click()
    app.wxWindowNR.ComboBox6.select("Установка пользователем")
    # app.wxWindowNR.Edit0.type_keys(100, with_spaces = True)
    # app.wxWindowNR.Edit1.select("C:\Users\Viktor\Desktop")
    app.wxWindowNR.ComboBox8.select("JPEG")


def scanner():
    app = Application().connect(path=r"C:\Program Files\VueScan\vuescan.exe")
    app.wxWindowNR.Edit3.type_keys(time.time())
    app.wxWindowNR.Сканировать.click()
    time.sleep(20)
    app_save = Application().connect(title_re="Выберите имя файла JPEG", class_name="#32770")
    app_save1 = app_save.top_window()
    app_save1.Botton.click()