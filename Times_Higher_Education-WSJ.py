from selenium import webdriver
import pandas as pd
import time
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import datetime

driver = webdriver.Chrome(executable_path="C:\\chrme\\chromedriver")  # Your Path
driver.get(
    'https://www.timeshighereducation.com/rankings/united-states/2017#!/page/0/length/-1/sort_by/rank/sort_order/asc/cols/stats')
# search = driver.find_element_by_xpath('//*[@id="edit-name"]')
wait = WebDriverWait(driver, 10)
search = wait.until(
    EC.visibility_of_element_located((By.CSS_SELECTOR, '.search-form--sentence-style input.form-control')))
fin_data = []
colleges = ['Illinois Institute of Technology',
            'Colorado School of Mines',
            'Case Western Reserve University',
            'Northeastern University',
            'New Jersey Institute of Technology',
            'University of Texas at Dallas',
            'University of Maryland, Baltimore County',
            'Missouri University of Science and Technology',
            'Michigan Technological University',
            'New Mexico Institute of Mining and Technology',
            'University of Massachusetts',
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
            'Rutgers, the State University of New Jersey',
            'Stevens Institute of Technology',
            'Montclair State University',
            'Seton Hall University',
            'Rowan University'
            ]
## out of loop
now = datetime.datetime.now()

for item in colleges:
    search.send_keys(item)
    time.sleep(1)
    for tr in driver.find_elements_by_xpath('''//*[@id="datatable-1"]/tbody//tr'''):

        try:
            if (tr.find_element_by_class_name('ranking-institution-title')).text == item:
                print('mil gaya')
                tds = tr.find_elements_by_tag_name('td')
                data = [td.text for td in tds]
                data[1] = data[1].split("\n")[0]
                data.insert(5, 'Wall Street Journal/Times Higher Education')
                data.insert(6, now.year)
                data.insert(7, pd.Timestamp(str(int(now.year) - 1) + '-09-27'))
                # data[5] = 'Wall Street Journal/Times Higher Education'
                # data[6] = now.year
                fin_data.insert(len(fin_data), data)
                print(data)
                search.clear()
        except NoSuchElementException:
            print('nahi mila')
            fin_data.insert(len(fin_data),
                            ['-', item, '-', '-', '-', 'Wall Street Journal/Times Higher Education', now.year,
                             pd.Timestamp(str(int(now.year)-1) + '-09-27')])
            search.clear()

print(fin_data)
driver.quit()
head = ['Rank', 'Name', 'Tuition and Fees', 'Room and Board', 'Salary after 10 years', 'Ranking Name', 'Ranking Year',
        'Publication Date']
df = pd.DataFrame(fin_data, columns=head)
df = df.assign(Scope='National')
df['Publication Date'] = df['Publication Date'].dt.strftime('%m/%d/%Y')
df.to_csv('C:\\Users\\Saurabh Pore\\Desktop\\NJIT\\RA\\Final\\THE_WSJ.csv', index=False)
