import time
import os
from selenium import webdriver
from dotenv import load_dotenv
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

load_dotenv()
STEAM_USERNAME = os.getenv('STEAM_USERNAME')
STEAM_PASSWORD = os.getenv('STEAM_PASSWORD')
FRIEND_STEAM_PROFILE = os.getenv('FRIEND_STEAM_PROFILE')

url_login = "https://steamcommunity.com/login/home/"
driver = webdriver.Chrome()

def login(driver):
    driver.get(url_login)

    # wait for username field to be present and visible
    username_field = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//input[@type='text']"))
    )
    username_field.click()  # Click first, then enter text
    username_field.send_keys(STEAM_USERNAME)

    # wait for password field and enter text
    password_field = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//input[@type='password']"))
    )
    password_field.click()
    password_field.send_keys(STEAM_PASSWORD)

    # click the login button
    login_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']"))
    )
    login_button.click()
    time.sleep(5)
    print("successfully logged in")

def main(): 
    login(driver)
    driver.get(FRIEND_STEAM_PROFILE)
    time.sleep(10)

if __name__ == "__main__":
    main()
