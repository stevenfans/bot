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

def webConnect(): 
    service = Service(executable_path="chromedriver.exe")
    driver = webdriver.Chrome(service=service)

    driver.get("https://www.target.com/p/olipop-spongebob-pineapple-paradise-soda-4pk-12-fl-oz-cans/-/A-94661680")

    input_element = driver.find_element(By.ID, 'addToCartButtonOrTextIdFor94661680')
    input_element.send_keys(Keys.ENTER)

    time.sleep(10)
    driver.quit()

def main():
    """
    This function serves as the main entry point of the script.
    """
    retrieve_messages(config.channelIds)
    webConnect()

if __name__ == "__main__":
    main() 
    
