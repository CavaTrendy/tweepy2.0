import time
from selenium import webdriver
count = 0
my_path = 'C:/Program Files (x86)/Google/Chrome/Application/chromedriver.exe'

while count < 100:
    new_url = "https://medium.com/gita-foundation/gita-opens-doors-to-crypto-exchanges-to-join-as-super-nodes-4b4a2ea0ad38"
    options = webdriver.ChromeOptions()
    options.add_argument("--incognito")
    driver = webdriver.Chrome(my_path, chrome_options=options)
    count += 1
    driver.get(new_url)
    driver.maximize_window()
    time.sleep(5)
    driver.execute_script("window.scrollTo(0,1080)")
    time.sleep(15)
    driver.execute_script("window.scrollTo(1080,2080)")
    time.sleep(15)
    driver.execute_script("window.scrollTo(2080,3080)")
    time.sleep(3)
    driver.execute_script("window.scrollTo(3080,1080)")
    time.sleep(15)
    driver.quit()
    time.sleep(600)




