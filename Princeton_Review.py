import pandas as pd
from beautifulscraper import urllib2
from bs4 import BeautifulSoup
import re
from selenium import webdriver
import time
from selenium.webdriver import ActionChains
from collections import defaultdict
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import datetime

colleges = ['Illinois Institute of Technology',
            'Colorado School of Mines',
            'Case Western Reserve University',
            'Northeastern University',
            'New Jersey Institute of Technology',
            'University of Texas at Dallas',
            'University of Maryland-Baltimore County',
            'Missouri University of Science and Technology',
            'Michigan Technological University',
            'New Mexico Institute of Mining and Technology',
            'University of Massachusetts-Lowell',
            'Louisiana Tech University',
            'Massachusetts Institute of Technology',
            'California Institute of Technology',
            'Carnegie Mellon University',
            'Rensselaer Polytechnic Institute',
            'Georgia Institute of Technology',
            'Virginia Polytechnic Institute and State University',
            'Texas Tech University',
            'Princeton University',
            'The College of New Jersey',
            'Rutgers University',
            'Stevens Institute of Technology',
            'Montclair State University',
            'Seton Hall University',
            'Rowan University'
            ]

driver = webdriver.Chrome(executable_path="C:\\chrme\\chromedriver")
wait = WebDriverWait(driver, 10)
driver.get('https://www.princetonreview.com/')
# element_to_hover_over = driver.find_element_by_xpath('//*[@id="desktopnav"]/nav/div/div[2]/ul[2]/li[2]/a')
# Hover to search
# hover = ActionChains(driver).move_to_element(element_to_hover_over)
# hover.perform()
# search = driver.find_element_by_xpath('//*[@id="siteSearchText2"]')
name = defaultdict(dict)
r_unwanted = re.compile("[\n\t\r]")
url = []
for college in colleges:
    element_to_hover_over = wait.until( EC.visibility_of_element_located((By.XPATH, '//*[@id="desktopnav"]/nav/div/div[2]/ul[2]/li[2]/a')))
    # element_to_hover_over = driver.find_element_by_xpath('//*[@id="desktopnav"]/nav/div/div[2]/ul[2]/li[2]/a')
    hover = ActionChains(driver).move_to_element(element_to_hover_over)
    hover.perform()
    # search = driver.find_element_by_xpath('//*[@id="siteSearchText2"]')
    search = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="siteSearchText2"]')))
    time.sleep(0.2)
    search.send_keys(college)
    driver.find_element_by_css_selector('#searchSiteButton2').click()
    time.sleep(0.2)
    url.insert(len(url), wait.until(EC.visibility_of_element_located(
        (By.XPATH, "//*[@id='___gcse_0']/div/div/div/div[5]/div[2]/div/div/div[2]/div[1]/div[1]/div/a"))).get_attribute(
        'href'))
    # url = driver.find_element_by_xpath("//*[@id='___gcse_0']/div/div/div/div[5]/div[2]/div/div/div[2]/div[1]/div[1]/div/a").get_attribute('href')

driver.quit()
print(url)

d = []
p = []
mydict = {}
description = {}

for u in url:
    page = urllib2.urlopen(u)
    tidy = BeautifulSoup(page, 'lxml')
    r_unwanted = re.compile("[\n\t\r]")
    div = tidy.find('div', {'class': 'enhancedRHS'})
    drow = div.find_all('div', {'class': 'row'})
    df = pd.DataFrame()
    # p_div = tidy.find('div', {'class': 'blurb readmore-js-section readmore-js-expanded'})
    article = tidy.find_all('article')
    print(len(article))

    for a in article:
        title = a.find('h4')
        list1 = [desc.text for desc in a.find_all('p')]
        str1 = ''.join(list1)
        description[title.text] = str1
    p.insert(len(p), description)
    description = {}

    for row in drow:
        if row.find('div', {'class': 'col-xs-9'}) is not None:
            if row.find('div', {'class': 'col-xs-3 bold'}) is None:
                mydict['Princeton Review' + '-' + row.find('div', {'class': 'col-xs-9'}).text.replace("\n", "")] = 'Yes'
            else:
                mydict['Princeton Review' + '-' + row.find('div', {'class': 'col-xs-9'}).text.replace("\n",
                                                                                                      "")] = r_unwanted.sub(
                    " ", row.find('div', {'class': 'col-xs-3 bold'}).text).replace(" ", "").replace("#", "")

        else:
            print('nothing found')
    d.insert(len(d), mydict)
    mydict = {}


# df_rank = pd.DataFrame([list(i.items())for i in d], columns=["Ranking Name", "Rank"])
df_rank = pd.DataFrame(d)
df_rank.insert(0, 'Name', colleges)
df_rank = df_rank.assign(Scope = 'National')
df_rank = df_rank.assign(Ranking_Year = datetime.datetime.now().year + 1)
df_rank = df_rank.assign(Publication_Date = pd.Timestamp('2017-08-31'))
df_rank['Publication_Date'] = df_rank['Publication_Date'].dt.strftime('%m/%d/%Y')

df_desc = pd.DataFrame(p)
df_final = df_rank.join(df_desc)
print(df_final)
df_final.to_csv('C:\\Users\\Saurabh Pore\\Desktop\\NJIT\\RA\\Final\\Princeton_Review.csv', index=False)
