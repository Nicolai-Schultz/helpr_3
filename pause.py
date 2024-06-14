from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
from selenium.webdriver.common.keys import Keys


# Specify the path to ChromeDriver
#chrome_driver_path = "C:/Users/nico/chromedriver-win64/chromedriver.exe"

# Configure the Chrome WebDriver with the specified service
s = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=s)

#Ting der virker 
"""
# Navigate to the website
driver.get("https://www.google.com/")

search_input = driver.find_element(By.XPATH, "/html/body/div[1]/div[3]/form/div[1]/div[1]/div[4]/center/input[2]")
search_input.click()"""

driver.get("https://www.google.com/")

driver.maximize_window()

element = driver.find_element(By.XPATH, "/html/body/div[2]/div[2]/div[3]/span/div/div/div/div[3]/div[1]/button[2]")
element.click()

element = driver.find_element(By.XPATH, "/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/textarea")
element.send_keys("Hello")
element.send_keys(Keys.RETURN)




try:
    # Keep the script running until the browser window is closed
    while True:
        if driver.window_handles:  # Check if there are any open browser windows
            time.sleep(1)  # Sleep for 1 second (adjust as needed)
        else:
            break  # Exit the loop if the window is closed
except KeyboardInterrupt:
    pass  # Handle keyboard interrupt (e.g., Ctrl+C) to gracefully exit


# Quit the browser when the loop exits
driver.quit()