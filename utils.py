from selenium.common.exceptions import TimeoutException, JavascriptException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from time import sleep
import os


EXECUTABLE_PATH = "./gecko/chromedriver"
SCREENSHOT_STORAGE = "data"

def setDriver(executable_path = EXECUTABLE_PATH, headless = False, maximize = True):
    chrome_options = webdriver.ChromeOptions()
    prefs = {"profile.default_content_setting_values.notifications" : 2}
    chrome_options.add_experimental_option("prefs",prefs)
    if maximize:
        chrome_options.add_argument("--start-maximized")
    if headless:
        chrome_options.add_argument("--headless")
    return webdriver.Chrome(executable_path = executable_path, chrome_options=chrome_options)

def completeLink(link, site):
    if link.startswith("http"):
        return link
    if link.startswith("/"):
        link = link[1:]
    return site + link

def scroll(driver, numScrolls = 20000, fastScroll = False):
    scroll_time = 8
    if fastScroll:
        driver.execute_script("document.body.style.transform = 'scale(0.05)'")
    current_scrolls = 0
    old_height = 0
    sleep(0.4)
    while True:
        try:
            if current_scrolls == numScrolls:
                return
            try:
                old_height = driver.execute_script("return document.body.scrollHeight")
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                WebDriverWait(driver, scroll_time, 0.05).until(
                    lambda driver: check_height(driver, old_height)
                )
                current_scrolls += 1
            except JavascriptException:
                pass
        except TimeoutException:
            break
    driver.execute_script("document.body.style.transform = 'scale(1.00)'")
    return

def check_height(driver, old_height):
    new_height = driver.execute_script("return document.body.scrollHeight")
    return new_height != old_height

def createStorage(site):
    try:
        os.makedirs(f"{SCREENSHOT_STORAGE}/{site}")
    except FileExistsError:
        pass

def hover(driver, element):
    script = "var evObj = document.createEvent('MouseEvents');" + \
                    "evObj.initMouseEvent(\"mouseover\",true, false, window, 0, 0, 0, 0, 0, false, false, false, false, 0, null);" + \
                    "arguments[0].dispatchEvent(evObj);"
    driver.execute_script(script, element)
