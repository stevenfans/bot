import config
import discord
from discord.ext import commands
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By 
from selenium.webdriver.common.keys import Keys
import requests
import json
import time

# --- CONFIG ---
HEADERS = config.headers

def retrieve_messages(channelID):
    r = requests.get(f'https://discord.com/api/v9/channels/{channelID}/messages?limit=50', headers=HEADERS)
    jsonn = json.loads(r.text) 
    i = 1 
    print(jsonn[-1])

def chromeProfileInit(): 
    profile_path = config.profile_path
    chrome_options = Options()
    # chrome_options.add_argument("--disable-blink-features=AutomationControlled") # disable automatic bot detection for selenium
    chrome_options.add_argument(f'user-data-dir={profile_path}')
    chrome_options.add_argument('--profile-directory=Default')
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("detach", True)
    return chrome_options

def webConnect(): 
    options = chromeProfileInit() 
    service = Service(executable_path="chromedriver.exe")
    driver = webdriver.Chrome(service=service, options=options)

    # # Remove navigator.webdriver
    # driver.execute_cdp_cmd(
    #     "Page.addScriptToEvaluateOnNewDocument",
    #     {
    #         "source": """
    #         Object.defineProperty(navigator, 'webdriver', {
    #         get: () => undefined
    #         })
    #         """
    #     }
    # )

    driver.get("https://www.target.com/p/olipop-spongebob-pineapple-paradise-soda-4pk-12-fl-oz-cans/-/A-94661680")
    # driver.get("https://www.google.com")

    time.sleep(0.5)

    # input_element = driver.find_element(By.ID, 'addToCartButtonOrTextIdFor94661680')
    input_element = driver.find_element(By.ID, 'addToCartButtonOrTextIdFor94661680')
    input_element.send_keys(Keys.ENTER)

    time.sleep(60)
    driver.quit()

def main():
    """
    This function serves as the main entry point of the script.
    """
    # retrieve_messages(config.channelIds)
    webConnect()

if __name__ == "__main__":
    main() 
    
