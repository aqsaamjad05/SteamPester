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
COMMENT_TEXT = "testing 123"
DAY_COUNT_FILE = "day_count.txt"

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

def post_comment(driver):
    # Navigate to friend's profile
    driver.get(FRIEND_STEAM_PROFILE)

    # Wait for the comment section to be visible
    try:
        comment_section = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, "commentthread_comment_timestamp"))
        )

        # Wait for the comment input field to be visible (using CSS Selector)
        comment_input = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "//textarea[@class='commentthread_textarea']"))
        )

        comment_input.click()

        # Type the comment
        comment_input.send_keys(COMMENT_TEXT)

        # Find and click the post button
        post_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "commentthread_Profile_76561199816114795_submit"))
        )
        post_button.click()

        print(f"Successfully posted the comment: {COMMENT_TEXT}")

    except Exception as e:
        print(f"Error posting comment: {str(e)}")


def main(): 
    login(driver)
    driver.get(FRIEND_STEAM_PROFILE)
    post_comment(driver)
    time.sleep(10)

if __name__ == "__main__":
    main()
