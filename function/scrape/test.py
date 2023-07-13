# python function/scrape/test.py
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep, time
from datetime import datetime, timedelta
import pandas as pd
from IPython.display import display

def main():
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)
    options.add_argument("start-maximized")
    PATH = "D:\beam\fourth-year-2\final project 1\data\scrape\driver\chromedriver.exe"

    driver = webdriver.Chrome(options=options, executable_path=PATH)

    html = []
    links = ['https://twitter.com/tanawatofficial/status/1656644953739788291', 'https://twitter.com/tanawatofficial/status/1656616243275890688', 'https://twitter.com/goldendoxl/status/1656620953995210752']
    for link in links:
        driver.get('https://publish.twitter.com/#')
        sleep(0.5)
        inputField = driver.find_element(By.XPATH, "//input[@id='configuration-query']")
        inputField.send_keys(link)
        sleep(0.2)
        
        submitButton = driver.find_element(By.XPATH, "//button[contains(@class, 'WidgetQuery-button')]")
        submitButton.click()
        sleep(0.5)
        
        code = driver.find_element(By.XPATH, "//samp").text
        html.append(code)
        sleep(0.5)
        print(code)


if __name__ == '__main__':
    main()