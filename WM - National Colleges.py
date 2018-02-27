import pandas as pd
from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import datetime

driver = webdriver.Chrome(executable_path="C:\\chrme\\chromedriver")
wait = WebDriverWait(driver, 10)
data1 = []
now = datetime.datetime.now()
for i in range(1, 16):
    url = 'http://washingtonmonthly.com/college_guide?ranking=2016-rankings-national-universities?page=' + str(i)
    driver.get(url)
    wait.until(EC.frame_to_be_available_and_switch_to_it("iFrameResizer0"))
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'table.tablesaw')))

    try:
        for row in driver.find_elements_by_xpath("//*[starts-with(@id,'table')]/tbody/tr"):
            tds = row.find_elements_by_tag_name('td')
            data = [td.text for td in tds]
            data.insert(len(data), 'Washington Monthly - National Universities')
            data.insert(len(data), now.year - 1)
            data.insert(len(data), pd.Timestamp(str(int(now.year) - 1) + '-08-29'))
            data1.insert(len(data1), data)
            print(data)
    except (NoSuchElementException, StaleElementReferenceException):
        print('Not Found')

# For Header
th = driver.find_elements_by_css_selector('table.tablesaw th')
header = [head.text for head in th]
header.insert(len(header), 'Ranking Name')
header.insert(len(header), 'Ranking Year')
header.insert(len(header), 'Publication Date')


df = pd.DataFrame(data1, columns=header)
df = df.assign(Scope = 'National')
df['Publication Date'] = df['Publication Date'].dt.strftime('%m/%d/%Y')
print(df)
df.to_csv('C:\\Users\\Saurabh Pore\\Desktop\\NJIT\\RA\\Final\\WM-National Universities.csv', index=False)
print(df)
driver.quit()
