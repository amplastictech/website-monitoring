import datetime
from selenium import webdriver
import os
import smtplib
from email.mime.text import MIMEText
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def send_email(subject, body):
    try:
        sender = os.getenv('GMAIL_USER')
        password = os.getenv('GMAIL_PASSWORD')
        recipient = os.getenv('EMAIL_RECIPIENT')
        
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = sender
        msg['To'] = recipient

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender, password)
            server.send_message(msg)
        
        logger.info("Email sent successfully")
    except Exception as e:
        logger.error(f"Failed to send email: {e}")

def check_webpage():
    options = webdriver.FirefoxOptions()
    options.add_argument('--headless')

    driver = webdriver.Firefox(options=options)
    
    try:
        url = os.getenv('TARGET_URL', 'https://www.kbdbodykits.com/jeep-wrangler-jk-flat-polyurethane-flat-fender-flares-kit')
        expected_text = os.getenv('EXPECTED_TEXT', 'Jeep Wrangler JK (2/4 Doors) & Unlimited 2007-2018 Front & Rear 4 Piece Polyurethane Fender Flares Kit')
        
        driver.get(url)
        
        if expected_text not in driver.page_source:
            now = datetime.datetime.now()
            filename = now.strftime("%Y-%m-%d_%H-%M-%S_jk.txt")
            
            os.makedirs("404", exist_ok=True)
            file_path = os.path.join("404", filename)
            
            with open(file_path, "w") as file:
                file.write("JK flares page not loaded")
            
            subject = "Website Check Alert: Text Not Found"
            body = f"Specified text NOT found on {url}!\nLogged in {file_path}"
            logger.info(f"Specified text NOT found! Logged in {filename}")
        else:
            subject = "Website Check: Success"
            body = f"Specified text found on {url}, no issues detected."
            logger.info("Specified text found, no issues.")
        
        # Send email in both cases
        send_email(subject, body)
            
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        subject = "Website Check: Error Occurred"
        body = f"An error occurred while checking {url}: {str(e)}"
        send_email(subject, body)
        
    finally:
        driver.quit()

if __name__ == "__main__":
    check_webpage()
