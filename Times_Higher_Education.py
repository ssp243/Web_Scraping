from bs4 import BeautifulSoup
from beautifulscraper import urllib2
from selenium import webdriver
import pandas as pd
import time
from selenium.common.exceptions import NoSuchElementException

baseurl = 'https://www.timeshighereducation.com'
url = 'https://www.timeshighereducation.com/world-university-rankings/2017/world-ranking#!/page/0/length/25/sort_by/rank/sort_order/asc/cols/stats'
page = urllib2.urlopen(url)

# Conversion to BS format
tidy = BeautifulSoup(page, 'lxml')
print(tidy.prettify())

# To find individual year URL
soup = tidy.find_all('select', {'id': "edit-jump"})
links = {}
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
            ] ## out of loop
# Chromedriver needed
head = ['Rank','Name','No. of FTE Students','Student:Staff Ratio','International Students','Female:Male Ratio','Ranking Name','Ranking Year','Publication Date','URL'] ## Out of loop
driver = webdriver.Chrome(executable_path="C:\\chrme\\chromedriver")  # Your Path
fin_data = []

for url in soup:
    option = url.find_all('option')
    print(option)
    for link in option:
        links[link.text] = (baseurl + link['value'] + '#!/page/0/length/-1/locations/US/sort_by/rank/sort_order/asc/cols/stats')
        driver.get(baseurl + link['value'] + '#!/page/0/length/-1/locations/US/sort_by/rank/sort_order/asc/cols/stats')
        #driver.get('https://www.timeshighereducation.com/world-university-rankings/2016/world-ranking#!/page/0/length/-1/locations/US/sort_by/rank/sort_order/asc/cols/stats')
        search = driver.find_element_by_css_selector('.search-form--sentence-style input.form-control')
        for item in colleges:
            search.send_keys(item)
            time.sleep(2)
            for tr in driver.find_elements_by_xpath('''//*[@id="datatable-1"]/tbody//tr'''):

                try:
                    if (tr.find_element_by_class_name('ranking-institution-title')).text == item:
                        print('mil gaya')
                        tds = tr.find_elements_by_tag_name('td')
                        data = [td.text for td in tds]
                        data[1] = data[1].split("\n")[0]
                        print(data[5])
                        if data[5] == 'n/a':
                            print('Galat wala')
                        else:
                            data_0 = data[5].split(":")[0]
                            data_1 = data[5].split(":")[1]
                            check = " " + data_0 + " " + ":" + data_1
                            del data[5]
                            data.insert(5, check)
                        data.insert(6, 'Times Higher Education')
                        data.insert(7, link.text)
                        data.insert(8, pd.Timestamp(str(int(link.text) - 1) + '-09-21'))
                        data.insert(9, (baseurl + link['value'] + '#!/page/0/length/-1/locations/US/sort_by/rank/sort_order/asc/cols/stats'))
                        fin_data.insert(len(fin_data), data)
                        search.clear()
                except NoSuchElementException:
                    print('nahi mila')
                    fin_data.insert(len(fin_data), ['-',item,'-','-','-','-','Times Higher Education',link.text, pd.Timestamp(str(int(link.text) - 1) + '-09-21'),'-']) ## Out of loop)
                    search.clear()


driver.quit()
df = pd.DataFrame(fin_data, columns=head)
df = df.assign(Scope='International')
df['Publication Date'] = df['Publication Date'].dt.strftime('%m/%d/%Y')
df.to_csv('C:\\Users\\Saurabh Pore\\Desktop\\NJIT\\RA\\Final\\THE.csv', index=False) # Your Path
