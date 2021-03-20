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



names_clean=[]

lifespan=[]
age=[]
jobinf=[f.get_text() for row in allrows for f in row.find_all('i')]
work=[]
for k in range(0, len(allrows)):
    names_clean.append(allrows[k].get_text(separator=',', strip=True).split(',')[0])
    try:
        tmp=allrows[k].get_text(separator=',', strip=True).split(',')[3]
    except IndexError:
        tmp=''
    if 'anos' in tmp:
        age.append(tmp)
    else:
        age.append('')
    l=allrows[k].get_text(separator='"', strip=True).split('"') 
    if len(l)>=7: 
        work.append(' '.join(l[4:-3]))
    else: 
        work.append('')
    if len(l)> 3: 
        lifespan.append(l[2]) 
    else: 
        lifespan.append('') 
             


#Get a clean column with images
        
imgs=[]            
for k in range(1, len(allrows)):
    try:
        imgs.append(allrows[k].find('a').get('href'))
    except AttributeError:
        imgs.append('')

for i in range(0,4):
    names_clean.remove('Retrato')
    lifespan.remove('Vida')
    try:
        imgs.remove('')
    except ValueError:
        continue
    
jobinf.insert(34,'')
del work[110:114]



header=header[1:]

#Get the final dataframe
tmpdf=pd.DataFrame.from_dict({'Nomes':names_clean, 'Classificacao':jobinf, 'Vida':lifespan,'Obra':work ,'Retrato':imgs})

tmpdf.to_csv('raw.csv', index=False)
