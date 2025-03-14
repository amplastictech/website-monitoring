import datetime
from selenium import webdriver
import os

options = webdriver.FirefoxOptions()
options.add_argument('--headless')

driver = webdriver.Firefox(options=options)

try:
    driver.get("https://www.kbdbodykits.com/jeep-wrangler-jk-flat-polyurethane-flat-fender-flares-kit")

    expected_text = "Jeep Wrangler JK (2/4 Doors) & Unlimited 2007-2018 Front & Rear 4 Piece Polyurethane Fender Flares Kit"

    if expected_text not in driver.page_source:
        now = datetime.datetime.now()
        filename = now.strftime("%Y-%m-%d_%H-%M-%S_jk.txt")

        os.makedirs("404", exist_ok=True)
        with open(os.path.join("404", filename), "w") as file:
            file.write("JK flares page not loaded")

        print(f"Specified text NOT found! Logged in {filename}")
    else:
        print("Specified text found, no issues.")

except Exception as e:
    print("An error occurred:", e)

finally:
    driver.quit()
