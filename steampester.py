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
DAY_COUNT_FILE = "day_count.txt"

url_login = "https://steamcommunity.com/login/home/"
driver = webdriver.Chrome()

def get_day_count():
    # reads the current day count from the file, increments it, and updates the file
    if not os.path.exists(DAY_COUNT_FILE):
        day_count = 1  # start at day 1 if the file doesn't exist
    else:
        with open(DAY_COUNT_FILE, "r") as file:
            day_count = int(file.read().strip()) + 1  # increment count

    with open(DAY_COUNT_FILE, "w") as file:
        file.write(str(day_count))  # save new count

    return day_count

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
    time.sleep(10)
    print("successfully logged in")

def post_comment(driver, comment_text):
    # navigate to friend's profile
    driver.get(FRIEND_STEAM_PROFILE)

    # wait for the comment section to be visible
    try:
        comment_section = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, "commentthread_comment_timestamp"))
        )

        # wait for the comment input field to be visible and then click on it
        comment_input = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "//textarea[@class='commentthread_textarea']"))
        )
        comment_input.click()

        # type the comment
        comment_input.send_keys(comment_text)

        # find and click the post button
        post_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.ID, "commentthread_Profile_76561198341399194_submit"))
        )
        post_button.click()

        print(f"Successfully posted the comment: {comment_text}")

    except Exception as e:
        print(f"Error posting comment: {str(e)}")


def main(): 
    day_count = get_day_count() # get and increment the day count
    comment_text = f'day {day_count} of asking sirnyges to hop on val :steambored: — SteamPester <3' # format comment
   
    login(driver)
    post_comment(driver, comment_text)

    time.sleep(5)
    driver.quit()

if __name__ == "__main__":
    main()
