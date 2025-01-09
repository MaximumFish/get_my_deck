from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from random import randint
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime
import requests


browser_options = Options()
browser_options.add_argument("--headless=new")
url = "https://store.steampowered.com/sale/steamdeckrefurbished"

bot_token = "00000000:00000000000000000000" # Your Telegram bot token here
chat_id = 00000000 # Your chat ID to send alerts to
    

def start():
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=browser_options)

    
    driver.get(url)
    return driver


def refresh(driver):
    driver.refresh()


def quit(driver):
    driver.quit()


def runner(driver):
    #all_btn = driver.find_elements(By.XPATH, "//*[@id='SaleSection_33131']")
    try:
        all_btn = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, "//*[@id='SaleSection_33131']")))
        x = all_btn[0].text
        x = x.split("00")[0]  ## HERE YOU CAN BREAKPOINT AND DETERMINE WHICH PART OF THE TEXT YOU ARE INTERESTED IN (E.G. STRIP FOR 64GB, 256GB ETC
        print(x)
        if "add" in x.lower():
            message = "OMG Steamdeck available! https://store.steampowered.com/sale/steamdeckrefurbished/"
            notify_url = f"https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_id}&text={message}"
            requests.get(notify_url) # this sends the message
            status = 1
        else:
            print(x)
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            status = 0
    except Exception as e:
        print(f"Error: {e}")
        status = 0
    return status


def get_my_deck():
    c= 0
    driver = start()
    time.sleep(10) ## DO NOT EDIT
    print("Started Scraper")
    while True:
        try:
            if c<11:
                status = runner(driver)
                if status == 1:
                    break
                randDelay = randint(10,60) # Random delay from 10 to 60 seconds.
                print(f'Next check in {randDelay} seconds.')
                time.sleep(randDelay)
                c = c+1
                refresh(driver)
            else:
                print("Rebooting")
                quit(driver)
                time.sleep(20) ## DO NOT EDIT
                c = 0
                driver = start()
        except Exception as e:
            print(e)
            driver.quit()
            time.sleep(20) ## DO NOT EDIT
            get_my_deck()

try:
    get_my_deck()
except:
    message = "Get-my-deck crashed. :("
    notify_url = f"https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_id}&text={message}"
    requests.get(notify_url)