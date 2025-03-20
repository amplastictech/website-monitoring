import datetime
from selenium import webdriver
import os
import smtplib
from email.mime.text import MIMEText
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def send_email(subject, body):
    try:
        sender = os.environ.get('GMAIL_USER')
        password = os.environ.get('GMAIL_PASSWORD')
        recipient = os.environ.get('EMAIL_RECIPIENT')
        
        if not all([sender, password, recipient]):
            raise ValueError("Missing email configuration in environment variables")
            
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
    log_dir = "404"
    file_created = False
    
    try:
        url = os.environ.get('TARGET_URL', 'https://www.kbdbodykits.com/jeep-wrangler-jk-flat-polyurethane-flat-fender-flares-kit')
        expected_text = os.environ.get('EXPECTED_TEXT', 'Jeep Wrangler JK (2/4 Doors) & Unlimited 2007-2018 Front & Rear 4 Piece Polyurethane Fender Flares Kit')
        
        driver.get(url)
        
        if expected_text not in driver.page_source:
            now = datetime.datetime.now()
            filename = now.strftime("%Y-%m-%d_%H-%M-%S_jk.txt")
            
            os.makedirs(log_dir, exist_ok=True)
            file_path = os.path.join(log_dir, filename)
            
            with open(file_path, "w") as file:
                file.write("JK flares page not loaded")
            
            subject = "Website Check Alert: Text Not Found"
            body = f"Specified text NOT found on {url}!\nLogged in {file_path}"
            logger.info(f"Specified text NOT found! Logged in {filename}")
            file_created = True
        else:
            subject = "Website Check: Success"
            body = f"Specified text found on {url}, no issues detected."
            logger.info("Specified text found, no issues.")
        
        send_email(subject, body)
            
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        subject = "Website Check: Error Occurred"
        body = f"An error occurred while checking {url}: {str(e)}"
        send_email(subject, body)
        
    finally:
        driver.quit()
        return file_created, log_dir

if __name__ == "__main__":
    file_created, log_dir = check_webpage()
    # If running locally, you might want to print something
    if file_created:
        print(f"Log file created in {log_dir}")
