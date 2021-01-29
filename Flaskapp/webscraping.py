# -*- coding: utf-8 -*-
"""
Created on Fri Jan 29 00:28:00 2021

@author: ozank
"""


import requests
from bs4 import BeautifulSoup
import pandas as pd
import pymongo
import dns
import pandas as pd


no_pages = 2

def get_data(pageNo):  
    headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0", "Accept-Encoding":"gzip, deflate", "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "DNT":"1","Connection":"close", "Upgrade-Insecure-Requests":"1"}

    r = requests.get('https://www.amazon.ca/Best-Sellers-Books/zgbs/books/ref=zg_bs_pg_'+str(pageNo)+'?ie=UTF8&pg='+str(pageNo), headers=headers)#, proxies=proxies)
    content = r.content
    soup = BeautifulSoup(content,features="lxml")
    #☻print(soup)

    alls = []
    for d in soup.findAll('div', attrs={'class':'a-section a-spacing-none aok-relative'}):
        #print(d)
        name = d.find('span', attrs={'class':'zg-text-center-align'})
        n = name.find_all('img', alt=True)
        #print(n[0]['alt'])
        author = d.find('a', attrs={'class':'a-size-small a-link-child'})
        rating = d.find('span', attrs={'class':'a-icon-alt'})
        users_rated = d.find('a', attrs={'class':'a-size-small a-link-normal'})
        price = d.find('span', attrs={'class':'p13n-sc-price'})
        imageurl = d.find('div', attrs={'class':'a-section a-spacing-small'})
        nimage = imageurl.find_all('img', src=True)
        #print(nimage[0]['src'])
        
        
        all1=[]

        if name is not None:
            #print(n[0]['alt'])
            all1.append(n[0]['alt'])
        else:
            all1.append("unknown-product")

        if author is not None:
            #print(author.text)
            all1.append(author.text)
        elif author is None:
            author = d.find('span', attrs={'class':'a-size-small a-color-base'})
            if author is not None:
                all1.append(author.text)
            else:    
                all1.append('0')

        if rating is not None:
            #print(rating.text)
            all1.append(rating.text)
        else:
            all1.append('-1')

        if users_rated is not None:
            #print(price.text)
            all1.append(users_rated.text)
        else:
            all1.append('0')     

        if price is not None:
            #print(price.text)
            all1.append(price.text)
        else:
            all1.append('0')
        alls.append(all1)    
        
        if imageurl is not None:
            #print(nimage[0]['src'])
            all1.append(nimage[0]['src'])
        else:
            all1.append("https://upload.wikimedia.org/wikipedia/commons/6/68/Solid_black.png")
    return alls

results = []
for i in range(1,no_pages+1):
    results.append(get_data(i))
#print(results)
flatten = lambda l: [item for sublist in l for item in sublist]
df = pd.DataFrame(flatten(results),columns=['Book Name','Author','Rating','Customers_Rated', 'Price','Imageurl'])
#print(df)



client = pymongo.MongoClient("mongodb+srv://ozan:kaya@cluster0.2v7o6.mongodb.net/<dbname>?retryWrites=true&w=majority")
db=client["AmazonData"]
col = db["BestBooks"]


#db.BestBooks.insert_many(df.to_dict('records'))
    