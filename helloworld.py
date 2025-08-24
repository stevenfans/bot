import config
import discord
from discord.ext import commands
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By 
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
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

def is_item_in_cart(driver, product_id):
    """
    Checks if a specific item is in the Target cart.

    Args:
        driver: The Selenium WebDriver instance.
        product_id: The unique product ID of the item.

    Returns:
        True if the item is found in the cart, False otherwise.
    """
    cart_url = "https://www.target.com/cart"
    driver.get(cart_url)
    
    # Construct a robust CSS selector using the data-test attribute.
    # The product ID (DPCI) can often be found in the product URL.
    # For example, a product URL like /p/lego-.../A-87248887 has DPCI 87248887.
    # item_selector = f"div[data-test='cartItem-{product_id}']"
    item_selector = f'//*[@id="item-title-b3923ac0-7ff7-11f0-8d6d-cb679971da6e"]/div/div'

    item_name = 'OLIPOP Spongebob Pineapple Paradise Soda - 4pk/12 fl oz Cans'
    cart_items = driver.find_elements(By.XPATH,f"//*[contains(text(), '{item_name}')]")
    
    try:
        # Wait up to 10 seconds for the item to appear in the cart.
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, item_selector))
        )
        print(f"Item with product ID '{product_id}' is in the cart.")
        return True
    except TimeoutException:
        print(f"Item with product ID '{product_id}' was not found in the cart.")
        return False

def webConnect(): 
    options = chromeProfileInit() 
    service = Service(executable_path="chromedriver.exe")
    driver = webdriver.Chrome(service=service, options=options)

    product_id = 'olipop-spongebob-pineapple-paradise-soda-4pk-12-fl-oz-cans'
    driver.get("https://www.target.com/p/olipop-spongebob-pineapple-paradise-soda-4pk-12-fl-oz-cans/-/A-94661680")
    # driver.get("https://www.google.com)

    time.sleep(0.5)

    # click the 'Add to Cart' button
    is_item_in_cart(driver, product_id)
    add_to_cart_element = driver.find_element(By.ID, 'addToCartButtonOrTextIdFor94661680')
    add_to_cart_element.send_keys(Keys.ENTER)

    # is item added to cart
    is_item_in_cart_element = driver.find_element(By.CLASS_NAME, 'h-text-lg')
    print(f'item is in cart {is_item_in_cart_element}')

    # checkout 
    checkout_element = driver.find_element(By.CLASS_NAME, 'styles_ndsBaseButton__W8Gl7 styles_md__X_r95 styles_mdGap__9J0yq styles_fullWidth__3XX6f styles_ndsButtonSecondary__iSf2I')
    checkout_element.send_keys(Keys.ENTER)

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
    
