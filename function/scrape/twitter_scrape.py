#python function/scrape/twitter_scrape.py
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import Select
from time import sleep, time
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from tqdm import tqdm
import re
from IPython.display import display


def get_hashtag_from_txt(file_name):
  hashtags = []
  with open(file_name, "r") as f:
    count = 3
    for line in f:
      if count%4 == 0:
        line = line.replace('\n', '')
        hashtags.append(line)
      count += 1
  return hashtags

def get_tomorrow_and_yesterday(day):
  tomorrow = datetime.strftime(datetime.strptime(day, '%Y-%m-%d').date() + timedelta(1), '%Y-%m-%d')
  yesterday = datetime.strftime(datetime.strptime(day, '%Y-%m-%d').date() - timedelta(1), '%Y-%m-%d')
  return tomorrow, yesterday

def get_queries(hashtag, later_day, earlier_day, min_likes):
  queries = []
  query_with_like_bracket = '(' + hashtag + ') min_faves:{} until:' + later_day + ' since:' + earlier_day
  query_with_like_quote = '"' + hashtag + '" min_faves:{} until:' + later_day + ' since:' + earlier_day
  if hashtag[0] == '#':
    queries.append(query_with_like_bracket.format(min_likes))
    queries.append('(' + hashtag + ') lang:th until:' + later_day + ' since:' + earlier_day)
  else:
    queries.append(query_with_like_quote.format(min_likes))
    queries.append('"' + hashtag + '" lang:th until:' + later_day + ' since:' + earlier_day)
  return queries

def get_driver():
  WINDOW_SIZE = "1920,1080" # for starting with no window
  options = webdriver.ChromeOptions()
  options.add_experimental_option("detach", True)
  # options.add_argument("start-maximized")
  options.add_argument("disable-extensions")
  options.add_argument("--window-size=%s" % WINDOW_SIZE) # for starting with no window
  options.add_argument("headless") # for starting with no window
  options.add_argument('log-level=3')
  PATH = "function\scrape\driver\chromedriver.exe"
  driver = webdriver.Chrome(options=options, executable_path=PATH)

  return driver

def login(driver, url):
  driver.get(url)
  print("starting..")
  
  sleep(3)

  twitter_email = "finalproj.twitter@gmail.com"
  email_input = driver.find_element(By.XPATH, "//input[@name='text']")
  email_input.send_keys(twitter_email)

  next_button = driver.find_element(By.XPATH, "//span[contains(text(),'Next')]")
  next_button.click()

  sleep(3)
  print("logging in..")
  try:

    twitter_password = "!Nb^VcQqm%@Twh8"
    password_input = driver.find_element(By.XPATH, "//input[@name='password']")
    password_input.send_keys(twitter_password)

    log_in_button = driver.find_element(By.XPATH, "//span[contains(text(),'Log in')]")
    log_in_button.click()

  except:

    twitter_username = "@a_arsirakarn"
    username_input = driver.find_element(By.XPATH, "//input[@name='text']")
    username_input.send_keys(twitter_username)

    next_button = driver.find_element(By.XPATH, "//span[contains(text(),'Next')]")
    next_button.click()

    sleep(3)

    twitter_password = "!Nb^VcQqm%@Twh8"
    password_input = driver.find_element(By.XPATH, "//input[@name='password']")
    password_input.send_keys(twitter_password)

    log_in_button = driver.find_element(By.XPATH, "//span[contains(text(),'Log in')]")
    log_in_button.click()
 

def search(query, driver):
    print("feeding query..")
    # test_query = "#แอมไซยาไนด์"
    # test_query = "(#กระติก) until:2022-03-02 since:2022-03-01"
    search_box = driver.find_element(By.XPATH, "//input[@data-testid='SearchBox_Search_Input']")
    search_box.send_keys(query)
    search_box.click()

    sleep(2) #----------------------------------------------------------------------------------------change this from 1 to 2

    query_span = '//span[contains(text(),' + "'" + 'Search for "' + query + '"' + "')]"
    try:
      drop_down = driver.find_element(By.XPATH, query_span)
    except:
      if query[0] == '#':
        query = query[1:]
      query_span = '//span[contains(text(),' + "'#" + query.capitalize() + "')]"
      drop_down = driver.find_element(By.XPATH, query_span)
    drop_down.click()

def scrapeTweetLink(driver, links, y, scroll_pause_time):
  try:
    all_tweets_link = driver.find_elements(By.XPATH, "//a[contains(@class, 'r-14j79pv')]")
  except:
    return links, new_height, y
  for href in all_tweets_link:
    links.append(href.get_attribute("href"))
  
  # Scroll down to bottom
  driver.execute_script("window.scrollTo(0, {});".format(y))
  y+= 800
  # Wait to load page
  # print(driver.execute_script("return document.body.scrollHeight"))
  sleep(scroll_pause_time)

  # Calculate new scroll height and compare with last scroll height
  new_height = driver.execute_script("return document.body.scrollHeight")
  # print("page height: " + str(new_height))
  # print("y: " + str(y))
  
  # if(y>new_height):
  #   break
  return links, new_height, y

