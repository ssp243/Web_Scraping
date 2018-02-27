from selenium import webdriver
import pandas as pd
import datetime

driver = webdriver.Chrome(executable_path="C:\\chrme\\chromedriver")
driver.set_window_size(1024, 768) # optional
driver.get('http://www.payscale.com')
driver.find_element_by_xpath('/html/body/div[4]/div[2]/div/div/div[2]/div/div').click()
driver.find_element_by_xpath('//*[@id="collegeRoiContent"]/div/div/div[2]/div/div[2]/a').click()
#driver.find_element_by_xpath('//*[@id="collegeRoiContent"]/div/div/div[1]/div[3]/div/div/a[2]').click()

# for title
th = driver.find_elements_by_xpath('//*[@id="collegeRoiContent"]/div/div/div[2]/table/thead/tr/th')
hdata = [header.text for header in th]
list1 = list(filter(None, hdata))
header = [x.strip() for x in list1]
del header[1]
header.insert(1, 'Name')
header.insert(7, 'Ranking Name')
header.insert(8, 'Scope')
header.insert(9, 'Ranking Year')
header.insert(10, 'Publication Date')
print(header)
data1 =[]
cdata = ()
now = datetime.datetime.now()

#for data
for tr in driver.find_elements_by_xpath('//*[@id="collegeRoiContent"]/div/div/div[2]/table/tbody/tr'):
     tds = tr.find_elements_by_tag_name('td')
     data = (td.text for td in tds)
     #data1 = list(filter(None, data))
     cdata = (list(filter(None, data)))
     del cdata[1]
     cdata.insert(7, 'Payscale_Best_Value_Colleges')
     cdata.insert(8, 'National')
     cdata.insert(9, now.year)
     cdata.insert(10, pd.Timestamp(str(int(now.year) - 1) + '-09-20'))
     print(cdata)
     data1.insert(len(data1),cdata)


print(data1)
df = pd.DataFrame(data1, columns=header)
df['Publication Date'] = df['Publication Date'].dt.strftime('%m/%d/%Y')
df.to_csv('C:\\Users\\Saurabh Pore\\Desktop\\NJIT\\RA\\Final\\payscale.csv', index=False)
driver.quit()
