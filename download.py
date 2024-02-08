import time
import pyautogui
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By

# Set up Firefox with download preferences
options = Options()
options.set_preference("browser.download.folderList", 2)
options.set_preference("browser.download.manager.showWhenStarting", False)
options.set_preference("browser.download.dir", "./directory")  # Replace with your desired directory
options.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/pdf")  # Set MIME type for PDF

# Initialize the Firefox webdriver with the desired download directory
driver = webdriver.Firefox(options=options)

# Navigate to the URL
url = "https://www.idx.co.id/StaticData/NewsAndAnnouncement/ANNOUNCEMENTSTOCK/From_EREP/202402/7ad706086a_09c7e77df6.pdf"
driver.get(url)

download_button = driver.find_element(By.ID, 'download')
# Click the "Download" button
download_button.click()
time.sleep(2)  # Wait for the save dialog to appear (you might need to adjust the waiting time)
# pyautogui.write('filename.pdf')  # Type the desired filename
pyautogui.press('enter')  # Press Enter to confirm the save

# Wait for the download to complete (you might need to adjust the waiting time)
time.sleep(10)

# Close the browser
driver.quit()
