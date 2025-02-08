import time
import os
from selenium import webdriver
from dotenv import load_dotenv
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

load_dotenv()
STEAM_USERNAME = os.getenv('STEAM_USERNAME')
STEAM_PASSWORD = os.getenv('STEAM_PASSWORD')
FRIEND_STEAM_PROFILE = os.getenv('FRIEND_STEAM_PROFILE')
FRIEND_STEAM_ID = os.getenv('FRIEND_STEAM_ID')
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
            EC.visibility_of_element_located((By.ID, f"commentthread_Profile_{FRIEND_STEAM_ID}_submit"))
        )

        post_button.click()

        print(f"Successfully posted the comment: {comment_text}")

    except Exception as e:
        print(f"Error posting comment: {str(e)}")


def delete_previous_comment(driver):
    try:
        print("SteamPester is searching for previous comments...")

        # wait for comments to load
        comments = WebDriverWait(driver, 15).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "commentthread_comment"))
        )
        # print number of comments to be found
        print(f"Found {len(comments)} comments.")

        for comment in comments:
            try:
                # get the author name
                author_element = WebDriverWait(comment, 5).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "commentthread_author_link"))
                )
                author_name = author_element.text.strip()

                # if i am the author of the comment...
                if author_name == STEAM_USERNAME:
                    print("SteamPester found your previous comment! Attempting to delete...")

                    # hover over the comment to reveal the delete button
                    ActionChains(driver).move_to_element(comment).perform()
                    time.sleep(2)  # wait for UI to update

                    # find the delete button
                    try:
                        delete_button = WebDriverWait(comment, 5).until(
                            EC.element_to_be_clickable(
                                (By.XPATH, ".//div[@class='commentthread_comment_actions']/a")
                            )
                        )
                    except Exception as e:
                        print(f"Error finding delete button: {e}")
                        continue

                    # click the delete button
                    delete_button.click()
                    print("SteamPester successfully deleted your previous comment!")

                    time.sleep(3)  # allow time for deletion to reflect

                    return  # exit after deleting the latest comment

            except Exception as e:
                print(f"Skipping a comment due to error: {e}")

        print("No previous comment found.")

    except Exception as e:
        print(f"Error deleting comment: {str(e)}")




def main(): 
    day_count = get_day_count() # get and increment the day count
    comment_text = f'day {day_count} of asking sirnyges to hop on val :steambored: — SteamPester <3' # format comment
   
    login(driver) # log in to Steam
    driver.get(FRIEND_STEAM_PROFILE) # navigate to friend's profile
    delete_previous_comment(driver) # delete previous comment
    time.sleep(2)
    post_comment(driver, comment_text) # post comment
    
    time.sleep(5)
    driver.quit()

if __name__ == "__main__":
    main()
