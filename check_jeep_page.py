import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
import os

options = webdriver.FirefoxOptions()
options.add_argument('--headless')  # Required for GitHub Actions
options.add_argument('--no-sandbox')

driver = webdriver.Firefox(options=options)

try:
    driver.get("https://www.kbdbodykits.com/jeep-wrangler-jk-flat-polyurethane-flat-fender-flares-kit")

    if "Jeep Wrangler JK (2/4 Doors) & Unlimited 2007-2018 Front & Rear 4 Piece Polyurethane Fender Flares Kit" not in driver.page_source:
        now = datetime.datetime.now()
        filename = now.strftime("%Y-%m-%d_%H-%M-%S_jk.txt")

        if not os.path.exists("404"):
            os.makedirs("404")
        with open(os.path.join("404", filename), "w") as file:
            file.write("jk flares page not loaded")

        print(f"Specified text was not found and logged in {filename}")
    else:
        print("Specified text found!")

except Exception as e:
    print("An error occurred:", e)

finally:
    driver.quit()
