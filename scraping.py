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


table=soup.find_all('table', attrs={'class':"wikitable unsortable"})
table_body=[table[i].find('tbody') for i in range(0, len(table))]
rows=[table_body[i].find_all('tr') for i in range(0, len(table_body))]


header=[f.get_text().strip('\n') for f in rows[0][0].find_all('th')] 
usefultables=rows[:][1:]
allrows=[rows[k][i] for k in range(0, len(rows)) for i in range(0, len(rows[k]))] 

results=[[f.get_text() for f in row.find_all('td')] for row in allrows]




rowspan=[]

#for no, tr in enumerate(allrows):
#    tmp=[]
#    for td_no, data in enumerate(tr.find_all('td')):
#        if data.has_attr('rowspan'):
#            rowspan.append((no, td_no, data['rowspan'], data.get_text()))
#
#
#if rowspan:
#     for i in rowspan:
#        for j in range(1, int(i[2])):
#            results[i[0]+j].insert(i[1], i[3])
            

names_clean=[]

lifespan=[]
age=[]
jobinf=[f.get_text() for row in allrows for f in row.find_all('i')]
work=[]
for k in range(0, len(allrows)):
    names_clean.append(allrows[k].get_text(separator=',', strip=True).split(',')[0])
    lifespan.append(allrows[k].get_text(separator=',', strip=True).split(',')[2])
    tmp=allrows[k].get_text(separator=',', strip=True).split(',')[3]
    if 'anos' in tmp:
        age.append(tmp)
    else:
        age.append('')
    l=allrows[k].get_text(separator='"', strip=True).split('"') 
    if len(l)>=7: 
        work.append(l[4:-3])
    else: 
        work.append('')

#Get a clean column with images
            
imgs=[]            
for k in range(1, len(allrows)):
    try:
        imgs.append(allrows[k].find('a').get('href'))
    except AttributeError:
        imgs.append('')


        #for i, k in enumerate(list(zip(imgs, names_clean))):
#    print (i, k)
results=[i[1:-2] for i in results]
results=[i for i in results if len(i)>=1]
header=header[1:]
names_clean=names_clean[1:]
jobinf=jobinf[1:]
scraped_df=pd.DataFrame(data=results[1:], columns=header)

#Get the final dataframe
tmpdf=pd.DataFrame.from_dict({'Nomes':names_clean, 'Classificacao':jobinf, 'Retrato':imgs})
tmpdf_scr=scraped_df.drop(['Santo', 'Ref'], axis=1)
final_df=pd.concat([tmpdf, tmpdf_scr], axis=1)

