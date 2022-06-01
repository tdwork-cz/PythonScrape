from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
import time
import pandas as pd

# Log in data
EMAIL = ''
PASSWORD = ''
LOGIN = ''
PERSON = input('Enter the name of celebrity:')

PATH = '/Applications/VS_Code_projects/Selenium/chromedriver'
driver = webdriver.Chrome(PATH)
baseUrl = 'https://twitter.com/login'
driver.get(baseUrl)
driver.maximize_window()
df = pd.DataFrame({'Text':[''],'Date':[''], 'Likes':[''], 'Reposts':[''], 'Comments':['']})

def send_custom_keys(driver, info, name):
    search = WebDriverWait(driver, 20).until(
    EC.presence_of_element_located((By.NAME, name))
    )
    search.send_keys(info)
    search.send_keys(Keys.RETURN)

# Filling in data to log in
time.sleep(2)
send_custom_keys(driver, EMAIL, 'text')
send_custom_keys(driver, LOGIN, 'text')
send_custom_keys(driver, PASSWORD, 'password')

try:
    acceptBtn = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="layers"]/div/div/div/div/div/div[2]/div[1]/div'))
    )
    acceptBtn.click()
except:
    pass

searchCelebrity = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, 'input[aria-label*="Search query"]'))
)
searchCelebrity.send_keys(PERSON)
searchCelebrity.send_keys(Keys.RETURN)
clickPeople = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[1]/div[2]/nav/div/div[2]/div/div[3]/a'))
    )
clickPeople.click()
firstPerson = WebDriverWait(driver,10).until(
    EC.presence_of_element_located((By.XPATH, '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[2]/div/section/div/div/div[1]/div/div/div/div/div[2]/div[1]/div[1]/div/div[1]/a'))
)
firstPerson.click()

time.sleep(2)
soup = BeautifulSoup(driver.page_source, 'lxml')

while True:
    postings = soup.find_all('div', {'class':'css-1dbjc4n r-1iusvr4 r-16y2uox r-1777fci r-kzbkwu'})
    # df = df.drop_duplicates()
    for post in postings:
        try:
            text = post.find('div', {'data-testid':'tweetText'}).text.strip()
            date = post.find('time').text.strip()
            [likes, reposts, comments] = list(map(lambda x:x.text.strip(),post.find_all('span', {'class':'css-901oao css-16my406 r-poiln3 r-bcqeeo r-qvutc0'})[:-4:-1]))
            df = df.append({'Text':text,'Date':date, 'Likes':likes, 'Reposts':reposts, 'Comments':comments}, ignore_index=True)
        except:
            pass
    if len(df) >= 100:
        break
    driver.execute_script('window.scrollBy(0, document.body.scrollHeight)')
    time.sleep(3)
    soup = BeautifulSoup(driver.page_source, 'lxml')

driver.quit()
df.to_csv('ronaldo.csv')