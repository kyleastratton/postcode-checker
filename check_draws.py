from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import smtplib
from email.mime.text import MIMEText

# Your Pick My Postcode login credentials
EMAIL = 'youremail@example.com'
POSTCODE = 'AB12CD'
RECIPIENT = 'youremail@example.com'

def get_draw_results():
    # Setup headless browser
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(options=options)

    try:
        # Go to the site and log in
        driver.get("https://pickmypostcode.com/login")
        time.sleep(2)

        driver.find_element(By.NAME, 'email').send_keys(EMAIL)
        driver.find_element(By.NAME, 'postcode').send_keys(POSTCODE)
        driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
        time.sleep(5)

        results = []

        # Loop through the draws
        draw_urls = [
            "https://pickmypostcode.com/draw/main-draw/",
            "https://pickmypostcode.com/draw/stackpot/",
            "https://pickmypostcode.com/draw/video-draw/",
            "https://pickmypostcode.com/draw/bonus-draw/",
            "https://pickmypostcode.com/draw/survey-draw/"
        ]

        for url in draw_urls:
            driver.get(url)
            time.sleep(10 if "video-draw" in url else 3)
            try:
                postcode = driver.find_element(By.CLASS_NAME, 'postcode').text
                results.append(f"{url.split('/')[-2].title()} Draw: {postcode}")
            except Exception:
                results.append(f"{url.split('/')[-2].title()} Draw: Not found or not visible")
        
        return "\n".join(results)

    finally:
        driver.quit()

def send_email(body):
    msg = MIMEText(body)
    msg['Subject'] = 'Pick My Postcode Results'
    msg['From'] = EMAIL
    msg['To'] = RECIPIENT

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(EMAIL, 'YOUR_APP_PASSWORD')  # Use an app password, not your real password
        server.send_message(msg)

# Main
if __name__ == '__main__':
    results = get_draw_results()
    send_email(results)
