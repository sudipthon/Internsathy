from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException

from multiprocessing import Manager
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor


def internsathi_join(acc):
    options = Options()
    # options.add_experimental_option("detach", True)  # this will live browser open
    options.add_argument('--headless')
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), options=options
    )
    try:

        driver.get(
            "https://internsathi.com?ref=r6i7vr8g"
        )  # https://internsathi.com?ref=r6i7vr8g

        driver.implicitly_wait(15)
        join_button = driver.find_element(
            By.XPATH, "/html/body/main/div/main/section[1]/div/div/div/button"
        )
        join_button.click()
        driver.implicitly_wait(5)

        first_name = driver.find_element(By.XPATH, '//*[@id="firstName"]')
        first_name.send_keys('a')

        last_name = driver.find_element(
            By.XPATH,
            "/html/body/div[2]/div/div/div/div[2]/div/div/div[2]/form/div[2]/div/input",
        )
        last_name.send_keys('b')

        email = driver.find_element(
            By.XPATH,
            "/html/body/div[2]/div/div/div/div[2]/div/div/div[2]/form/div[3]/div/input",
        )
        email.send_keys(acc)

        join_button = driver.find_element(
            By.XPATH, "/html/body/div[2]/div/div/div/div[2]/div/div/div[2]/form/button"
        )
        join_button.click()
        time.sleep(7)
    except Exception as e:
        print(e)
    driver.quit()
 


def internsathi_verify(acc):
    i = ""
    options = Options()
    # options.add_experimental_option(  "detach", True )  # this will live browser open
    options.add_argument("--headless")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), options=options
    )
    try:
        driver.get(
            "https://internsathi.com?ref=r6i7vr8g"
        )  # https://internsathi.com?ref=r6i7vr8g

        driver.implicitly_wait(15)
        join_button = driver.find_element(
            By.XPATH, "/html/body/main/div/main/section[1]/div/div/div/button"
        )
        join_button.click()
        driver.implicitly_wait(5)

        check_entry = driver.find_element(
            By.XPATH,
            "/html/body/div[2]/div/div/div/div[2]/div/div/div[2]/div[2]/button",
        )
        check_entry.click()

        try:
            time.sleep(2)
            email = WebDriverWait(driver, 15).until(
                EC.element_to_be_clickable((By.ID, "firstName"))
            )
            email.send_keys(acc)

        except Exception as e:
            time.sleep(3)
            email = WebDriverWait(driver, 15).until(
                EC.element_to_be_clickable((By.ID, "firstName"))
            )
            email.send_keys(acc)

            # time.sleep(5)

        get_pos = driver.find_element(
            By.XPATH, '//*[@id="headlessui-dialog-panel-:r3:"]/div[2]/form/button'
        )
        get_pos.click()

        try:
            driver.implicitly_wait(7)
            resend_link = driver.find_element(
                By.XPATH,
                "/html/body/div[2]/div/div/div/div[2]/div/div/div[2]/p/span[3]/button",
            )
            resend_link.click()
            time.sleep(2)

        except Exception as e:
            i = acc

    except Exception as e:
        print(e)
    driver.quit()

    if i != "":
        return i
    return None


if __name__ == "__main__":
    with open("unverified_email.txt", "r") as f:
        email_list = f.read().splitlines()
        # email_list = ['1abc1@gmail.com','abc12@gmail.com']

    print(len(email_list))
 
    start_time=time.time()
    with ProcessPoolExecutor(max_workers=6) as executor:
        verified_email = list(executor.map(internsathi_verify, email_list))
        # executor.map(internsathi_join, email_list)
        unverified_email = [i for i in email_list if i not in verified_email]
    end_time=time.time()
        # print(verified_email)
    print(end_time-start_time)

    with open("verified_email.txt", "a") as f:
        for i in verified_email:
            if i is not None:
                f.write(i + "\n")


    with open("unverified_email.txt", "w") as f:
        for i in unverified_email:
            f.write(i + "\n")
