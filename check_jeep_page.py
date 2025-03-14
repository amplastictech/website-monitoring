import datetime
from selenium import webdriver
import os

options = webdriver.FirefoxOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')

driver = webdriver.Firefox(options=options)

try:
    url = "https://www.kbdbodykits.com/jeep-wrangler-jk-flat-polyurethane-flat-fender-flares-kit"
    driver.get(url=url)

    expected_text = "Jeep Wrangler JK (2/4 Doors) & Unlimited 2007-2018 Front & Rear 4 Piece Polyurethane Fender Flares Kit"
    now = datetime.datetime.now()

    if expected_text not in driver.page_source:
        os.makedirs("404", exist_ok=True)
        filename = now.strftime("%Y-%m-%d_%H-%M-%S_jk.txt")
        filepath = os.path.join("404", filename)

        with open(filepath, "w") as file:
            file.write("JK flares page not loaded")

        print(f"Specified text NOT FOUND. Logged in {filename}")
    else:
        print("Specified text found! No log created.")

except Exception as e:
    print("An error occurred:", e)

finally:
    driver.quit()
