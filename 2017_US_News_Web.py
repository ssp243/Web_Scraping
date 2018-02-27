from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from collections import defaultdict
import datetime
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

colleges = ['Illinois Institute of Technology',
            'College of New Jersey',
            'Colorado School of Mines',
            'Case Western Reserve University',
            'Northeastern University',
            'New Jersey Institute of Technology',
            'University of Texas--Dallas',
            'University of Maryland--Baltimore County',
            'Missouri University of Science and Technology',
            'Michigan Technological University',
            'New Mexico Institute of Mining and Technology',
            'University of Massachusetts--Lowell',
            'Louisiana Tech University',
            'Massachusetts Institute of Technology',
            'California Institute of Technology',
            'Carnegie Mellon University',
            'Rensselaer Polytechnic Institute',
            'Georgia Institute of Technology',
            'Virginia Tech',
            'Princeton University',
            'Rutgers University--New Brunswick',
            'Rutgers University--Newark',
            'Stevens Institute of Technology',
            'Montclair State University',
            'Seton Hall University',
            'Rowan University',
            'Texas Tech University'
            ]

name = defaultdict(dict)
#############################################################################################

for college in colleges:
    path_to_extension = r'C:\Users\Saurabh Pore\Desktop\1.13.3_0'
    chrome_options = Options()
    chrome_options.add_argument('load-extension=' + path_to_extension)
    driver = webdriver.Chrome(executable_path="C:\\chrme\\chromedriver", chrome_options=chrome_options)
    driver.create_options()
    wait = WebDriverWait(driver, 10)
    driver.get("https://secure.usnews.com/member/login")
    username = driver.find_element_by_xpath('//*[@id="username"]')
    password = driver.find_element_by_xpath('//*[@id="password"]')
    username.send_keys('deess@njit.edu')
    password.send_keys('thorom1')
    driver.find_element_by_xpath('//*[@id="login_form"]/input[3]').click()
    searchb = wait.until( EC.visibility_of_element_located((By.CSS_SELECTOR, 'body > div.off-canvas-wrap > div > header > div > nav > div > section:nth-child(2) > span.js-header-search-button.show-for-medium-up.display-inline-block-for-medium-up > span.js-header-search-button-show > svg'))).click()
    search = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id[starts-with(., "colleges-nav-search-")]]')))
    search.send_keys(college, Keys.ENTER)
    wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id[starts-with(., "view-")]]/div/section/div[1]/h3/a'))).click()
    wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id[starts-with(.,"sub-nav-")]]/ul/li[2]/a'))).click()
    #############################################################################################
    ul = driver.find_elements_by_xpath('//*[@id="content-main"]/div[1]/div[2]/ul')
    data =[]
    for u in ul:
        data = u.text.splitlines()
    print(data)
    for d in data:
         if d.startswith('At'):
             data.remove(d)
             print('removed')
         else:
             print('Okay')
    for stat in data:
         name[college]['US News - ' + str(stat.split('in', 1)[1]).strip(' \n#')] = str(stat.split('in', 1)[0]).strip(' \n#')
    driver.quit()
###########################################################################################################
df_new = pd.DataFrame(name).stack().reset_index()
print(df_new)
df_new.columns = ['Ranking Name', 'Name', 'Rank']
df_new = df_new[['Name', 'Ranking Name', 'Rank']]
df_new.insert(3, 'Scope', 'National')
df_new.insert(4, 'Ranking Year', datetime.datetime.now().year)
df_new.insert(5, 'Publication Date', pd.Timestamp('3/14/2017'))
df_new['Publication Date'] = df_new['Publication Date'].dt.strftime('%m/%d/%Y')
df_new.to_csv('C:\\Users\\Saurabh Pore\\Desktop\\NJIT\\RA\\Final\\2017_US_News_Web.csv', index=False)


#
