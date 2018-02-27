from bs4 import BeautifulSoup
from beautifulscraper import urllib2
import re
import pandas as pd
import datetime


url = 'http://time.com/money/best-colleges/rankings/best-colleges/'
page = urllib2.urlopen(url)

# Conversion to BS format
tidy = BeautifulSoup(page, 'lxml')
#print(tidy.prettify())

table = tidy.find('table')
print(table)

# For Header
th = table.find_all('th')
header = [td.text for td in th]
#print(header)
h = re.compile("([A-za-z]{4})(.*)")
n = h.match(header[0])
del header[0]
header.insert(0, n.group(1))
header.insert(1, 'Name')
header.insert(8, 'Ranking Name')
header.insert(9, 'Scope')
header.insert(10, 'Ranking Year')
header.insert(11, 'Publication Date')


# For Data
data = []
tbody = tidy.find({id: 'table-body'})
print(tbody)
trs = tbody.find_all('tr')
now = datetime.datetime.now()
name = ''
# Access Individual tr
for tr in trs:
     tds = tr.find_all('td')
     for td in tds:
        if td.find('a', {'class':'_1RI9D22X'}) is not None:
            name = ''
            name = td.find('a', {'class':'_1RI9D22X'}).text
     test = [td.text for td in tds]
     if len(test) == 7:
        test.insert(8, 'Money Best-Colleges')
        test.insert(9, 'National')
        test.insert(10, now.year)
        test.insert(10, pd.Timestamp(str(now.year) + '-07-10'))
        data.append(test)
     test.insert(1, name)

# cleaning
list2 = []
for i in range(0, len(data)):
     list2.insert(len(list2), list(filter(None, data[i])))

final_list = list(filter(None, list2))
print(final_list)
# For Separate Rank And School
r = re.compile("([0-9]+)(.*)")
my_list = []
for i in range(0, len(final_list)-1):
      m = r.match(final_list[i][0])
      del final_list[i][0]
      my_list.insert(len(my_list), [m.group(1)] + final_list[i])


print(my_list)
df = pd.DataFrame(my_list, columns=header)
df = df.assign(Scope = 'National')
df['Publication Date'] = df['Publication Date'].dt.strftime('%m/%d/%Y')
colleges = ['Illinois Institute of Technology',
            'Colorado School of Mines',
            'Case Western Reserve University',
            'Northeastern University',
            'New Jersey Institute of Technology',
            'The University of Texas at Dallas',
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
            'Georgia Institute of Technology-Main Campus',
            'Virginia Polytechnic Institute and State University',
            'Texas Tech University',
            'Princeton University',
            'The College of New Jersey',
            'Rutgers University-New Brunswick',
            'Stevens Institute of Technology',
            'Montclair State University',
            'Seton Hall University',
            'Rowan University'
            ] ## out of loo
dfnew = df.loc[df['Name'].isin(colleges)]
print(dfnew)
#print(df)
df.to_csv('C:\\Users\\Saurabh Pore\\Desktop\\NJIT\\RA\\Final\\Time.csv', index=False) # Your Path
dfnew.to_csv('C:\\Users\\Saurabh Pore\\Desktop\\NJIT\\RA\\Final\\Time_Filter.csv', index=False) # Your Path



