#!/home/barbara/miniconda/bin/python

"""
Scraping wiki page
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd

url='https://pt.wikipedia.org/wiki/Lista_de_santos_portugueses#Santos_Portugueses_(1139%E2%80%93presente)'

resp=requests.get(url)

html=resp.content

soup=BeautifulSoup(html, 'html.parser')


table=soup.find('table', attrs={'class':"wikitable unsortable"})
table_body=table.find('tbody')
rows=table_body.find_all('tr')


header=[f.get_text().strip('\n') for f in rows[0].find_all('th')] 
allrows=rows[1:]


results=[[f.get_text() for f in row.find_all('td')] for row in allrows]

rowspan=[]

for no, tr in enumerate(allrows):
    tmp=[]
    for td_no, data in enumerate(tr.find_all('td')):
        if data.has_attr('rowspan'):
            rowspan.append((no, td_no, data['rowspan'], data.get_text()))


if rowspan:
     for i in rowspan:
        for j in range(1, int(i[2])):
            results[i[0]+j].insert(i[1], i[3])
    
jobinf_t=[[f.get_text() for f in row.find_all('i')] for row in allrows]

jobinf=list(map(lambda x:x[0], jobinf_t))       


#Get a clean column with the names
names_clean=[]
for k, t  in  enumerate(allrows):
    if (len(allrows[k].find_all('td'))) == 6:
        for i in allrows[k].find_all('td')[1].contents[0].children: 
            names_clean.append(i)
    elif (len(allrows[k].find_all('td'))) == 1:
        for i in allrows[k].find_all('td')[0].contents[0].children:
                names_clean.append(i)
    elif (len(allrows[k].find_all('td'))) == 2:
        for i in allrows[k].find_all('td')[0].contents[0].children:
            names_clean.append(i)

#Get a clean column with images
            
imgs=[]            
for k in range(1, len(allrows)):
#    #Imgs if available
    try:
        imgs.append(rows[k].find_all('td')[0].find_all('a')[0].get('href'))
       # print (rows[k].find_all('td')[0].find_all('a')[0].get('href'))
    except IndexError:
        imgs.append('')

imgs.append('')
#for i, k in enumerate(list(zip(imgs, names_clean))):
#    print (i, k)

scraped_df=pd.DataFrame(data=results, columns=header)

#Get the final dataframe
tmpdf=pd.DataFrame.from_dict({'Nomes':names_clean, 'Classificacao':jobinf, 'Retrato':imgs})
tmpdf_scr=scraped_df.drop(['Santo', 'Ref', 'Retrato'], axis=1)
final_df=pd.concat([tmpdf, tmpdf_scr], axis=1)

