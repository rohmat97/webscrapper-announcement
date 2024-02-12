import time
import pyautogui
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

from renameFile import copy_and_rename_xlsx

executable_path = './geckodriver'
# Set up Firefox with download preferences
options = webdriver.FirefoxOptions()
options.set_preference("browser.download.folderList", 2)
options.set_preference("browser.download.manager.showWhenStarting", False)
# options.set_preference("browser.download.dir", "./file")  # Replace with your desired directory
options.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/pdf")  # Set MIME type for PDF

# Open Firefox WebDriver with specified options
driver = webdriver.Firefox(options=options)
# Open the webpage
driver.get('https://www.idx.co.id/id/berita/pengumuman')
initial_window_handle = driver.current_window_handle
initial_url = driver.current_url
# Find the input element for "Kata kunci..."
keyword_input = driver.find_element(By.CSS_SELECTOR, '.filter-items input.form-input')
# Type a search term into the input field
keyword_input.send_keys("Laporan Bulanan Registrasi Pemegang Efek")
# Wait for a few seconds to observe the changes (optional)
time.sleep(2)
len_menu = driver.find_element(By.XPATH,"//li[@class='ph-8']").text.split(' ')[1]

for i in range(int(len_menu)):
    index = i+1
    if(index>1):
        driver.get('https://www.idx.co.id/id/berita/pengumuman')
        # next page
        next_button = driver.find_element(By.XPATH,"//select[@class='form-input']")
        next_button.click()
        pyautogui.typewrite(f'{index}')
        pyautogui.press('enter')
        time.sleep(1)
    
    div_elements = driver.find_elements(By.CSS_SELECTOR, 'div.attach-card')
    time.sleep(1)
    # Iterate through each div element and click on it
    list_menu = []
    for div_element in div_elements:
        list_menu.append({'name':div_element.text.split('\n')[1], 'code':div_element.text.split('\n')[1].split('[')[1].split(' ')[0]})

    print(list_menu)
    for menu in list_menu:
        span_element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, f"//span[text()='{menu['code']}                                                                                                ']"))
        )

        print(span_element.text)  # Print text for debugging
        span_element.click()

        time.sleep(1)
        new_window_handle = [handle for handle in driver.window_handles if handle != initial_window_handle][0]
        time.sleep(1)
        driver.switch_to.window(new_window_handle)
        tempUrl = driver.current_url.split('/')
        fileName = tempUrl[len(tempUrl)-1]
        # Find the "Download" button by its ID
        download_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, 'download'))
        )

        # Click the "Download" button
        download_button.click()
        # Wait for the download to complete (you might need to adjust the waiting time)
        time.sleep(1)

        # Use PyAutoGUI to handle the save dialog
        pyautogui.press('enter')
        time.sleep(1)
        pyautogui.press('enter')
        time.sleep(1)
        pyautogui.press('enter')
        time.sleep(1)
        source_file = f'/Users/rohmatdasuki/Downloads/{fileName}'
        destination_folder = './file'
        new_filename = f"{menu['name']}.pdf"
        copy_and_rename_xlsx(source_file, destination_folder, new_filename)
        time.sleep(1)
        # Wait for some time before proceeding to the next menu
        driver.switch_to.window(initial_window_handle)
        print(driver.current_url)
        time.sleep(1)
    handles = driver.window_handles
    for handle in handles[1:]:
        driver.switch_to.window(handle)
        driver.close()
    # Switch back to the original tab
    driver.switch_to.window(handles[0])
    time.sleep(1)
time.sleep(5)
driver.quit()