def clickLastest(driver):
  latest = driver.find_element(By.XPATH, "//span[contains(text(),'Latest')]")
  latest.click()
  
# def lastestTweetLink(driver, links, scrollNum, SCROLL_PAUSE_TIME):
#   for i in tqdm(range(0,scrollNum)):
      
#     all_tweets_link = driver.find_elements(By.XPATH, "//a[contains(@class, 'r-14j79pv')]")

#     for href in all_tweets_link:
#       links.append(href.get_attribute("href"))

#     driver.execute_script("window.scrollTo(0, {});".format(i*800))
#     sleep(SCROLL_PAUSE_TIME)

#     new_height = driver.execute_script("return document.body.scrollHeight")
#     # print("page height: " + str(new_height))
#     # print("y: " + str(i*800))
#     if(i*800>new_height):
#         break
#   links = list(dict.fromkeys(links))
#   links[:] = [url for url in links if "status" in url]
#   return links
  
def searchLink(driver, link, df):
    driver.get(link)
    sleep(1.2)
    # try:
    tweet = driver.find_element(By.XPATH, "//div[@data-testid='tweetText']").text
    # except:
    #   continue

    react_str = ""
    try:
        reactions = driver.find_elements(By.XPATH, "//div[contains(@class, 'r-1mf7evn')]")
        for reaction in reactions:
            react_str += reaction.text + "|"
    except:
        pass
    
    react_str = react_str.strip()
    react_str = react_str.replace("\n", "")
    react_str = react_str.replace(",", "")
    for i in range(1,10):
      KText = ".{}K".format(i)
      react_str = react_str.replace(KText, "{}00".format(i))
    react_str = react_str.replace("K", "000")
    all_reactions = react_str.split("|")

    likes = 0
    retweets = 0
    quotes = 0
    bookmarks = 0
    for element in all_reactions:
      if "Retweet" in element:
        retweets = int(re.findall(r'\d+', element)[0])
      elif "Likes" in element:
        likes = int(re.findall(r'\d+', element)[0])
      elif "Quotes" in element:
        quotes = int(re.findall(r'\d+', element)[0])
      elif "Bookmarks" in element:
        bookmarks = int(re.findall(r'\d+', element)[0])
    tweet_time = driver.find_element(By.XPATH, "//time").text
    tweet_time = tweet_time.replace("· ", "")
    username = driver.find_elements(By.XPATH,"//div[contains(@class, 'r-1wvb978')]")[1].text

    df.loc[len(df.index)] = [tweet_time, tweet, username, likes, retweets, quotes, bookmarks, link] 

    return df
  
def getEmbeddedTweet(driver, links):
  html = []
  for link in links:
    driver.get('https://publish.twitter.com/#')
    sleep(1)
    inputField = driver.find_element(By.XPATH, "//input[@id='configuration-query']")
    inputField.send_keys(link)
    sleep(0.2)
    
    submitButton = driver.find_element(By.XPATH, "//button[contains(@class, 'WidgetQuery-button')]")
    submitButton.click()
    sleep(0.5)
    
    code = driver.find_element(By.XPATH, "//code").text
    html.append(code)
    sleep(0.5)
  
  return html
  
def main():
  URL = "https://twitter.com/i/flow/login"
  start = time()
  driver = get_driver()
  login(driver, URL)
  sleep(5)
  query = "(#กระติก) until:2022-03-02 since:2022-03-01"
  hashtag = "#กระติก"
  search(query, driver)
  sleep(3)
  searchTop = False
  searchLatest = True
  links = []
  
  scrollNum = 5
  
  if searchTop:
    print("searching through top tweets..")
    y = 0
    new_height = 0
    scroll_pause_time = 0.8
    while True:
      links, new_height, y  = scrapeTweetLink(driver, links, y, scroll_pause_time)
      if(y>new_height):
        break
      
  if searchLatest:  
    clickLastest(driver)
    sleep(3)
    print("searching through latest tweets..")
    y = 0
    new_height = 0
    scroll_pause_time = 0.5
    for i in tqdm(range(0,scrollNum)):
      links, new_height, y = scrapeTweetLink(driver, links, y, scroll_pause_time)
      if(y>new_height):
        break
      
  links = list(dict.fromkeys(links))
  links[:] = [url for url in links if "status" in url]
  
  df = pd.DataFrame(columns=['date','content','username','like_count','retweet_count','quote_count','bookmark_count', 'link'])
  
  for link in tqdm(links):
    try:
      df = searchLink(driver, link, df)
    except: continue
  df['hashtag'] = hashtag
  display(df)

  end = time()
  print("time used:")
  print(end - start)

if __name__ == '__main__':
    main()
