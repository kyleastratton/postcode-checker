from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import smtplib
from email.mime.text import MIMEText
import os

EMAIL = os.environ['EMAIL']
POSTCODE = os.environ['POSTCODE']
RECIPIENT = os.environ['RECIPIENT']
APP_PASS = os.environ['APP_PASS']

def get_draw_results():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    from selenium.webdriver.chrome.service import Service

        service = Service('/usr/bin/chromedriver')
        driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get("https://pickmypostcode.com/login")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, 'email')))

        driver.find_element(By.NAME, 'email').send_keys(EMAIL)
        driver.find_element(By.NAME, 'postcode').send_keys(POSTCODE)
        driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
        time.sleep(5)

        results = []

        draw_urls = [
            "https://pickmypostcode.com/draw/main-draw/",
            "https://pickmypostcode.com/draw/stackpot/",
            "https://pickmypostcode.com/draw/video-draw/",
            "https://pickmypostcode.com/draw/bonus-draw/",
            "https://pickmypostcode.com/draw/survey-draw/"
        ]

        for url in draw_urls:
            driver.get(url)
            if "video-draw" in url:
                time.sleep(10)
            else:
                time.sleep(3)
            try:
                postcode = driver.find_element(By.CLASS_NAME, 'postcode').text
                results.append(f"✅ {url.split('/')[-2].replace('-', ' ').title()} Draw: {postcode}")
            except Exception:
                results.append(f"❌ {url.split('/')[-2].replace('-', ' ').title()} Draw: Not found or not visible")

        return "\n".join(results)

    finally:
        driver.quit()

def send_email(body):
    msg = MIMEText(body)
    msg['Subject'] = 'Pick My Postcode Results'
    msg['From'] = EMAIL
    msg['To'] = RECIPIENT

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(EMAIL, APP_PASS)
        server.send_message(msg)

if __name__ == '__main__':
    results = get_draw_results()
    send_email(results)
