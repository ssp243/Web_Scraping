from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from bs4 import BeautifulSoup
from beautifulscraper import urllib2
import re
from collections import defaultdict
import datetime
import pandas as pd

url ='https://www.forbes.com/top-colleges/list/#tab:rank'
driver = webdriver.Chrome(executable_path="C:\\chrme\\chromedriver")
wait = WebDriverWait(driver, 20)
driver.get(url)
th = wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'body#entity_list #contentwrapper #content #list_table #the_list thead tr th')))
print(th)
##############################################
header = [h.text for h in th]
header = list(filter(None, header))
print(header)
#################################################
#wait.until(EC.visibility_of_all_elements_located((driver.execute_script("window.scrollTo(0, document.body.scrollHeight);"))))
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);") # to scroll down
time.sleep(10) # time to load all scripts correctly optional
tr = driver.find_elements_by_xpath('//*[@id="list-table-body"]/tr')
print(len(tr))

colleges = ['Illinois Institute of Technology',
            'Colorado School of Mines',
            'Case Western Reserve University',
            'Northeastern University',
            'New Jersey Institute of Technology',
            'University of Texas, Dallas',
            'University of Maryland, Baltimore County',
            'Missouri University of Science and Technology',
            'Michigan Technological University',
            'New Mexico Institute of Mining and Technology',
            'University of Massachusetts Lowell',
            'Louisiana Tech University',
            'Massachusetts Institute of Technology',
            'California Institute of Technology',
            'Carnegie Mellon University',
            'Rensselaer Polytechnic Institute',
            'Georgia Institute of Technology',
            'Virginia Tech',
            'Texas Tech University',
            'Princeton University',
            'College of New Jersey',
            'Rutgers',
            'Stevens Institute of Technology',
            'Montclair State University',
            'Seton Hall University',
            'Rowan University'
            ] ## out of loop
url =[]
fin_data =[]
urldict = {}
for row in tr:
        tds = row.find_elements_by_tag_name('td')
        data = [td.text.strip(' \n#') for td in tds]
        data = list(filter(None, data))
        print(data)
        if len(data) is not 0:
            fin_data.insert(len(fin_data), data)
            if row.find_element_by_class_name('name').text in colleges:
                url.insert(len(url), row.find_element_by_tag_name('a').get_attribute("href"))
                urldict[row.find_element_by_class_name('name').text] = row.find_element_by_tag_name('a').get_attribute("href")
                print(urldict)
        else:
            del data
            print('Data Del')

df = pd.DataFrame(fin_data, columns=header)
df.insert(6, 'Scope', 'National')
df.insert(7, 'Ranking Year', datetime.datetime.now().year)
df.insert(8, 'Publication Date', pd.Timestamp('8/2/2017'))
df['Publication Date'] = df['Publication Date'].dt.strftime('%m/%d/%Y')
df.to_csv('C:\\Users\\Saurabh Pore\\Desktop\\NJIT\\RA\\Final\\2017_Forbes_Summary.csv', index=False) # Your Path
driver.quit()
########################################################################################################

name = defaultdict(dict)
for key, value in urldict.items():
    mydicto ={}
    print(value)
    page = urllib2.urlopen(value)
    # Conversion to BS format
    tidy = BeautifulSoup(page, 'lxml')
    #print(tidy.prettify())
    div = tidy.find('div', {'class':'forbeslists fright'})
    li = div.findAll('li')
    div1 = tidy.findAll('div', {'class':'rankonlist'})
    for d in div1:
        r = re.findall(r'\d+', d.text)
        name[key]['Forbes - ' + str(d.find('a').text).strip(' \n')] = str(r[0])
    for l in li:
            if ':' not in l.text:
                name[key]['Forbes - ' + str(l.text.split('in')[1]).strip(' \n')] = str(l.text.split('in')[0]).strip(' \n#')
            else:
                name[key]['Forbes - ' + str(l.text.split(':')[0]).strip(' \n')] = str(l.text.split(':')[1]).strip(' \n')

df_new = pd.DataFrame(name).stack().reset_index()
print(df_new)
df_new.columns = ['Ranking Name', 'Name', 'Rank']
df_new = df_new[['Name', 'Ranking Name', 'Rank']]
df_new.insert(3, 'Scope', 'National')
df_new.insert(4, 'Ranking Year', datetime.datetime.now().year)
df_new.insert(5, 'Publication Date', pd.Timestamp('8/2/2017'))
df_new['Publication Date'] = df_new['Publication Date'].dt.strftime('%m/%d/%Y')
df_new.to_csv('C:\\Users\\Saurabh Pore\\Desktop\\NJIT\\RA\\Final\\2017_Forbes.csv', index=False)



