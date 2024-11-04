# email_sender.py

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
import time, os

def send_email(destEmail, message):
    options = Options()
    options.add_argument('--headless')
    
    # Retrieve email credentials from environment variables
    userName = "jdmax15.auto.email@gmail.com"
    # Set password as an environment variable. Open cmd.exe > enter "setx MY_PASSWORD 'password'" on Windows or "export MY_PASSWORD='password'" on Linux."
    passWord = os.getenv("MY_PASSWORD")

    if not passWord:
        print("Password not found in environment variables")

    # Prepare email details
    currentTime = time.strftime("%Y-%m-%d %H:%M:%S")
    subject = f"{currentTime}: AUTOMATED EMAIL FROM JOEL"

    try:
        # Initialize the browser and open Gmail
        browser = webdriver.Firefox(options=options)
        browser.get('https://gmail.com')
        print('Opening browser in background...')

        # Login steps
        emailElem = browser.find_element(By.ID, 'identifierId')
        emailElem.send_keys(userName)
        print('Username entered...')
        
        nextButton = browser.find_element(By.CSS_SELECTOR, '.VfPpkd-LgbsSe-OWXEXe-k8QpJ > span:nth-child(4)')
        nextButton.click()
        
        passwordElem = WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.NAME, "Passwd")))
        passwordElem.send_keys(passWord)
        passwordElem.send_keys(Keys.ENTER)
        print('Password entered...')

        # Compose email
        composeButton = WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".T-I-KE")))
        composeButton.click()

        # Enter recipient
        recipientsBox = WebDriverWait(browser, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "input[aria-label='To recipients']"))
        )
        recipientsBox.send_keys(destEmail)

        # Enter subject
        subjectBox = WebDriverWait(browser, 10).until(
            EC.visibility_of_element_located((By.NAME, "subjectbox"))
        )
        subjectBox.send_keys(subject)

        # Enter message body
        messageBox = WebDriverWait(browser, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "div[aria-label='Message Body']"))
        )
        messageBox.send_keys(message)

        # Click "Send" button
        sendButton = browser.find_element(By.CSS_SELECTOR, "div[aria-label='Send ‪(Ctrl-Enter)‬']")
        sendButton.click()
        print(f"Message sent successfully to {destEmail}")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        time.sleep(3)  # Allow time for email to send before quitting
        browser.quit()
        print('Closing browser...')
